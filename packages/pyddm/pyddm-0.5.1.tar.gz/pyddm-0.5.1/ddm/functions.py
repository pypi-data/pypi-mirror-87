# Copyright 2018 Max Shinn <maxwell.shinn@yale.edu>
#           2018 Norman Lam <norman.lam@yale.edu>
# 
# This file is part of PyDDM, and is available under the MIT license.
# Please see LICENSE.txt in the root directory for more information.

__all__ = ['models_close', 'fit_model', 'fit_adjust_model',
           'evolution_strategy', 'solve_partial_conditions',
           'hit_boundary', 'dependence_hit_boundary', 'display_model',
           'get_model_loss', 'set_N_cpus']

import copy

import numpy as np
from scipy.optimize import minimize, basinhopping, differential_evolution, OptimizeResult

from . import parameters as param
from .model import Model, Solution, Fitted, Fittable
from .sample import Sample
from .models.drift import DriftConstant
from .models.noise import NoiseConstant
from .models.ic import ICPointSourceCenter
from .models.bound import BoundConstant
from .models.overlay import OverlayNone, OverlayChain
from .models.loss import LossLikelihood

from paranoid.types import Boolean, Number, String, Set, Unchecked, Natural1, Maybe
from paranoid.decorators import accepts, returns, requires, ensures, paranoidconfig
from paranoid.settings import Settings as paranoid_settings
from .models.paranoid_types import Conditions

from .fitresult import FitResult, FitResultEmpty

# For parallelization support
_parallel_pool = None # Note: do not change this directly.  Call set_N_cpus() instead.
#@accepts(Natural1)
#@paranoidconfig(enabled=False)
def set_N_cpus(N):
    global _parallel_pool
    if _parallel_pool is not None:
        _parallel_pool.close()
    if N != 1:
        try:
            import pathos
        except ImportError:
            raise ImportError("Parallel support requires pathos.  Please install pathos.")
        #_parallel_pool = pathos.multiprocessing.Pool(N)
        _parallel_pool = pathos.pools._ProcessPool(N)
        _parallel_pool.n_cpus = N
    else:
        _parallel_pool = None


@accepts(Model, Model, tol=Number)
@requires("m1.get_model_type() == m2.get_model_type()")
@returns(Boolean)
def models_close(m1, m2, tol=.1):
    """Determines whether two models are similar.

    This compares the parameters of models `m1` and `m2` and checks to
    make sure that each of the parameters in model `m1` is within a
    distance of `tol` of `m2`.  Return True if this is the case,
    otherwise False."""
    p1 = m1.get_model_parameters()
    p2 = m2.get_model_parameters()
    assert len(p1) == len(p2)
    assert m1.get_model_type() == m2.get_model_type()
    for mp1, mp2 in zip(p1, p2):
        if np.abs(mp1-mp2) > tol:
            return False
    return True

def get_model_loss(model, sample, lossfunction=LossLikelihood, method=None):
    """A shortcut to compusing the loss of a model.

    A shortcut method to compute the loss (under loss function
    `lossfunction`) of Model `model` with respect to Sample `sample`.
    Optionaly, specificy the numerical method `method` to use
    (e.g. analytical, numerical, implicit, etc.)
    
    Note that this should not be used when performing model fits, as
    it is faster to use the optimizations implemented in
    fit_adjust_model.
    """
    # Count parameters (for AIC/BIC), making sure not to double count
    # for repeated parameters.
    params = []
    for component in model.dependencies:
        for param_name in component.required_parameters:
            pv = getattr(component, param_name) # Parameter value in the object
            if pv not in params and isinstance(pv, Fittable):
                params.append(pv)
    lf = lossfunction(sample, required_conditions=model.required_conditions,
                      T_dur=model.T_dur, dt=model.dt, method=method,
                      nparams=len(params), samplesize=len(sample))
    return lf.loss(model)


