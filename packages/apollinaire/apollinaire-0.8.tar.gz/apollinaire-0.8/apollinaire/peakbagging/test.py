from apollinaire.peakbagging import *
import pandas as pd

def test_a2z (a2z_file) :

  df_a2z = read_a2z (a2z_file)
  check_a2z (df_a2z, verbose=True) 
  pkb = a2z_to_pkb (df_a2z)
  df_pkb = pd.DataFrame (data=pkb)
  
  print (df_a2z)
  print (df_pkb.to_string ())
  print (get_list_order (df_a2z))

if __name__ == '__main__' :

  test_a2z ('test.a2z')
