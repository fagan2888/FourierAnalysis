# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 14:29:59 2019

@author: 86156
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from ipdb import set_trace
from sqlhelper import 



def loadStock():
    df = pd.read_excel('补全后数据.xlsx', index_col = 0, sheet_name = 0)
    df = df[df.index>'1993-04-30']
    df = df[df.index<'2017-05-01']
    return df
    
def loadBond():
    df = pd.read_excel('补全后数据.xlsx', index_col = 0, sheet_name = 1)
    df = df[df.index>'2006-08-31']
    df = df[df.index<'2017-02-01']
    return df
    
def loadPPI():
    df = pd.read_excel('补全后数据.xlsx', index_col = 0, sheet_name = 4)
    df = df[df.index>'1996-09-30']
    df = df[df.index<'2017-02-01']
    return df
   
def loadCPI():
    df = pd.read_excel('补全后数据.xlsx', index_col = 0, sheet_name = 5)
    df = df[df.index>'1996-09-30']
    df = df[df.index<'2017-02-01']
    return df
    
def loadGoods():
    df = pd.read_excel('补全后数据.xlsx', index_col = 0, sheet_name = 3)
    df = df[df.index>'1995-12-31']
    df = df[df.index<'2017-02-01']
    return df     
    
    
if __name__ == '__main__':
    stock = loadStock()
    bond = loadBond()
    PPI = loadPPI()
    CPI = loadCPI()
    goods = loadGoods()
    
    k = 0
    for i in PPI.columns.values:
        y = PPI[i]
        #k += 1
        #plt.figure(k)
        plt.plot(y)
        #plt.title(i)
       
    k = 0
    for i in stock.columns.values:    
        y = stock[i]
        fy = abs(fft(y))
        fy = fy[0:len(fy)]
        #k += 1
        #plt.figure(k)
        plt.plot(fy)
        #plt.title(i)
    