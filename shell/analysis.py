# created by zhaoliyuan

# help to do analysis and other operations on dataframes with data loading from database

import pandas as pd
from datetime import *
from dateutil.parser import parse
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

#    # load basic data
#    df = loadStockIndex('','')
#    sh000001 = df[df['S_INFO_WINDCODE'] == '000001.SH']
#    sh000001['TRADE_DT'] = sh000001['TRADE_DT'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
#    sh000001.sort_values('TRADE_DT', ascending = True, inplace = True)
#    sh000001.reset_index(inplace = True, drop = True)
#
#    sz399001 = df[df['S_INFO_WINDCODE'] == '399001.SZ']
#    sz399001['TRADE_DT'] = sz399001['TRADE_DT'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
#    sz399001.sort_values('TRADE_DT', ascending = True, inplace = True)
#    sz399001.reset_index(inplace = True, drop = True)
#
#    h11007 = loadBondIndex('','')
#    h11007['TRADE_DT'] = h11007['TRADE_DT'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
#    h11007.sort_values('TRADE_DT', ascending = True, inplace = True)
#    h11007.reset_index(inplace = True, drop = True)
#
#    # fullfill the dataframe
#    def fullfill(df):
#        i = 0
#        df['TRADE_DT'] = df['TRADE_DT'].apply(lambda x: parse(x))
#        maxDate = df['TRADE_DT'].max()
#        while True:
#            date = df['TRADE_DT'][i]
#            if date == maxDate:
#                break
#            else:
#                i += 1
#            reference = date + timedelta(days = 1)
#            if df[df['TRADE_DT'] == reference].empty:
#                newRow = df[df['TRADE_DT'] == date]
#                newRow['TRADE_DT'] = reference
#                df = pd.concat([df[df['TRADE_DT']<=date],newRow,df[df['TRADE_DT']>date]])
#                df.reset_index(drop = True, inplace = True)
#        df['TRADE_DT'] = df['TRADE_DT'].apply(lambda x: str(x))
#        df.reset_index(drop = True, inplace = True)
#        return df
#   
#    sh000001 = fullfill(sh000001)
#    sz399001 = fullfill(sz399001)
#    h11007 = fullfill(h11007)
#
#    # change data to monthly data
#    def toMonthly(df, dates):
#        df[dates] = df[dates].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
#        bools = df[dates].str.endswith('-01')
#        newDf = df[bools]
#        return newDf
#    
#    sh000001Monthly = toMonthly(sh000001,'TRADE_DT')
#    sz399001Monthly = toMonthly(sz399001,'TRADE_DT')
#    h11007Monthly = toMonthly(h11007,'TRADE_DT')
#    sh000001Monthly.S_DQ_CHANGE = sh000001Monthly.S_DQ_CLOSE.pct_change()
#    sz399001Monthly.S_DQ_CHANGE = sz399001Monthly.S_DQ_CLOSE.pct_change()
#    h11007Monthly.S_DQ_CHANGE = h11007Monthly.S_DQ_CLOSE.pct_change()
#
#    # save monthly data
#    excel = pd.ExcelWriter('monthly.xlsx')
#    sh000001Monthly.to_excel(excel, sheet_name = '上证综指月频')
#    sz399001Monthly.to_excel(excel, sheet_name = '深证综指月频')
#    excel.save()

    # fourier analysis
    def fourier(y):
        plt.plot(y)
        fy = abs(fft(y))
        plt.plot(fy)
    
#    sh000001Monthly = pd.read_excel('monthly.xlsx',index_col = 0, sheet_name = '上证综指月频')
#    sz399001Monthly = pd.read_excel('monthly.xlsx', index_col = 0, sheet_name = '深证综指月频')
#    fourier(sh000001Monthly['S_DQ_CHANGE'])
#    fourier(sz399001Monthly['S_DQ_CHANGE'])
#    df1 = pd.read_excel('monthly.xlsx', index_col = 0, sheet_name = '上证综指月频')
#    df2 = pd.read_excel('monthly.xlsx', index_col = 0, sheet_name = '深证综指月频')
#
#    # calculate year-on-year data
#    def yearOnYear(df,values, dates):
#        df = df.sort_values(dates)
#        df = df.reset_index(drop = True)
#        df['YEAR_ON_YEAR_RETURN'] = 0.0
#        for i in range(len(df)-12):
#            df['YEAR_ON_YEAR_RETURN'][i+12] = df.iloc[i+12][values] / df.iloc[i][values] - 1
#        return df
#
#    df1 = yearOnYear(df1, 'S_DQ_CLOSE', 'TRADE_DT')
#    df2 = yearOnYear(df2, 'S_DQ_CLOSE', 'TRADE_DT')
#
#    # save monthly data with year-on-year rate
#    excel = pd.ExcelWriter('monthly.xlsx')
#    df1.to_excel(excel, sheet_name = '上证综指月频')
#    df2.to_excel(excel, sheet_name = '深证综指月频')
#    excel.save()

    # select data
    df1 = pd.read_excel('monthly.xlsx', index_col = 0, sheet_name = '上证综指月频')
    df2 = pd.read_excel('monthly.xlsx', index_col = 0, sheet_name = '深证综指月频')
    df1['TRADE_DT'] = df1['TRADE_DT'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
    df2['TRADE_DT'] = df2['TRADE_DT'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
    df1 = df1[df1['TRADE_DT']>'1996-01-01']
    df2 = df2[df2['TRADE_DT']>'1996-01-01']
    excel =  pd.ExcelWriter('monthly_part.xlsx')
    df1.to_excel(excel, sheet_name = '上证综指月频')
    df2.to_excel(excel, sheet_name = '深证综指月频')
    excel.save()


if __name__ ==  '__main__':
    analysis()

