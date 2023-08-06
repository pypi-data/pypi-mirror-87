import numpy as np
import emcee
import pandas as pd
from .peakbagging import define_window
from .bayesian import (log_prior) 
from .chain_reader import (hdf5_to_pkb, chain_to_a2z,
                           read_chain, chain_element_to_a2z)
from .likelihood import wrapped_log_l
from .fit_tools import a2z_to_pkb, make_cornerplot
from .analyse_window import sidelob_param
from pathos.multiprocessing import ProcessPool
import glob
from os import path
import scipy
from scipy.integrate import trapz
from tqdm import tqdm

def rebinned_power (freq, psd, f0, t) :
  '''
  Return the rebinned power with a rebinning t around the frequency f0.
  '''

  res = freq[2] - freq[1]
  indexes, = np.nonzero ((freq>f0-res)&(freq<f0+res))
  ii = indexes[0]

  rp = np.sum (psd[ii-int (t/2):ii+int (t/2) + 1]) / t 

  return rp 

def pdet_h0 (freq, psd, f0, t) :

  '''
  Test the probability to have a given power value considering a H0 hypothesis.
  '''

  rp = rebinned_power (freq, psd, f0, t)
  pdet = np.power (rp, t-1) * np.exp (-rp) / scipy.special.gamma (t)

  return pdet

