import numpy as np
from astropy.io import fits
from astropy.table import Table
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

'''
Module to compute power spectra density (PSD) from
  timeseries (series_to_psd) or Fourier transform 
  (tf_to_psd).

PSD can then be saved as fits file with the psd_to_fits
  function.

PSD saved into fits file can be directly plotted with the 
  plot_fits function.

The echelle_diagram function allow to compute and optionnally
  plot the echelle diagram of the PSD.
'''

def tf (series, dt) :

  """
  Take a timeseries and compute its properly normalised
  Fourier transform.

  :param series: input timeseries
  :type series: ndarray

  :param dt: sampling of the timeseries
  :type dt: float

  :return: frequency and psd array
  :rtype: tuple of ndarray
  """
  freq = np.fft.rfftfreq (series.size, d=dt)
  tf = np.fft.rfft (series) / (series.size / 2.)

  return freq, tf

def series_to_psd (series, dt, correct_dc=False) :

  """
  Take a timeseries and compute its PSD

  :param series: input timeseries
  :type series: ndarray

  :param dt: sampling of the timeseries
  :type dt: float

  :param correct_dc: if set to True, will compute the duty_cycle
    to adjust the psd values. Optional, default False.
  :type correct_dc: bool

  :return: frequency and psd array
  :rtype: tuple of ndarray
  """
  freq = np.fft.rfftfreq (series.size, d=dt)
  tf = np.fft.rfft (series) / (series.size / 2.)
  T = series.size * dt
  PSD = np.abs (tf) * np.abs (tf) * T / 2.

  if correct_dc :
    dc = np.count_nonzero (series) / series.size
    PSD = PSD / dc

  return freq, PSD

def tf_to_psd (tf, T) :

  '''
  :param tf: complex Fourier transform from which to
    compute the PSD.
  :type tf: ndarray 

  :param T: resolution of the Fourier transform.
  :type T: float

  :return: corresponding PSD
  :rtype: ndarray
  '''

  PSD = np.abs (tf) * np.abs (tf) * T / 2.
  return PSD 


def psd_to_fits (freq, psd, filename) :
  '''
  Save frequency and power vector into a fits file.

  :param freq: frequency vector.
  :type freq: ndarray
  :param psd: psd vector.
  :type psd: ndarray
  :param filename: name of the fits file to create.
  :type filename: str
  '''

  data = np.c_[freq,psd]
  hdu = fits.PrimaryHDU (data)
  hdu.writeto (filename)

  return

def plot_psd_fits (filename, rv=True, index=0) :
  '''
  Plot the PSD of a fits file containing frequency and power 
  array. The frequency in the file are supposed to be in Hz and
  the power in (m/s)^2/Hz (spectroscopy) or ppm^2/Hz (photometry)

  :param filename: name of the fits file
  :type filename: str

  :param rv: set to True if it is a radial velocity PSD, to False
    if it is a photometric PSD.
  :type rv: bool

  :param index: index of the hdulist of the fits file where the PSD can
    be found. Default is 0.
  :type index: int
  '''

  hdu = fits.open (filename) [index]
  data = np.array (hdu.data)
  fig = plt.figure (figsize=(12,6))
  ax = fig.add_subplot (111)
  ax.plot (data[:,0]*1.e6, data[:,1]*1.e-6)
  ax.set_xlabel (r'Frequency ($\mu$Hz)')
  if rv==True :
     ax.set_ylabel (r'PSD ((m/s)$^2$/$\mu$Hz)')
  else :
     ax.set_ylabel (r'PSD (ppm$^2$/$\mu$Hz)')

  return

