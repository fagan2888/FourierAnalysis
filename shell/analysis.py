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

    # load basic data
    df = loadStockIndex('','')
    sh000001 = df[df['S_INFO_WINDCODE'] == '000001.SH']
    sh000001['TRADE_DT'] = sh000001['TRADE_DT'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
    sh000001.sort_values('TRADE_DT', ascending = True, inplace = True)
    sh000001.reset_index(inplace = True, drop = True)

    sz399001 = df[df['S_INFO_WINDCODE'] == '399001.SZ']
    sz399001['TRADE_DT'] = sz399001['TRADE_DT'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
    sz399001.sort_values('TRADE_DT', ascending = True, inplace = True)
    sz399001.reset_index(inplace = True, drop = True)

    h11007 = loadBondIndex('','')
    h11007['TRADE_DT'] = h11007['TRADE_DT'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
    h11007.sort_values('TRADE_DT', ascending = True, inplace = True)
    h11007.reset_index(inplace = True, drop = True)

    # fullfill the dataframe
    def fullfill(df):
        i = 0
        df['TRADE_DT'] = df['TRADE_DT'].apply(lambda x: parse(x))
        maxDate = df['TRADE_DT'].max()
        while True:
            date = df['TRADE_DT'][i]
            if date == maxDate:
                break
            else:
                i += 1
            reference = date + timedelta(days = 1)
            if df[df['TRADE_DT'] == reference].empty:
                newRow = df[df['TRADE_DT'] == date]
                newRow['TRADE_DT'] = reference
                df = pd.concat([df[df['TRADE_DT']<=date],newRow,df[df['TRADE_DT']>date]])
                df.reset_index(drop = True, inplace = True)
        df['TRADE_DT'] = df['TRADE_DT'].apply(lambda x: str(x))
        df.reset_index(drop = True, inplace = True)
        return df
   
    sh000001 = fullfill(sh000001)
    sz399001 = fullfill(sz399001)
    h11007 = fullfill(h11007)
    sh000001.S_DQ_CHANGE = sh000001.S_DQ_CLOSE.pct_change()
    sz399001.S_DQ_CHANGE = sz399001.S_DQ_CLOSE.pct_change()

    # save daily data
    excel = pd.ExcelWriter('daily.xlsx')
    sh000001.to_excel(excel, sheet_name = '上证综指日频')
    sz399001.to_excel(excel, sheet_name = '深证综指日频')
    excel.save()

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

    # calculate year-on-year data
    def yearOnYear(df,values, dates, newname = 'YEAR_ON_YEAR_RETURN', steps = 12):
        df = df.sort_values(dates)
        df = df.reset_index(drop = True)
        df[newname] = 0.0
        for i in range(len(df)-steps):
            df[newname][i+steps] = df.iloc[i+steps][values] / df.iloc[i][values] - 1
        return df

#    df1 = pd.read_excel('monthly.xlsx', index_col = 0, sheet_name = '上证综指月频')
#    df2 = pd.read_excel('monthly.xlsx', index_col = 0, sheet_name = '深证综指月频')
#    df1 = yearOnYear(df1, 'S_DQ_CLOSE', 'TRADE_DT')
#    df2 = yearOnYear(df2, 'S_DQ_CLOSE', 'TRADE_DT')
#
#    # save monthly data with year-on-year rate
#    excel = pd.ExcelWriter('monthly.xlsx')
#    df1.to_excel(excel, sheet_name = '上证综指月频')
#    df2.to_excel(excel, sheet_name = '深证综指月频')
#    excel.save()

    df1 = pd.read_excel('daily.xlsx', index_col = 0, sheet_name = '上证综指日频')
    df2 = pd.read_excel('daily.xlsx', index_col = 0, sheet_name = '深证综指日频')
    df1 = yearOnYear(df1, 'S_DQ_CLOSE', 'TRADE_DT', steps = 365)
    df2 = yearOnYear(df2, 'S_DQ_CLOSE', 'TRADE_DT', steps = 365)
    df1 = yearOnYear(df1, 'S_DQ_CLOSE', 'TRADE_DT', newname = 'MONTH_ON_MONTH_RETURN', steps = 30)
    df2 = yearOnYear(df2, 'S_DQ_CLOSE', 'TRADE_DT', newname = 'MONTH_ON_MONTH_RETURN', steps = 30)
    df1 = yearOnYear(df1, 'S_DQ_CLOSE', 'TRADE_DT', newname = 'WEEK_ON_WEEK_RETURN', steps = 7)
    df2 = yearOnYear(df2, 'S_DQ_CLOSE', 'TRADE_DT', newname = 'WEEK_ON_WEEK_RETURN', steps = 7)

    # save monthly data with year-on-year rate
    excel = pd.ExcelWriter('daily.xlsx')
    df1.to_excel(excel, sheet_name = '上证综指日频')
    df2.to_excel(excel, sheet_name = '深证综指日频')
    excel.save()
    
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
    
    # load data for fourier analysis
    sh000001Monthly = pd.read_excel('monthly_part.xlsx',index_col = 0, sheet_name = '上证综指月频')
    sz399001Monthly = pd.read_excel('monthly_part.xlsx', index_col = 0, sheet_name = '深证综指月频')
    y = sh000001Monthly['YEAR_ON_YEAR_RETURN']
    y = sz399001Monthly['YEAR_ON_YEAR_RETURN']
    
    sh000001daily = pd.read_excel('daily.xlsx',index_col = 0, sheet_name = '上证综指日频')
    sz399001daily = pd.read_excel('daily.xlsx', index_col = 0, sheet_name = '深证综指日频')
    y = sh000001daily['WEEK_ON_WEEK_RETURN']
    y = sz399001daily['WEEK_ON_WEEK_RETURN']
    y = sh000001daily['MONTH_ON_MONTH_RETURN']
    y = sz399001daily['MONTH_ON_MONTH_RETURN']
    y = sh000001daily['YEAR_ON_YEAR_RETURN']
    y = sz399001daily['YEAR_ON_YEAR_RETURN']
    
    # fourier analysis
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

    plt.plot(period,fy)
    plt.plot(period,power)
    
    df = pd.DataFrame(columns = ['position', 'value'])
    df['position'] = period
    df['value'] = fy
    df = df[df['position']<150]
    
    plt.plot(df['position'], df['value'])
    
    
    # find the top/bottom n points
    def tpoint(x, y, n = 3, choice = 'max'):
        df = pd.DataFrame(columns = ['position', 'value'])
        df['position'] = x
        df['value'] = y
        
        if choice == 'max':
            df.sort_values(by = 'value', ascending = False, inplace = True)
        else:
            df.sort_values(by = 'value', ascending = True, inplace = True)

        outDf = df.iloc[0:n,:]
        outDf.sort_values(by = 'value', inplace = True)
        outDf.reset_index(drop = True, inplace = True)
        
        return outDf

    out1 = tpoint(df['position'], df['value'], n = 10)
    out2 = tpoint(period,power, n = 10)

    # using mean value to make the curve smooth
    def movingAverage(value, T):
        newValue = list()
        for i in range(T):
            newValue.append(value[i])
            
        for i in range(T, len(value)):
            newValue.append(sum(value[i-T:i]) / T)
        
        return newValue
    
    newFy = movingAverage(fy, 30)
    newPpower = movingAverage(power, 30)
    
    plt.plot(period, newFy)
    plt.plot(period, newPower)

if __name__ ==  '__main__':
    analysis()