def fit_model(sample,
              drift=DriftConstant(drift=0),
              noise=NoiseConstant(noise=1),
              bound=BoundConstant(B=1),
              IC=ICPointSourceCenter(),
              dt=param.dt, dx=param.dx, fitparams=None,
              fitting_method="differential_evolution",
              method=None,
              overlay=OverlayNone(),
              lossfunction=LossLikelihood,
              verbose=True,
              name="fit_model",
              verify=False):
    """Fit a model to reaction time data.
    
    The data `sample` should be a Sample object of the reaction times
    to fit in seconds (NOT milliseconds).  This function will generate
    a model using the `drift`, `noise`, `bound`, and `IC`
    parameters to specify the model.  At least one of these should
    have a parameter which is a "Fittable()" instance, as this will be
    the parameter to be fit.
    
    Optionally, dt specifies the temporal resolution with which to fit
    the model.

    `method` specifies how the model should be fit.
    "differential_evolution" is the default, which seems to be able to
    accurately locate the global maximum without using a
    derivative. "simple" uses a derivative-based method to minimize,
    and just uses randomly initialized parameters and gradient
    descent.  "basin" uses "scipy.optimize.basinhopping" to find an
    optimal solution, which is much slower but also gives better
    results than "simple".  It does not appear to give better results
    than "differential_evolution".

    `fitparams` is a dictionary of kwargs to be passed directly to the
    minimization routine for fine-grained low-level control over the
    optimization.  Normally this should not be needed.  

    `lossfunction` is a subclass of LossFunction representing the
    method to use when calculating the goodness-of-fit.  Pass the
    subclass itself, NOT an instance of the subclass.
    
    `name` gives the name of the model after it is fit.

    If `verify` is False (the default), checking for programming
    errors is disabled during the fit. This can decrease runtime and
    may prevent crashes.  If verification is already disabled, this
    does not re-enable it.
    
    `verbose` enables out-of-boundaries warnings and prints the model
    information at each evaluation of the fitness function.

    Returns a "Model()" object with the specified `drift`, `noise`,
    `bound`, `IC`, and `overlay`.

    The model will include a "FitResult" object, accessed as
    m.fitresult.  This can be used to get the value of the objective
    function, as well as to access diagnostic information about the
    fit.

    This function will automatically parallelize if set_N_cpus() has
    been called.
    """
    
    # Use the reaction time data (a list of reaction times) to
    # construct a reaction time distribution.
    T_dur = np.ceil(max(sample)/dt)*dt
    assert T_dur < 30, "Too long of a simulation... are you using milliseconds instead of seconds?"
    # For optimization purposes, create a base model, and then use
    # that base model in the optimization routine.  First, set up the
    # model with all of the Fittables inside.  Deep copy on the entire
    # model is a shortcut for deep copying each individual component
    # of the model.
    m = copy.deepcopy(Model(name=name, drift=drift, noise=noise, bound=bound, IC=IC, overlay=overlay, T_dur=T_dur, dt=dt, dx=dx))
    return fit_adjust_model(sample, m, fitparams=fitparams, fitting_method=fitting_method, 
                            method=method, lossfunction=lossfunction, verbose=verbose)


