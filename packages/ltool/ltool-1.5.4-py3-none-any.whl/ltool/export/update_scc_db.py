#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:58:36 2020

@author: nick
"""
import os
import datetime as dt
import mysql.connector

def update(fpath, meas_id, prod_id, cfg):
    
        
    time_now  = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    arg = "SELECT scc_version.ID FROM scc_version WHERE " +\
        "scc_version.is_latest=1"
    scc_ver = str(search(cfg = cfg, arg = arg)[0][0])
    
    arg = f"SELECT count(ID) FROM ltool_products WHERE " +\
        "ltool_products.__measurements__ID='" + meas_id + "' " +\
            "AND _product_ID=" + prod_id
    isempty = search(cfg = cfg, arg = arg)[0][0]

    if isempty == 0:

        arg = f"INSERT INTO " +\
        "ltool_products(__measurements__ID,_product_ID,creation_date," +\
        "_scc_version_ID,filename) " +\
        "VALUES('" + meas_id + "'," + prod_id + ",'" + time_now +"'," +\
        "'" + scc_ver + "','" + fpath + "')"

        execute(cfg = cfg, arg = arg)
            

    if isempty != 0:
        
        arg = f"UPDATE ltool_products SET " +\
        "creation_date='" + time_now + "'," +\
        "_scc_version_ID=" + scc_ver + ",filename='" + fpath + "' " +\
        "WHERE ltool_products.__measurements__ID='" + meas_id + "' " +\
        "AND _product_ID=" + prod_id
        
        execute(cfg = cfg, arg = arg)

def search(cfg, arg):
    
    mydb = mysql.connector.connect(
      host=cfg.dtb['host'],
      user=cfg.dtb['user'],
      passwd=cfg.dtb['password'],
      port=cfg.dtb['port'],
      db=cfg.dtb['scc-db-name']
    )

    cur = mydb.cursor()

    cur.execute(arg)
    
    query = cur.fetchall()

    mydb.close()
    
    return(query)

def execute(cfg, arg):
    
    mydb = mysql.connector.connect(
      host=cfg.dtb['host'],
      user=cfg.dtb['user'],
      passwd=cfg.dtb['password'],
      port=cfg.dtb['port'],
      db=cfg.dtb['scc-db-name']
    )   

    cur = mydb.cursor()

    cur.execute(arg)
    mydb.commit()
        
    mydb.close()
    
    return()