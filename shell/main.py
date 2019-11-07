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
from sqlhelper import *



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
        y = stock['上证综指']
        plt.plot(y)
        # 傅里叶变换振幅
        fy = abs(fft(y))
        fy = fy[0:len(fy)//2]
        # 傅里叶变换功率
        power = abs(np.square(fft(y)))
        power = power[0:len(power)//2]
        # 傅里叶变换频率 周期
        # 最高频率为 1/2 最低频率为 2/nfft 
        # nfft为采样周期
        nfft = len(y)
        nyquist = 1/2 
        freq = [nyquist*i/np.floor(nfft/2) for i in range(1,int(np.floor(nfft/2)+1))]
        freq = np.array(freq)
        period = 1/freq
        #k += 1
        #plt.figure(k)
        plt.plot(period,fy)
        plt.plot(period,power)
        #plt.title(i)
    
