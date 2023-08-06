import numpy as np
import pandas as pd
import numba

def split_a2z (df_a2z) :

  inf_a2z = df_a2z[list(range (4))].to_numpy ()
  inf_a2z = inf_a2z.astype (np.str_)
  param_a2z = df_a2z[list(range (4,9))].to_numpy ()
  param_a2z = param_a2z.astype (np.float64)
  n = inf_a2z[inf_a2z[:, 2]=='freq', 0].astype (np.float64)
  l = inf_a2z[inf_a2z[:, 2]=='freq', 1].astype (np.float64)

  return n, l, inf_a2z, param_a2z

def match (n, l, aux, aux_param, inf_amp=None, param_amp=None, name=None) :

 incr = 0
 if l > 1 :
   incr+= 1
 if l > 3 :
   incr+= 1
 
 value = 0
 value_err = 0

 if np.any ((aux[:, 0]==str(n)) & (aux[:, 1]==str(l))) : 
   cond = (aux[:, 0]==str(n)) & (aux[:, 1]==str(l))
   value = aux_param[cond, 0][0]
   value_err = aux_param[cond, 1][0]

 elif (l==4) | (l==5) :

   if name=='split' :
     value = 0.4       #splitting are fixed to 400 nHz for those modes if not given specifically
     value_err = 0. 
     return value, value_err

   elif np.any ( (aux[:,0]==str(n+incr)) & (aux[:,1]=='0') & (aux_param[:,2]==0) ) :
     l_ref = '0'
     ref_ratio = 1.
   else :
     l_ref = '1'
     ref_ratio = 1.8
   value = aux_param[(aux[:,0]==str(n+incr)) & (aux[:,1]==l_ref) & (aux_param[:,2]==0), 0][0] 
   value_err = aux_param[(aux[:,0]==str(n+incr)) & (aux[:,1]==l_ref) & (aux_param[:,2]==0), 1][0] 
   if inf_amp is not None :
     value = value / ref_ratio
     value_err = value_err / ref_ratio
     if l==4 :
       value = value * 0.0098
       value_err = value_err * 0.0098
     if l==5 :
       value = value * 0.001
       value_err = value_err * 0.001
     
 elif (np.any ( (aux[:, 0]==str(n+incr)) & (aux[:, 1]=='a') ) ) :
   cond2 = (aux[:, 0]==str(n+incr)) & (aux[:, 1]=='a')
   value = aux_param[cond2, 0][0]
   value_err = aux_param[cond2, 1][0]
   if inf_amp is not None :
     value = value * param_amp[inf_amp[:, 1]==str(l), 0][0]

 elif np.any (aux[:,0]=='a') :
   value = aux_param[aux[:,0]=='a', 0][0]   
   value_err = aux_param[aux[:,0]=='a', 1][0]   
   if inf_amp is not None :
     value = value * param_amp[inf_amp[:, 1]==str(l), 0][0]

 return value, value_err

def fill_param (pkb, name, inf_a2z, param_a2z) :
  
  if name=='height' :
    ind = 4
  if name=='width' :
    ind = 6
  if name=='angle' :
    ind = 8
  if name=='split' :
    ind = 10
  if name=='asym' :
    ind = 12

  aux = inf_a2z[inf_a2z[:, 2]==name, :]
  aux_param = param_a2z[inf_a2z[:, 2]==name, :]

  if name =='height' :
    inf_amp = inf_a2z[inf_a2z[:, 2]=='amp_l', :]
    param_amp = param_a2z[inf_a2z[:, 2]=='amp_l', :]
  else :
    inf_amp = None
    param_amp = None

  for ii in range (pkb.shape[0]) :
      v, verr = match (int(pkb[ii, 0]), int (pkb[ii, 1]), aux, aux_param, 
                       inf_amp=inf_amp, param_amp=param_amp, name=name)
      pkb[ii, ind] = v
      pkb[ii, ind+1] = verr

  return

def a2z_to_pkb_nopandas (n, l, inf_a2z, param_a2z) :

  freq = param_a2z[inf_a2z[:, 2]=='freq', 0]
  freq_err = param_a2z[inf_a2z[:, 2]=='freq', 1]
  pkb = np.zeros ((n.size, 14)) 
  pkb[:, 0] = n
  pkb[:, 1] = l
  pkb[:, 2] = freq
  pkb[:, 3] = freq_err

  fill_param (pkb, 'height', inf_a2z, param_a2z) 
  fill_param (pkb, 'width', inf_a2z, param_a2z) 
  if np.any (inf_a2z[:, 2]=='split') :
    fill_param (pkb, 'split', inf_a2z, param_a2z) 
    #pkb[(pkb[:,1]==4)|(pkb[:,1]==5), 10] = 0.4 #fixing splitting for high degrees modes 
    #pkb[(pkb[:,1]==4)|(pkb[:,1]==5), 11] = 0. #fixing splitting for high degrees modes 
    pkb[pkb[:,1]==0, 10] = 0. #fixing splitting for l=0 modes 
    pkb[pkb[:,1]==0, 11] = 0. 
  if np.any (inf_a2z[:, 2]=='asym') :
    fill_param (pkb, 'asym', inf_a2z, param_a2z) 

  if np.any (inf_a2z[:, 2]=='angle') :
    pkb[:, 8] = param_a2z[inf_a2z[:, 2]=='angle', 0][0]
    pkb[:, 9] = param_a2z[inf_a2z[:, 2]=='angle', 1][0]
  else :
    pkb[:, 8] = 90

  return pkb

def wrapper_a2z_to_pkb_nopandas (df_a2z) :

  n, l, inf_a2z, param_a2z = split_a2z (df_a2z)
  pkb = a2z_to_pkb_nopandas (n, l, inf_a2z, param_a2z)

  return pkb

