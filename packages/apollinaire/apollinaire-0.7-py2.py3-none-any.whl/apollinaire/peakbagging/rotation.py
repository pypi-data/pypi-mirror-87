# coding: utf-8

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from .modified_optimize import _minimize_powell
from .fit_tools import *
from pathos.multiprocessing import ProcessPool
import sys
import numdifftools as nd
import matplotlib
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import emcee
import corner
from apollinaire.psd import degrade_psd
from .background import (background_model, extract_param,
                        log_prior, harvey)


def convert_prot (prot) :
  '''
  Convert input prot (in days) to frequency (in µHz).
  '''
  f = 1e6 / (prot*86400)

  return f

def create_label (n_harvey, n_harmonic) :

  labels = ['f1']
  for ii in range (n_harmonic) :
    labels.append ('h_' + str (ii+1))
    labels.append ('w_' + str (ii+1))
  for ii in range (n_harvey) :
    labels.append ('A_H_' + str (ii+1))
    labels.append ('nuc_H_' + str (ii+1))
    labels.append ('alpha_H_' + str (ii+1))

  return labels


def compute_cuts (f1, n_harmonic, numax) :

  cut_peak = (n_harmonic+2) * f1
  high_cut = 1./3. * numax

  return cut_peak, high_cut

def create_vector_to_fit (freq, psd, n_harmonic, low_cut, f1, numax, num=5000, smoothing=50) :

  cut_peak, high_cut = compute_cuts (f1, n_harmonic, numax)

  psd = psd[(freq>low_cut)&(freq<high_cut)]
  freq = freq[(freq>low_cut)&(freq<high_cut)]

  aux_freq_1 = freq[freq<cut_peak]
  aux_psd_1 = psd[freq<cut_peak]
  aux_freq_2 = freq[freq>cut_peak]
  aux_psd_2 = psd[freq>cut_peak]

  aux_freq_2, aux_psd_2 = degrade_psd (aux_freq_2, aux_psd_2, smoothing=smoothing, num=num)

  freq_fit = np.concatenate ((aux_freq_1, aux_freq_2))
  psd_fit = np.concatenate ((aux_psd_1, aux_psd_2))

  return psd_fit, freq_fit

def create_param_vector (f1, height, width, param_back, n_harvey=2, n_harmonic=1) :
  '''
  Create input param vector for rotation peak fit.

  :param f1: initial guess for first harmonic frequency value.
  :type f1: float

  :param height: height of the first harmonic
  :type height: float
 
  :param width: width of the first harmonic
  :type width: float

  :param_back: background parameter vector obtained with a background fit.
  :type param_back: array-like

  :param n_harvey: number of Harvey model which were used to fit the background.
    Optional, default 2.
  :type n_harvey: int
  '''

  input_param = np.empty (1+2*n_harmonic+3*n_harvey)
  
  input_param[0] = f1 
  for ii in range (n_harmonic) :
    input_param [1+2*ii] = height / (ii+1)
    input_param [2+2*ii] = width
  input_param[1+2*n_harmonic:] = param_back[:3*n_harvey]

  return input_param

def create_rotation_guess (freq, psd, prot, param_back, n_harvey=2, n_harmonic=1) :

  f1 = convert_prot (prot)
  back_model = background_model (freq, param_harvey=param_back[:3*n_harvey], n_harvey=n_harvey)
  w = 1e-2 * f1
  aux = psd - back_model
  h = np.maximum (0, np.mean (aux[(freq>f1-w)&(freq<f1+w)])) 
  guess = create_param_vector (f1, h, w, param_back, n_harvey=n_harvey, n_harmonic=n_harmonic)

  return guess

def get_low_bounds (guess, low_cut, n_harmonic=1) :

  low_bounds = np.empty (guess.size)
  low_bounds[0] = 0.95 * guess[0]
  low_bounds[1] = 0.1 * guess[1]
  for ii in range (n_harmonic) :
    low_bounds[1+2*ii] = 0.
    low_bounds[2+2*ii] = 0.
  low_bounds[1+2*n_harmonic:] = 0.9 * guess[1+2*n_harmonic]

  return low_bounds

def get_up_bounds (guess, n_harmonic=1) :

  up_bounds = np.empty (guess.size)
  up_bounds [0] = 1.05 * guess[0]
  up_bounds[1] = 3. * guess[1]
  for ii in range (n_harmonic) :
    up_bounds[1+2*ii] = 5. * guess[1+2*ii]
    up_bounds[2+2*ii] = 5. * guess[1+2*ii]
  up_bounds[1+2*n_harmonic:] = 1.1 * guess[1+2*n_harmonic:]

  return up_bounds

