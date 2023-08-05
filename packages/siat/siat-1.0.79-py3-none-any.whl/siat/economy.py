# -*- coding: utf-8 -*-
"""
本模块功能：宏观经济分析
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2020年8月31日
最新修订日期：2020年8月31日
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""
#==============================================================================
#关闭所有警告
import warnings; warnings.filterwarnings('ignore')
#==============================================================================
def get_econ_factors(start,end,scope='China',factor='GDP'):
   """
   【支持的因子种类(factor)】
   GDP, CPI, PPI,...

   【支持的国家/地区(scope)】
   US: 美国
   China: 中国
   Korea: 韩国
   Japan: 日本
   India: 印度

   【支持的取样频率(freq)】
   Annual: 年
   Quarterly: 季度
   Monthly: 月
   """
   s=fred_factor_codes() 

   #帮助1：国家列表
   if scope=='?':
       scopelist=list(set(list(s[s['factor']==factor]['scope'])))
       if len(scopelist)==0:
           print("#Error(get_econ_factors): no such economy factor,",factor)
       else:
           title="\n*** Supported scopes for factor, "+factor+':'
           print(title)
           linelen=0
           for i in range(len(scopelist)):
               print(scopelist[i],end='')
               linelen=linelen+len(scopelist[i])+2
               if (linelen >= len(title)-2): 
                   print(''); linelen=0
               else:
                   if (i+1) < len(scopelist): 
                       print(', ',end='')
                   else:
                       print('')
       return None
   
   #帮助2：经济指标
   if (scope != '?') and (factor=='?'):
       factorlist=list(set(list(s[s['scope']==scope]['factor'])))
       if len(factorlist)==0:
           print("#Error(get_econ_factors): no or unavailable country/region,",scope)
       else:
           title="\n*** Supported factors for scope, "+scope+':'
           print(title)
           linelen=0
           for i in range(len(factorlist)):
               print(factorlist[i],end='')
               linelen=linelen+len(factorlist[i])+2
               if (linelen >= len(title)-2): 
                   print(''); linelen=0
               else:
                   if (i+1) < len(factorlist): 
                       print(', ',end='')
                   else:
                       print('')
       return None

   #匹配：scope+factor+freq
   ss=s[s['scope'].isin([scope]) & s['factor'].isin([factor])]  
   #如果未找到匹配的模式，显示信息后返回
   if len(ss)==0:
        print("#Error(get_econ_factors): no such data entry available for",scope,factor)
        return None

   #取出对应的关键字symbol
   symbol=list(ss['symbol'])[0]

   #按照关键字抓取数据
   import pandas_datareader as web
   try:
        ds=web.get_data_fred(symbol,start,end)
   except:
        print("#Error(get_econ_factors): connection to data source failed!")        
        return None
   if len(ds)==0:
        print("#Error(get_econ_factors): server returned empty data!")        
        return None
   # 结果字段统一改名
   ds.columns=['VALUE'] 
   ds['scope']=list(ss['scope'])[0]
   ds['factor']=list(ss['factor'])[0]
   ds['freq']=list(ss['freq'])[0]
   ds['name']=list(ss['name'])[0]
   ds['symbol']=list(ss['symbol'])[0]
   ds['units']=list(ss['units'])[0]

   return ds

if __name__=='__main__':
    start='2010-1-1'; end='2020-8-31'
    scope='China'; factor='Real GDP Per Capita'
    
    ds1=get_econ_factors('2010-1-1','2020-8-31','China','GDP')
    ds2=get_econ_factors('2010-1-1','2020-8-31','China','Real GDP')
    ds3=get_econ_factors('2010-1-1','2020-8-31','India','Constant GDP')
    get_econ_factors('2010-1-1','2020-8-31','?','Constant GDP')
    get_econ_factors('2010-1-1','2020-8-31','China','?')
#==============================================================================
def economy_trend(start,end,scope='China',factor='GDP',datatag=False,power=3,zeroline=False):
    """
    功能：绘制宏观经济指标，单线，有趋势线    
    """
    #检查日期期间的合理性
    valid,_,_=check_period(start,end)
    if not valid:
        print('#Error(trend_economy): period not valid:',start,end)
        return
    
    #获取指标
    ds=get_econ_factors(start,end,scope,factor)
    if (ds is None):
        #print('#Error(trend_economy): scope/economic factor not available:',scope,'/',factor)
        return

    #绘图
    ylabeltxt=factor
    titletxt=scope+': '+list(ds['name'])[0]
    
    import datetime
    today=datetime.date.today()
    footnote='单位: '+list(ds['units'])[0]+', '+list(ds['freq'])[0]+ \
        '\n数据来源: FRED|IMF|OECD/IBA/UPENN/WB, '+str(today)
    ds.dropna(inplace=True)
    plot_line(ds,'VALUE',factor,ylabeltxt,titletxt,footnote,datatag,power=power,zeroline=zeroline)
    
    return ds


if __name__=='__main__':
    start='2010-1-1'; end='2020-8-31'
    scope='USA'; factor='Real GDP Per Capita'
    
    ds=economy_trend(start,end,scope='China',factor='GDP')
    ds=economy_trend(start,end,scope='Japan',factor='Real GDP')

#==============================================================================
def compare_economy(tickers,measures,fromdate,todate,power=0,twinx=False):
    """
    功能：对比绘制折线图：一个国家的两种测度，或两个国家的同一个测度。
    输入：
    国家代码tickers，如果是一个列表且内含两个代码，则认为希望比较两个国家的
    同一个测度指标。如果是一个列表但只内含一个国家代码或只是一个国家代码的字符串，
    则认为希望比较一个国家的两个测度指标。
    测度指标measures：如果是一个列表且内含两个测度指标，则认为希望比较一个国家的
    两个测度指标。如果是一个列表但只内含一个测度指标或只是一个测度指标的字符串，
    则认为希望比较两个国家的同一个测度指标。
    如果两个判断互相矛盾，以第一个为准。
    开始日期fromdate，结束日期todate。
    输出：绘制经济指标折线图，手动指定是否使用单轴或双轴坐标。
    返回：无
    """
    #检查日期期间的合理性
    valid,_,_=check_period(fromdate,todate)
    if not valid:
        print('#Error(compare_economy): period not valid:',fromdate,todate)
        return
    
    #判断国家代码个数
    #如果tickers只是一个字符串
    security_num = 0
    if isinstance(tickers,str): 
        security_num = 1
        ticker1 = tickers
    #如果tickers是一个列表
    if isinstance(tickers,list): 
        security_num = len(tickers)
        if security_num == 0:
            print("#Error(compare_economy): 未提供国家代码！")
            return
        if security_num >= 1: ticker1 = tickers[0]
        if security_num >= 2: ticker2 = tickers[1]
            
    #判断测度个数
    #如果measures只是一个字符串
    measure_num = 0
    if isinstance(measures,str): 
        measure_num = 1
        measure1 = measures
    #如果measures是一个列表
    if isinstance(measures,list): 
        measure_num = len(measures)
        if measure_num == 0:
            print("#Error(compare_economy): 未提供测度指标！")
            return
        if measure_num >= 1: measure1 = measures[0]
        if measure_num >= 2: measure2 = measures[1]

    import datetime; today=datetime.date.today()
    #是否单一国家代码+两个测度指标
    if (security_num == 1) and (measure_num >= 2):
        #国家ticker1：抓取经济指标measure1
        df1=get_econ_factors(fromdate,todate,ticker1,measure1)
        if df1 is None: return None, None

        #国家ticker1：抓取经济指标measure2
        df2=get_econ_factors(fromdate,todate,ticker1,measure2)
        if df2 is None: return None, None
        
        #绘制单个国家的双指标对比图
        ylabeltxt=''
        titletxt=ticker1+':\n'+ \
            measure1+'对比'+measure2
        footnote=measure1+': '+list(df1['units'])[0]+', '+list(df1['freq'])[0]+ \
            '\n'+measure2+': '+list(df2['units'])[0]+', '+list(df2['freq'])[0]+ \
            '\n数据来源: FRED|IMF|OECD, '+str(today)
            
        plot_line2(df1,ticker1,'VALUE',measure1, \
               df2,ticker1,'VALUE',measure2, \
               ylabeltxt,titletxt,footnote, \
               power=power,twinx=twinx)        
        
    elif (security_num >= 2) and (measure_num >= 1):
        #双国家+单个测度指标        
        #国家ticker1：抓取经济指标measure1
        df1=get_econ_factors(fromdate,todate,ticker1,measure1)
        if df1 is None: return None, None

        #国家ticker2：抓取经济指标measure1
        df2=get_econ_factors(fromdate,todate,ticker2,measure1)
        if df2 is None: return None, None

        #绘制双国家单指标对比图
        ylabeltxt=measure1
        #这里的GNP指标实际上是GNP vs GDP的百分比
        if measure1 == 'GNP':
            ylabeltxt='GNP/GDP%'
        titletxt=ticker1+'对比'+ticker2+'\n'+list(df1['name'])[0]
        
        footnote='单位: '+list(df1['units'])[0]+', '+list(df1['freq'])[0]+ \
            '\n数据来源: FRED|IMF|OECD, '+str(today)
            
        plot_line2(df1,ticker1,'VALUE',measure1, \
               df2,ticker2,'VALUE',measure1, \
               ylabeltxt,titletxt,footnote, \
               power=power,twinx=twinx)         
    else:
        print("#Error(compare_economy): 未能理解需要比较的内容！")
        return None,None

    return df1,df2

if __name__ =="__main__":
    tickers=['China','India']
    measures='GDP'
    fromdate='2010-1-1'
    todate='2020-8-31'
    
    df=compare_economy(tickers,measures,fromdate,todate)
    df=compare_economy(tickers,measures,fromdate,todate,twinx=True)

    df=compare_economy(tickers,'GDP Per Capita',fromdate,todate)
    df=compare_economy(tickers,'GDP Per Capita',fromdate,todate,twinx=True)

    df=compare_economy('India',['Real GDP','Real GDP Per Capita'],fromdate,todate,twinx=True)
    df=compare_economy('Japan',['Real GDP','Real GDP Per Capita'],fromdate,todate,twinx=True)
    df=compare_economy('Israel',['Real GDP','Real GDP Per Capita'],fromdate,todate,twinx=True)

#==============================================================================
def econ_fin_depth(fromdate,todate,scope,power=0,graph=True):
    """
    功能：经济的金融化深度，一个国家
    """
    #检查日期期间的合理性
    valid,_,_=check_period(fromdate,todate)
    if not valid:
        print('#Error(econ_fin_depth): period not valid:',fromdate,todate)
        return None   
    
    #获取GDP，按季度，本币
    gdp_qtr=get_econ_factors(fromdate,todate,scope,'Constant GDP')
    gdp_qtr['date']=gdp_qtr.index.date
    datecvt=lambda x: str(x)[0:4]
    gdp_qtr['date_str']=gdp_qtr['date'].apply(datecvt)

    import numpy as np
    gdp_annual=gdp_qtr.groupby(['date_str'])['VALUE'].agg(['count',np.sum])
    gdp_annual2=gdp_annual[gdp_annual['count']==4]

    #获取M2，按月，本币
    m2_mth=get_econ_factors(fromdate,todate,scope,'M2')
    m2_mth['date']=m2_mth.index.date
    datecvt=lambda x: str(x)[0:4]
    m2_mth['date_str']=m2_mth['date'].apply(datecvt)

    m2_annual=m2_mth.groupby(['date_str'])['VALUE'].agg(['count',np.sum])
    m2_annual2=m2_annual[m2_annual['count']==12]

    #合并
    import pandas as pd
    m2_gdp=pd.merge(m2_annual2,gdp_annual2,on='date_str')
    m2_gdp.dropna(inplace=True)
    m2_gdp['m2/gdp']=m2_gdp['sum_x']/m2_gdp['sum_y']
    
    df=m2_gdp[['m2/gdp']]

    #绘图
    if not graph: return df
    colname='m2/gdp'
    collabel="经济的金融深度"
    ylabeltxt="M2/GDP比例"
    titletxt=scope+': 经济的金融深度'
    footnote="数据来源: FRED/OECD/WB"
    plot_line(df,colname,collabel,ylabeltxt,titletxt,footnote,power=power)

    return df

if __name__=='__main__':
    fromdate='2000-1-1'; todate='2020-8-31'
    scope="China"
    cn=econ_fin_depth(fromdate,todate,scope,power=4)
    print(min(cn['m2/gdp']),max(cn['m2/gdp']))
    print(cn)
    jp=econ_fin_depth(fromdate,todate,'Japan',power=0)    
    us=econ_fin_depth(fromdate,todate,'USA',power=0)
    kr=econ_fin_depth(fromdate,todate,'Korea',power=0)

#==============================================================================
def compare_efd(fromdate,todate,scopelist,power=0):
    """
    功能：比较经济的金融化深度，两个国家
    """
    #检查日期期间的合理性
    valid,_,_=check_period(fromdate,todate)
    if not valid:
        print('#Error(econ_fin_depth): period not valid:',fromdate,todate)
        return None,None   

    #检查国家列表
    if isinstance(scopelist,list): 
        if len(scopelist) < 2:
            print("#Error(compare_efd): need a list with 2 countries",scopelist)
            return None,None
        scope1 = scopelist[0]; scope2 = scopelist[1]
    else:
        print("#Error(compare_efd): need a list with 2 countries",scopelist)
        return None,None
 
    #计算scope1/2的efd。美国的M2指标单位是Billions Dollars
    df1=econ_fin_depth(fromdate,todate,scope1,graph=False)
    if scope1=='USA':
        df1['m2/gdp']=df1['m2/gdp']*1000000000.0
    df2=econ_fin_depth(fromdate,todate,scope2,graph=False)
    if scope2=='USA':
        df2['m2/gdp']=df2['m2/gdp']*1000000000.0
    
    #绘图
    ticker1=scope1; ticker2=scope2
    colname1='m2/gdp'; colname2='m2/gdp'
    label1="EFD"; label2="EFD"
    ylabeltxt="EFD系数"
    titletxt=scope1+'对比'+scope2+': \n经济的金融深度'
    footnote="注: 经济的金融深度(EFD)=M2/GDP. "+ "数据来源: IMF/FRED"
    plot_line2(df1,ticker1,colname1,label1, \
               df2,ticker2,colname2,label2, \
               ylabeltxt,titletxt,footnote, \
               power=power)
    return df1,df2

if __name__=='__main__':
    fromdate='2000-1-1'; todate='2020-8-31'
    scopelist=["China","Japan"]
    power=4
    cn,us=compare_efd(fromdate,todate,['China','USA'])
    cn,jp=compare_efd(fromdate,todate,['China','Japan'])
    cn,kr=compare_efd(fromdate,todate,['China','Korea'])

#==============================================================================
def economy_security(scope,fromdate,todate,econ_factor,sec_ticker):
    """
    功能：比较宏观经济与证券市场之间的关联关系
    scope: 国家/地区
    econ_factor: 例如GDP
    sec_ticker: 例如标普500指数、道琼斯指数、上证综合指数
    输出： df
    """
    #检查日期期间的合理性
    valid,_,_=check_period(fromdate,todate)
    if not valid:
        print('#Error(economy_security): period not valid:',fromdate,todate)
        return None,None

    #获得econ_factor
    econ=get_econ_factors(fromdate,todate,scope,econ_factor)
    if econ is None:
        print('#Error(economy_security): scope/economic factor not available:',scope,econ_factor)
        return None,None
    econ_growth='Growth %'
    econ[econ_growth]=econ['VALUE'].pct_change()*100.0
    
    #获得sec_ticker行情
    sec=get_price(sec_ticker,fromdate,todate)
    if sec is None:
        print('#Error(economy_security): ticker info not available:',sec_ticker)
        return None,None    

    #绘图1： 直接指标，双轴
    econ_min1,econ_max1=get_df_period(econ)    
    sec_min1,sec_max1=get_df_period(sec)
    min1=max(econ_min1,sec_min1)
    max1=min(econ_max1,sec_max1)
    econ1=set_df_period(econ,min1,max1)
    sec1=set_df_period(sec,min1,max1)    
    
    df1=econ1; ticker1=econ_factor; colname1='VALUE'; label1=econ_factor
    df2=sec1; ticker2=sec_ticker; colname2='Close'; label2=sec_ticker
    ylabeltxt=''
    titletxt=scope+": 宏观经济与证券市场的关系"
    footnote="数据来源: FRED|Yahoo Finance"
    plot_line2(df1,ticker1,colname1,label1, \
               df2,ticker2,colname2,label2, \
               ylabeltxt,titletxt,footnote, \
               power=0,twinx=True)

    #绘图2： 增长指标，双轴
    econ2=econ.dropna()
    econ_min1,econ_max1=get_df_period(econ2)    
    sec_min1,sec_max1=get_df_period(sec)
    min1=max(econ_min1,sec_min1)
    max1=min(econ_max1,sec_max1)
    econ3=set_df_period(econ,min1,max1)    
    sec3=set_df_period(sec,min1,max1)    
    df1=econ3; df2=sec3
    
    colname1=econ_growth; label1=econ_growth
    titletxt=scope+": 经济增长与证券市场的关系"
    plot_line2(df1,ticker1,colname1,label1, \
               df2,ticker2,colname2,label2, \
               ylabeltxt,titletxt,footnote, \
               power=0,twinx=True)
    return econ,sec

if __name__=='__main__':
    fromdate='2010-1-1'; todate='2019-12-31'
    scope='China'; econ_factor='GDP'; sec_ticker='000001.SS'

    df_cn1=economy_security('China','1995-1-1','2019-12-31','GDP Per Capita','000001.SS')    
    df_cn2=economy_security('China','1995-1-1','2019-12-31','CNP GDP','000001.SS')
    df_us1=economy_security('USA','1980-1-1','2019-12-31','GDP','^DJI')
    df_us2=economy_security('USA','1980-1-1','2019-12-31','GDP','^GSPC')
#==============================================================================
def get_df_period(df):
    """
    功能： 获得df中日期索引的最小最大值
    """
    df_min=min(df.index)
    df_max=max(df.index)
    return df_min,df_max

if __name__=='__main__':
    df=get_price('AAPL','2020-1-1','2020-1-31')
    get_df_period(df)
    
#==============================================================================
def set_df_period(df,df_min,df_max):
    """
    功能： 去掉df中日期范围以外的记录
    """
    df1=df[df.index >= df_min]
    df2=df1[df1.index <= df_max]
    return df2

if __name__=='__main__':
    df=get_price('AAPL','2020-1-1','2020-1-31')    
    df_min,df_max=get_df_period(df)    
    df2=set_df_period(df,df_min,df_max)

#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
def plot_line(df,colname,collabel,ylabeltxt,titletxt,footnote,datatag=False, \
              power=0,zeroline=False):
    """
    功能：绘制折线图。如果power=0不绘制趋势图，否则绘制多项式趋势图
    假定：数据表有索引，且已经按照索引排序
    输入：数据表df，数据表中的列名colname，列名的标签collabel；y轴标签ylabeltxt；
    标题titletxt，脚注footnote；是否在图中标记数据datatag；趋势图的多项式次数power
    输出：折线图
    返回值：无
    """
    import matplotlib.pyplot as plt
    
    #设置绘图时的汉字显示
    #plt.rcParams['font.sans-serif'] = ['FangSong']  # 设置默认字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体
    # 解决保存图像时'-'显示为方块的问题
    plt.rcParams['axes.unicode_minus'] = False  

    #先绘制折线图
    plt.plot(df.index,df[colname],'-',label=collabel, \
             linestyle='-',linewidth=2,color='blue', \
                 marker='o',markersize=2)
    #绘制数据标签
    if datatag:
        for x, y in zip(df.index, df[colname]):
            plt.text(x,y+0.1,'%.2f' % y,ha='center',va='bottom',color='black')        
    
    #是否绘制水平0线
    if zeroline and (min(df[colname]) < 0):
        plt.axhline(y=0,ls=":",c="black")
        
    #绘制趋势线
    if power > 0:
        try:
            #生成行号，借此将横轴的日期数量化，以便拟合
            df['id']=range(len(df))
        
            #设定多项式拟合，power为多项式次数
            import numpy as np
            #print("DEBUG(plot_line): power=",power)
            parameter = np.polyfit(df.id, df[colname], power)
            f = np.poly1d(parameter)
            plt.plot(df.index, f(df.id),"r--", label="趋势线")
        except: pass
    
    plt.legend(loc='best')
    xmin=min(df.index); xmax=max(df.index)
    plt.xlim(xmin, xmax)    
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    #plt.xticks(rotation=45)
    plt.ylabel(ylabeltxt)
    plt.xlabel(footnote)
    
    #xmin=min(df.index); xmax=max(df.index)
    #plt.xlim(xmin, xmax)
    plt.title(titletxt,fontsize=12)
    plt.show()
    plt.close()
    return

if __name__ =="__main__":
    plot_line(df,'Close',"收盘价","价格","万科股票","数据来源：雅虎财经",power=4)

#==============================================================================
def plot_line2_coaxial(df1,ticker1,colname1,label1, \
                       df2,ticker2,colname2,label2, \
                    ylabeltxt,titletxt,footnote, \
                    power=0,datatag1=False,datatag2=False,zeroline=False):
    """
    功能：绘制两个证券的折线图。如果power=0不绘制趋势图，否则绘制多项式趋势图
    假定：数据表有索引，且已经按照索引排序
    输入：
    证券1：数据表df1，证券代码ticker1，列名1，列名标签1；
    证券2：数据表df2，证券代码ticker2，列名2，列名标签2；
    标题titletxt，脚注footnote；是否在图中标记数据datatag；趋势图的多项式次数power
    输出：绘制同轴折线图
    返回值：无
    """
 
    import matplotlib.pyplot as plt
    #设置绘图时的汉字显示
    #plt.rcParams['font.sans-serif'] = ['FangSong']  # 设置默认字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体
    # 解决保存图像时'-'显示为方块的问题
    plt.rcParams['axes.unicode_minus'] = False  
    
    #证券1：先绘制折线图
    plt.plot(df1.index,df1[colname1],'-',label=codetranslate(ticker1)+'('+label1+')', \
             linestyle='-',linewidth=2)
    #证券1：绘制数据标签
    if datatag1:
        for x, y in zip(df1.index, df1[colname1]):
            plt.text(x,y+0.1,'%.2f' % y,ha='center',va='bottom',color='black')        

    #是否绘制水平0线
    if zeroline and ((min(df1[colname1]) < 0) or (min(df2[colname2]) < 0)):
        plt.axhline(y=0,ls=":",c="black")
        
    #绘证券1：制趋势线
    if power > 0:
        try:
            #生成行号，借此将横轴的日期数量化，以便拟合
            df1['id']=range(len(df1))
        
            #设定多项式拟合，power为多项式次数
            import numpy as np
            parameter = np.polyfit(df1.id, df1[colname1], power)
            f = np.poly1d(parameter)
            plt.plot(df1.index, f(df1.id),"r--", label=codetranslate(ticker1)+"(趋势线)")
        except: pass
    
    #证券2：先绘制折线图
    plt.plot(df2.index,df2[colname2],'-',label=codetranslate(ticker2)+'('+label2+')', \
             linestyle='-.',linewidth=2)
    #证券2：绘制数据标签
    if datatag2:
        for x, y in zip(df2.index, df2[colname2]):
            plt.text(x,y+0.1,'%.2f' % y,ha='center',va='bottom',color='black')        
        
    #绘证券2：制趋势线
    if power > 0:
        try:
            #生成行号，借此将横轴的日期数量化，以便拟合
            df2['id']=range(len(df2))
        
            #设定多项式拟合，power为多项式次数
            import numpy as np
            parameter = np.polyfit(df2.id, df2[colname2], power)
            f = np.poly1d(parameter)
            plt.plot(df2.index, f(df2.id),"r--", label=codetranslate(ticker2)+"(趋势线)")
        except: pass
    
    plt.legend(loc='best')
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    #plt.xticks(rotation=45)
    plt.ylabel(ylabeltxt)
    plt.xlabel(footnote)
    plt.title(titletxt,fontsize=12)
    plt.show()
    plt.close()
    return

if __name__ =="__main__":
    df1 = get_price('000002.SZ', '2020-1-1', '2020-3-16')
    df2 = get_price('600266.SS', '2020-1-1', '2020-3-16')
    ticker1='000002.SZ'; ticker2='600266.SS'
    colname1='Close'; colname2='Close'
    label1="收盘价"; label2="收盘价"
    ylabeltxt="价格"
    plot_line2_coaxial(df1,'000002.SZ','High','最高价', \
        df1,'000002.SZ','Low','最低价',"价格", \
        "证券价格走势对比图","数据来源：雅虎财经")
    plot_line2_coaxial(df1,'000002.SZ','Open','开盘价', \
        df1,'000002.SZ','Close','收盘价',"价格", \
        "证券价格走势对比图","数据来源：雅虎财经")

    plot_line2_coaxial(df2,'600266.SS','Open','开盘价', \
        df2,'600266.SS','Close','收盘价',"价格", \
        "证券价格走势对比图","数据来源：雅虎财经")

#==============================================================================
def plot_line2_twinx(df1,ticker1,colname1,label1,df2,ticker2,colname2,label2, \
        titletxt,footnote,power=0,datatag1=False,datatag2=False):
    """
    功能：绘制两个证券的折线图。如果power=0不绘制趋势图，否则绘制多项式趋势图
    假定：数据表有索引，且已经按照索引排序
    输入：
    证券1：数据表df1，证券代码ticker1，列名1，列名标签1；
    证券2：数据表df2，证券代码ticker2，列名2，列名标签2；
    标题titletxt，脚注footnote；是否在图中标记数据datatag；趋势图的多项式次数power
    输出：绘制双轴折线图
    返回值：无
    """
    import matplotlib.pyplot as plt
    #设置绘图时的汉字显示
    #plt.rcParams['font.sans-serif'] = ['FangSong']  # 设置默认字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体
    # 解决保存图像时'-'显示为方块的问题
    plt.rcParams['axes.unicode_minus'] = False  

    #证券1：绘制折线图，双坐标轴
    import matplotlib.dates as mdates
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(df1.index,df1[colname1],'-',label=codetranslate(ticker1)+'('+label1+')', \
             linestyle='-',linewidth=2,color='blue')   
    #证券1：绘制数据标签
    if datatag1:
        for x, y in zip(df1.index, df1[colname1]):
            ax.text(x,y+0.1,'%.2f' % y,ha='center',va='bottom',color='black')

    #绘证券1：制趋势线
    if power > 0:
        #生成行号，借此将横轴的日期数量化，以便拟合
        df1['id']=range(len(df1))
        
        #设定多项式拟合，power为多项式次数
        import numpy as np
        parameter = np.polyfit(df1.id, df1[colname1], power)
        f = np.poly1d(parameter)
        ax.plot(df1.index, f(df1.id),"r--", label=codetranslate(ticker1)+"(趋势线)")

    #绘证券2：建立第二y轴
    ax2 = ax.twinx()
    ax2.plot(df2.index,df2[colname2],'-',label=codetranslate(ticker2)+'('+label2+')', \
             linestyle='-.',linewidth=2,color='orange')
    #证券2：绘制数据标签
    if datatag2:
        for x, y in zip(df2.index, df2[colname2]):
            ax2.text(x,y+0.1,'%.2f' % y,ha='center',va='bottom',color='black')
    
    #绘证券2：制趋势线
    if power > 0:
        #生成行号，借此将横轴的日期数量化，以便拟合
        df2['id']=range(len(df2))
        
        #设定多项式拟合，power为多项式次数
        import numpy as np
        parameter = np.polyfit(df2.id, df2[colname2], power)
        f = np.poly1d(parameter)
        ax2.plot(df2.index, f(df2.id),"c--", label=codetranslate(ticker2)+"(趋势线)")        
        
    ax.set_xlabel(footnote)
    ax.set_ylabel(label1+'('+codetranslate(ticker1)+')')
    ax.legend(loc='upper left')
    ax2.set_ylabel(label2+'('+codetranslate(ticker2)+')')
    ax2.legend(loc='upper right')
    
    #自动优化x轴标签
    #格式化时间轴标注
    #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d')) 
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    
    plt.title(titletxt, fontsize=12)
    plt.show()
    
    return


if __name__ =="__main__":
    df1 = get_price('000002.SZ', '2020-1-1', '2020-3-16')
    df2 = get_price('600266.SS', '2020-1-1', '2020-3-16')
    ticker1='000002.SZ'; ticker2='600266.SS'
    colname1='Close'; colname2='Close'
    label1="收盘价"; label2="收盘价"
    ylabeltxt="价格"
    plot_line2_twinx(df1,'000002.SZ','Close','收盘价', \
        df2,'600266.SS','Close','收盘价', \
        "证券价格走势对比图","数据来源：雅虎财经")

    plot_line2_twinx(df1,'000002.SZ','Close','收盘价', \
        df2,'600266.SS','Close','收盘价', \
        "证券价格走势对比图","数据来源：雅虎财经",power=3)

    
#==============================================================================
def plot_line2(df1,ticker1,colname1,label1, \
               df2,ticker2,colname2,label2, \
               ylabeltxt,titletxt,footnote, \
               power=0,datatag1=False,datatag2=False,yscalemax=5, \
               zeroline=False,twinx=False):
    """
    功能：绘制两个证券的折线图。如果power=0不绘制趋势图，否则绘制多项式趋势图
    假定：数据表有索引，且已经按照索引排序
    输入：
    证券1：数据表df1，证券代码ticker1，列名1，列名标签1；
    证券2：数据表df2，证券代码ticker2，列名2，列名标签2；
    标题titletxt，脚注footnote；是否在图中标记数据datatag；趋势图的多项式次数power
    输出：默认绘制同轴折线图，若twinx=True则绘制双轴折线图
    返回值：无
    """
    
    if not twinx:            
        plot_line2_coaxial(df1,ticker1,colname1,label1, \
                           df2,ticker2,colname2,label2, \
                ylabeltxt,titletxt,footnote,power,datatag1,datatag2,zeroline)
    else:
        plot_line2_twinx(df1,ticker1,colname1,label1, \
                         df2,ticker2,colname2,label2, \
                         titletxt,footnote,power,datatag1,datatag2)
    return

#==============================================================================
def plot_barh(df,colname,titletxt,footnote,datatag=True,colors=['r','g','b','c','m','y','k']):
    """
    功能：绘制水平柱状图，并可标注数据标签。
    输入：数据集df；列名colname；标题titletxt；脚注footnote；
    是否绘制数据标签datatag，默认是；柱状图柱子色彩列表。
    输出：水平柱状图
    """
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False  

    plt.barh(df.index,df[colname],align='center',color=colors,alpha=0.8)
    coltxt=ectranslate(colname)
    plt.xlabel(footnote)
    plt.title(titletxt,fontsize=14)
    
    xmin=int(min(df[colname]))
    xmax=(int(max(df[colname]))+1)*1.1
    plt.xlim([xmin,xmax])

    for x,y in enumerate(list(df[colname])):
        plt.text(y+0.1,x,'%s' % y,va='center')

    yticklist=list(df.index)
    yticknames=[]
    for yt in yticklist:
        ytname=codetranslate(yt)
        yticknames=yticknames+[ytname]
    plt.yticks(df.index,yticknames)

    plt.show(); plt.close()
    
    return

#==============================================================================
def check_period(fromdate, todate):
    """
    功能：根据开始/结束日期检查日期与期间的合理性
    输入参数：
    fromdate：开始日期。格式：YYYY-MM-DD
    enddate：开始日期。格式：YYYY-MM-DD
    输出参数：
    validity：期间合理性。True-合理，False-不合理
    start：开始日期。格式：datetime类型
    end：结束日期。格式：datetime类型
    """
    import pandas as pd
    
    #测试开始日期的合理性
    try:
        start=pd.to_datetime(fromdate)
    except:
        print("*** 错误#1(check_period)，无效的日期:",fromdate)
        return None, None, None         
    
    #测试结束日期的合理性
    try:
        end=pd.to_datetime(todate)
    except:
        print("*** 错误#2(check_period)，无效的日期:",todate)
        return None, None, None          
    
    #测试日期期间的合理性
    if start > end:
        print("*** 错误#3(check_period)，无效的日期期间: 从",fromdate,"至",todate)
        return None, None, None     

    return True, start, end

if __name__ =="__main__":
    check_period('2020-1-1','2020-2-4')
    check_period('2020-1-1','2010-2-4')

#==============================================================================
def ticker_check(ticker, source="yahoo"):
    """
    检查证券代码，对于大陆证券代码、香港证券代码和东京证券代码进行修正。
    输入：证券代码ticker，数据来源source。
    上交所证券代码后缀为.SS或.SH或.ss或.sh，深交所证券代码为.SZ或.sz
    港交所证券代码后缀为.HK，截取数字代码后4位
    东京证交所证券代码后缀为.T，截取数字代码后4位
    source：yahoo或tushare
    返回：字母全部转为大写。若是大陆证券返回True否则返回False。
    若选择yahoo数据源，上交所证券代码转为.SS；
    若选择tushare数据源，上交所证券代码转为.SH
    """
    #测试用，完了需要注释掉
    #ticker="600519.sh"
    #source="yahoo"
    
    #将字母转为大写
    ticker1=ticker.upper()
    #截取字符串最后2/3位
    suffix2=ticker1[-2:]
    suffix3=ticker1[-3:]
    
    #判断是否大陆证券
    if suffix3 in ['.SH', '.SS', '.SZ']:
        prc=True
    else: prc=False

    #根据数据源的格式修正大陆证券代码
    if (source == "yahoo") and (suffix3 in ['.SH']):
        ticker1=ticker1.replace(suffix3, '.SS')        
    if (source == "tushare") and (suffix3 in ['.SS']):
        ticker1=ticker1.replace(suffix3, '.SH')  

    #若为港交所证券代码，进行预防性修正，截取数字代码后4位，加上后缀共7位
    if suffix3 in ['.HK']:
        ticker1=ticker1[-7:]     

    #若为东交所证券代码，进行预防性修正，截取数字代码后4位，加上后缀共6位
    if suffix2 in ['.T']:
        ticker1=ticker1[-6:]  
    
    #返回：是否大陆证券，基于数据源/交易所格式修正后的证券代码
    return prc, ticker1        

#测试各种情形
if __name__=='__main__':
    prc, ticker=ticker_check("600519.sh","yahoo")
    print(prc,ticker)
    print(ticker_check("600519.SH","yahoo"))    
    print(ticker_check("600519.ss","yahoo"))    
    print(ticker_check("600519.SH","tushare"))    
    print(ticker_check("600519.ss","tushare"))    
    print(ticker_check("000002.sz","tushare"))
    print(ticker_check("000002.sz","yahoo"))
    print(ticker_check("00700.Hk","yahoo"))
    print(ticker_check("99830.t","yahoo"))

#==============================================================================
def get_price(ticker, fromdate, todate):
    """
    功能：从雅虎财经抓取单个证券价格或指数价格，不能处理多个证券列表。
    输入：证券代码，开始日期，结束日期。
    ticker: 证券代码。
    大陆股票代码加上后缀.SZ或.SS，港股代码去掉前导0加后缀.HK。
    fromdate: 样本开始日期。
    todate: 样本结束日期。既可以是今天日期，也可以是一个历史日期。    
    输出：证券价格序列，按照日期升序排列。原汁原味的抓取数据。
    """

    #仅支持单个证券代码
    if not isinstance(ticker,str):
        print("*** 错误#1(get_price)，仅支持单个证券代码!")        
        return None  
    
    #校验证券代码
    _,ticker=ticker_check(ticker, source="yahoo")

    #检查期间合理性
    result,start,end=check_period(fromdate,todate)
    if result is None:
        print("*** 错误#2(get_price)，无效的日期或期间!")        
        return None         
    
    #使用pandas_datareader抓取雅虎证券价格
    try:
        from pandas_datareader import data
    except:
        print("*** 错误#3：需要先安装插件pandas-datareader，然后重新运行！")
        print("安装方法：")
        print("打开Anaconda prompt，执行命令：pip install pandas-datareader")
        return None    
    
    try:
        price=data.DataReader(ticker,'yahoo',start,end)
    except:
        print("*** 错误#4(get_price)，抓取证券价格失败!")        
        print("信息:",ticker,fromdate,todate) 
        print("可能的原因:")
        print("  1)网络连接不稳定.")
        print("  2)证券代码无效.")
        print("  3)所选证券期间内暂停交易或退市.")
        return None            
    
    #抓取未失败但返回空数据
    if len(price)==0:
        print("*** 错误#5(get_price)，未能抓取到有效价格信息!")
        return None         
    
    """
    #去掉比起始日期更早的样本
    price2=price[price.index >= fromdate]
    #去掉比结束日期更晚的样本
    price2=price2[price2.index <= todate]
    
    #按日期升序排序，近期的价格排在后面
    sortedprice=price2.sort_index(axis=0,ascending=True)
    """
    
    #生成字符串型的日期字段date，方便以后使用
    price['datetmp']=price.index
    price['date']=price['datetmp'].apply(lambda x:x.date())
    del price['datetmp']

    #加入星期几
    price["Weekday"]=price.index.weekday + 1  
    
    #加入证券代码，便于后期处理
    price['ticker']=ticker

    return price

if __name__ =="__main__":
    df=get_price('000002.SZ','2020-2-1','2020-3-31')
    df=get_price('^GSPC','2020-1-1','2020-3-4')
    print(df['Close'].tail(10))
    price=get_price(['000001.SS','^HSI'],'2020-1-1','2020-2-4')
    apclose=price['Close']['^HSI']
    print(price['Close']['^HSI'].tail(10))

#==============================================================================
def ectranslate(eword):
    """
    翻译英文专业词汇至中文，便于显示或绘图时输出中文而不是英文。
    输入：英文专业词汇。输出：中文专业词汇
    """
    import pandas as pd
    ecdict=pd.DataFrame([
        ['Gross Domestic Product','国内生产总值'],['GNI','国民生产总值'],
        
        ], columns=['eword','cword'])

    try:
        cword=ecdict[ecdict['eword']==eword]['cword'].values[0]
    except:
        #未查到翻译词汇，返回原词
        cword=eword
   
    return cword

if __name__=='__main__':
    eword='Exp Adj Ret'
    print(ectranslate('Annual Adj Ret%'))
    print(ectranslate('Annual*Adj Ret%'))


#==============================================================================
def codetranslate(code):
    """
    翻译证券代码为证券名称。
    输入：证券代码。输出：证券名称
    """
    import pandas as pd
    codedict=pd.DataFrame([
        ['000001.SS','上证综合指数'],['399001.SZ','深证成分指数'],
        ['^GSPC','标普500指数'],['^DJI','道琼斯工业指数'],
        ['WISGP.SI','富时新加坡指数'], ['^STI','新加坡海峡时报指数'],
        ['^IXIC','纳斯达克综合指数'],
        ['FVTT.FGI','富时越南指数'],['^RUT','罗素2000指数'],
        ['^HSI','恒生指数'],['^N225','日经225指数'],
        ['WIKOR.FGI','富时韩国指数'],['^KS11','韩国综合指数'],
        ['^KOSPI','韩国综合指数'],['^BSESN','印度孟买敏感指数'],
        ['^FCHI','法国CAC40指数'],['^GDAXI','德国DAX指数'],
        
        ], columns=['code','codename'])

    try:
        codename=codedict[codedict['code']==code]['codename'].values[0]
    except:
        #未查到翻译词汇，返回原词
        codename=code
   
    return codename

if __name__=='__main__':
    code='GOOG'
    print(codetranslate('000002.SZ'))
    print(codetranslate('9988.HK'))

#==============================================================================
#==============================================================================
def fred_factor_codes():
   import pandas as pd
   s=pd.DataFrame([
        # GDP未扣除通胀和汇率变化因素
        ['China','GDP','Annual','Gross Domestic Product','MKTGDPCNA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['USA','GDP','Annual','Gross Domestic Product','MKTGDPUSA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Japan','GDP','Annual','Gross Domestic Product','MKTGDPJPA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['India','GDP','Annual','Gross Domestic Product','MKTGDPINA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Korea','GDP','Annual','Gross Domestic Product','MKTGDPKRA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Russia','GDP','Annual','Gross Domestic Product','MKTGDPRUA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Singapore','GDP','Annual','Gross Domestic Product','MKTGDPSGA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Malaysia','GDP','Annual','Gross Domestic Product','MKTGDPMYA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Indonesia','GDP','Annual','Gross Domestic Product','MKTGDPIDA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Vietnam','GDP','Annual','Gross Domestic Product','MKTGDPVNA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Thailand','GDP','Annual','Gross Domestic Product','MKTGDPTHA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Australia','GDP','Annual','Gross Domestic Product','MKTGDPAUA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['France','GDP','Annual','Gross Domestic Product','MKTGDPFRA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Germany','GDP','Annual','Gross Domestic Product','MKTGDPDEA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['UK','GDP','Annual','Gross Domestic Product','MKTGDPGBA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Israel','GDP','Annual','Gross Domestic Product','MKTGDPILA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Italy','GDP','Annual','Gross Domestic Product','MKTGDPITA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Cambodia','GDP','Annual','Gross Domestic Product','MKTGDPKHA646NWDB','Current USD, Not Seasonally Adjusted'],
        
        #真实GDP，不变价格，年度，2011美元计价
        ['India','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNAINA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['China','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNACNA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['Japan','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNAJPA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['Korea','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNAKRA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['Thailand','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNATHA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['Vietnam','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNAVNA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['Cambodia','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNAKHA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['Hong Kong','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNAHKA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['Singapore','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNASGA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['Malaysia','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNAMYA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['Indonesia','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNAIDA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['USA','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNAUSA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['UK','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNAGBA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['France','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNAFRA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['Germany','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNADEA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['Italy','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNAITA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['Israel','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNAILA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['Russia','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNARUA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        ['Australia','CNP GDP','Annual','Real GDP at Constant National Prices','RGDPNAAUA666NRUG','2011 USD Millions, Not Seasonally Adjusted'],
        
        # 真实GDP：扣除通胀和与美元汇率变化因素，本地货币，季度
        # Real GDP is an inflation-adjusted measure, also as "constant price"/"inflation-cirrected"/"constant dollar"
        ['China','Constant GDP','Quarterly','Current Price Gross Domestic Product','CHNGDPNQDSMEI','Local Currency, Seasonally Adjusted'],
        ['Japan','Constant GDP','Quarterly','Current Price Gross Domestic Product','JPNGDPNQDSMEI','Local Currency, Seasonally Adjusted'],
        ['USA','Constant GDP','Quarterly','Current Price Gross Domestic Product','USAGDPNQDSMEI','Local Currency, Seasonally Adjusted'],
        ['Korea','Constant GDP','Quarterly','Current Price Gross Domestic Product','KORGDPNQDSMEI','Local Currency, Seasonally Adjusted'],
        ['Russia','Constant GDP','Quarterly','Current Price Gross Domestic Product','RUSGDPNQDSMEI','Local Currency, Seasonally Adjusted'],
        ['India','Constant GDP','Quarterly','Current Price Gross Domestic Product','INDGDPNQDSMEI','Local Currency, Seasonally Adjusted'],
        ['France','Constant GDP','Quarterly','Current Price Gross Domestic Product','FRAGDPNQDSMEI','Local Currency, Seasonally Adjusted'],
        ['Germany','Constant GDP','Quarterly','Current Price Gross Domestic Product','DEUGDPNQDSMEI','Local Currency, Seasonally Adjusted'],
        ['UK','Constant GDP','Quarterly','Current Price Gross Domestic Product','GBRGDPNQDSMEI','Local Currency, Seasonally Adjusted'],
        ['Australia','Constant GDP','Quarterly','Current Price Gross Domestic Product','AUSGDPNQDSMEI','Local Currency, Seasonally Adjusted'],
        
        # Rario of GNP to GDP
        ['China','GNP','Annual','Ratio of GNP to GDP','GNPGDPCNA156NUPN','Percent, Not Seasonally Adjusted'],
        ['USA','GNP','Annual','Ratio of GNP to GDP','GNPGDPUSA156NUPN','Percent, Not Seasonally Adjusted'],
        ['Japan','GNP','Annual','Ratio of GNP to GDP','GNPGDPJPA156NUPN','Percent, Not Seasonally Adjusted'],
        
        # 人均GDP：未扣除通胀因素
        ['China','GDP Per Capita','Annual','Gross Domestic Product Per Capita','PCAGDPCNA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Japan','GDP Per Capita','Annual','Gross Domestic Product Per Capita','PCAGDPJPA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['USA','GDP Per Capita','Annual','Gross Domestic Product Per Capita','PCAGDPUSA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Korea','GDP Per Capita','Annual','Gross Domestic Product Per Capita','PCAGDPKRA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['India','GDP Per Capita','Annual','Gross Domestic Product Per Capita','PCAGDPINA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Singapore','GDP Per Capita','Annual','Gross Domestic Product Per Capita','PCAGDPSGA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Malaysia','GDP Per Capita','Annual','Gross Domestic Product Per Capita','PCAGDPMYA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Indonesia','GDP Per Capita','Annual','Gross Domestic Product Per Capita','PCAGDPIDA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Vietnam','GDP Per Capita','Annual','Gross Domestic Product Per Capita','PCAGDPVNA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Thailand','GDP Per Capita','Annual','Gross Domestic Product Per Capita','PCAGDPTHA646NWDB','Current USD, Not Seasonally Adjusted'],
        ['Cambodia','GDP Per Capita','Annual','Gross Domestic Product Per Capita','PCAGDPKHA646NWDB','Current USD, Not Seasonally Adjusted'],
        
        # 不变价格人均GDP：扣除通胀和汇率因素
        ['China','Constant GDP Per Capita','Annual','Constant Price GDP Per Capita','NYGDPPCAPKDCHN','2010 USD, Not Seasonally Adjusted'],
        ['USA','Constant GDP Per Capita','Annual','Constant Price GDP Per Capita','NYGDPPCAPKDUSA','2010 USD, Not Seasonally Adjusted'],
        ['Japan','Constant GDP Per Capita','Annual','Constant Price GDP Per Capita','NYGDPPCAPKDJPN','2010 USD, Not Seasonally Adjusted'],
        ['Russia','Constant GDP Per Capita','Annual','Constant Price GDP Per Capita','NYGDPPCAPKDRUS','2010 USD, Not Seasonally Adjusted'],
        ['France','Constant GDP Per Capita','Annual','Constant Price GDP Per Capita','NYGDPPCAPKDFRA','2010 USD, Not Seasonally Adjusted'],
        ['Germany','Constant GDP Per Capita','Annual','Constant Price GDP Per Capita','NYGDPPCAPKDDEU','2010 USD, Not Seasonally Adjusted'],
        ['Italy','Constant GDP Per Capita','Annual','Constant Price GDP Per Capita','NYGDPPCAPKDITA','2010 USD, Not Seasonally Adjusted'],
        ['Singapore','Constant GDP Per Capita','Annual','Constant Price GDP Per Capita','NYGDPPCAPKDSGP','2010 USD, Not Seasonally Adjusted'],
        ['Malaysia','Constant GDP Per Capita','Annual','Constant Price GDP Per Capita','NYGDPPCAPKDMYS','2010 USD, Not Seasonally Adjusted'],
        ['Indonesia','Constant GDP Per Capita','Annual','Constant Price GDP Per Capita','NYGDPPCAPKDIDN','2010 USD, Not Seasonally Adjusted'],
        ['India','Constant GDP Per Capita','Annual','Constant Price GDP Per Capita','NYGDPPCAPKDIND','2010 USD, Not Seasonally Adjusted'],
        
        # CPI
        ['China','CPI','Monthly','Consumer Price Index: All Items','CHNCPIALLMINMEI','Index 2015=100, Not Seasonally Adjusted'],
        ['USA','CPI','Monthly','Consumer Price Index: All Items','USACPIALLMINMEI','Index 2015=100, Not Seasonally Adjusted'],
        ['Japan','CPI','Monthly','Consumer Price Index: All Items','JPNCPIALLMINMEI','Index 2015=100, Not Seasonally Adjusted'],
        ['Korea','CPI','Monthly','Consumer Price Index: All Items','KORCPIALLMINMEI','Index 2015=100, Not Seasonally Adjusted'],
        ['India','CPI','Monthly','Consumer Price Index: All Items','INDCPIALLMINMEI','Index 2015=100, Not Seasonally Adjusted'],
        ['France','CPI','Monthly','Consumer Price Index: All Items','FRACPIALLMINMEI','Index 2015=100, Not Seasonally Adjusted'],
        ['Germany','CPI','Monthly','Consumer Price Index: All Items','DEUCPIALLMINMEI','Index 2015=100, Not Seasonally Adjusted'],
        ['Australia','CPI','Monthly','Consumer Price Index: All Items','AUSCPIALLMINMEI','Index 2015=100, Not Seasonally Adjusted'],
        ['UK','CPI','Monthly','Consumer Price Index: All Items','GBRCPIALLMINMEI','Index 2015=100, Not Seasonally Adjusted'],
        ['Italy','CPI','Monthly','Consumer Price Index: All Items','ITACPIALLMINMEI','Index 2015=100, Not Seasonally Adjusted'],
        ['Spain','CPI','Monthly','Consumer Price Index: All Items','ESPCPIALLMINMEI','Index 2015=100, Not Seasonally Adjusted'],
        ['Russia','CPI','Monthly','Consumer Price Index: All Items','RUSCPIALLMINMEI','Index 2015=100, Not Seasonally Adjusted'],
        ['Indonesia','CPI','Monthly','Consumer Price Index: All Items','IDNCPIALLMINMEI','Index 2015=100, Not Seasonally Adjusted'],
        ['Israel','CPI','Monthly','Consumer Price Index: All Items','ISRCPIALLMINMEI','Index 2015=100, Not Seasonally Adjusted'],

        # PPI
        ['Sweden','PPI','Monthly','Producer Prices Index: Total Industrial Activities','PIEATI01SEM661N','Index 2015=100, Not Seasonally Adjusted'],
        ['Spain','PPI','Monthly','Producer Prices Index: Total Industrial Activities','PIEATI01ESM661N','Index 2015=100, Not Seasonally Adjusted'],
        ['UK','PPI','Monthly','Producer Prices Index: Total Industrial Activities','PIEATI01GBM661N','Index 2015=100, Not Seasonally Adjusted'],
        ['Italy','PPI','Monthly','Producer Prices Index: Total Industrial Activities','PIEATI01ITM661N','Index 2015=100, Not Seasonally Adjusted'],
        ['Euro Area','PPI','Monthly','Producer Prices Index: Total Industrial Activities','PIEATI01EZM661N','Index 2015=100, Not Seasonally Adjusted'],
        ['Switzerland','PPI','Monthly','Producer Prices Index: Total Industrial Activities','PIEATI01CHM661N','Index 2015=100, Not Seasonally Adjusted'],
        ['France','PPI','Monthly','Producer Prices Index: Total Industrial Activities','PIEATI01FRM661N','Index 2015=100, Not Seasonally Adjusted'],
        ['Germany','PPI','Monthly','Producer Prices Index: Total Industrial Activities','PIEATI01DEM661N','Index 2015=100, Not Seasonally Adjusted'],
        ['USA','PPI','Monthly','Producer Prices Index: Total Industrial Activities','PIEAMP01USM661N','Index 2015=100, Not Seasonally Adjusted'],
        ['Mexico','PPI','Monthly','Producer Prices Index: Total Industrial Activities','PIEATI02MXM661N','Index 2015=100, Not Seasonally Adjusted'],
        ['Japan','PPI','Monthly','Producer Prices Index: Total Industrial Activities','PIEATI02JPM661N','Index 2015=100, Not Seasonally Adjusted'],
        ['Korea','PPI','Monthly','Producer Prices Index: Total Industrial Activities','PIEATI02KRM661N','Index 2015=100, Not Seasonally Adjusted'],
        ['Russia','PPI','Monthly','Producer Prices Index: Total Industrial Activities','PIEATI02RUM661N','Index 2015=100, Not Seasonally Adjusted'],
        ['Canada','PPI','Monthly','Producer Prices Index: Total Industrial Activities','PIEAMP01CAM661N','Index 2015=100, Not Seasonally Adjusted'],
        
        # PPI China, up to 2015 & Annualonly
        ['China','PPI','Annual','Producer Prices Index: Total Industrial Activities','PIEATI01CNA661N','Index 2015=100, Not Seasonally Adjusted'],

        # CPI%, Growth Rate over Previous Period
        ['USA','YoY CPI','Monthly','Consumer Price Index: All Items Growth Rate','CPALTT01USM657N','Growth Rate Previous Period, Not Seasonally Adjusted'],
        ['China','YoY CPI','Monthly','Consumer Price Index: All Items Growth Rate','CPALTT01CNM657N','Growth Rate Previous Period, Not Seasonally Adjusted'],
        ['Japan','YoY CPI','Monthly','Consumer Price Index: All Items Growth Rate','CPALTT01USM657N','Growth Rate Previous Period, Not Seasonally Adjusted'],
        ['Korea','YoY CPI','Monthly','Consumer Price Index: All Items Growth Rate','CPALTT01KRM657N','Growth Rate Previous Period, Not Seasonally Adjusted'],
        ['Russia','YoY CPI','Monthly','Consumer Price Index: All Items Growth Rate','CPALTT01RUM657N','Growth Rate Previous Period, Not Seasonally Adjusted'],
        ['India','YoY CPI','Monthly','Consumer Price Index: All Items Growth Rate','CPALTT01INM657N','Growth Rate Previous Period, Not Seasonally Adjusted'],
        ['France','YoY CPI','Monthly','Consumer Price Index: All Items Growth Rate','CPALTT01FRM657N','Growth Rate Previous Period, Not Seasonally Adjusted'],
        ['Germany','YoY CPI','Monthly','Consumer Price Index: All Items Growth Rate','CPALTT01DEM657N','Growth Rate Previous Period, Not Seasonally Adjusted'],
        ['Canada','YoY CPI','Monthly','Consumer Price Index: All Items Growth Rate','CPALTT01CAM657N','Growth Rate Previous Period, Not Seasonally Adjusted'],
        ['UK','YoY CPI','Monthly','Consumer Price Index: All Items Growth Rate','CPALTT01GBM657N','Growth Rate Previous Period, Not Seasonally Adjusted'],

        # PPI%, Growth Rate same period previous year
        ['China','YoY PPI','Monthly','Producer Prices Index: Industrial Activities','CHNPIEATI01GYM','Growth rate same period previous year, Not Seasonally Adjusted'],
        ['UK','YoY PPI','Monthly','Producer Prices Index: Industrial Activities','GBRPIEATI01GYM','Growth rate same period previous year, Not Seasonally Adjusted'],
        ['France','YoY PPI','Monthly','Producer Prices Index: Industrial Activities','FRAPIEATI01GYM','Growth rate same period previous year, Not Seasonally Adjusted'],
        ['Germany','YoY PPI','Monthly','Producer Prices Index: Industrial Activities','DEUPIEATI01GYM','Growth rate same period previous year, Not Seasonally Adjusted'],
        ['Japan','YoY PPI','Monthly','Producer Prices Index: Industrial Activities','JPNPIEATI02GYM','Growth rate same period previous year, Not Seasonally Adjusted'],
        ['Korea','YoY PPI','Monthly','Producer Prices Index: Industrial Activities','KORPIEATI02GYM','Growth rate same period previous year, Not Seasonally Adjusted'],
        ['Italy','YoY PPI','Monthly','Producer Prices Index: Industrial Activities','ITAPIEATI01GYM','Growth rate same period previous year, Not Seasonally Adjusted'],
        ['Spain','YoY PPI','Monthly','Producer Prices Index: Industrial Activities','ITAPIEATI01GYM','Growth rate same period previous year, Not Seasonally Adjusted'],
        ['Poland','YoY PPI','Monthly','Producer Prices Index: Industrial Activities','POLPIEATI01GYM','Growth rate same period previous year, Not Seasonally Adjusted'],
        ['USA','YoY PPI','Monthly','Producer Prices Index: Industrial Activities','PIEAMP02USM659N','Growth rate same period previous year, Not Seasonally Adjusted'],
        
        # Interest rate, Discount rate，中央银行的再贴现率，央行给予商业银行的短期贷款利率
        ['China','Discount Rate','Monthly','Central Bank Discount Rate','INTDSRCNM193N','Percent per Annum, Not Seasonally Adjusted'],
        ['USA','Discount Rate','Monthly','Central Bank Discount Rate','INTDSRUSM193N','Percent per Annum, Not Seasonally Adjusted'],
        ['India','Discount Rate','Monthly','Central Bank Discount Rate','INTDSRINM193N','Percent per Annum, Not Seasonally Adjusted'],
        ['Japan','Discount Rate','Monthly','Central Bank Discount Rate','INTDSRJPM193N','Percent per Annum, Not Seasonally Adjusted'],
        ['Korea','Discount Rate','Monthly','Central Bank Discount Rate','INTDSRKRM193N','Percent per Annum, Not Seasonally Adjusted'],
        ['Brazil','Discount Rate','Monthly','Central Bank Discount Rate','INTDSRBRM193N','Percent per Annum, Not Seasonally Adjusted'],
        
        # Immediate Interest rate, less than 25 hours, interbank rate
        ['China','Immediate Rate','Monthly','Immediate Rates: Less than 24 Hours: Interbank Rate','IRSTCI01CNM156N','Percent per Annum, Not Seasonally Adjusted'],
        ['USA','Immediate Rate','Monthly','Immediate Rates: Less than 24 Hours: Interbank Rate','IRSTCI01USM156N','Percent per Annum, Not Seasonally Adjusted'],
        ['Japan','Immediate Rate','Monthly','Immediate Rates: Less than 24 Hours: Interbank Rate','IRSTCI01JPM156N','Percent per Annum, Not Seasonally Adjusted'],
        ['Korea','Immediate Rate','Monthly','Immediate Rates: Less than 24 Hours: Interbank Rate','IRSTCI01KRM156N','Percent per Annum, Not Seasonally Adjusted'],
        ['India','Immediate Rate','Monthly','Immediate Rates: Less than 24 Hours: Interbank Rate','IRSTCI01INM156N','Percent per Annum, Not Seasonally Adjusted'],
        ['France','Immediate Rate','Monthly','Immediate Rates: Less than 24 Hours: Interbank Rate','IRSTCI01FRM156N','Percent per Annum, Not Seasonally Adjusted'],
        ['Germany','Immediate Rate','Monthly','Immediate Rates: Less than 24 Hours: Interbank Rate','IRSTCI01DEM156N','Percent per Annum, Not Seasonally Adjusted'],
        ['Australia','Immediate Rate','Monthly','Immediate Rates: Less than 24 Hours: Interbank Rate','IRSTCI01AUM156N','Percent per Annum, Not Seasonally Adjusted'],
        ['Indonesia','Immediate Rate','Monthly','Immediate Rates: Less than 24 Hours: Interbank Rate','IRSTCI01IDM156N','Percent per Annum, Not Seasonally Adjusted'],
        ['Russia','Immediate Rate','Monthly','Immediate Rates: Less than 24 Hours: Interbank Rate','IRSTCI01RUM156N','Percent per Annum, Not Seasonally Adjusted'],

        ['LIBOR','Immediate Rate','Daily','Overnight London Interbank Offered Rate, based on USD','USDONTD156N','Percent per Annum, Not Seasonally Adjusted'],
        ['UK','LIBOR','Daily','Overnight London Interbank Offered Rate, based on USD','USDONTD156N','Percent per Annum, Not Seasonally Adjusted'],
        
        # Foreign exchange rate, to USD
        ['China','Exchange Rate','Daily','Local Currency/USD Foreign Exchange Rate','DEXCHUS','Chinese Yuan/1 US$, Not Seasonally Adjusted'],
        ['Japan','Exchange Rate','Daily','Local Currency/USD Foreign Exchange Rate','DEXJPUS','Japanese Yen/1 US$, Not Seasonally Adjusted'],
        ['Korea','Exchange Rate','Daily','Local Currency/USD Foreign Exchange Rate','DEXKOUS','South Korea Won/1 US$, Not Seasonally Adjusted'],
        ['Singapore','Exchange Rate','Daily','Local Currency/USD Foreign Exchange Rate','DEXSIUS','Singapore Dollars/1 US$, Not Seasonally Adjusted'],
        ['China Hong Kong','Exchange Rate','Daily','Local Currency/USD Foreign Exchange Rate','DEXHKUS','HK Dollars/1 US$, Not Seasonally Adjusted'],
        ['Australia','Exchange Rate','Daily','USD/Local Currency Foreign Exchange Rate','DEXUSAL','US Dollars/1 Australian Dollar, Not Seasonally Adjusted'],
        ['Euro','Exchange Rate','Daily','USD/Local Currency Foreign Exchange Rate','DEXUSEU','US Dollars/1 Euro, Not Seasonally Adjusted'],
        ['India','Exchange Rate','Daily','Local Currency/USD Foreign Exchange Rate','DEXINUS','Indian Rupees/1 US$, Not Seasonally Adjusted'],
        ['UK','Exchange Rate','Daily','USD/Local Currency Foreign Exchange Rate','DEXUSUK','US Dollars/1 British Pound, Not Seasonally Adjusted'],
        ['Canada','Exchange Rate','Daily','Local Currency/USD Foreign Exchange Rate','DEXCAUS','Canadian Dollars/1 US$, Not Seasonally Adjusted'],
        ['Mexico','Exchange Rate','Daily','Local Currency/USD Foreign Exchange Rate','DEXMXUS','Mexican New Pesos/1 US$, Not Seasonally Adjusted'],
        ['Brazil','Exchange Rate','Daily','Local Currency/USD Foreign Exchange Rate','DEXBZUS','Brazilian Reals/1 US$, Not Seasonally Adjusted'],
        ['Venezuela','Exchange Rate','Daily','Local Currency/USD Foreign Exchange Rate','DEXVZUS','Venezuelan Bolivares/1 US$, Not Seasonally Adjusted'],
        ['South Africa','Exchange Rate','Daily','Local Currency/USD Foreign Exchange Rate','DEXSFUS','South African Rand/1 US$, Not Seasonally Adjusted'],
        ['Sweden','Exchange Rate','Daily','Local Currency/USD Foreign Exchange Rate','DEXSDUS','Swedish Kronor/1 US$, Not Seasonally Adjusted'],
        ['Thailand','Exchange Rate','Daily','Local Currency/USD Foreign Exchange Rate','DEXTHUS','Thai Baht/1 US$, Not Seasonally Adjusted'],
        ['New Zealand','Exchange Rate','Daily','USD/Local Currency Foreign Exchange Rate','DEXUSNZ','US Dollars/1 New Zealand Dollar, Not Seasonally Adjusted'],
        ['China Taiwan','Exchange Rate','Daily','Local Currency/USD Foreign Exchange Rate','DEXTAUS','New Taiwan Dollars/1 US$, Not Seasonally Adjusted'],
        ['Malaysia','Exchange Rate','Daily','Local Currency/USD Foreign Exchange Rate','DEXMAUS','Malaysian Ringgit/1 US$, Not Seasonally Adjusted'],
        ['Denmark','Exchange Rate','Daily','Local Currency/USD Foreign Exchange Rate','DEXDNUS','Danish Kroner/1 US$, Not Seasonally Adjusted'],
        
        # M0，本地货币，月度
        ['China','M0','Monthly','National Monetary Policy M0','MYAGM0CNM189N','National Currency, Seasonally Adjusted'],
        
        # M1，本地货币，月度
        ['China','M1','Monthly','National Monetary Policy M1','MANMM101CNM189S','National Currency, Seasonally Adjusted'],
        ['USA','M1','Monthly','National Monetary Policy M1','MANMM101USM189S','National Currency, Seasonally Adjusted'],
        ['Japan','M1','Monthly','National Monetary Policy M1','MANMM101JPM189S','National Currency, Seasonally Adjusted'],
        ['Euro Area','M1','Monthly','Euro Area Monetary Policy M1','MANMM101EZM189S','National Currency, Seasonally Adjusted'],
        ['Korea','M1','Monthly','National Monetary Policy M1','MANMM101KRM189S','National Currency, Seasonally Adjusted'],
        ['India','M1','Monthly','National Monetary Policy M1','MANMM101INM189S','National Currency, Seasonally Adjusted'],
        
        # M2，本地货币，月度
        ['China','M2','Monthly','National Monetary Policy M2','MYAGM2CNM189N','National Currency, Not Seasonally Adjusted'],
        ['Japan','M2','Monthly','National Monetary Policy M2','MYAGM2JPM189N','National Currency, Seasonally Adjusted'],
        ['Korea','M2','Monthly','National Monetary Policy M2','MYAGM2KRM189N','National Currency, Not Seasonally Adjusted'],
        ['France','M2','Monthly','National Monetary Policy M2','MYAGM2FRM189N','National Currency, Not Seasonally Adjusted'],
        ['Italy','M2','Monthly','National Monetary Policy M2','MYAGM2ITM189N','National Currency, Not Seasonally Adjusted'],
        ['Russia','M2','Monthly','National Monetary Policy M2','MYAGM2RUM189N','National Currency, Not Seasonally Adjusted'],
        ['Indonesia','M2','Monthly','National Monetary Policy M2','MYAGM2IDM189N','National Currency, Not Seasonally Adjusted'],
        ['Brazil','M2','Monthly','National Monetary Policy M2','MYAGM2BRM189N','National Currency, Not Seasonally Adjusted'],
        ['USA','M2','Monthly','National Monetary Policy M2','M2NS','Billions of Dollars, Not Seasonally Adjusted'],

        # M3，本地货币，月度
        ['China','M3','Monthly','National Monetary Policy M3','MABMM301CNM189S','National Currency, Seasonally Adjusted'],
        ['USA','M3','Monthly','National Monetary Policy M3','MABMM301USM189S','National Currency, Seasonally Adjusted'],
        ['Japan','M3','Monthly','National Monetary Policy M3','MABMM301JPM189S','National Currency, Seasonally Adjusted'],
        ['UK','M3','Monthly','National Monetary Policy M3','MABMM301GBM189S','National Currency, Seasonally Adjusted'],
        ['Euro Area','M3','Monthly','Euro Area Monetary Policy M3','MABMM301EZM189S','National Currency, Seasonally Adjusted'],
        ['Australia','M3','Monthly','National Monetary Policy M3','MABMM301AUM189S','National Currency, Seasonally Adjusted'],

        # Stock Market Cap to GDP
        ['China','SMC to GDP','Annual','Stock Market Capitalization to GDP','DDDM01CNA156NWDB','Percent, Not Seasonally Adjusted'],
        ['USA','SMC to GDP','Annual','Stock Market Capitalization to GDP','DDDM01USA156NWDB','Percent, Not Seasonally Adjusted'],
        ['Japan','SMC to GDP','Annual','Stock Market Capitalization to GDP','DDDM01JPA156NWDB','Percent, Not Seasonally Adjusted'],
        ['Korea','SMC to GDP','Annual','Stock Market Capitalization to GDP','DDDM01KRA156NWDB','Percent, Not Seasonally Adjusted'],
        ['India','SMC to GDP','Annual','Stock Market Capitalization to GDP','DDDM01INA156NWDB','Percent, Not Seasonally Adjusted'],
        ['Singapore','SMC to GDP','Annual','Stock Market Capitalization to GDP','DDDM01SGA156NWDB','Percent, Not Seasonally Adjusted'],
        ['Malaysia','SMC to GDP','Annual','Stock Market Capitalization to GDP','DDDM01MYA156NWDB','Percent, Not Seasonally Adjusted'],
        ['Indonesia','SMC to GDP','Annual','Stock Market Capitalization to GDP','DDDM01IDA156NWDB','Percent, Not Seasonally Adjusted'],
        ['Vietnam','SMC to GDP','Annual','Stock Market Capitalization to GDP','DDDM01VNA156NWDB','Percent, Not Seasonally Adjusted'],
        ['China Hong Kong','SMC to GDP','Annual','Stock Market Capitalization to GDP','DDDM01HKA156NWDB','Percent, Not Seasonally Adjusted'],
        ['France','SMC to GDP','Annual','Stock Market Capitalization to GDP','DDDM01FRA156NWDB','Percent, Not Seasonally Adjusted'],
        ['Germany','SMC to GDP','Annual','Stock Market Capitalization to GDP','DDDM01DEA156NWDB','Percent, Not Seasonally Adjusted'],
        ['UK','SMC to GDP','Annual','Stock Market Capitalization to GDP','DDDM01GBA156NWDB','Percent, Not Seasonally Adjusted'],
        ['Italy','SMC to GDP','Annual','Stock Market Capitalization to GDP','DDDM01ITA156NWDB','Percent, Not Seasonally Adjusted'],
        ['Spain','SMC to GDP','Annual','Stock Market Capitalization to GDP','DDDM01ESA156NWDB','Percent, Not Seasonally Adjusted'],
        ['Israel','SMC to GDP','Annual','Stock Market Capitalization to GDP','DDDM01ILA156NWDB','Percent, Not Seasonally Adjusted'],
        ['Canada','SMC to GDP','Annual','Stock Market Capitalization to GDP','DDDM01CAA156NWDB','Percent, Not Seasonally Adjusted'],

        # 消费者信心综合指数：OECD
        ['China','Consumer Confidence','Monthly','Consumer Confidence Composite Indicator by OECD','CSCICP03CNM665S','Normalised (Normal=100), Seasonally Adjusted'],
        ['USA','Consumer Confidence','Monthly','Consumer Confidence Composite Indicator by OECD','CSCICP03USM665S','Normalised (Normal=100), Seasonally Adjusted'],
        ['Japan','Consumer Confidence','Monthly','Consumer Confidence Composite Indicator by OECD','CSCICP03JPM665S','Normalised (Normal=100), Seasonally Adjusted'],
        ['Korea','Consumer Confidence','Monthly','Consumer Confidence Composite Indicator by OECD','CSCICP03KRM665S','Normalised (Normal=100), Seasonally Adjusted'],
        ['Indonesia','Consumer Confidence','Monthly','Consumer Confidence Composite Indicator by OECD','CSCICP03IDM665S','Normalised (Normal=100), Seasonally Adjusted'],
        ['France','Consumer Confidence','Monthly','Consumer Confidence Composite Indicator by OECD','CSCICP03FRM665S','Normalised (Normal=100), Seasonally Adjusted'],
        ['Germany','Consumer Confidence','Monthly','Consumer Confidence Composite Indicator by OECD','CSCICP03DEM665S','Normalised (Normal=100), Seasonally Adjusted'],
        ['Italy','Consumer Confidence','Monthly','Consumer Confidence Composite Indicator by OECD','CSCICP03ITM665S','Normalised (Normal=100), Seasonally Adjusted'],
        ['Spain','Consumer Confidence','Monthly','Consumer Confidence Composite Indicator by OECD','CSCICP03ESM665S','Normalised (Normal=100), Seasonally Adjusted'],

        # 粗出生率；又称为出生率。指1年内平均每千人中出生人数的比率。它反映一定时期内人口的出生水平。
        ['China','Birth Rate','Annual','Crude Birth Rate','SPDYNCBRTINCHN','Births per 1,000 People, Not Seasonally Adjusted'],
        ['USA','Birth Rate','Annual','Crude Birth Rate','SPDYNCBRTINUSA','Births per 1,000 People, Not Seasonally Adjusted'],
        ['Japan','Birth Rate','Annual','Crude Birth Rate','SPDYNCBRTINJPN','Births per 1,000 People, Not Seasonally Adjusted'],
        ['Korea','Birth Rate','Annual','Crude Birth Rate','SPDYNCBRTINKOR','Births per 1,000 People, Not Seasonally Adjusted'],
        ['France','Birth Rate','Annual','Crude Birth Rate','SPDYNCBRTINFRA','Births per 1,000 People, Not Seasonally Adjusted'],
        ['Germany','Birth Rate','Annual','Crude Birth Rate','SPDYNCBRTINDEU','Births per 1,000 People, Not Seasonally Adjusted'],
        ['India','Birth Rate','Annual','Crude Birth Rate','SPDYNCBRTININD','Births per 1,000 People, Not Seasonally Adjusted'],
        ['Indonesia','Birth Rate','Annual','Crude Birth Rate','SPDYNCBRTINIDN','Births per 1,000 People, Not Seasonally Adjusted'],
        ['Singapore','Birth Rate','Annual','Crude Birth Rate','SPDYNCBRTINSGP','Births per 1,000 People, Not Seasonally Adjusted'],
        ['Vietnam','Birth Rate','Annual','Crude Birth Rate','SPDYNCBRTINVNM','Births per 1,000 People, Not Seasonally Adjusted'],
        ['Pakistan','Birth Rate','Annual','Crude Birth Rate','SPDYNCBRTINPAK','Births per 1,000 People, Not Seasonally Adjusted'],
        ['Cambodia','Birth Rate','Annual','Crude Birth Rate','SPDYNCBRTINKHM','Births per 1,000 People, Not Seasonally Adjusted'],
        ['Malaysia','Birth Rate','Annual','Crude Birth Rate','SPDYNCBRTINMYS','Births per 1,000 People, Not Seasonally Adjusted'],
        ['Australia','Birth Rate','Annual','Crude Birth Rate','SPDYNCBRTINAUS','Births per 1,000 People, Not Seasonally Adjusted'],
        ['Italy','Birth Rate','Annual','Crude Birth Rate','SPDYNCBRTINITA','Births per 1,000 People, Not Seasonally Adjusted'],
        ['Spain','Birth Rate','Annual','Crude Birth Rate','SPDYNCBRTINESP','Births per 1,000 People, Not Seasonally Adjusted'],

        # 人口增长率；出生率-死亡率。
        #Annual population growth rate for year t is the exponential rate of growth of midyear population from year t-1 to t, 
        #expressed as a percentage.
        ['China','Population Growth','Annual','Population Growth by WB','SPPOPGROWCHN','Percent Change at Annual Rate, NSA'],
        ['USA','Population Growth','Annual','Population Growth by WB','SPPOPGROWUSA','Percent Change at Annual Rate, NSA'],
        ['Japan','Population Growth','Annual','Population Growth by WB','SPPOPGROWJPN','Percent Change at Annual Rate, NSA'],
        ['Korea','Population Growth','Annual','Population Growth by WB','SPPOPGROWKOR','Percent Change at Annual Rate, NSA'],
        ['India','Population Growth','Annual','Population Growth by WB','SPPOPGROWIND','Percent Change at Annual Rate, NSA'],

        # 青年人失业率：WB
        ['China','Youth Unemployment','Annual','Youth Unemployment Rate by WB','SLUEM1524ZSCHN','Percent(Age 15-24, seeking employment), NSA'],
        ['USA','Youth Unemployment','Annual','Youth Unemployment Rate by WB','SLUEM1524ZSUSA','Percent(Age 15-24, seeking employment), NSA'],
        ['Japan','Youth Unemployment','Annual','Youth Unemployment Rate by WB','SLUEM1524ZSJPN','Percent(Age 15-24, seeking employment), NSA'],
        ['Korea','Youth Unemployment','Annual','Youth Unemployment Rate by WB','SLUEM1524ZSKOR','Percent(Age 15-24, seeking employment), NSA'],
        ['India','Youth Unemployment','Annual','Youth Unemployment Rate by WB','SLUEM1524ZSIND','Percent(Age 15-24, seeking employment), NSA'],

        # GNI: Gross National Income
        ['China','GNI','Annual','Gross National Income','MKTGNICNA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],
        ['USA','GNI','Annual','Gross National Income','MKTGNIUSA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],
        ['Japan','GNI','Annual','Gross National Income','MKTGNIJPA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],
        ['Korea','GNI','Annual','Gross National Income','MKTGNIKRA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],
        ['India','GNI','Annual','Gross National Income','MKTGNIINA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],
        ['Vietnam','GNI','Annual','Gross National Income','MKTGNIVNA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],
        ['Thailand','GNI','Annual','Gross National Income','MKTGNITHA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],
        ['Cambodia','GNI','Annual','Gross National Income','MKTGNIKHA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],
        ['China Hong Kong','GNI','Annual','Gross National Income','MKTGNIHKA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],
        ['Malaysia','GNI','Annual','Gross National Income','MKTGNIMYA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],
        ['Singapore','GNI','Annual','Gross National Income','MKTGNISGA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],
        ['Indonesia','GNI','Annual','Gross National Income','MKTGNIIDA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],
        ['Australia','GNI','Annual','Gross National Income','MKTGNIAUA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],
        ['New Zealand','GNI','Annual','Gross National Income','MKTGNINZA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],
        ['UK','GNI','Annual','Gross National Income','MKTGNIGBA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],
        ['Germany','GNI','Annual','Gross National Income','MKTGNIDEA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],
        ['France','GNI','Annual','Gross National Income','MKTGNIFRA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],
        ['Spain','GNI','Annual','Gross National Income','MKTGNIESA646NWDB','Current U.S. Dollars, Not Seasonally Adjusted'],

        # 出口对进口的比例
        ['China','Exports to Imports','Monthly','Ratio of Exports to Imports','XTEITT01CNM156S','Percent, Seasonally Adjusted'],
        ['India','Exports to Imports','Monthly','Ratio of Exports to Imports','XTEITT01INM156N','Percent, Seasonally Adjusted'],
        ['Brazil','Exports to Imports','Monthly','Ratio of Exports to Imports','XTEITT01BRM156S','Percent, Seasonally Adjusted'],
        ['Russia','Exports to Imports','Monthly','Ratio of Exports to Imports','XTEITT01RUM156S','Percent, Seasonally Adjusted'],
        ['Indonesia','Exports to Imports','Monthly','Ratio of Exports to Imports','XTEITT01IDM156S','Percent, Seasonally Adjusted'],

        # 人口雇佣比例
        ['China','Employment to Populatio','Annual','Employment to Population Ratio by WB','SLEMPTOTLSPZSCHN','Percent, Not Seasonally Adjusted'],
        ['USA','Employment to Populatio','Annual','Employment to Population Ratio by WB','SLEMPTOTLSPZSUSA','Percent, Not Seasonally Adjusted'],
        ['Japan','Employment to Populatio','Annual','Employment to Population Ratio by WB','SLEMPTOTLSPZSJPN','Percent, Not Seasonally Adjusted'],
        ['Korea','Employment to Populatio','Annual','Employment to Population Ratio by WB','SLEMPTOTLSPZSKOR','Percent, Not Seasonally Adjusted'],
        ['India','Employment to Populatio','Annual','Employment to Population Ratio by WB','SLEMPTOTLSPZSIND','Percent, Not Seasonally Adjusted'],

        # 人口总数
        ['China','Population','Annual','Total Population','POPTOTCNA647NWDB','Persons, Not Seasonally Adjusted'],
        ['USA','Population','Annual','Total Population','POPTOTUSA647NWDB','Persons, Not Seasonally Adjusted'],
        ['Japan','Population','Annual','Total Population','POPTOTJPA647NWDB','Persons, Not Seasonally Adjusted'],
        ['Korea','Population','Annual','Total Population','POPTOTKRA647NWDB','Persons, Not Seasonally Adjusted'],
        ['India','Population','Annual','Total Population','POPTOTINA647NWDB','Persons, Not Seasonally Adjusted'],
        
        # 其他
        ], columns=['scope','factor','freq','name','symbol','units'])
    
   return s


#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
if __name__ =="__main__":
    fromdate='2020-1-5'
    todate='2020-10-1'

def pmi_china(fromdate,todate):
    """
    功能：绘制中国的PMI指数制造业/非制造业单线图
    """
    #检查日期期间的合理性
    valid,start,end=check_period(fromdate,todate)
    if not valid:
        print('#Error(pmi_china): period not valid:',fromdate,todate)
        return None      
    
    #日期变换，将日都重置为每月的第一日
    year=start.year
    month=start.month    
    fromdate1=str(year)+'-'+str(month)+'-'+'1'

    year=end.year
    month=end.month    
    todate1=str(year)+'-'+str(month)+'-'+'1'
    _,start,end=check_period(fromdate1,todate1)
    
    #获取PMI数据
    import akshare as ak
    df = ak.macro_china_pmi()
    
    #截取日期区间数据
    import pandas as pd
    df['date']=pd.to_datetime(df['月份'])
    df.set_index('date',inplace=True)    
    df1=df[df.index >= start]
    df2=df1[df1.index <= end]
    
    #形成水平50线
    df2['benchmark']=50   
    
    #将字符串表示的数值转换为数值型，否则绘图很乱
    df2['制造业PMI']=df2['制造业-指数'].astype('float')
    df2['非制造业PMI']=df2['非制造业-指数'].astype('float')
    
    #绘图：制造业
    import siat.grafix as gfx
    ticker1=ticker2='PMI'
    colname2="benchmark"
    label2="景气/衰退分界线"
    ylabeltxt=''
    
    import datetime
    today=datetime.date.today()
    footnote="数据来源：东方财富，"+str(today)
    
    colname1="制造业PMI"
    label1="制造业"    
    titletxt="中国采购经理人指数PMI：制造业"
    gfx.plot_line2(df2,ticker1,colname1,label1, \
               df2,ticker2,colname2,label2, \
               ylabeltxt,titletxt,footnote)
    
    #绘图：非制造业
    colname1="非制造业PMI"
    label1="非制造业"    
    titletxt="中国采购经理人指数PMI：非制造业"
    gfx.plot_line2(df2,ticker1,colname1,label1, \
               df2,ticker2,colname2,label2, \
               ylabeltxt,titletxt,footnote)    
    #返回数据
    return df

#==============================================================================
