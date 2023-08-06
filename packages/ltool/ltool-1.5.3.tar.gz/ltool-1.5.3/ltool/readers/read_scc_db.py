# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 10:45:43 2016

@author: nick

"""
import numpy as np
import os
import logging
from dateutil.parser import parse 
from datetime import datetime
from netCDF4 import Dataset

logger = logging.getLogger(__name__)

def read_scc_db(fpath, end_fill):

    prod_arr = []
    alt_arr = []
    dt_start_arr = []
    metadata = []
    wave = []
    for i in range(len(fpath)):
        path = fpath[i]

        base = os.path.basename(path)
        
        logger.info(f"       Reading file: {base} ")
        
        fh = Dataset(path, mode='r')
        temp_meta = fh.__dict__
        temp_meta['title'] = 'Geometrical properties of aerosol layers'
        
        # Dates
        start_m = parse(fh.measurement_start_datetime)
        dt_start = datetime(start_m.year, start_m.month, start_m.day, 
                            start_m.hour, start_m.minute, start_m.second)
        
        # Profiles
        alt = np.round(fh.variables['altitude'][:].data/1000., decimals = 5)
        prod = 1e6*fh.variables['backscatter'][0, 0, :].data
        rh = (fh.variables['backscatter_calibration_range'][0,1] + fh.variables['backscatter_calibration_range'][0,0])/2.
        
        # Nans above the reference height and where prod =  9.96920997e+36              
        step = np.round(alt[1] - alt[0], decimals = 5)
        mask = (alt < rh) & (prod >= 0.) & (prod < 1e6)
        
        # Wavelength
        wave.append(str(int(fh.variables['wavelength'][0].data)))
        
        prod = prod[mask]
        alt = alt[mask]                
        
        if (len(alt) > 0) & (len(prod) > 0):
            # Interpolate intermediate nans and also keep nan above half wavelet step above end
            alt_n = np.round(np.arange(alt[0] - end_fill[i], alt[-1] + end_fill[i], step), decimals = 5)
            prod_n = np.interp(alt_n, np.hstack((alt[0] - end_fill[i], alt, alt[-1] + end_fill[i])),
                               np.hstack((prod[0], prod, prod[-1])))
            
            
            # Append to lists
            if (len(prod[prod == prod]) > 10) & (len(alt[prod > 0.]) > 10):
                dt_start_arr.append(dt_start)
                alt_arr.append(alt_n)
                prod_arr.append(prod_n)
                temp_meta['input_file'] = base
                metadata.append(temp_meta)

    return(dt_start_arr, alt_arr, prod_arr, metadata, wave)