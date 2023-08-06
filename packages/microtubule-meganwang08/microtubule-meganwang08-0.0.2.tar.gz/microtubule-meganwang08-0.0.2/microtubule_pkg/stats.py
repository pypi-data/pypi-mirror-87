import numpy as np
import pandas as pd
import scipy.stats as st
import numba
import scipy.optimize
import scipy.stats as st
import warnings
import tqdm
import bebi103
try:
    import multiprocess
except:
    import multiprocessing as multiprocess

rg = np.random.default_rng(1284)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#2.2
def ecdf_vals(raw_data):
    """
    Computes the empirical cumulative distribution function for a collection of provided data.
    Parameters
    ----------
    raw_data : 1d-array, Pandas Series, or list
        One-dimensional collection of data for which the ECDF will
        be computed
    Returns
    -------
    x, y : 1d-arrays
        The sorted x data and the computed ECDF
    """
    data = np.array(raw_data)
    return (np.sort(data), np.arange(0,len(data)) / len(data))

#5.1
def catastrophe_sim(b_pairs_):
    """
    Simulats microtubule catastrophe using the time between poisson processes as an exponential
    distribution.
    Parameters
    ----------
    b_pairs_ : Nested 1D list ex: [[1,9],[3,5],[2,4]]
        collection of data for which the catastrope
        simulation will be computed
    Returns
    -------
    catastrope_simulation: dictionary of catastrope points
    keys are indexes from b_pairs_ and values are an 1D array
    simulated valuess
    """
    catastrophe_simulation = {}
    for n, pair in enumerate(b_pairs_):
        catastrophe_simulation[n] = (np.array([rg.exponential(1/pair[0]) + rg.exponential(1/pair[1]) for i in range(150)]))
    return catastrophe_simulation

def __pdf_func(t, b1, b2):
    """
    Computes the pdf/ecdf distribution function for a collection of provided data.
    Parameters
    ----------
    t : 1d- numpy array of time points
    b1, b2: numerical values for b1 and b2
    Returns
    -------
    1d-arrays with the theoretical for the pdf/ecdf
    """
    return ((b1*b2)/(b2 - b1))*(np.e**(-b1*t) - np.e**(-b2*t))

def cdf_func(t, b1, b2):
    """
    Computes the cdf distribution function for a collection of provided data.
    Parameters
    ----------
    t : 1d- numpy array of time points
    b1, b2: numerical values for b1 and b2
    Returns
    -------
    1d-arrays with the theoretical for the cdf
    """
    return ((b1*b2)/(b2 - b1))*((1/b1)*(1 - np.e**(-b1*t)) - (1/b2)*(1 - np.e**(-b2*t)))

#6.1
@numba.njit
def draw_bs_sample(data):
    """Draw a bootstrap sample from a 1D data set."""
    return np.random.choice(data, size=len(data))

@numba.njit
def draw_perm_sample(x, y):
    """Generate a permutation sample."""
    concat_data = np.concatenate((x, y))
    np.random.shuffle(concat_data)
    return concat_data[:len(x)], concat_data[len(x):]

def draw_perm_reps_ks_2samp(x, y, size=1):
    """Generate ks values from two 1D data sets."""
    out = np.empty(size)
    for i in range(size):
        x_perm, y_perm = draw_perm_sample(x, y)
        out[i] = scipy.st.ks_2samp(x_perm, y_perm, alternative='two-sided')[0]
    return out

def __ecdf(x, data):
    """Give the value of an ECDF at arbitrary points x."""
    y = np.arange(len(data) + 1) / len(data)
    return y[np.searchsorted(np.sort(data), x, side="right")]

def dkw_conf_int(x, data, alpha):
    """Compute a DKW confidence interval."""
    epislon = np.sqrt(np.log(2/alpha) / 2 / len(data))

    ecdf_y = __ecdf(x, data)

    lower_bound = np.maximum(0, ecdf_y - epislon)
    upper_bound = np.minimum(1, ecdf_y + epislon)

    return lower_bound, upper_bound

#8.2A
def log_like_iid_gamma(params, n):
    """Log likelihood for i.i.d. Ganmma measurements."""
    alpha, beta = params

    if alpha <= 0 or beta <= 0:
        return -np.inf

    return np.sum(st.gamma.logpdf(n, alpha, loc=0, scale=1/beta))

def mle_iid_gamma(n):
    """Perform maximum likelihood estimates for parameters for i.i.d.
    gamma measurements, parametrized by alpha, beta"""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        res = scipy.optimize.minimize(
            fun=lambda params, n: -log_like_iid_gamma(params, n),
            x0=np.array([2.2, 0.005]),
            args=(n,),
            method='Powell'
        )

    if res.success:
        alpha, beta = res.x

    else:
        raise RuntimeError('Convergence failed with message', res.message)

    return res.x

def draw_bs_sample(data):
    """Draw a bootstrap sample from a 1D data set."""
    return rg.choice(data, size=len(data))


def draw_bs_reps_mle(mle_fun, data, args=(), size=1, progress_bar=False):
    """Draw nonparametric bootstrap replicates of maximum likelihood estimator.

    Parameters
    ----------
    mle_fun : function
        Function with call signature mle_fun(data, *args) that computes
        a MLE for the parameters
    data : one-dimemsional Numpy array
        Array of measurements
    args : tuple, default ()
        Arguments to be passed to `mle_fun()`.
    size : int, default 1
        Number of bootstrap replicates to draw.
    progress_bar : bool, default False
        Whether or not to display progress bar.

    Returns
    -------
    output : numpy array
        Bootstrap replicates of MLEs.
    """
    if progress_bar:
        iterator = tqdm.tqdm(range(size))
    else:
        iterator = range(size)

    return np.array([mle_fun(draw_bs_sample(data), *args) for _ in iterator])

