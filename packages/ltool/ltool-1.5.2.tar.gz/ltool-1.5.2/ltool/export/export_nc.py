#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 21:31:10 2020

@author: nick
"""
import os
import configparser
from dateutil import parser as parse_date

def export_nc(geom, metadata, alpha, wave, thres, fname, dir_out):
    
    if not os.path.exists(dir_out):
        os.makedirs(dir_out)
    
    geom_dts = geom.to_dataset('features')
    geom_dts.attrs = metadata
    geom_dts.attrs['processor_name'] = 'ltools'
    
    geom_dts['layer_method'] = 'WCT'
    geom_dts.layer_method['long_name'] = 'The wavelet covariance transform (WCT) is used for the layer detection.'
    
    geom_dts['detection_limit'] = thres
    geom_dts.detection_limit.attrs['units'] = 'Mm^{-1} sr^{-1}'
    geom_dts.detection_limit.attrs['long_name'] = 'Wavelength specific value. It is used to descern between noise and actual layers'
    
    
    geom_dts['dilation'] = alpha
    geom_dts.dilation.attrs['units'] = 'Km'
    geom_dts.dilation.attrs['long_name'] = 'The dillation value (window) used for the wavelet covariance transform calculations'
    
    geom_dts['wavelength'] = float(wave)
    geom_dts.wavelength.attrs['units'] = 'nm'
    geom_dts.wavelength.attrs['long_name'] = 'The wavelength of the ELDA product used to obtain the geometrical properties'

    geom_dts.residual_layer_flag.attrs['long_name'] = 'Flags the first layer when its base is not identified and is substituted with the first range bin instead'
    geom_dts.residual_layer_flag.attrs['values'] = '0 for normal layers, 1 for the residual layer'
    
    geom_dts.base.attrs['units'] = 'Km'
    geom_dts.base.attrs['long_name'] = 'The layer base (ASL)'
    
    geom_dts.center_of_mass.attrs['units'] = 'Km'
    geom_dts.center_of_mass.attrs['long_name'] = 'The layer center of mass, average altitude weighted by the product values (ASL)'
    
    geom_dts.top.attrs['units'] = 'Km'
    geom_dts.top.attrs['long_name'] = 'The layer top (ASL)'
    
    geom_dts.peak.attrs['units'] = 'Km'
    geom_dts.peak.attrs['long_name'] = 'The height of the product maximum within the layer (ASL)'
    
    geom_dts.thickness.attrs['units'] = 'Km'
    geom_dts.thickness.attrs['long_name'] = 'The layer thickness (top - base)'
    
    geom_dts.base_sig.attrs['long_name'] = 'The product value at the base of the layer scaled by the detection limit'
    
    geom_dts.top_sig.attrs['long_name'] = 'The product value at the top of the layer scaled by the detection limit'
    
    geom_dts.peak_sig.attrs['long_name'] = 'The product value at the peak of the layer scaled by the detection limit'
    
    geom_dts.weight.attrs['long_name'] = 'Integrated product within the layer scaled by the detection limit times the thikness of the layer'

    geom_dts.sharpness.attrs['long_name'] = 'Minimum difference between the product value at the peak and the product value at the base or top, scaled by the detection limit'        
    
    geom_dts.trend.attrs['long_name'] = 'Difference between the product value at the top and the product value at the base, scaled by the detection limit'        
    
    geom_dts.to_netcdf(os.path.join(dir_out,fname))
        
    return(geom_dts)

def nc_name(metadata, prod_id, wave, ver):
    
    parser = configparser.ConfigParser()
    parser.read('./default.ini')
    
    app = parser._sections['info']['name']
    ver = parser._sections['info']['version']

    ms_id = metadata['measurement_ID']
    
    st_id = metadata['station_ID']
    
    prod_id = prod_id.zfill(7)
    
    wave = wave.zfill(4)
    
    start_t = parse_date.parse(metadata['measurement_start_datetime'])\
        .strftime('%Y%m%d%H%M')
    stop_t = parse_date.parse(metadata['measurement_stop_datetime'])\
        .strftime('%Y%m%d%H%M')
        
    fname = f'{st_id}_{wave}_{prod_id}_{start_t}_{stop_t}_{ms_id}_{app}_v{ver}.nc'

    return(fname)