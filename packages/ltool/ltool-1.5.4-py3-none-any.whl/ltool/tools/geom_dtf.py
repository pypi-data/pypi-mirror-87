#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 28 12:54:41 2017

@author: nick
"""
import pandas as pd
import numpy as np
from .wavelet import wavelet
from scipy.signal import argrelmax, argrelmin
import xarray as xr
import warnings

warnings.filterwarnings("ignore")

def feature_id(alt, sig, alpha, peak_margin, log):
    
    bases = []
    tops = []
    rl_flag = []
    
    wct_lims = [0.25, -0.25]
    
    rl = np.nan
    
    step = np.round(alt[1] - alt[0], decimals = 5)

    # Wavelet covariance transform
    wct = wavelet(sig, step, alpha)
    
    # Normalize by the dilation
    wct = wct/alpha
    
    # Index of potential features
    t_index = argrelmin(wct)[0]
    b_index = argrelmax(wct)[0]
    
    # Setting dataframes of potential features
    tops_dtf = pd.DataFrame(data = np.vstack((t_index, 
                                              sig[t_index], 
                                              wct[t_index], 
                                              [1]*t_index.shape[0])).T, 
                            columns = ['index', 'sig', 'wct', 'flag'], 
                            index = alt[t_index], dtype = object)
    bases_dtf = pd.DataFrame(data = np.vstack((b_index, 
                                               sig[b_index], 
                                               wct[b_index], 
                                               [0]*b_index.shape[0])).T, 
                             columns = ['index', 'sig', 'wct', 'flag'], 
                             index = alt[b_index], dtype = object)   
        
    # Filter out features with normalized wct values below the thershold
    # Sort by ascending order  
    mask_tops = (tops_dtf.wct.values < wct_lims[-1])
    
    mask_bases = (bases_dtf.wct.values > wct_lims[0])
    
    tops_dtf = tops_dtf.iloc[mask_tops, :].sort_index(axis = 0, 
                                                      ascending=True, 
                                                      inplace=False)  
    
    bases_dtf = bases_dtf.iloc[mask_bases, :].sort_index(axis = 0, 
                                                         ascending=True, 
                                                         inplace=False)  
    
    if bases_dtf.shape[0] > 0 and tops_dtf.shape[0] > 0:
        # Combine bases and tops in merged and sort by altitude    
        merged = tops_dtf.append(bases_dtf).sort_index(axis = 0, 
                                                       ascending=True, 
                                                       inplace=False)    
       
        # Ensure last layer is always a top
        tflag = tops_dtf.index
        if len(tflag) > 0:
            merged = merged.loc[(merged.index <= tflag[-1]), :]     
            
        # Search for a top-base pattern that signifies the change of layer and 
        # keep only those features in merged 
        if len(merged) > 0 and (merged.flag.values == 0).any() \
        and (merged.flag.values == 1).any:
            layer_ind = [] 
            stack = 0
            for i in range(0, merged.shape[0] - 1):
                pattern = [merged.flag.iloc[i], merged.flag.iloc[i+1]]
                if pattern[0] == 1 and pattern[1] == 0:
                    max_wct = np.nanmax(merged.wct.values[stack:i+1])
                    min_wct = np.nanmin(merged.wct.values[stack:i+1])
                    max_mask = ((merged.wct.values[stack:i+1] >= peak_margin*max_wct) & 
                                (merged.wct.values[stack:i+1] > wct_lims[0]))
                    min_mask = ((merged.wct.values[stack:i+1] <= peak_margin*min_wct) & 
                                (merged.wct.values[stack:i+1] < wct_lims[-1]))
                    if max_mask.any():
                        layer_ind.append(min(merged.index.values[stack:i+1][max_mask]))
                    if min_mask.any():
                        layer_ind.append(max(merged.index.values[stack:i+1][min_mask]))
                    stack = i + 1
            max_wct = np.nanmax(merged.wct.values[stack:])
            min_wct = np.nanmin(merged.wct.values[stack:])
            max_mask = ((merged.wct.values[stack:] >= peak_margin*max_wct) & 
                        (merged.wct.values[stack:] > wct_lims[0]))
            min_mask = ((merged.wct.values[stack:] <= peak_margin*min_wct) & 
                        (merged.wct.values[stack:] < wct_lims[-1]))            
            if max_mask.any():
                layer_ind.append(min(merged.index.values[stack:][max_mask]))
            if min_mask.any():
                layer_ind.append(max(merged.index.values[stack:][min_mask]))

            merged = merged.loc[layer_ind, :].sort_index(axis = 0, 
                                                         ascending=True, 
                                                         inplace=False) 

        #Check if rl exists, it is the first element of merged if it is a top
        if len(merged) > 0 and (merged.flag.values == 0).any() \
        and (merged.flag.values == 1).any:
            if merged.flag.values[0] == 1:
                rl = merged.index.values[0]
                merged = merged.iloc[1:, :]
        
            # Split again to bases and tops arrays 
            tops = np.round(np.sort(merged[merged.flag == 1].index.values), 
                            decimals = 5)
            bases = np.round(np.sort(merged[merged.flag == 0].index.values), 
                             decimals = 5)
            
            # If rl exists merge it to bases and tops (base is start of the profile)
            # rl_flag is 0 for layers and 1 for rl
            rl_flag = np.zeros(bases.shape, dtype = int) 
            if rl == rl:
                bases = np.hstack((alt[alt >= alt[0] + alpha/2.][0], bases))
                tops = np.hstack(([rl], tops))
                rl_flag = np.hstack(([1], rl_flag))
        
    return(rl_flag, bases, tops, wct)
    
def geom_prop(rl_flag, bases, tops, alt, sig, log):

    geom = []
    # Calculate layer thickness, center of mass, peak, and weight of the layer (ratio to the total integrated product)
    if len(bases) > 0:
        tck = np.round(tops - bases, decimals = 5)
        com = np.nan*np.zeros(bases.shape)
        dpth = np.nan*np.zeros(bases.shape)
        peak = np.nan*np.zeros(bases.shape) 
        bsig = np.nan*np.zeros(bases.shape) 
        tsig = np.nan*np.zeros(bases.shape) 
        psig = np.nan*np.zeros(bases.shape) 
        msig = np.nan*np.zeros(bases.shape) 
        shrp = np.nan*np.zeros(bases.shape) 
        trnd = np.nan*np.zeros(bases.shape) 
        wgh = np.nan*np.zeros(bases.shape)
        
        for i in range(bases.shape[0]):
            
            sig_l = sig[(alt >= bases[i]) & (alt <= tops[i])]
            alt_l = alt[(alt >= bases[i]) & (alt <= tops[i])]

            bases[i] = np.round(bases[i], decimals = 5) 
            tops[i] = np.round(tops[i], decimals = 5) 

            com[i] = np.round(np.trapz(sig_l*alt_l, x = alt_l)/
                              np.trapz(sig_l, x = alt_l), decimals = 5)
            
            dpth[i] = np.round(np.trapz(sig_l, x = alt_l)/
                               (tck[i]), decimals = 3)         
            
            wgh[i] = np.round(np.trapz(sig_l, x = alt_l)/
                              (np.trapz(sig, x = alt)), decimals = 5)         
            
            mask_max = (sig_l == np.nanmax(sig_l))

            peak[i] = np.round(alt_l[mask_max][-1], decimals = 5)
            psig[i] = np.round(sig_l[mask_max][-1], decimals = 3)
            bsig[i] = np.round(sig_l[0], decimals = 3)
            tsig[i] = np.round(sig_l[-1], decimals = 3)
            msig[i] = np.round(np.min([bsig[i], tsig[i]]), decimals = 3)
            shrp[i] = np.round((psig[i] - np.max([bsig[i], tsig[i]])), 
                               decimals = 3)
            trnd[i] = np.round((tsig[i] - bsig[i]), decimals = 3)

        # Export to xarray Data Array, ensure there are layers left after removing the insignificant ones
        if len(bases) > 0:
            features = ['residual_layer_flag', 'base', 'center_of_mass', 'top', 
                        'peak', 'thickness', 'base_sig', 'top_sig', 'peak_sig', 
                        'depth', 'sharpness', 'trend', 'weight']
            layers = np.arange(1, bases.shape[0]+1, 1)
            layer_data = np.vstack((rl_flag.astype(object), 
                                    bases.astype(object), 
                                    com.astype(object), 
                                    tops.astype(object), 
                                    peak.astype(object), 
                                    tck.astype(object), 
                                    bsig.astype(object), 
                                    tsig.astype(object), 
                                    psig.astype(object), 
                                    dpth.astype(object),
                                    shrp.astype(object),
                                    trnd.astype(object),
                                    wgh.astype(object))).T
            layer_data = layer_data
            geom = xr.DataArray(data = layer_data, 
                                coords = [layers, features], 
                                dims = ['layers','features'],
                                name = 'geometrical_properties')
        
    return(geom)

def mask_layers(geom, log):
    
    dpth = 1.
    tck = 0.1
    
    if len(geom) > 0:
# Remove insignificant layers 
        mask = ((geom.loc[:, 'depth'].values > dpth) &\
                (geom.loc[:, 'thickness'].values > tck))
                
        
        geom = geom[mask]
        
    return(geom)