def fit_adjust_model(sample, model, fitparams=None, fitting_method="differential_evolution",
                     lossfunction=LossLikelihood, verify=False, method=None, verbose=True):
    """Modify parameters of a model which has already been fit.
    
    The data `sample` should be a Sample object of the reaction times
    to fit in seconds (NOT milliseconds).  At least one of the
    parameters for one of the components in the model should be a
    "Fitted()" instance, as these will be the parameters to fit.
    
    `fitting_method` specifies how the model should be fit.
    "differential_evolution" is the default, which seems to be able to
    accurately locate the global maximum without using a
    derivative. "simple" uses a derivative-based method to minimize,
    and just uses randomly initialized parameters and gradient
    descent.  "basin" uses "scipy.optimize.basinhopping" to find an
    optimal solution, which is much slower but also gives better
    results than "simple".  It does not appear to give better results
    than "differential_evolution".  Alternatively, a custom objective
    function may be used by setting `fitting_method` to be a function
    which accepts the "x_0" parameter (for starting position) and
    "constraints" (for min and max values).

    `fitparams` is a dictionary of kwargs to be passed directly to the
    minimization routine for fine-grained low-level control over the
    optimization.  Normally this should not be needed.  

    `lossfunction` is a subclass of LossFunction representing the
    method to use when calculating the goodness-of-fit.  Pass the
    subclass itself, NOT an instance of the subclass.

    `name` gives the name of the model after it is fit.

    If `verify` is False (the default), checking for programming
    errors is disabled during the fit. This can decrease runtime and
    may prevent crashes.  If verification is already disabled, this
    does not re-enable it.

    `method` gives the method used to solve the model, and can be
    "analytical", "numerical", "cn", "implicit", or "explicit".

    `verbose` enables out-of-boundaries warnings and prints the model
    information at each evaluation of the fitness function.

    Returns the same model object that was passed to it as an
    argument.  However, the parameters will be modified.  The model is
    modified in place, so a reference is returned to it for
    convenience only.

    After running this function, the model will be modified to include
    a "FitResult" object, accessed as m.fitresult.  This can be used
    to get the value of the objective function, as well as to access
    diagnostic information about the fit.

    This function will automatically parallelize if set_N_cpus() has
    been called.
    """
    # Disable paranoid if `verify` is False.
    paranoid_state = paranoid_settings.get('enabled')
    renorm_warnings_state = param.renorm_warnings
    if paranoid_state and not verify:
        paranoid_settings.set(enabled=False)
        param.renorm_warnings = False
    # Loop through the different components of the model and get the
    # parameters that are fittable.  Save the "Fittable" objects in
    # "params".  Create a list of functions to set the value of these
    # parameters, named "setters".
    m = model
    components_list = [m.get_dependence("drift"),
                       m.get_dependence("noise"),
                       m.get_dependence("bound"),
                       m.get_dependence("IC"),
                       m.get_dependence("overlay")]
    required_conditions = list(set([x for l in components_list for x in l.required_conditions]))
    assert 0 < len([1 for component in components_list
                      for param_name in component.required_parameters
                          if isinstance(getattr(component, param_name), Fittable)]), \
           "Models must contain at least one Fittable parameter in order to be fit"
    params = [] # A list of all of the Fittables that were passed.
    setters = [] # A list of functions which set the value of the corresponding parameter in `params`
    for component in components_list:
        for param_name in component.required_parameters:
            pv = getattr(component, param_name) # Parameter value in the object
            if isinstance(pv, Fittable):
                # Create a function which sets each parameter in the
                # list to some value `a` for model `x`.  Note the
                # default arguments to the function are necessary here
                # to preserve scope.  Without them, these variables
                # would be interpreted in the local scope, so they
                # would be equal to the last value encountered in the
                # loop.
                def setter(x,a,pv=pv,component=component,param_name=param_name):
                    if not isinstance(a, Fittable):
                        a = pv.make_fitted(a)
                    setattr(x.get_dependence(component.depname), param_name, a)
                    # Return the fitted instance so we can chain it.
                    # This way, if the same Fittable object is passed,
                    # the same Fitted object will be in both places in
                    # the solution.
                    return a 
                
                # If we have the same Fittable object in two different
                # components inside the model, we only want the Fittable
                # object in the list "params" once, but we want the setter
                # to update both.
                if id(pv) in map(id, params):
                    pind = list(map(id, params)).index(id(pv))
                    oldsetter = setters[pind]
                    # This is a hack way of executing two functions in
                    # a single function call while passing forward the
                    # same argument object (not just the same argument
                    # value)
                    newsetter = lambda x,a,setter=setter,oldsetter=oldsetter : oldsetter(x,setter(x,a)) 
                    setters[pind] = newsetter
                else: # This setter is unique (so far)
                    params.append(pv)
                    setters.append(setter)
                
    # And now get rid of the Fittables, replacing them with the
    # default values.  Simultaneously, create a list to pass to the
    # solver.
    x_0 = []
    constraints = [] # List of (min, max) tuples.  min/max=None if no constraint.
    for p,s in zip(params, setters):
        default = p.default()
        s(m, default)
        minval = p.minval if p.minval > -np.inf else None
        maxval = p.maxval if p.maxval < np.inf else None
        constraints.append((minval, maxval))
        x_0.append(default)
    # Set up a loss function
    lf = lossfunction(sample, required_conditions=required_conditions,
                      T_dur=m.T_dur, dt=m.dt, method=method,
                      nparams=len(params), samplesize=len(sample))
    # A function for the solver to minimize.  Since the model is in
    # this scope, we can make use of it by using, for example, the
    # model `m` defined previously.
    def _fit_model(xs):
        for x,p,s in zip(xs, params, setters):
            # Sometimes the numpy optimizers will ignore bounds up to
            # floating point errors, i.e. if your upper bound is 1,
            # they will give 1.000000000001.  This fixes that problem
            # to make sure the model is within its domain.
            if x > p.maxval:
                if verbose:
                    print("Warning: optimizer went out of bounds.  Setting %f to %f" % (x, p.maxval))
                x = p.maxval
            if x < p.minval:
                if verbose:
                    print("Warning: optimizer went out of bounds.  Setting %f to %f" % (x, p.minval))
                x = p.minval
            s(m, x)
        lossf = lf.loss(m)
        if verbose:
            print(repr(m), "loss="+ str(lossf))
        return lossf
    # Cast to a dictionary if necessary
    if fitparams is None:
        fitparams = {}
    # Run the solver
    if fitting_method == "simple":
        x_fit = minimize(_fit_model, x_0, bounds=constraints)
        assert x_fit.success, "Fit failed: %s" % x_fit.message
    elif fitting_method == "simplex":
        x_fit = minimize(_fit_model, x_0, method='Nelder-Mead')
    elif fitting_method == "basin":
        x_fit = basinhopping(_fit_model, x_0, minimizer_kwargs={"bounds" : constraints, "method" : "TNC"}, **fitparams)
    elif fitting_method == "differential_evolution":
        if "disp" not in fitparams.keys():
            fitparams["disp"] = verbose
        x_fit = differential_evolution(_fit_model, constraints, **fitparams)
    elif fitting_method == "hillclimb":
        x_fit = evolution_strategy(_fit_model, x_0, **fitparams)
    elif callable(fitting_method):
        x_fit = fitting_method(_fit_model, x_0=x_0, constraints=constraints)
    else:
        raise NotImplementedError("Invalid fitting method")
    res = FitResult(method=(method if method is not None else "auto"),
                    fitting_method=fitting_method, loss=lf.name, value=x_fit.fun,
                    nparams=len(params), samplesize=len(sample),
                    mess=(x_fit.message if "message" in x_fit.__dict__ else ""))
    m.fitresult = res
    print("Params", x_fit.x, "gave", x_fit.fun)
    for x,s in zip(x_fit.x, setters):
        s(m, x)
    if not verify:
        paranoid_settings.set(enabled=paranoid_state)
        param.renorm_warnings = renorm_warnings_state
    return m

