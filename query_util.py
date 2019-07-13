###################################
# Modeule containing functions
# to retrieve Gaia DR2 from the TAP
# services
###################################

from astroquery.gaia import Gaia
from typing import Dict
import warnings
from numpy import ndarray
import os
import numpy as np
import pandas as pd
from astropy.time import Time
from astroquery.utils.tap.core import TapPlus

warnings.filterwarnings("ignore", module='astropy.io.votable.tree')

def get_ast_data(dr2_source_id: int) -> Dict:
    """Gets astrometric data for a Gaia DR2 sourc

    :param dr2_source_id: Gaia DR2 source id
    :return : Dictionary of the results, with the keys 
        being the GDR2 column names.
    """

    query = ("SELECT *"
             "FROM gaiadr2.gaia_source "
             "WHERE gaiadr2.gaia_source.source_id=" + str(dr2_source_id)
            )
    job = Gaia.launch_job_async(query)
    return job.get_results()

def get_gost_times(dr2_source_id: int,time='utc',
                   data_dir='GOST_data/') -> ndarray:
    """Returns an array of times that Gaia saw a particular source.
     
    :param dr2_source_id: Gaia DR2 source id.
    :param time: obersevation time format.
    :param data_dir: directory where the gost data is.
    :return Array of times in the unit of Julian years 
    """
    
    file_path = data_dir+str(dr2_source_id) + '_GOST.csv'    

    if os.path.isfile(file_path):
        
         GOST_data = pd.read_csv(file_path)
         times = GOST_data[' ObservationTimeAtGaia[UTC]'].values  
                

         t = Time(times.tolist(),format='isot', scale='utc')

         return np.array(t.jyear,dtype=float)
    
    else:
        raise Exception("GOST data for DR2 source: " + str(dr2_source_id) + " not found.")

def get_lens_mass(dr2_lens_id: int) -> float:
    """Gets the esimated lens mass. 

    This was calculated by methods
    described in Kluter et al (2018b) 
    https://arxiv.org/abs/1807.11077

    :param dr2_lens_id: Gaia DR2 lens source id
    :return: lens mass [Msol]
    """
    
    Kluter = TapPlus(url="http://dc.zah.uni-heidelberg.de/__system__/tap/run/tap")
    
    # only select the top 1 because they may be more than one event
    # caused by the same lens.
    query = ("SELECT top 1 mass "
             "FROM plc2.data "
             "WHERE plc2.data.lens_id=" + str(dr2_lens_id)
            )
    job = Kluter.launch_job(query)
    results = job.get_results()
     
    #check if the query return anything 
    if len(results['mass']) == 0:
        raise Exception("Did not find a lens mass in Kluter's database for : " + str(dr2_lens_id))    
    else:
        return results['mass'][0]