def param_split (param, n_harmonic=1) :

  param_rot = param[:1+2*n_harmonic]
  param_harvey = param[1+2*n_harmonic:]

  return param_harvey, param_rot

def peak_model (freq, param_rot, n_harmonic, profile='gaussian') :

  model = np.zeros (freq.size)

  f1 = param_rot[0]

  for ii in range (n_harmonic) :
    A = param_rot[1+2*ii] 
    w = param_rot[2+2*ii] 
    xxx = (freq - (ii+1)*f1) / w
    if profile == 'lorentzian' :
      model += A / (1 + 4. * xxx * xxx)
    if profile == 'sinc' :
      model += A * np.sinc (xxx) * np.sinc (xxx)
    if profile == 'gaussian' :
      model += A * np.exp (- xxx * xxx)

  return model

def rotation_model (freq, psd, param, n_harvey, n_harmonic, noise=0) :

  param_harvey, param_rot = param_split (param, n_harmonic)
  model = background_model (freq, param_harvey, n_harvey=n_harvey, noise=noise)
  model = model + peak_model (freq, param_rot, n_harmonic)
  return model

def log_likelihood_rotation (param, freq, psd, n_harvey, n_harmonic, noise=0) :
  '''
  Compute negative log_likelihood for fitting model on 
  background.

  :param param: param to fit passed by perform_mle_back. Param are given in 
  the following order: Harvey law parameters, power law parameters, Gaussian p-mode 
  envelope parameters, noise constant. 

  :param freq: frequency vector in µHz.
  :type freq: ndarray

  :param psd: power density vector in ppm^2/µHz or (m/s)^2/muHz.
  :type psd: ndarray

  :param n_harvey: number of Harvey laws to use to build the background
  model.  
  :type n_harvey: int

  :param n_harmonic: number of Harvey laws to use to build the background
  model.  
  :type n_harmonic: int
  '''

  model = rotation_model (freq, psd, param, n_harvey, n_harmonic, noise=noise)

  aux = psd / model + np.log (model)
  log_l = np.sum (aux)

  return log_l

def log_probability_rotation (param_to_fit, freq, psd, bounds, n_harvey, n_harmonic, norm=None, noise=0) :
  '''
  Compute the positive posterior log probability (unnormalised) of the parameters to fit. 

  :param_to_fit: backgrounds parameters to fit.
  :type param_to_fit: 1d ndarray
 
  :param param: param to fit passed by perform_mle_back.  

  :param freq: frequency vector in µHz.
  :type freq: ndarray

  :param psd: power density vector in ppm^2/µHz or (m/s)^2/muHz.
  :type psd: ndarray

  :param n_harvey: number of Harvey laws to use to build the background
  model.  
  :type n_harvey: int

  :param n_harmonic: number of Harvey laws to use to build the background
  model.  
  :type n_harmonic: int

  :param norm: if given, the param_to_fit and bounds input vectors will be multiplied by this vector. 
  Optional, default ``None``.
  :type norm: ndarray

  :return: posterior probability value
  :rtype: float
  '''

  param_to_fit = np.copy (param_to_fit) #make a copy to not modify the reference array
  bounds = np.copy (bounds)

  if norm is not None :
    param_to_fit = param_to_fit * norm
    bounds[:,0] = bounds[:,0] * norm
    bounds[:,1] = bounds[:,1] * norm

  l_prior = log_prior (param_to_fit, bounds)

  if not np.isfinite (l_prior) :
    return - np.inf
  l_likelihood = - log_likelihood_rotation (param_to_fit, freq, psd, n_harvey, n_harmonic, noise=noise)

  l_proba = l_prior + l_likelihood

  return l_proba