def echelle_diagram (freq, PSD, dnu, twice=False,
                   smooth=10, cmap='cividis', mode_freq=None, mode_freq_err=None,
                   vmin=None, vmax=None) :

  '''
  Build the echelle diagram of a given PSD.  

  :param freq: input vector of frequencies.
  :type freq: ndarray

  :param PSD: input vector of power. Must be of same size than freq.
  :type PSD: ndarray

  :param dnu: the large frequency separation use to cut slices 
    into the diagram. 
  :type dnu: float

  :param twice: slice using 2 x *dnu* instead of *dnu*, default False.
  :type twice: bool

  :param smooth: size of the rolling window used to smooth the PSD. Default 10.
  :type smooth: int

  :param cmap: select one available color map provided by matplotlib, default ``inferno``
  :type cmap: str

  :param mode_freq: frequency array of the modes to represent on the diagram.
  :type mode_freq: ndarray.

  :param mode_freq_err: frequency uncertainty of the modes to represent on the diagram.
  :type mode_freq_err: ndarray.

  :return: the matplotlib Figure to plot.
  :rtype: matplotlib Figure
  '''


  if smooth != 1 :
    PSD = pd.Series(data=PSD).rolling (window=smooth, min_periods=1, 
                             center=True).mean().to_numpy()

  if twice==True :
    dnu = 2.*dnu

  res = freq[2]-freq[1]

  n_slice = int (np.floor_divide (freq[-1]-freq[0], dnu))
  len_slice = int (np.floor_divide (dnu, res))

  if (n_slice*len_slice > PSD.size) :
    len_slice -= 1

  ed = PSD[:len_slice*n_slice]
  ed = np.reshape (ed, (n_slice, len_slice))

  freq_ed = freq[:len_slice*n_slice]
  freq_ed = np.reshape (freq_ed, (n_slice, len_slice))
  x_freq = freq_ed[0,:] - freq_ed[0,0]
  y_freq = freq_ed[:,0]

  fig = plt.figure (figsize=(16, 16))
  ax = fig.add_subplot (111)
  ax.pcolormesh (x_freq, y_freq, ed, cmap=cmap, vmin=vmin, vmax=vmax, shading='auto')

  if mode_freq is not None :
    x_mode = np.zeros (mode_freq.size)
    y_mode = np.zeros (mode_freq.size)
    for ii, elt in enumerate (mode_freq) :
        aux_1 = elt - y_freq
        aux_2 = y_freq[aux_1>0]
        aux_1 = aux_1[aux_1>0]
        jj = np.argmin (aux_1)
        x_mode[ii] = aux_1[jj]
        y_mode[ii] = aux_2[jj] 
    ax.errorbar (x=x_mode, y=y_mode, xerr=mode_freq_err, fmt='+', color='white', barsabove=True,
                 capsize=2., markersize=8.)

  ax.set_xlabel (r'Frequency mod. ' + str('%.1f' % dnu) + r' $\mu$Hz')
  ax.set_ylabel (r'Frequency ($\mu$Hz)')

  return fig

def echelle_diagram_old (freq, PSD, dnu, twice=False,
                   smooth=10, cmap='cividis', mode_freq=None, mode_freq_err=None,
                   vmin=None, vmax=None) :

  '''
  Build the echelle diagram of a given PSD.  

  :param freq: input vector of frequencies.
  :type freq: ndarray

  :param PSD: input vector of power. Must be of same size than freq.
  :type PSD: ndarray

  :param dnu: the large frequency separation use to cut slices 
    into the diagram. 
  :type dnu: float

  :param twice: slice using 2 x *dnu* instead of *dnu*, default False.
  :type twice: bool

  :param smooth: size of the rolling window used to smooth the PSD. Default 10.
  :type smooth: int

  :param cmap: select one available color map provided by matplotlib, default ``inferno``
  :type cmap: str

  :param mode_freq: frequency array of the modes to represent on the diagram.
  :type mode_freq: ndarray.

  :param mode_freq_err: frequency uncertainty of the modes to represent on the diagram.
  :type mode_freq_err: ndarray.

  :return: the matplotlib Figure to plot.
  :rtype: matplotlib Figure
  '''


  if smooth != 1 :
    PSD = pd.Series(data=PSD).rolling (window=smooth, min_periods=1, win_type='triang', 
                             center=True).mean().to_numpy()

  if twice==True :
    dnu = 2.*dnu

  res = freq[2]-freq[1]

  n_slice = int (freq.size*res / dnu)
  len_slice = int ((freq[-1]-freq[0]) / (n_slice*res))

  if (n_slice*len_slice > PSD.size) :
    len_slice -= 1

  ed = PSD[:len_slice*n_slice]
  ed = np.reshape (ed, (n_slice, len_slice))

  freq_ed = freq[:len_slice*n_slice]
  freq_ed = np.reshape (freq_ed, (n_slice, len_slice))
  x_freq = freq_ed[0,:] - freq_ed[0,0]
  y_freq = freq_ed[:,0]

  if mode_freq is not None :
    x_mode = ((mode_freq / res).astype (np.int_) % len_slice) * res 

  fig = plt.figure (figsize=(16, 16))
  ax = fig.add_subplot (111)
  ax.pcolormesh (x_freq, y_freq, ed, cmap=cmap, vmin=vmin, vmax=vmax)
  if mode_freq is not None :
    ax.errorbar (x=x_mode, y=mode_freq, xerr=mode_freq_err, fmt='+', color='white', barsabove=True,
                 capsize=2., markersize=8.)
  ax.set_xlabel (r'Frequency mod. ' + str('%.1f' % dnu) + r' $\mu$Hz')
  ax.set_ylabel (r'Frequency ($\mu$Hz)')

  return fig
