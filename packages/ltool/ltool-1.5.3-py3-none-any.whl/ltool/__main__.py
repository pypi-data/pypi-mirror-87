#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 11:15:48 2016

@author: lidar2
"""
import os
import sys
import warnings
import logging
import getpass
import datetime
from .tools.geom_dtf import feature_id, geom_prop, mask_layers
from .readers.read_scc_db import read_scc_db
from .readers.get_files import database
from .readers.parse_config import parse_config
from .export.export_nc import export_nc, nc_name
from .export.update_scc_db import update
from .readers.read_config import config
from .debug import log_pack
from .version import __version__

logger = logging.getLogger()

def setup_directories(cfg):
    """ Check if the output folder exists. If not, create it."""
    output_dir = cfg.scc['output-dir']

    log_dir = cfg.scc['log-dir']
    if log_dir:
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)
            logger.info("Logging directory does not exist. Creating it. %s" % log_dir)

    if not os.path.isdir(output_dir):
        logger.info("Output directory does not exist. Creating it. %s" % output_dir)
        os.makedirs(output_dir)

    return()

def main(args=None):
###############################################################################
# O) Definitions
###############################################################################
    log_pack.scc_logger(logger)
    logger.setLevel('DEBUG')
    start_time = datetime.datetime.now()
    logger.info(f"------ ltool version {__version__} ------")
    logger.info("----------------------------------------------------------------")
    logger.info("------ Processing started on %s ------" % start_time)
    
#Ignores all warnings --> they are not printed in terminal
    warnings.filterwarnings('ignore')

    logger.info("Parsing ltool options ")    
    try:
        meas_id, cfg_path = parse_config()
    except Exception as e:
        logger.error("Error while parsing ltool options ")
        sys.exit(1)
    logger.info("Options succesfully parsed ")    
   
#Reading of the configuration file    
    logger.info("Parsing the configuration file ")    
    try:
        cfg = config(cfg_path)
    except Exception as e:
        logger.error("Error while reading the configuration file ")
        sys.exit(2)
    logger.info("Configuration file succesfully parsed ")    
    
# Make directories if they do not exist
    try:
        setup_directories(cfg)
    except Exception as e:
        logger.error("Error while setting up required directories ")
        sys.exit(3)
    
# Add filepath configuration for logging purposes
    log_pack.add_filepath(cfg, meas_id, logger)
    
# Change logging level according to config file
    logger.setLevel(cfg.scc['log-level'].upper())

# Threshold to select the sharpest peaks (63% less sharp than the sharpest)
    margin = 0.63
    
# Get array of input files from an scc database query
    logger.info("----------------------------------------------------------------")
    logger.info("------ Processing started on %s ------" % start_time)
    logger.info("Quering the measurement paths in the SCC database ")
    try:
        files, rpath, alphas, det_lims, ids = database(meas_id, cfg = cfg)
    except Exception as e:
        logger.error("Error while executing a measurement ID query in the SCC database ")
        sys.exit(4)                
    logger.info("Measurement paths succesfully collected ")    
    
###############################################################################
# A) Preprocessing
###############################################################################
# A.1) Reading lidar profiles
# Optical Profiles
    logger.info("Section A: Reading the SCC files ")
    try:
        dt_start_arr, alt_arr, prod_arr, metadata, wave = \
            read_scc_db(files, end_fill = alphas)
    except Exception as e:
        logger.error("Error while reading the SCC files ")
        sys.exit(5)   
    logger.info("       All SCC files succesfully read ")
    
###############################################################################
# B) Geometrical retrievals
############################################################################### 
    list_geom = []
    list_geom_dts = []
    list_dates = []

    for i in range(0, len(files)):
        logger.info(f"****** Proccessing file: {os.path.basename(files[i])} ******")
        logger.info("Section B: Proceeding to the layering algorithm ")

        norm = prod_arr[i]/det_lims[i]
        
# B.1) Identify layers and each base and top
        try:
            rl_flag, bases, tops, wct = feature_id(alt_arr[i], norm,
                                                   alpha = alphas[i], 
                                                   peak_margin = margin,
                                                   log = logger)
        except Exception as e:
            logger.error("Error while identifying layer boundaries ")
            sys.exit(6)  
        logger.info("       Potential layer boundaries succesfully identified ")

# B.2) Use base and top to the profile to extract aditional 
# geometrical properties
        try:
            geom = geom_prop(rl_flag, bases, tops, alt_arr[i], norm, log = logger)
        except Exception as e:
            logger.error("Error while calculating layer properties ")
            sys.exit(7)  
        logger.info("       Layer properties succesfully calculated ")
        
# B.3) Filter out irregular features
        try:
            geom = mask_layers(geom, log = logger)
        except Exception as e:
            logger.error("Error while filtering out irregular layers ")
            sys.exit(8)  
        logger.info("       Irregular layers succesfully filtered out ")
    
        
###############################################################################
# C) Exporting
###############################################################################
        logger.info("Section C: Exporting layer properties ")
            
        if len(geom) > 0:
# C.1) Export to netcdf
# C.1.i) Netcdf filename
            try:
                fname = nc_name(metadata[i], prod_id = ids[i], wave = wave[i], 
                                ver = __version__)
            except Exception as e:
                logger.error("Error while creating the netcdf filename ")
                sys.exit(9)  
            logger.info("       Netcdf filename succesfully created ")
            
# C.1.ii) Netcdf file        
            try:
                dir_out = os.path.join(cfg.scc['output-dir'],meas_id)
                geom_dts = export_nc(geom, metadata[i], alphas[i], wave[i], 
                                     det_lims[i], fname, dir_out)
            except Exception as e:
                logger.error("Error while creating the netcdf files ")
                sys.exit(10)
            logger.info("       Exporting in NetCDF format succesfully completed ")
            
# C.2) Save in lists
            list_dates.append(dt_start_arr[i])
            list_geom.append(geom)
            list_geom_dts.append(geom_dts)
            logger.info("       Exporting in python list format succesfully completed ")
    
# C.3) Update the database
            try:
                fpath = os.path.join(rpath[i],fname)
                update(fpath, meas_id = meas_id, prod_id = ids[i], cfg = cfg)
            except Exception as e:
                logger.error("Error while updating the scc database ")
                sys.exit(11)         
            logger.info("       SCC database succesfully updated ")
        else:
            logger.warning("       No layers were identified for this measurement! ")

###############################################################################
# End of Program
############################################################################### 
    stop_time = datetime.datetime.now()
    duration = stop_time - start_time
    
    logger.info("------ Processing finished on %s ------" % stop_time)
    logger.info("------ Total duration: %s ------" % duration)
    logger.info("----------------------------------------------------------------")
    logging.shutdown()
    
    sys.exit(0)