def evolution_strategy(fitness, x_0, mu=1, lmbda=3, copyparents=True, mutate_var=.002, mutate_prob=.5, evals=100):
    """Optimize using the Evolution Strategy (ES) heuristic method.

    Evolution Strategy is an optimization method specified in the form
    (lambda + mu) or (lambda, mu), for some integer value of lambda
    and mu.  The algorithm will generate an intial population of
    lambda individuals.  Each individual will have an equal number of
    offspring, so that there is a total of mu organisms in the next
    generation.  In the case of the (lambda + mu) algorithm, the
    parents are also copied into the next generation.  Then, the
    lambda best organisms in this population are selected to
    reproduce.

    The starting population includes `x_0` and `lmbda`-1 other
    individuals generated by mutating `x_0`.  Mutations occur by
    perturbing `x_0` by a Gaussian-distributed variable (so-called
    "Gaussian convolution") with variance `mutate_var`.  Each element
    is changed with a probability `mutate_prob`.  The number of
    function evaluations will be approximately `evals`, as this
    algorithm will iterate `evals`/`lmbda` times.

    `lmbda` is the lambda parameter (note the spelling difference) and
    `mu` is the mu parameter for the ES.  If `copyparents` is True,
    use (`lmbda` + `mu`), and if it is False, use (`lmbda`, `mu`).

    The purpose of this is if you already have a good model, but you
    want to test the local space to see if you can make it better.
    """
    assert isinstance(lmbda, int) and isinstance(mu, int), "Bad lambda and mu"
    assert lmbda/mu == lmbda//mu, "Lambda must be a multiple of mu"
    x_0 = list(x_0) # Ensure we have a list, not an ndarray
    it = evals//lmbda
    
    # Mutation function: with a probability of `mutate_prob`, add a
    # uniform gaussian random variable multiplied by the current value
    # of the parameter, with variance `mutate_var`.
    mutate = lambda x : [e+np.random.normal(0, mutate_var) if np.random.random()<mutate_prob else e for e in x]
    # Set up the initial population.  We make the initial population
    # by mutating X_0.  This is not good for explorative search but is
    # good for exploitative search.
    P = [(x_0, fitness(x_0))]
    best = P[0]
    for _ in range(0, lmbda-1):
        new = mutate(x_0)
        fit = fitness(new)
        if fit < best[1]:
            best = (new, fit)
        P.append((new, fit))
    for _ in range(0, it):
        # Find the `mu` best individuals
        P.sort(key=lambda e : e[1])
        Q = P[0:mu]
        # Copy the parents if we're supposed to
        P = Q.copy() if copyparents else []
        # Create the next generation population
        for q in Q:
            for _ in range(0, lmbda//mu):
                new = mutate(q[0])
                fit = fitness(new)
                if fit < best[1]:
                    best = (new, fit)
                P.append((new, fit))
    return OptimizeResult(x=np.asarray(best[0]), success=True, fun=best[1], nit=it)

#@accepts(Model, Sample, Conditions, Unchecked, Set(["analytical", "numerical", "cn", "implicit", "explicit"]))
#@returns(Unchecked)
def solve_all_conditions(model, sample, conditions={}, method=None):
    """Solve the model for all conditions relevant to the sample.

    This takes the following parameters:

    - `model` - A Model() object
    - `sample` - A Sample() object which has conditions for each of
      the required conditions in `model`
    - `conditions` - Restrict to specific conditions
    - `method` - A string describing the solver method.  Can be
      "analytical", "numerical", "cn", "implicit", or "explicit".

    For each value of each relevant condition in sample (i.e. those in
    the model's required conditions), this will solve the model for
    that set of parameters.  It returns a dictionary indexed by a
    frozenset of the condition names and values, with the Solution
    object as the value, e.g.:
    
        {frozenset({('reward', 3)}): <Solution object>,
         frozenset({('reward', 1)}): <Solution object>}

    This function will automatically parallelize if set_N_cpus() has
    been called.
    """

    conds = sample.condition_combinations(required_conditions=model.required_conditions)
    if method is None:
        meth = model.solve
    elif method == "analytical":
        meth = model.solve_analytical
    elif method == "numerical":
        meth = model.solve_numerical
    elif method == "cn":
        meth = model.solve_numerical_cn
    elif method == "implicit":
        meth = model.solve_numerical_implicit
    elif method == "explicit":
        meth = model.solve_numerical_explicit
    else:
        raise ValueError("Invalid method "+method)

    cache = {}
    if _parallel_pool is None: # No parallelization
        for c in conds:
            cache[frozenset(c.items())] = meth(conditions=c)
        return cache
    else: # Parallelize across pool
        if paranoid_settings.get('enabled') is False:
            # The *2 makes sure that this runs on all subprocesses,
            # since you can't broadcast commands to all processes
            _parallel_pool.map(lambda x : paranoid_settings.set(enabled=False), [None]*_parallel_pool.n_cpus*2)
        sols = _parallel_pool.map(meth, conds, chunksize=1)
        for c,s in zip(conds, sols):
            cache[frozenset(c.items())] = s
        return cache


# TODO explicitly test this in unit tests
@accepts(Model, Maybe(Sample), Maybe(Conditions), Maybe(Set(["analytical", "numerical", "cn", "implicit", "explicit"])))
# @returns(Solution) # This doesn't actually return a solution, only a solution-like object
@requires('sample is not None --> all((c in sample.condition_names() for c in model.required_conditions))')
@requires('conditions is not None and sample is not None --> all((c in sample.condition_names() for c in conditions))')
@requires('conditions is not None and sample is None --> all((c in conditions for c in model.required_conditions))')
@requires("method == 'explicit' --> model.can_solve_explicit(conditions=conditions)")
@requires("method == 'cn' --> model.can_solve_cn()")
def solve_partial_conditions(model, sample=None, conditions=None, method=None):
    """Solve a model without specifying the value of all conditions

    This function solves `model` according to the ratio of trials in
    `sample`.  For example, suppose `sample` has 100 trials with high
    coherence and 50 with low coherence.  This will then return a
    solution with 2/3*(PDF high coherence) + 1/3*(PDF low coherence).
    This is especially useful when comparing a model to a sample which
    may have many different conditions.  

    Alternatively, if no sample is available, it will solve all
    conditions passed in `conditions` in equal ratios.

    The advantage to this function over Model.solve() is that the
    former can only handle a single value for each condition, whereas
    this function accepts can do it lists for condition values as
    well.

    The `conditions` variable limits the solution to a subset of
    `sample` which satisfy `conditions`.  The elements of the
    dictionary `conditions` should be specified either as values or as
    a list of values.

    Optionally, `method` describes the solver to use.  It can be
    "analytical", "numerical", "cn" (Crank-Nicolson), "implicit"
    (backward Euler), "explicit" (forward Euler), or None
    (auto-detect method).

    This function will automatically parallelize if set_N_cpus() has
    been called.

    """
    if conditions is None:
        conditions = {}
    T_dur = model.T_dur
    dt = model.dt
    if sample:
        # If a sample is passed, include only the parts of the sample
        # that satisfy the passed conditions.
        samp = sample.subset(**conditions)
    else:
        # If no sample is passed, create a dummy sample.  For this, we
        # need all of the conditions to be specified in the
        # "conditions" variable.  We then construct a sample with
        # exactly one element correct and zero elements error for each
        # potential combinations of conditions.  For instance, if
        # there are two conditions with only one value of each passed
        # (as scalars), only one element will be created.  If each of
        # these two instead has two values passed (as a list), create
        # four elements in the sample, etc.
        assert len(set(model.required_conditions) - set(conditions.keys())) == 0, \
            "If no sample is passed, all conditions must be specified"
        # Build cond_combs as the data matrix iteratively. Initial
        # value is a correct response with an RT of 1 (as per the
        # first expected elements of Sample.from_numpy_array().
        cond_combs = [[0, 1]] 
        all_conds = list(sorted(conditions.keys()))
        for c in all_conds:
            vs = conditions[c]
            if not isinstance(vs, list):
                vs = [vs]
            cond_combs = [cc + [v] for cc in cond_combs for v in vs]
        samp = Sample.from_numpy_array(np.asarray(cond_combs), all_conds)
    model_corr = 0*model.t_domain()
    model_err = 0*model.t_domain()
    model_undec = -1 # Set to dummy value -1 so we can detect this in our loop
    # If we have an overlay, this function should not calculate the
    # (incorrect) undecided probability
    if not isinstance(model.get_dependence("overlay"), OverlayNone):
        model_undec = None
    all_conds = solve_all_conditions(model, samp, conditions=conditions, method=method)
    for conds in samp.condition_combinations(required_conditions=model.required_conditions):
        subset = samp.subset(**conds)
        sol = all_conds[frozenset(conds.items())]
        model_corr += len(subset)/len(samp)*sol.pdf_corr()
        model_err += len(subset)/len(samp)*sol.pdf_err()
        # We can't get the size of the undecided pdf until we have a
        # specific set of conditions.  Once we do, if the simulation
        # method doesn't support an undecided probability, set it to
        # None.  If it does, add it together, making sure they are
        # always the same size.  (They may not be the same size if the
        # bound depends on a parameter.)  If they are ever not the
        # same size, set it to None rather than trying to align them.
        if sol.undec is not None and isinstance(model_undec, int) and model_undec == -1:
            model_undec = len(subset)/len(samp)*sol.pdf_undec()
        if sol.undec is not None and model_undec is not None and len(model_undec) == len(sol.undec):
            model_undec += len(subset)/len(samp)*sol.pdf_undec()
        else:
            model_undec = None
    return Solution(model_corr*model.dt, model_err*model.dt, model, conditions, pdf_undec=model_undec)

@accepts(Model)
@returns(Boolean)
def hit_boundary(model):
    """Returns True if any Fitted objects are close to their min/max value"""
    components_list = [model.get_dependence("drift"),
                       model.get_dependence("noise"),
                       model.get_dependence("bound"),
                       model.get_dependence("IC"),
                       model.get_dependence("overlay")]
    hit = False
    for component in components_list:
        for param_name in component.required_parameters:
            pv = getattr(component, param_name) # Parameter value in the object
            if isinstance(pv, Fitted):
                if (pv - pv.minval)/(pv.maxval-pv.minval) < .01: # No abs because pv always > pv.minval
                    print("%s hit the lower boundary of %f with value %f" % (param_name, pv.minval, pv))
                    hit = True
                if (pv.maxval-pv)/(pv.maxval-pv.minval) < .01: # No abs because pv.maxval always > pv
                    print("%s hit the lower boundary of %f with value %f" % (param_name, pv.maxval, pv))
                    hit = True
    return hit

@accepts(Fittable)
@returns(Boolean)
def dependence_hit_boundary(pv):
    """Returns True if a Fitted instance has hit the boundary.

    Fitted instances may have minimum or maximum values attached to
    them.  If it does, and if it has gotten close to this min/max
    while fitting, return True.  Otherwise, or if the value is not a
    Fitted object, return False.
    """
    if isinstance(pv, Fitted):
        if (pv - pv.minval)/(pv.maxval-pv.minval) < .01: # No abs because pv always > pv.minval
            return True
        if (pv.maxval-pv)/(pv.maxval-pv.minval) < .01: # No abs because pv.maxval always > pv
            return True
    return False

def display_model(model, print_output=True):
    """A readable way to display models.

    `model` should be any Model object.  Prints a description of the
    model, and does not return anything.
    """
    OUT = ""
    assert isinstance(model, Model), "Invalid model"
    # Separate the code to display a single component so we can reuse
    # it to display the components of chains (e.g. OverlayChain).
    def display_component(component, prefix=""):
        OUT = ""
        OUT += prefix+"%s" % component.name + "\n"
        fixed = []
        fitted = []
        fittable = []
        if len(component.required_parameters) == 0:
            OUT += prefix+"(No parameters)" + "\n"
        for param_name in component.required_parameters:
            pv = getattr(component, param_name) # Parameter value in the object
            if isinstance(pv, Fitted):
                if dependence_hit_boundary(pv):
                    fitted.append(prefix+"- %s: %f (WARNING: AT BOUNDARY)" % (param_name, pv))
                else:
                    fitted.append(prefix+"- %s: %f" % (param_name, pv))
            elif isinstance(pv, Fittable):
                fittable.append(prefix+"- %s: Fittable (default %f)" % (param_name, pv.default()))
            else:
                fixed.append(prefix+"- %s: %f" % (param_name, pv))
        for t,vs in [("Fixed", fixed), ("Fitted", fitted), ("Fittable", fittable)]:
            if len(vs) > 0:
                OUT += prefix+t+" parameters:" + "\n"
                for v in vs:
                    OUT += v + "\n"
        return OUT
    # Start displaying the model information
    OUT += ("Model %s information:\n" % model.name) if model.name != "" else "Model information:" + "\n"
    for component in model.dependencies:
        OUT += "%s component %s:" % (component.depname, type(component).__name__) + "\n"
        if isinstance(component, OverlayChain):
            for o in component.overlays:
                OUT += "    %s component %s:" % (o.depname, type(o).__name__) + "\n"
                OUT += display_component(o, prefix="        ")
        else:
            OUT += display_component(component, prefix="    ")
    if not isinstance(model.fitresult, FitResultEmpty):
        OUT += "Fit information:\n"
        OUT += "    Loss function: %s\n" % model.fitresult.loss
        OUT += "    Loss function value: %s\n" % model.fitresult.value()
        OUT += "    Fitting method: %s\n" % model.fitresult.fitting_method
        OUT += "    Solver: %s\n" % ("forward Euler" if model.fitresult.method == "explicit" \
                                     else "backward Euler" if model.fitresult.method == "implicit" \
                                     else "Crank-Nicoloson" if model.fitresult.method == "cn" \
                                     else model.fitresult.method)
        OUT += "    Other properties:\n"
        for p,v in model.fitresult.properties.items():
            OUT += "        - %s: %s\n" % (p,repr(v))
    if not print_output:
        return OUT
    else:
        print(OUT)
