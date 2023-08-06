# -*- coding: utf-8 -*-
"""
Created on Thu May  5 15:19:16 2016

@author: nick
"""
import numpy as np

def wavelet(sig,step,alpha):
    
    ihalf = int(alpha/(2*step))
    wsig = np.nan*np.zeros(len(sig))
    
    for i in range(ihalf+1,len(sig)-ihalf-1):
        int_d = np.trapz(sig[(i-ihalf):i+1],dx=step)
        int_u = np.trapz(sig[i:(i+ihalf)+1],dx=step)
        if (int_u == int_u) and (int_d == int_d):
            wsig[i]=(np.trapz(-sig[(i-ihalf):i+1],dx=step)+np.trapz(sig[i:(i+ihalf)+1],dx=step))/alpha
    return(wsig)