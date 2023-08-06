import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

def smooth (psd, smoothing=50) :

  if smoothing!=1 :
    psd = pd.Series(data=psd).rolling (window=smoothing, min_periods=1, win_type='triang', 
                             center=True).mean().to_numpy()

  return psd

def create_log_freq (freq, num=1000) :

  '''
  Take an array with frequency linearly spaced and returns an array
  with frequency logarithmically spaced
  '''

  log_freq = np.logspace (np.log10 (freq[1]), np.log10 (freq[-1]), num=num, endpoint=False) 
  # I use the 2nd bin and not the first to avoid a check_bound error in the interpolation

  return log_freq

def degrade_psd (freq, psd, num=1000, smoothing=50) :
  '''
  Take a psd linearly sampled, smooth it, interpolate it
  and return a psd logarithmically sampled.

  :param freq: frequency array.
  :type freq: ndarray

  :param psd: power array
  :type psd: ndarray

  :param num: number of point in the output arrays.
  :type num: int

  :param smoothing: coeff used to smooth the input psd.
  :type smoothing: int

  :return: freq and psd logarithmically sampled.
  :rtype: tuple of ndarray
  '''

  psd = smooth (psd)
  f = interp1d (freq, psd)
  log_freq = create_log_freq (freq, num=num)
  log_psd = f (log_freq)

  return log_freq, log_psd