def test_h0 (freq, psd, back, pkb, tmax=99) : 

  '''
  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power vector
  :type psd: ndarray

  :param back: model background power vector.
  :type back: ndarray

  :param pkb: pkb array with the parameters of the fitted modes, The H0 test will be 
    performed around the modes frequency.
  :type pkb: ndarray

  :param tmax: max number of rebinning that will be performed around the considered mode
    frequency. Rebinning values are all odds and ``tmax`` must be odd too. Optional, default 
    99.   
  '''

  if tmax%2!=1 :
    raise Exception ('tmax must be odd')

  aux_psd = psd/back
  aux = pkb[:,:3]

  result = np.zeros ((pkb.shape[0], (tmax+1)//2 + 3))

  for ii, elt in enumerate (aux) :
    result[ii, 0] = elt[0]
    result[ii, 1] = elt[1]
    result[ii, 2] = elt[2]
    for jj, t in zip (range (3, result.shape[1]), range (1, tmax+1, 2)) :
      p = pdet_h0 (freq, aux_psd, elt[2], t)
      result[ii, jj] = p

  return result

def likelihood_mode (param_pkb, freq, psd, back, free=1, use_sinc=False, asym_profile='nigam-kosovichev', param_wdw=None, instr='geometric') :

  log_l_sw = wrapped_log_l (freq, psd, back, free, param_pkb, instr, param_wdw, use_sinc, asym_profile)
  log_l_s = wrapped_log_l (freq, psd, back, free, param_pkb[param_pkb[:,1]<2, :], instr, param_wdw, use_sinc, asym_profile)

  return log_l_sw, log_l_s

def likelihood_h0 (psd, free=1) :

  model_h0 = np.full (psd.size, np.median (psd))
  #model_h0 = np.full (psd.size, free)
  aux = psd / model_h0 + np.log (model_h0)
  log_l_h0 = np.sum (aux)

  return log_l_h0

def model_likelihood_h1 (param_pkb, freq, psd, back, free=1, use_sinc=False, asym_profile='nigam-kosovichev', param_wdw=None, instr='geometric') :
  '''
  Compute the likelihood of the different models to compare.

  :return: in the following order, negative logarithmic likelihood of the model with two modes, of the model with only the strong mode
    and of the H0 model. 
  :rtype: tuple of float 
  '''

  log_l_sw, log_l_s = likelihood_mode (param_pkb, freq, psd, back, free=free, 
                                       use_sinc=use_sinc, asym_profile=asym_profile, 
                                       param_wdw=param_wdw, instr=instr)
  log_l_h0 = likelihood_h0 (psd)

  return log_l_sw, log_l_s, log_l_h0

def param_h1_bayes () :

  param = np.full (2, 0.25)
  low_bounds = np.empty (param.size)
  up_bounds = np.empty (param.size)
  low_bounds[0] = 1e-15
  low_bounds[1] = 1e-15
  up_bounds[0] = 1
  up_bounds[1] = 1
  bounds = np.c_[low_bounds, up_bounds]

  return param, bounds

def log_probability_h1 (param, bounds, log_l_sw, log_l_s, log_l_h0) :
  '''
  A log likelihood for the h1 test taking as parameters the probability of each detection model for a pair
  of mode.

  :param param: ``param[0]`` is the proba of detecting the two modes and ``param[1]`` is the proba to detect
    only the stronger mode. 
  :type param: ndarray
  '''

  l_prior = log_prior (bounds, param)

  if not np.isfinite (l_prior) :
    return - np.inf
  if param[0] + param[1] > 1 :
    return - np.inf

  proba = (1 - param[0] - param[1]) * np.exp (-log_l_h0) + param[0] * np.exp (-log_l_sw) + param[1] * np.exp (-log_l_s)

  l_proba = l_prior + np.log (proba)

  return l_proba

def bayes_factor (freq, psd, back, df_a2z, n, strategy='pair', l02=True, dnu=None, do_not_use_dnu=True, 
                  thin=10, discard=0, instr='geometric', use_sinc=False, asym_profile='nigam-kosovichev', hdf5Dir='./',
                  progress=True, wdw=None, add_ampl=False) :

  '''
  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power vector
  :type psd: ndarray

  :param back: model background power vector.
  :type back: ndarray

  :param n: mode order for which the statistical test will evaluate the model. 
  :type n: int

  :param df_a2z: a2z input DataFrame that was used for the fit. The DataFrame is only used to compute
    the window inside which the fit was performed. 
  :type df_a2z: pandas DataFrame

  :param strategy: strategy that was used for the fit, ``order`` or ``pair``. Optional, default ``pair``. 
  :type strategy: str

  :param l02: If set to True, the model will be evaluated for the even pair, for the odd pair if set to ``False``.
    Optional, default ``True``.
  :type l02: bool

  :param dnu: large separation of the modes. In this function, it will only be used to adapt the fitting window for 
  fitted modes above 1200 muHz. Optional, default ``None``. 
  :type dnu: float.

  :param do_not_use_dnu: if set to ``True``, fitting window will be computed without using dnu value. Optional, default ``True``.
  :type do_not_use_dnu: bool

  :return: tuple of float, in the following order: probability of model with two modes, probability of model with only the strong 
    mode, probaility of the H0 hypothesis, number of models on which the probability has been estimated. 
  :rtype: ndarray
  '''

  if wdw is not None :
    dt = 1 / (2*freq[-1])
    param_wdw = sidelob_param (wdw, dt=dt)
  else :
    param_wdw = None

  # Input df_a2z is used only to redefine the same fitting window
  df_a2z.loc[:,6] = 1
  if l02 :
    df_a2z.loc[(df_a2z[0]==str(n))&(df_a2z[1]=='0'), 6] = 0
    df_a2z.loc[(df_a2z[0]==str(n-1))&(df_a2z[1]=='2'), 6] = 0
  else :
    df_a2z.loc[(df_a2z[0]==str(n))&(df_a2z[1]=='1'), 6] = 0
    df_a2z.loc[(df_a2z[0]==str(n-1))&(df_a2z[1]=='3'), 6] = 0
  up_bound, low_bound = define_window (df_a2z, strategy, dnu=dnu, do_not_use_dnu=do_not_use_dnu)
  aux_freq = freq[(freq>low_bound)&(freq<up_bound)]
  aux_back = back[(freq>low_bound)&(freq<up_bound)]
  aux_psd = psd[(freq>low_bound)&(freq<up_bound)] / aux_back 

  # The sampler is searched and read to obtain the pkb
  if strategy == 'pair' :
    if l02 :
      filename = 'mcmc_sampler_order_' + str(n).rjust (2, '0') + '_degrees_02.h5'
    else :
      filename = 'mcmc_sampler_order_' + str(n).rjust (2, '0') + '_degrees_13.h5'
  else :
      filename = 'mcmc_sampler_order_' + str(n).rjust (2, '0') + '.h5'

  filename = path.join (hdf5Dir, filename)

  flatchain, labels, degrees, order = read_chain (filename, thin=thin, discard=discard)
  p0 = 0 
  psw = 0
  ps = 0
  log_l_h0 = likelihood_h0 (aux_psd)
  
  for param in tqdm (flatchain) :
    df = chain_element_to_a2z (param, labels, degrees, order, add_ampl=add_ampl, instr=instr) 
    pkb = a2z_to_pkb (df)
    free = param[labels=='background']
    log_l_sw, log_l_s = likelihood_mode (pkb, aux_freq, aux_psd, aux_back, free=free, use_sinc=use_sinc, 
                                         asym_profile=asym_profile, param_wdw=param_wdw, instr=instr)
    #log_l_h0 = likelihood_h0 (aux_psd, free)
    # We are working with negative likelihood
    if (log_l_sw <= log_l_s) & (log_l_sw < log_l_h0) :
      psw += 1
    if (log_l_s < log_l_h0) & (log_l_s < log_l_sw) :
      ps += 1
    if (log_l_h0 <= log_l_sw) & (log_l_h0 <= log_l_s) :
      p0 += 1

  psw = psw / flatchain.shape[0]
  ps = ps / flatchain.shape[0]
  p0 = p0 / flatchain.shape[0]

  return psw, ps, p0, flatchain.shape[0]

