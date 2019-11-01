# created by zhaoliyuan

# help to do analysis and other operations on dataframes with data loading from database

import pandas as pd
from datetime import *
import numpy as np
from loadData import *
# for sql database updating
from sqlhelper import batch
# fourier analysis
from scipy.fftpack import fft
# drawing 
import matplotlib.pyplot as plt
# for debug
from ipdb import set_trace 

def analysis():

    # load basic data
    df = loadStockIndex('','')
    sh000001 = df[df['S_INFO_WINDCODE'] == '000001.SH']
    sh000001['TRADE_DT'] = sh000001['TRADE_DT'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
    sh000001.sort_values('TRADE_DT', ascending = True, inplace = True)

    sz399001 = df[df['S_INFO_WINDCODE'] == '399001.SZ']
    sz399001['TRADE_DT'] = sz399001['TRADE_DT'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
    sz399001.sort_values('TRADE_DT', ascending = True, inplace = True)

    h11007 = loadBondIndex('','')
    h11007['TRADE_DT'] = h11007['TRADE_DT'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
    h11007.sort_values('TRADE_DT', ascending = True, inplace = True)

    # change data to monthly data
    def toMonthly(df, dates):
        bools = df[dates].str.endswith('-01')
        mask = df[bools]
        return mask
    
    sh000001Monthly = toMonthly(sh000001,'TRADE_DT')
    sz399001Monthly = toMonthly(sz399001,'TRADE_DT')
    h11007Monthly = toMonthly(h11007,'TRADE_DT')
    sh000001Monthly.S_DQ_CHANGE = sh000001Monthly.S_DQ_CLOSE.pct_change()
    sz399001Monthly.S_DQ_CHANGE = sz399001Monthly.S_DQ_CLOSE.pct_change()
    h11007Monthly.S_DQ_CHANGE = h11007Monthly.S_DQ_CLOSE.pct_change() # 这个数据并非每个月都有！！！

    # save monthly data
    excel = pd.ExcelWriter('monthly.xlsx')
    sh000001Monthly.to_excel(excel, sheet_name = '上证综指月频')
    sz399001Monthly.to_excel(excel, sheet_name = '深证综指月频')
    excel.save()

if __name__ ==  '__main__':
    analysis()

