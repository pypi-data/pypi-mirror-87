# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os; os.chdir("S:/siat")
from siat.bond import *

aytm=0.08
yper=3
fv=100
c=0.1
mterm=1
bond_malkiel4(aytm,yper,c,fv,mterm)

bplist=[-300,-250,-200,-150,-100,-50,50,100,150,200,250,300]
bplist=[-50,-40,-30,-20,-10,10,20,30,40,50]
bplist=[-250,-200,-150,-100,-50,50,100,150,200,250]
bplist=[-500,-400,-300,-200,-100,100,200,300,400,500]
bond_malkiel4(aytm,yper,c,fv,mterm,bplist)


country='米国'
name='美国10年期国债'
fromdate='2020-1-1'
todate='2020-5-6'

ak.bond_investing_global_country_name_url(country="美国")
df=ak.bond_investing_global(country="中国", index_name="中国1年期国债", period="每周", start_date="2000-01-01", end_date="2020-06-06")

country_bond_list(country)
df=country_bond_price(country,name,fromdate,todate)


    c=0.026
    v=30
    mlist=[4,6,8,10,12,14,16]
    f=2
    r=0.03
df=cf_day_remain_trend(0.026,30,mlist,2,0.03)
df=cf_day_remain_trend(0.035,30,mlist,2,0.03)