#8.2B

def derived_log_likelihood(n, beta_1, delta_beta):
    """
    finds derivated log likelihood for beta and delta_beta
    """
    ans = []
    for number in n:
        a = np.log(beta_1 * (beta_1 + delta_beta) / delta_beta)
        b = -beta_1 * number
        c = np.log(1 - np.exp(-delta_beta * number))
        ans.append(a + b + c)
    return ans

def log_like_iid_derived(params, n):
    """Log likelihood for i.i.d. microtubule measurements using derived PDF
    from hw5.2. parameterized by beta_1, delta_beta"""
    beta_1, delta_beta = params
    if beta_1 <= 0 or delta_beta <= 0:
        return -np.inf
    return np.sum(derived_log_likelihood(n, beta_1, delta_beta))

def mle_iid_derived(n):
    """Obtain maximum likelihood estimates for parameters for
    the microtubule time to catastrophe measurements, parametrized by beta_1, delta_beta"""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = scipy.optimize.minimize(
            fun=lambda params, n: -log_like_iid_derived(params, n),
            x0=np.array([2, 1]),
            args=(n,),
            method='Powell'
        )

    if res.success:
        beta_1, delta_beta = res.x
        beta_2 = delta_beta + beta_1
    else:
        raise RuntimeError('Convergence failed with message', res.message)
    return np.append(res.x, beta_2)

def gen_samples(beta_1, delta_beta, beta2_, size, rg):
    """
    generates bootstrap samples from beta_1, delta_beta, beta2_, given a size and rg
    """
    beta_2 = delta_beta + beta_1
    return rg.exponential(1/beta_1, size=size) + rg.exponential(1/beta_2, size=size)

def draw_parametric_bs_reps_mle(
    mle_fun, gen_fun, data, args=(), size=1, n_jobs=1, progress_bar=False
):
    """Draw nonparametric bootstrap replicates of maximum likelihood estimator.

    Parameters
    ----------
    mle_fun : function
        Function with call signature mle_fun(data, *args) that computes
        a MLE for the parameters
    gen_fun : function
        Function to randomly draw a new data set out of the model
        distribution parametrized by the MLE. Must have call
        signature `gen_fun(*params, size, *args, rg)`.
    data : one-dimemsional Numpy array
        Array of measurements
    args : tuple, default ()
        Arguments to be passed to `mle_fun()`.
    size : int, default 1
        Number of bootstrap replicates to draw.
    n_jobs : int, default 1
        Number of cores to use in drawing bootstrap replicates.
    progress_bar : bool, default False
        Whether or not to display progress bar.

    Returns
    -------
    output : numpy array
        Bootstrap replicates of MLEs.
    """
    # Just call the original function if n_jobs is 1 (no parallelization)
    if n_jobs == 1:
        return _draw_parametric_bs_reps_mle(
            mle_fun, gen_fun, data, args=args, size=size, progress_bar=progress_bar
        )

    # Set up sizes of bootstrap replicates for each core, making sure we
    # get all of them, even if sizes % n_jobs != 0
    sizes = [size // n_jobs for _ in range(n_jobs)]
    sizes[-1] += size - sum(sizes)

    # Build arguments
    arg_iterable = [(mle_fun, gen_fun, data, args, s, progress_bar, None) for s in sizes]

    with multiprocess.Pool(n_jobs) as pool:
        result = pool.starmap(_draw_parametric_bs_reps_mle, arg_iterable)

    return np.concatenate(result)

def _draw_parametric_bs_reps_mle(
    mle_fun, gen_fun, data, args=(), size=1, progress_bar=False, rg=None,
):
    """Draw parametric bootstrap replicates of maximum likelihood estimator.

    Parameters
    ----------
    mle_fun : function
        Function with call signature mle_fun(data, *args) that computes
        a MLE for the parameters
    gen_fun : function
        Function to randomly draw a new data set out of the model
        distribution parametrized by the MLE. Must have call
        signature `gen_fun(*params, size, *args, rg)`.
    data : one-dimemsional Numpy array
        Array of measurements
    args : tuple, default ()
        Arguments to be passed to `mle_fun()`.
    size : int, default 1
        Number of bootstrap replicates to draw.
    progress_bar : bool, default False
        Whether or not to display progress bar.
    rg : numpy.random.Generator instance, default None
        RNG to be used in bootstrapping. If None, the default
        Numpy RNG is used with a fresh seed based on the clock.

    Returns
    -------
    output : numpy array
        Bootstrap replicates of MLEs.
    """
    if rg is None:
        rg = np.random.default_rng()

    params = mle_fun(data, *args)

    if progress_bar:
        iterator = tqdm.tqdm(range(size))
    else:
        iterator = range(size)

    return np.array(
        [mle_fun(gen_fun(*params, size=len(data), *args, rg=rg)) for _ in iterator]
    )

#9.1
def gen_gamma(alpha, beta, size, rg):
    """
    generates random alphas from gamma distribution of an inputed size
    """
    return rg.gamma(alpha, scale=1/beta, size=size)