def visualise_rotation (freq, psd, low_cut, f1, numax, param_fitted=None, guess=None, n_harvey=2,
                        n_harmonic=3, filename=None, spectro=True, alpha=1., show=False, noise=0) :

  '''
  Plot fitted rotation peaks against real PSD (and possibly against initial guess).
  '''

  cut_peak, high_cut = compute_cuts (f1, n_harmonic, numax)

  if (param_fitted is None) and (guess is None) :
    raise Exception ('No pattern was given to plot !')
 

  fig = plt.figure (figsize=(12,6))
  ax = fig.add_subplot (111)

  ax.plot (freq, psd, color='darkgrey')
  ax.plot (freq[(freq>low_cut)&(freq<high_cut)], psd[(freq>low_cut)&(freq<high_cut)], color='black')
  if guess is not None :
    guess_model = rotation_model (freq, psd, guess, n_harvey, n_harmonic, noise=noise)
    ax.plot (freq, guess_model, color='green')
    guess_harvey, param_rot = param_split (guess, n_harmonic)
    guess_harvey = np.reshape (guess_harvey, (n_harvey, guess_harvey.size//n_harvey))
    for elt in guess_harvey :
      ax.plot (freq, harvey (freq, *elt), ':', color='green')
  if param_fitted is not None :
    fitted_model = rotation_model (freq, psd, param_fitted, n_harvey, n_harmonic, noise=noise)
    ax.plot (freq, fitted_model, color='red', alpha=alpha)
    fitted_harvey, param_rot = param_split (param_fitted, n_harmonic)
    fitted_harvey = np.reshape (fitted_harvey, (n_harvey, fitted_harvey.size//n_harvey))
    for elt in fitted_harvey :
      ax.plot (freq, harvey (freq, *elt), '--', color='red', alpha=alpha)

  ax.set_xlabel (r'Frequency ($\mu$Hz)')
  if spectro :
    ax.set_ylabel (r'PSD ((m/s)$^2$/$\mu$Hz)')
  else :
    ax.set_ylabel (r'PSD (ppm$^2$/$\mu$Hz)')

  ax.set_xscale ('log')
  ax.set_yscale ('log')

  ax.set_ylim (0.9*np.amin(psd), 1.1*np.amax(psd))

  if filename is not None:
    plt.savefig (filename, format='pdf')

  if show :
    plt.show ()

  plt.close ()

  return


def perform_mle_rotation (freq, psd, param_back, prot, n_harvey=2, n_harmonic=3, low_cut=1., guess=None, low_bounds=None, up_bounds=None, method=_minimize_powell,
                          filename=None, spectro=False, num=5000, smoothing=50, show=True, show_guess=False) :

  '''
  Perform MLE over rotation model. 

  :param freq: frequency vector in µHz.
  :type freq: ndarray

  :param psd: power density vector in ppm^2/µHz or (m/s)^2/muHz.
  :type psd: ndarray

  :param param_back: input parameters for the background.
  :type param_back: array-like

  :param n_harvey: number of Harvey laws to use to build the background
    model. Optional, default 2. 
  :type n_harvey: int

  :param n_harmonic: number of Harvey laws to use to build the background
    model. Optional, default 3.  
  :type n_harmonic: int

  :param guess: first guess directly passed by the users. If guess is ``None``, the 
    function will automatically infer a first guess. Optional, default ``None``.
    Parameters given in the following order:
    *first harmonic frequency value, height, width, alpha, beta, param_harvey (3 n_harvey)*
  :type guess: array-like.

  :param low_cut: Spectrum below this frequency will be ignored for the fit. The frequency value
    must be given in µHz. Optional, default 1.
  :type low_cut: float

  :param method: minimization method used by the scipy minimize function. Optional, default _minimize_powell
    (modified version allowing to use bounds)

  :param low_bounds: lower bounds to consider in the parameter space exploration. Must have the same structure
    than guess.
  :type low_bounds: ndarray

  :param up_bounds: upper bounds to consider in the parameter space exploration. Must have the same structure
    than guess.
  :type up_bounds: ndarray

  :param show: if set to ``True``, will show at the end a plot summarising the fit. Optional, default ``True``.
  :type show: bool

  :param filename: if given, the summary plot will be saved under this filename. Optional, default ``None``.
    ``show`` argument must have been set to ``True``. 
  :type filename: str

  :param spectro: if set to ``True``, make the plot with unit consistent with radial velocity, else with 
    photometry. Automated guess will also be computed consistently with spectroscopic measurements. 
    Optional, default ``False``.
  :type spectro: bool

  :param num: number of points of the logarithmically sampled spectrum if ``quickfit`` is set to ``True``. Optional, default 50.
  :type num: int

  :param smoothing: size of the boxcar window used for the smoothing if set to ``True``. Optional, default 50.
  :type smoothing: int

  :param show: if set to ``True``, will show at the end a plot summarising the fit. Optional, default ``True``.
  :type show: bool

  :param show_guess: if set to ``True``, will show at the beginning a plot summarising the guess. Optional, default ``False``.
  :type show_guess: bool

  :return: fitted rotation model and corresponding parameters.
  :rtype: tuple of array
  '''

  if guess is None :
    guess = create_rotation_guess (freq, psd, prot, param_back, n_harvey=n_harvey, n_harmonic=n_harmonic)
  if up_bounds is None :
    up_bounds = get_up_bounds (guess, n_harmonic=n_harmonic)
  if low_bounds is None :
    low_bounds = get_low_bounds (guess, low_cut, n_harmonic=n_harmonic)
  if method is _minimize_powell :
    bounds = (low_bounds, up_bounds)
  else :
    bounds = np.c_[low_bounds, up_bounds]

  labels = create_label (n_harvey, n_harmonic)
  numax = param_back[n_harvey*3+3]
  noise = param_back[-1]

  aux_freq, aux_psd = create_vector_to_fit (freq, psd, n_harmonic, low_cut, guess[0], numax, num=num, smoothing=smoothing)

  if show_guess :
    visualise_rotation (freq, psd, low_cut, f1, numax, param_fitted=None, guess=guess, n_harvey=n_harvey,
                        n_harmonic=n_harmonic, filename=None, spectro=spectro, alpha=0.8, show=True, noise=noise)

  print ('Beginning fit')
  param = np.copy (guess)
  result = minimize (log_likelihood_rotation, param,
                     args=(aux_freq, aux_psd, n_harvey, n_harmonic, noise), bounds=bounds,
                     method=method)

  print (result.message)
  param_model = result.x

  fitted_model = rotation_model (freq, psd, param_model, n_harvey, n_harmonic, noise=noise)

  visualise_rotation (freq, psd, low_cut, guess[0], numax, param_fitted=param_model, guess=guess, n_harvey=n_harvey,
                        n_harmonic=n_harmonic, filename=filename, spectro=spectro, alpha=0.8, show=show, noise=noise)

  return fitted_model, param_model


def explore_distribution_rotation (freq, psd, param_back, prot, n_harvey=2, n_harmonic=3, low_cut=1., guess=None, 
                                   low_bounds=None, up_bounds=None, method=_minimize_powell,
                                   filename=None, spectro=False, num=5000, smoothing=50, show=True, show_guess=False,
                                   show_corner=True, nsteps=1000, parallelise=False, progress=False, nwalkers=64, filemcmc=None,
                                   coeff_discard=50, thin=1) :

  '''
  Use a MCMC framework to fit the rotation model. 

  :param freq: frequency vector in µHz.
  :type freq: ndarray

  :param psd: power density vector in ppm^2/µHz or (m/s)^2/muHz.
  :type psd: ndarray

  :param param_back: input parameters for the background.
  :type param_back: array-like

  :param n_harvey: number of Harvey laws to use to build the background
    model. Optional, default 2. 
  :type n_harvey: int

  :param n_harmonic: number of Harvey laws to use to build the background
    model. Optional, default 3.  
  :type n_harmonic: int

  :param guess: first guess directly passed by the users. If guess is ``None``, the 
    function will automatically infer a first guess. Optional, default ``None``.
    Parameters given in the following order:
    *first harmonic frequency value, height, width, alpha, beta, param_harvey (3 n_harvey)*
  :type guess: array-like.

  :param low_cut: Spectrum below this frequency will be ignored for the fit. The frequency value
    must be given in µHz. Optional, default 1.
  :type low_cut: float

  :param low_bounds: lower bounds to consider in the parameter space exploration. Must have the same structure
    than guess.
  :type low_bounds: ndarray

  :param up_bounds: upper bounds to consider in the parameter space exploration. Must have the same structure
    than guess.
  :type up_bounds: ndarray

  :param show: if set to ``True``, will show at the end a plot summarising the fit. Optional, default ``True``.
  :type show: bool

  :param filename: if given, the summary plot will be saved under this filename. Optional, default ``None``.
    ``show`` argument must have been set to ``True``. 
  :type filename: str

  :param spectro: if set to ``True``, make the plot with unit consistent with radial velocity, else with 
    photometry. Automated guess will also be computed consistently with spectroscopic measurements. 
    Optional, default ``False``.
  :type spectro: bool

  :param num: number of points of the logarithmically sampled spectrum if ``quickfit`` is set to ``True``. Optional, default 50.
  :type num: int

  :param smoothing: size of the boxcar window used for the smoothing if set to ``True``. Optional, default 50.
  :type smoothing: int

  :param show: if set to ``True``, will show at the end a plot summarising the fit. Optional, default ``True``.
  :type show: bool

  :param show_guess: if set to ``True``, will show at the beginning a plot summarising the guess. Optional, default ``False``.
  :type show_guess: bool

  :param filemcmc: name of the hdf5 where to store the chain. If filename is ``None``, the name will not
    be stored. Optional, default ``None``.
  :type filename: string

  :param parallelise: If set to ``True``, use Python multiprocessing tool to parallelise process.
    Optional, default ``False``.
  :type parallelise: bool

  :param show: if set to ``True``, will show at the end a plot summarising the fit. Optional, default ``True``.
  :type show: bool

  :param show_corner: if set to ``True``, will show the corner plot summarising the MCMC process. 
    Plot will be saved as a pdf is ``filemcmc`` is also specified. Optional, default ``True``.
  :type show: bool

  :param show_guess: if set to ``True``, will show at the beginning a plot summarising the guess. Optional, default ``False``.
  :type show_guess: bool

  :param coeff_discard: coeff used to compute the number of values to discard: total amount of
    sampled values will be divided by coeff_discard. Optional, default 50.
  :type coeff_discard: int

  :param thin: take only every ``thin`` steps from the chain. Optional, default 1. 
  :type thin: int

  :return: fitted rotation model, corresponding parameters and sigma obtained by MCMC exploration.
  :rtype: tuple of array
  '''

  if guess is None :
    guess = create_rotation_guess (freq, psd, prot, param_back, n_harvey=n_harvey, n_harmonic=n_harmonic)
  if up_bounds is None :
    up_bounds = get_up_bounds (guess, n_harmonic=n_harmonic)
  if low_bounds is None :
    low_bounds = get_low_bounds (guess, low_cut, n_harmonic=n_harmonic)

  labels = create_label (n_harvey, n_harmonic)
  numax = param_back[n_harvey*3+3]
  noise = param_back[-1]

  aux_freq, aux_psd = create_vector_to_fit (freq, psd, n_harmonic, low_cut, guess[0], numax, num=num, smoothing=smoothing)

  if show_guess :
    visualise_rotation (freq, psd, low_cut, f1, numax, param_fitted=None, guess=guess, n_harvey=n_harvey,
                        n_harmonic=n_harmonic, filename=None, spectro=spectro, alpha=0.8, show=True, noise=noise)

  print ('Beginning fit')

  bounds = np.c_[low_bounds, up_bounds]

  norm = np.abs (guess)

  if parallelise :
    pool = ProcessPool ()
  else :
    pool = None

  param_to_pass = np.copy (guess)
  bounds_to_pass = np.copy (bounds)

  #normalisation step
  param_to_pass = param_to_pass / norm
  bounds_to_pass[:,0] = bounds_to_pass[:,0] / norm
  bounds_to_pass[:,1] = bounds_to_pass[:,1] / norm

  pos = param_to_pass + 1e-4 * np.random.randn(nwalkers, param_to_pass.size)
  nwalkers, ndim = pos.shape

  if filemcmc is not None :
    backend = emcee.backends.HDFBackend(filemcmc)
    backend.reset(nwalkers, ndim)
    #saving parameters name and normalisation information
    filemcmc_info = filemcmc[:len(filemcmc)-3] + '.dat'
    np.savetxt (filemcmc_info, np.c_[norm], fmt='%-s')
  else :
    backend = None

  sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability_rotation,
                                  args=(aux_freq, aux_psd, bounds_to_pass, n_harvey, n_harmonic,
                                        norm, noise),
                                  backend=backend, pool=pool)
  sampler.run_mcmc(pos, nsteps, progress=progress)

  discard = nsteps // coeff_discard

  if show_corner :
    make_cornerplot (sampler, ndim, discard, thin, labels, norm, filemcmc=filemcmc)

  flat_samples = sampler.get_chain(discard=discard, thin=thin, flat=True)
  centiles = np.percentile(flat_samples, [16, 50, 84], axis=0) * norm

  param_model = centiles[1,:]
  sigma_model = np.maximum (centiles[1,:] - centiles[0,:], centiles[2,:] - centiles[1,:])

  fitted_model = rotation_model (freq, psd, param_model, n_harvey, n_harmonic, noise=noise)

  visualise_rotation (freq, psd, low_cut, guess[0], numax, param_fitted=param_model, guess=guess, n_harvey=n_harvey,
                        n_harmonic=n_harmonic, filename=filename, spectro=spectro, alpha=0.8, show=show, noise=noise)

  return fitted_model, param_model, sigma_model



