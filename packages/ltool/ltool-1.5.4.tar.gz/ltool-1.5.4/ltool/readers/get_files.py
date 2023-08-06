#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 13:03:44 2020

@author: nick
"""
import mysql.connector
import numpy as np
import os, glob, re

def database(meas_id, cfg):
    
    mydb = mysql.connector.connect(
      host=cfg.dtb['host'],
      user=cfg.dtb['user'],
      passwd=cfg.dtb['password'],
      port=cfg.dtb['port'],
      db=cfg.dtb['scc-db-name']
    )
    
    cur = mydb.cursor()
    
    cur.execute("SELECT measurements.ID, products.ID, " +\
                "ltool_product_options._input_product_ID, " +\
                "ltool_product_options.dilation, " +\
                "product_options.detection_limit, " +\
                "ltool_product_options.detection_limit_factor, " +\
                "elda_products.filename FROM measurements INNER JOIN " +\
                "system_product INNER JOIN products INNER JOIN product_options " +\
                "INNER JOIN ltool_product_options INNER JOIN elda_products ON " +\
                "system_product._system_ID=measurements._hoi_system_ID AND " +\
                "system_product._Product_ID=products.ID AND " +\
                "product_options._product_ID=elda_products._product_ID AND " +\
                "products._ltool_product_option_ID=ltool_product_options.ID AND " +\
                "ltool_product_options._input_product_ID=elda_products._product_ID AND " +\
                "elda_products.__measurements__ID=measurements.ID WHERE " +\
                "products._prod_type_ID=10 AND measurements.ID='" +\
                meas_id+"'")

    
    query = cur.fetchall()
    
    files = np.array([os.path.join(cfg.scc['input-dir'], x[6]) for x in query])
    
    rpath = np.array([os.path.split(x[6])[0] for x in query])

    alphas = np.array([x[3]/100. for x in query])
    
    det_lims = np.array([1E6*float(x[4]) for x in query])
    
    ids = np.array([x[1] for x in query]).astype(str)
    
    mydb.close()
        
    return(files, rpath, alphas, det_lims, ids)