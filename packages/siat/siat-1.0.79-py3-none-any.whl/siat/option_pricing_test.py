# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:08:44 2020

@author: Peter
"""


import os; os.chdir("S:/siat")
from siat.option_pricing import *

bsm_aprice([30,50],42,183,0.015,0.23,90,1.5)
df=bsm_maturity(40,42,[200,100],0.015,0.23,90,1.5)
bsm_sigma(40,42,183,0.015,[0.1,0.4],90,1.5)

df=stock_trend_by_option('AAPL',7)
df=stock_trend_by_option('JD',7) 
df=stock_trend_by_option('MSFT',7) 
df=stock_trend_by_option('BABA',7) 
df=stock_trend_by_option('GS',7) 
df=stock_trend_by_option('PDD',7) 

df=recent_stock_split('AAPL')
df=recent_stock_split('MSFT')

get_last_close('AAPL')
get_last_close('MSFT')

import time
tupTime = time.localtime(1604350755)#秒时间戳
stadardTime = time.strftime("%Y-%m-%d %H:%M:%S", tupTime)
print(stadardTime)


ticker="AAPL"
mdate="2020-11-06"
opt_call, opt_put=option_chain(ticker,mdate,printout=False)


from siat.stock import *
div=stock_dividend('AAPL','2020-1-1','2020-11-3')
splt=stock_split('AAPL','2020-1-1','2020-11-3')


df=predict_stock_trend_by_option('AAPL')

df=predict_stock_trend_by_option('02020.HK',lastndays=7)
df=predict_stock_trend_by_option('2331.HK',lastndays=7)
df=predict_stock_trend_by_option('1368.HK',lastndays=7)

splt=stock_split('NKE','2020-1-1','2020-11-3')
df=predict_stock_trend_by_option('NKE',lastndays=30)

splt=stock_split('ADS.DE','2020-1-1','2020-11-3')
df=predict_stock_trend_by_option('ADS.DE',lastndays=30)

splt=stock_split('JD','2020-1-1','2020-11-3')
df=predict_stock_trend_by_option('JD')

splt=stock_split('BABA','2020-1-1','2020-11-3')
df=predict_stock_trend_by_option('BABA',lastndays=30)
