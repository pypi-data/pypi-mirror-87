# -*- coding: utf-8 -*-
"""
本模块功能：投资组合的风险调整收益率教学插件(算法II)
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2018年10月16日
最新修订日期：2020年8月17日
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
作者邮件：wdehong2000@163.com
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""

#==============================================================================
#关闭所有警告
import warnings; warnings.filterwarnings('ignore')
#==============================================================================
def get_ff_factors(start,end,scope='US',factor='FF3',freq='daily'):
    
    import pandas as pd
    s=pd.DataFrame([
        ['US','FF3','monthly','F-F_Research_Data_Factors',0],
        ['US','FF3','yearly','F-F_Research_Data_Factors',1],
        ['US','FF3','weekly','F-F_Research_Data_Factors_weekly',0],
        ['US','FF3','daily','F-F_Research_Data_Factors_daily',0],
        ['US','FF5','monthly','F-F_Research_Data_5_Factors_2x3',0],
        ['US','FF5','yearly','F-F_Research_Data_5_Factors_2x3',1],
        ['US','FF5','daily','F-F_Research_Data_5_Factors_2x3_daily',0],  
        ['US','Mom','monthly','F-F_Momentum_Factor',0],
        ['US','Mom','yearly','F-F_Momentum_Factor',1],
        ['US','Mom','daily','F-F_Momentum_Factor_daily',0],  
        ['US','ST_Rev','monthly','F-F_ST_Reversal_Factor',0],
        ['US','ST_Rev','yearly','F-F_ST_Reversal_Factor',1],
        ['US','ST_Rev','daily','F-F_ST_Reversal_Factor_daily',0],    
        ['US','LT_Rev','monthly','F-F_LT_Reversal_Factor',0],
        ['US','LT_Rev','yearly','F-F_LT_Reversal_Factor',1],
        ['US','LT_Rev','daily','F-F_LT_Reversal_Factor_daily',0],   \
        ['Global','FF3','monthly','Global_3_Factors',0],
        ['Global','FF3','yearly','Global_3_Factors',1],
        ['Global','FF3','daily','Global_3_Factors_Daily',0],   
        ['Global_ex_US','FF3','monthly','Global_ex_US_3_Factors',0],
        ['Global_ex_US','FF3','yearly','Global_ex_US_3_Factors',1],
        ['Global_ex_US','FF3','daily','Global_ex_US_3_Factors_Daily',0],  
        ['Europe','FF3','monthly','Europe_3_Factors',0],
        ['Europe','FF3','yearly','Europe_3_Factors',1],
        ['Europe','FF3','daily','Europe_3_Factors_Daily',0],  
        ['Japan','FF3','monthly','Japan_3_Factors',0],
        ['Japan','FF3','yearly','Japan_3_Factors',1],
        ['Japan','FF3','daily','Japan_3_Factors_Daily',0],    
        ['Asia_Pacific_ex_Japan','FF3','monthly','Asia_Pacific_ex_Japan_3_Factors',0],
        ['Asia_Pacific_ex_Japan','FF3','yearly','Asia_Pacific_ex_Japan_3_Factors',1],
        ['Asia_Pacific_ex_Japan','FF3','daily','Asia_Pacific_ex_Japan_3_Factors_Daily',0],   
        ['North_America','FF3','monthly','North_America_3_Factors',0],
        ['North_America','FF3','yearly','North_America_3_Factors',1],
        ['North_America','FF3','daily','North_America_3_Factors_Daily',0], \
        ['Global','FF5','monthly','Global_5_Factors',0],
        ['Global','FF5','yearly','Global_5_Factors',1],
        ['Global','FF5','daily','Global_5_Factors_Daily',0],   
        ['Global_ex_US','FF5','monthly','Global_ex_US_5_Factors',0],
        ['Global_ex_US','FF5','yearly','Global_ex_US_5_Factors',1],
        ['Global_ex_US','FF5','daily','Global_ex_US_5_Factors_Daily',0],  
        ['Europe','FF5','monthly','Europe_5_Factors',0],
        ['Europe','FF5','yearly','Europe_5_Factors',1],
        ['Europe','FF5','daily','Europe_5_Factors_Daily',0],  
        ['Japan','FF5','monthly','Japan_5_Factors',0],
        ['Japan','FF5','yearly','Japan_5_Factors',1],
        ['Japan','FF5','daily','Japan_5_Factors_Daily',0],    
        ['Asia_Pacific_ex_Japan','FF5','monthly','Asia_Pacific_ex_Japan_5_Factors',0],
        ['Asia_Pacific_ex_Japan','FF5','yearly','Asia_Pacific_ex_Japan_5_Factors',1],
        ['Asia_Pacific_ex_Japan','FF5','daily','Asia_Pacific_ex_Japan_5_Factors_Daily',0],   
        ['North_America','FF5','monthly','North_America_5_Factors',0],
        ['North_America','FF5','yearly','North_America_5_Factors',1],
        ['North_America','FF5','daily','North_America_5_Factors_Daily',0], \
        ['Global','Mom','monthly','Global_Mom_Factor',0],
        ['Global','Mom','yearly','Global_Mom_Factor',1],
        ['Global','Mom','daily','Global_Mom_Factor_Daily',0],   
        ['Global_ex_US','Mom','monthly','Global_ex_US_Mom_Factor',0],
        ['Global_ex_US','Mom','yearly','Global_ex_US_Mom_Factor',1],
        ['Global_ex_US','Mom','daily','Global_ex_US_Mom_Factor_Daily',0],  
        ['Europe','Mom','monthly','Europe_Mom_Factor',0],
        ['Europe','Mom','yearly','Europe_Mom_Factor',1],
        ['Europe','Mom','daily','Europe_Mom_Factor_Daily',0],  
        ['Japan','Mom','monthly','Japan_Mom_Factor',0],
        ['Japan','Mom','yearly','Japan_Mom_Factor',1],
        ['Japan','Mom','daily','Japan_Mom_Factor_Daily',0],    
        ['Asia_Pacific_ex_Japan','Mom','monthly','Asia_Pacific_ex_Japan_MOM_Factor',0],
        ['Asia_Pacific_ex_Japan','Mom','yearly','Asia_Pacific_ex_Japan_MOM_Factor',1],
        ['Asia_Pacific_ex_Japan','Mom','daily','Asia_Pacific_ex_Japan_MOM_Factor_Daily',0],   
        ['North_America','Mom','monthly','North_America_Mom_Factor',0],
        ['North_America','Mom','yearly','North_America_Mom_Factor',1],
        ['North_America','Mom','daily','North_America_Mom_Factor_Daily',0]                 
        ], columns=['scope','factor','freq','symbol','seq'])

    #数据源
    source='famafrench'
    if scope == "China": scope="Asia_Pacific_ex_Japan"
    
    #匹配：scope+factor+freq
    ss=s[s['scope'].isin([scope]) & s['factor'].isin([factor]) \
                                  & s['freq'].isin([freq])]  
    #如果未找到匹配的模式，显示信息后返回
    if len(ss)==0:
        print("Error #1(get_ff_factors): No data item available for",scope,factor,freq)
        return None

    #重新索引，第1行的索引编号为0
    sss=ss.reset_index(drop=True)    
    #取出对应的symbol
    symbol=sss.iloc[0]['symbol']    
    #取出对应的月(0)/年(1)编号
    seq=sss.iloc[0]['seq']

    #抓取数据
    import pandas_datareader.data as web
    try:
        ds = web.DataReader(symbol,source,start,end)
    except:
        print("Error #2(get_ff_factors): Server did not respond")        
        return None
    
    #提取希望的资产定价因子
    factor_df=ds[seq]
    if len(factor_df)==0:
        print("Error #3(get_ff_factors): Server returned empty data for",start,end,scope,factor,freq)
        return None    
    
    return factor_df


if __name__=='__main__':
    ff3_daily=get_ff_factors('2019-05-01','2019-06-30','US','FF3','daily')

#==============================================================================
def get_rf(startdate,enddate,scope='US',freq='daily'):
    """
    功能：按照市场获得无风险收益率，百分比表示
    输入：开始日期，解释日期，市场，频率
    """    

    try:
        rf_df=get_ff_factors(startdate,enddate,scope,'FF3',freq)
    except:
        print("Error #1 (get_rf): RF server did not respond.")
        return None    
    if rf_df is None:
        print("Error #2 (get_rf): Fetching risk-free return failed")
        return None

    #强制转换索引格式，彻底消除后续并表的潜在隐患
    rf_df['ffdate']=rf_df.index.astype('str')
    import pandas as pd
    rf_df['ffdate']=pd.to_datetime(rf_df['ffdate'])
    rf_df.set_index(['ffdate'],inplace=True)    
    
    return rf_df

#==============================================================================
def check_period(fromdate,todate):
    """
    功能：根据开始/结束日期检查期间日期的合理性
    输入参数：
    fromdate：开始日期。格式：YYYY-MM-DD
    enddate：开始日期。格式：YYYY-MM-DD
    输出参数：
    validity：期间合理性。True-合理，False-不合理
    start：开始日期。格式：datetime类型
    end：结束日期。格式：datetime类型
    """
    import pandas as pd
    try:
        start=pd.to_datetime(fromdate)
    except:
        print("Error #1(check_period): invalid date:",fromdate)
        return None,None,None         
    try:
        end=pd.to_datetime(todate)
    except:
        print("Error #2(check_period): invalid date:",todate)
        return None,None,None          
    if start > end:
        print("Error #3(check_period): invalid period: from",fromdate,"to",todate)
        return None,None,None     

    return True,start,end

#==============================================================================
def decompose_portfolio(portfolio):
    """
    功能：将一个投资组合字典分解为股票代码列表和份额列表
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合
    输出：市场，市场指数，股票代码列表和份额列表
    """
    #仅为测试用
    #portfolio={'Market':('US','^GSPC'),'EDU':0.4,'TAL':0.3,'TEDU':0.2}
    
    #从字典中提取信息
    keylist=list(portfolio.keys())
    scope=portfolio[keylist[0]][0]
    mktidx=portfolio[keylist[0]][1]
    
    slist=[]
    plist=[]
    for key,value in portfolio.items():
        slist=slist+[key]
        plist=plist+[value]
    stocklist=slist[1:]    
    portionlist=plist[1:]

    return scope,mktidx,stocklist,portionlist    

if __name__=='__main__':
    portfolio1={'Market':('US','^GSPC'),'EDU':0.4,'TAL':0.3,'TEDU':0.2}
    scope,mktidx,tickerlist,sharelist=decompose_portfolio(portfolio1)
    _,_,tickerlist,sharelist=decompose_portfolio(portfolio1)

#==============================================================================
def get_prices_yahoo(ticker,fromdate,todate):
    """
    功能：从雅虎财经抓取股票股价或指数价格或投资组合价值，使用pandas_datareader
    输入：股票代码或股票代码列表，开始日期，结束日期
    ticker: 股票代码或者股票代码列表。
    大陆股票代码加上后缀.SZ或.SS，港股代码去掉前导0加后缀.HK
    fromdate: 样本开始日期。
    todate: 样本结束日期。既可以是今天日期，也可以是一个历史日期   
    
    输出：股票价格序列，按照日期升序排列。原汁原味的抓取数据
    *Close price adjusted for splits.
    **Adjusted close price adjusted for both dividends and splits. 
    """
    #检查期间合理性
    result,start,end=check_period(fromdate,todate)
    if result is None:
        print("Error #1(get_prices_yahoo): failed to get stock prices!")        
        return None         
    
    #抓取雅虎股票价格
    from pandas_datareader import data
    try:
        prices=data.DataReader(ticker,'yahoo',start,end)
    except:
        print("Error #2(get_prices_yahoo): failed to get stock prices!")        
        print("Information:",ticker,fromdate,todate) 
        print("Possible reasons:")
        print("  1)internet connection problems.")
        print("  2)incorrect stock code.")
        print("  3)stock delisted or suspended during the period.")
        return None            
    if len(prices)==0:
        print("Error #3(get_prices_yahoo): fetched empty stock data!")
        print("Possible reasons:")
        print("  1)internet connection problems.")
        print("  2)incorrect stock code.")
        print("  3)stock delisted or suspended during the period.")
        return None         
    
    #去掉比起始日期更早的样本
    price2=prices[prices.index >= start]
    #去掉比结束日期更晚的样本
    price2=price2[price2.index <= end]
    
    #按日期升序排序，近期的价格排在后面
    sortedprice=price2.sort_index(axis=0,ascending=True)

    return sortedprice


#==============================================================================
def cvt_yftickerlist(ticker):
    """
    功能：转换pandas_datareader的tickerlist为yfinance的格式
    输入参数：单一股票代码或pandas_datareader的股票代码列表

    输出参数：yfinance格式的股票代码列表
    """
    #如果不是股票代码列表，直接返回股票代码
    if not isinstance(ticker,list): return ticker,False
    
    #如果是股票代码列表，但只有一个元素
    if len(ticker)==1: return ticker[0],False
    
    #如果是股票代码列表，有两个及以上元素
    yftickerlist=ticker[0]
    for t in ticker[1:]:
        yftickerlist=yftickerlist+' '+t
    
    return yftickerlist,True


if __name__=='__main__':
    tl1,islist=cvt_yftickerlist('AAPL')
    tl1,islist=cvt_yftickerlist(['AAPL'])
    tl1,islist=cvt_yftickerlist(['AAPL','MSFT'])
    tl1,islist=cvt_yftickerlist(['AAPL','MSFT','0700.hk'])
    print(tl1)

#==============================================================================
def get_prices_yf(ticker,start,end):
    """
    功能：从雅虎财经抓取股价，使用yfinance(对非美股抓取速度快，但有时不太稳定)
    输入：股票代码或股票代码列表，开始日期，结束日期
    ticker: 股票代码或股票代码列表。大陆股票代码加上后缀.SZ或.SS，港股代码去掉前导0加后缀.HK
    start: 样本开始日期，尽量远的日期，以便取得足够多的原始样本，yyyy-mm-dd
    end: 样本结束日期，既可以是今天日期，也可以是一个历史日期
    
    输出：指定收盘价格序列，最新日期的股价排列在前
    """
    
    #仅为调试用的函数入口参数，正式使用前需要注释掉！
    """
    ticker=['AAPL','MSFT']
    start='2019-10-1'
    end='2019-10-10'
    """
    #---------------------------------------------
   
    #转换日期
    r,startdate,enddate=check_period(start,end)
    if r is None:
        print("Error #1(get_prices_yf): invalid time period")
        return None        
        
    #抓取雅虎股票价格
    import yfinance as yf
    try:
        ticker1,islist=cvt_yftickerlist(ticker)
        if not islist: 
            stock=yf.Ticker(ticker1)
            #下载单一股票的股价
            p=stock.history(start=start,end=end)
        else: 
            #下载股票列表的股价
            p=yf.download(ticker1,start=start,end=end,progress=False)
        
    except:
        print("Error #1(get_prices_yf): server not responsed!")
        return None
    
    if len(p) == 0:
        print("Error #2(get_prices_yf): server reached but returned no data!")
        return None
    
    #去掉比起始日期更早的样本
    price=p[p.index >= startdate]
    #去掉比结束日期更晚的样本
    price2=price[price.index <= enddate]
    
    #按日期升序排序，近期的价格排在后面
    sortedprice=price2.sort_index(axis=0,ascending=True)

    #返回日期升序的股价序列    
    return sortedprice

if __name__=='__main__':
    df1=get_prices_yf('AAPL','2019-10-1','2019-10-8')
    df2=get_prices_yf(['AAPL'],'2019-10-1','2019-10-8')
    df3=get_prices_yf(['AAPL','MSFT'],'2019-10-1','2019-10-8')
    df4=get_prices_yf(['AAPL','MSFT','IBM'],'2019-10-1','2019-10-8')

#==============================================================================
def get_portfolio_prices(tickerlist,sharelist,fromdate,todate):
    """
    功能：抓取投资组合的每日价值
    输入：股票代码列表，份额列表，开始日期，结束日期
    tickerlist: 股票代码列表
    sharelist：持有份额列表，与股票代码列表一一对应
    fromdate: 样本开始日期。格式：'YYYY-MM-DD'
    todate: 样本结束日期。既可以是今天日期，也可以是一个历史日期    
    
    输出：投资组合的价格序列，按照日期升序排列
    """
    
    #仅为调试用的函数入口参数，正式使用前需要注释掉！
    #tickerlist=['AAPL','MSFT']
    #sharelist=[2,1]
    #fromdate='2019-8-1'
    #todate  ='2019-8-31'
    #---------------------------------------------
    
    #检查股票列表个数与份额列表个数是否一致
    if len(tickerlist) != len(sharelist):
        print("Error #1(get_portfolio_prices): numbers of stocks and shares mismatch.")
        return None        
    
    #从雅虎财经抓取股票价格
    p=get_prices_yahoo(tickerlist,fromdate,todate)
    
    import pandas as pd
    #计算投资者的开盘价
    op=p['Open']
    #计算投资组合的价值
    oprice=pd.DataFrame(op.dot(sharelist))
    oprice.rename(columns={0: 'Open'}, inplace=True)    

    #计算投资者的收盘价
    cp=p['Close']
    #计算投资组合的价值
    cprice=pd.DataFrame(cp.dot(sharelist))
    cprice.rename(columns={0: 'Close'}, inplace=True) 
    
    #计算投资者的调整收盘价
    acp=p['Adj Close']
    #计算投资组合的价值
    acprice=pd.DataFrame(acp.dot(sharelist))
    acprice.rename(columns={0: 'Adj Close'}, inplace=True) 

    #合成开盘价、收盘价和调整收盘价
    ocprice=pd.merge(oprice,cprice,how='inner',left_index=True,right_index=True)
    prices=pd.merge(ocprice,acprice,how='inner',left_index=True,right_index=True)

    #提取日期和星期几
    prices['Date']=prices.index.strftime("%Y-%m-%d")
    prices['Weekday']=prices.index.weekday+1

    prices['Portfolio']=str(tickerlist)
    prices['Shares']=str(sharelist)
    prices['Adjustment']=prices.apply(lambda x: \
          False if x['Close']==x['Adj Close'] else True, axis=1)

    stockdf=prices[['Portfolio','Shares','Date','Weekday', \
                    'Open','Close','Adj Close','Adjustment']]  

    return stockdf      


#==============================================================================
def calc_treynor_ratio(regdf):
    """
    功能：计算一项特雷诺指数
    输入：数据框，至少含有Ret-Rf和Mkt-Rf两项
    输出：特雷诺指数，Ret-Rf均值
    """
    
    #计算风险溢价Ret-RF均值
    ret_rf_mean=regdf['Ret-RF'].mean()
    
    #使用CAPM回归计算投资组合的贝塔系数，这里得到的alpha就是Jensen's alpha
    from scipy import stats
    output=stats.linregress(regdf['Mkt-RF'],regdf['Ret-RF'])
    (beta,alpha,r_value,p_value,std_err)=output 
    
    #计算特雷诺指数
    tr=ret_rf_mean/beta
    
    ret_mean=regdf['Close'].mean()
    return tr,ret_mean

#==============================================================================
def calc_alpha_ratio(regdf):
    """
    功能：计算一项詹森阿尔法指数
    输入：数据框，至少含有Ret-Rf和Mkt-Rf两项
    输出：詹森阿尔法指数，Ret-Rf均值
    """
    """
    #计算风险溢价Ret-RF均值
    ret_rf_mean=regdf['Ret-RF'].mean()
    """
    #使用CAPM回归计算投资组合的贝塔系数，这里得到的alpha就是Jensen's alpha
    from scipy import stats
    output=stats.linregress(regdf['Mkt-RF'],regdf['Ret-RF'])
    (beta,alpha,r_value,p_value,std_err)=output 
    
    ret_mean=regdf['Close'].mean()
    return alpha,ret_mean

#==============================================================================
def calc_sharpe_ratio(regdf):
    """
    功能：计算一项夏普指数
    输入：数据框，至少含有Ret-Rf和Mkt-Rf两项
    输出：夏普指数，Ret-Rf均值
    """
    #计算风险溢价Ret-RF均值和标准差
    ret_rf_mean=regdf['Ret-RF'].mean()
    ret_rf_std=regdf['Ret-RF'].std()
    
    #计算夏普指数
    sr=ret_rf_mean/ret_rf_std
    
    ret_mean=regdf['Close'].mean()
    return sr,ret_mean


#==============================================================================
def calc_sortino_ratio(regdf):
    """
    功能：计算一项索替诺指数
    输入：数据框，至少含有Ret-Rf和Mkt-Rf两项
    输出：索替诺指数，Ret-Rf均值
    """
    
    #计算风险溢价Ret-RF均值和下偏标准差LPSD
    ret_rf_mean=regdf['Ret-RF'].mean()
    reg2=regdf[regdf['Ret-RF'] < 0]
    ret_rf_lpsd=reg2['Ret-RF'].std()
    
    #计算索梯诺指数
    sr=ret_rf_mean/ret_rf_lpsd
    
    ret_mean=regdf['Close'].mean()
    return sr,ret_mean

#==============================================================================
def print_rar_ratio(regdf,portfolio,ret_mean,ratio_name,ratio):
    """
    功能：打印风险调整后的收益率
    输入：数据框，投资组合构成，收益溢价均值，指数名称，指数
    输出：打印
    """

    #从字典中提取信息
    scope,mktidx,stocklist,portionlist=decompose_portfolio(portfolio)
    stocklist1,_=cvt_yftickerlist(stocklist)
    
    date_start=str(regdf.index[0].year)+'-'+str(regdf.index[0].month)+ \
            '-'+str(regdf.index[0].day)
    date_end=str(regdf.index[-1].year)+'-'+str(regdf.index[-1].month)+ \
            '-'+str(regdf.index[-1].day)            
    print("\n===== 风险调整收益率 =====")
    print("市场指数:",scope,'\b,',mktidx)
    print("成分股  :",stocklist1)
    print("持仓权重:",portionlist)
    print("计算期间:",date_start,"至",date_end)
    print("收益率均值(%):",round(ret_mean,4))
    print(ratio_name.capitalize(),"比率(%):",round(ratio,4))
    
    return 
#==============================================================================
def treynor_ratio_portfolio(portfolio,start,end,printout=True):
    """
    功能：按天计算一个投资组合的特雷诺指数
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合，开始日期，结束日期
    输出：特雷诺指数
    """

    #仅为测试用
    #portfolio={'Market':('US','^GSPC'),'EDU':0.4,'TAL':0.3,'TEDU':0.2,'RYB':0.1}
    #start='2019-06-01'
    #end  ='2019-06-30'
    #scope='US'
    
    #第1步：各种准备和检查工作
    #设定错误信息的函数名
    func_name='treynor_ratio_portfolio'
    #设定需要计算的指数名称
    ratio_name="treynor"
    
    result,startdate,enddate=check_period(start,end)
    if not result:
        message="Error #1 ("+func_name+"): "+"Wrong start or end date"
        print(message)
        return None,None    
    
    #从字典中提取信息
    scope,mktidx,stocklist,portionlist=decompose_portfolio(portfolio)
    
    #第2步：计算投资组合的日收益率序列
    #抓取日投资组合价格
    sp=get_portfolio_prices(stocklist,portionlist,startdate,enddate)
    #计算日收益率，表示为百分比
    import pandas as pd
    ret_pf=pd.DataFrame(sp['Close'].pct_change())*100.0
    ret_pf=ret_pf.dropna()

    #第3步：获得无风险收益率/市场收益率序列
    #获得期间的日无风险收益率(抓取的RF为百分比) 
    rf_df=get_rf(startdate,enddate,scope='US',freq='daily')  
    if rf_df is None:
        message="Error #2 ("+func_name+"): "+"No data available for rf"
        print(message)
        return None,None 
    
    #第4步：合并投资组合日收益率与无风险利率/市场收益率序列
    #合并rf_df与ret_pf
    reg=pd.merge(ret_pf,rf_df,how='inner',left_index=True,right_index=True)
    reg['Ret-RF']=reg['Close']-reg['RF']
    reg=reg.dropna()
    if len(reg) == 0:
        message="Error #2 ("+func_name+"): "+"Empty data for calculation"
        print(message)
        return None,None 
    
    #第5步：计算风险调整后的收益率
    ##########风险调整后的收益率，计算开始##########
    tr,ret_mean=calc_treynor_ratio(reg)
    ##########风险调整后的收益率，计算结束##########
    
    #第6步：打印结果
    if printout == True:
        print_rar_ratio(reg,portfolio,ret_mean,ratio_name,tr)
    
    return tr,ret_mean


if __name__=='__main__':
    portfolio1={'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    tr1,ret1=treynor_ratio_portfolio(portfolio1,'2019-01-01','2019-01-31')


#==============================================================================
def rar_ratio_portfolio(portfolio,start,end,ratio_name='treynor',printout=True):
    """
    功能：按天计算一个投资组合的风险调整后的收益率指数
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合，开始日期，结束日期
    输出：风险调整后的收益率指数
    """

    #仅为测试用
    #portfolio={'Market':('US','^GSPC'),'EDU':0.4,'TAL':0.3,'TEDU':0.2,'RYB':0.1}
    #start='2019-06-01'
    #end  ='2019-06-30'
    #scope='US'
    
    #第1步：各种准备和检查工作
    #设定错误信息的函数名
    func_name='rar_ratio_portfolio'
    
    ratio_list=['treynor','sharpe','sortino','alpha']
    if ratio_name not in ratio_list:
        message="Error #1 ("+func_name+"): "+"Not supported rar ratio type"
        print(message)
        return None,None         
    
    result,startdate,enddate=check_period(start,end)
    if not result:
        message="Error #2 ("+func_name+"): "+"Wrong start or end date"
        print(message)
        return None,None    
    
    #从字典中提取信息
    scope,mktidx,stocklist,portionlist=decompose_portfolio(portfolio)
    
    #第2步：计算投资组合的日收益率序列
    #抓取日投资组合价格
    sp=get_portfolio_prices(stocklist,portionlist,startdate,enddate)
    #计算日收益率，表示为百分比
    import pandas as pd
    ret_pf=pd.DataFrame(sp['Close'].pct_change())*100.0
    ret_pf=ret_pf.dropna()

    #第3步：获得无风险收益率/市场收益率序列
    #获得期间的日无风险收益率(抓取的RF为百分比) 
    rf_df=get_rf(startdate,enddate,scope='US',freq='daily')  
    if rf_df is None:
        message="Error #3 ("+func_name+"): "+"No data available for rf"
        print(message)
        return None,None 
    
    #第4步：合并投资组合日收益率与无风险利率/市场收益率序列
    #合并rf_df与ret_pf
    reg=pd.merge(ret_pf,rf_df,how='inner',left_index=True,right_index=True)
    reg['Ret-RF']=reg['Close']-reg['RF']
    reg=reg.dropna()
    if len(reg) == 0:
        message="Error #4 ("+func_name+"): "+"Empty data for ratio calculation"
        print(message)
        return None,None 
    
    #第5步：计算风险调整后的收益率
    ##########风险调整后的收益率，计算开始##########
    calc_func='calc_'+ratio_name+'_ratio'
    rar,ret_mean=eval(calc_func)(reg)
    ##########风险调整后的收益率，计算结束##########
    
    #第6步：打印结果
    if printout == True:
        print_rar_ratio(reg,portfolio,ret_mean,ratio_name,rar)
    
    return rar,ret_mean


if __name__=='__main__':
    portfolio1={'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    tr1,rp1=treynor_ratio_portfolio(portfolio1,'2019-01-01','2019-01-31')


#==============================================================================
def rar_ratio_rolling(portfolio,start,end,ratio_name='treynor', \
                      window=30,graph=True):
    """
    功能：滚动计算一个投资组合的风险调整后的收益率指数
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合，开始日期，结束日期，指数名称，滚动窗口宽度(天数)
    输出：风险调整后的收益率指数序列
    注意：因需要滚动计算，开始和结束日期之间需要拉开距离
    """

    #仅为测试用
    """
    portfolio={'Market':('US','^GSPC'),'EDU':0.4,'TAL':0.3,'TEDU':0.2}
    start='2018-06-01'
    end  ='2019-06-30'
    scope='US'
    ratio_name='treynor'
    window=30
    graph=True
    """
    
    #第1步：各种准备和检查工作
    print("***Start to calculate rolling ratios, please wait ...")
    #设定错误信息的函数名
    func_name='rar_ratio_portfolio'
    
    ratio_list=['treynor','sharpe','sortino','alpha']
    if ratio_name not in ratio_list:
        message="Error #1 ("+func_name+"): "+"Not supported rar ratio type"
        print(message)
        return None,None         
    
    result,startdate,enddate=check_period(start,end)
    if not result:
        message="Error #2 ("+func_name+"): "+"Wrong start or end date"
        print(message)
        return None,None    
    
    #从字典中提取信息
    scope,mktidx,stocklist,portionlist=decompose_portfolio(portfolio)
    
    #第2步：计算投资组合的日收益率序列
    #抓取日投资组合价格
    sp=get_portfolio_prices(stocklist,portionlist,startdate,enddate)
    #计算日收益率，表示为百分比
    import pandas as pd
    ret_pf=pd.DataFrame(sp['Close'].pct_change())*100.0
    ret_pf=ret_pf.dropna()

    #第3步：获得无风险收益率/市场收益率序列
    #获得期间的日无风险收益率(抓取的RF为百分比) 
    rf_df=get_rf(startdate,enddate,scope='US',freq='daily')  
    if rf_df is None:
        message="Error #3 ("+func_name+"): "+"No data available for rf"
        print(message)
        return None,None 
    
    #第4步：合并投资组合日收益率与无风险利率/市场收益率序列
    #合并rf_df与ret_pf
    reg=pd.merge(ret_pf,rf_df,how='inner',left_index=True,right_index=True)
    if len(reg) == 0:
        message="Error #4 ("+func_name+"): "+"Empty data for ratio calculation"
        print(message)
        return None,None     
    reg['Ret-RF']=reg['Close']-reg['RF']
    reg=reg.dropna()
    
    #第5步：滚动计算风险调整后的收益率
    ##########风险调整后的收益率，计算开始##########
    #用于保存rar和ret_rf_mean
    import pandas as pd
    import numpy as np
    datelist=reg.index.to_list()
    calc_func='calc_'+ratio_name+'_ratio'
    
    rars=pd.DataFrame(columns=('Date','RAR','Mean(Ret)')) 
    for i in np.arange(0,len(reg)):
        i1=i+window-1
        if i1 >= len(reg): break
        
        #构造滚动窗口
        windf=reg[reg.index >= datelist[i]]
        windf=windf[windf.index <= datelist[i1]]
        #print(i,datelist[i],i1,datelist[i1],len(windf))
        
        #使用滚动窗口计算
        rar,ret_mean=eval(calc_func)(windf)
        
        #记录计算结果
        row=pd.Series({'Date':datelist[i1],'RAR':rar,'Mean(Ret)':ret_mean})
        rars=rars.append(row,ignore_index=True)        
    
    rars.set_index(['Date'],inplace=True) 
    ##########风险调整后的收益率，计算结束##########
    
    #第6步：绘图
    if graph == True:
        draw_rar_ratio(rars,portfolio,ratio_name)
    
    return rars


if __name__=='__main__':
    portfolio1={'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    tr1,ret1=treynor_ratio_portfolio(portfolio1,'2019-01-01','2019-01-31')
#==============================================================================
def draw_rar_ratio(rars,portfolio,ratio_name):
    """
    功能：绘制滚动窗口曲线
    输入：滚动数据df，投资组合，指数名称
    """
    
    scope,mktidx,stocklist,portionlist=decompose_portfolio(portfolio)
    stocklist1,_=cvt_yftickerlist(stocklist)
    
    import matplotlib.pyplot as plt    
    plt.figure(figsize=(8,5))
 
    labeltxt=ratio_name.capitalize()+' ratio(%)'    
    plt.plot(rars['RAR'],label=labeltxt,color='red',lw=3)
    plt.plot(rars['Mean(Ret)'],label='Stock(s) return(%)',color='blue',lw=1)
    plt.axhline(y=0.0,color='black',linestyle=':')
    
    titletxt='风险调整收益的滚动趋势\n'+ \
        '股票: '+stocklist1+'\n'+ \
        '持仓权重: '+str(portionlist)   
    plt.title(titletxt,fontsize=12,fontweight='bold') 
    
    ylabeltxt="收益率(%)"
    plt.ylabel(ylabeltxt,fontsize=12)
    plt.xticks(rotation=45,fontsize=9)
    plt.legend(loc='best') 
    
    import datetime as dt; today=dt.date.today() 
    footnote="数据来源：雅虎财经，"+str(today)
    plt.xlabel(footnote)
    plt.show()

    #使用seaborn绘图
    """
    import seaborn as sns
    with sns.axes_style("whitegrid"):
        fig, ax = plt.subplots(figsize=(8,5))
        ax.plot(rars['RAR'],label=labeltxt,color='red',lw=3)
        ax.plot(rars['Mean(Ret)'],label='Stock(s) return(%)',color='blue',lw=1)
        plt.axhline(y=0.0,label='Zero return',color='black',linestyle=':')
        ax.set_title(titletxt)
        ax.set_ylabel(ylabeltxt)
        plt.xticks(rotation=45)
        ax.legend(loc='best')
        ax.set_ylim([1.2*(rars['RAR'].min()), 1.1*(rars['RAR'].max())])    
    """
    return
#==============================================================================
def sharpe_ratio_portfolio(portfolio,start,end,printout=True):
    """
    功能：按天计算一个投资组合的夏普指数
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合，开始日期，结束日期
    输出：夏普指数
    """

    #仅为测试用
    #portfolio={'Market':('US','^GSPC'),'AAPL':0.2,'MSFT':0.6,'IBM':0.2}
    #start='2019-01-01'
    #end  ='2019-01-31'
    
    freq='daily'
    keylist=list(portfolio.keys())
    scope=portfolio[keylist[0]][0]
    mktidx=portfolio[keylist[0]][1]
    
    #从字典中提取信息
    slist=[]
    plist=[]
    for key,value in portfolio.items():
        slist=slist+[key]
        plist=plist+[value]
    stocklist=slist[1:]    
    portionlist=plist[1:]
    
    #检查份额配比是否合理
    """
    if round(sum(portionlist),1) != 1.0:
        print("Error #1 (sharpe_ratio): Incorrect total of portions")
        return None,None
    """
    
    #抓取指数和股票价格
    tickerlist=[mktidx]+stocklist
    import pandas as pd
    try:
        startdate=pd.to_datetime(start)
        enddate=pd.to_datetime(end)
    except:
        print("Error #2 (sharpe_ratio): incorrect start/end date(s)")
        return None,None       
    
    import pandas_datareader as pdr
    try:
        price=pdr.DataReader(tickerlist,'yahoo',start=startdate,end=enddate)
    except:
        print("Error #3 (sharpe_ratio): Server did not respond")
        return None,None
    
    if len(price) == 0:
        print("Error #4 (sharpe_ratio): Server returned empty data")
        return None,None
        
    #提取股指和投资组合中各个股票的收盘价    
    closeprice=price['Close'] 

    #将股价乘以各自的份额，放入新的表sp中  
    sp=pd.DataFrame(columns=stocklist)
    for stock in stocklist:
        pos=stocklist.index(stock)
        portion=portionlist[pos]
        sp[stock]=closeprice[stock]*portion

    #逐行汇总汇总，形成每日投资组合的价格
    #在同一行中对各个列的数值计算：axis=1
    sp['PORTFOLIO']=sp.apply(lambda row: sum(row), axis =1)
    ret_pf=pd.DataFrame(sp['PORTFOLIO'].pct_change())*100.0
    ret_pf=ret_pf.dropna()
    
    #获得期间的无风险收益率 
    try:
        rf_df=get_ff_factors(startdate,enddate,scope,'FF3',freq)
    except:
        print("Error #5 (sharpe_ratio): RF server did not respond")
        return None,None        
    if len(rf_df) == 0:
        print("Error #6 (sharpe_ratio): RF server returned empty data")
        return None,None

    #强制转换索引格式，彻底消除下面并表的潜在隐患
    rf_df['ffdate']=rf_df.index.astype('str')
    rf_df['ffdate']=pd.to_datetime(rf_df['ffdate'])
    rf_df.set_index(['ffdate'],inplace=True)
    
    #合并rf_df与ret_pf
    reg=pd.merge(ret_pf,rf_df,how='inner',left_index=True,right_index=True)
    reg['Ret-RF']=reg['PORTFOLIO']-reg['RF']
    reg=reg.dropna()
    
    #计算风险溢价Ret-RF均值和标准差
    ret_rf_mean=reg['Ret-RF'].mean()
    ret_rf_std=reg['Ret-RF'].std()
    
    #计算夏普指数
    sr=ret_rf_mean/ret_rf_std
    
    #打印报告
    if printout == True:
        date_start=str(reg.index[0].year)+'-'+str(reg.index[0].month)+ \
            '-'+str(reg.index[0].day)
        date_end=str(reg.index[-1].year)+'-'+str(reg.index[-1].month)+ \
            '-'+str(reg.index[-1].day)            
        print("\n===== 风险调整收益率 =====")
        print("投资组合：",portfolio)
        print("计算期间：",date_start,"至",date_end, \
          "(可用日期)")
        print("风险溢价均值(%)：",round(ret_rf_mean,4))
        print("夏普比率(%)：",round(sr,4))
        import datetime as dt; today=dt.date.today()
        print("*数据来源：雅虎财经，"+str(today))
    
    return sr,ret_rf_mean


if __name__=='__main__':
    portfolio={'Market':('US','^GSPC'),'AAPL':0.2,'MSFT':0.5,'IBM':0.3}
    sr1,rp1=sharpe_ratio_portfolio(portfolio,'2019-01-01','2019-01-31')


#==============================================================================
def sortino_ratio_portfolio(portfolio,start,end,printout=True):
    """
    功能：按天计算一个投资组合的索梯诺指数
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合，开始日期，结束日期
    输出：索梯诺指数
    """

    #仅为测试用
    #portfolio={'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    #start='2019-01-01'
    #end  ='2019-01-31'
    
    freq='daily'
    keylist=list(portfolio.keys())
    scope=portfolio[keylist[0]][0]
    mktidx=portfolio[keylist[0]][1]
    
    #从字典中提取信息
    slist=[]
    plist=[]
    for key,value in portfolio.items():
        slist=slist+[key]
        plist=plist+[value]
    stocklist=slist[1:]    
    portionlist=plist[1:]
    
    #检查份额配比是否合理
    """
    if round(sum(portionlist),1) != 1.0:
        print("Error #1 (sortino_ratio): Incorrect total of portions")
        return None,None
    """
    
    #抓取指数和股票价格
    tickerlist=[mktidx]+stocklist
    import pandas as pd
    try:
        startdate=pd.to_datetime(start)
        enddate=pd.to_datetime(end)
    except:
        print("Error #2 (sortino_ratio): Incorrect start/end date(s)")
        return None,None
        
    import pandas_datareader as pdr
    try:
        price=pdr.DataReader(tickerlist,'yahoo',start=startdate,end=enddate)
    except:
        print("Error #3 (sortino_ratio): Server did not respond")
        return None,None
    
    if len(price) == 0:
        print("Error #4 (sortino_ratio): Server returned empty data")
        return None,None
        
    #提取股指和投资组合中各个股票的收盘价    
    closeprice=price['Close'] 

    #将股价乘以各自的份额，放入新的表sp中  
    sp=pd.DataFrame(columns=stocklist)
    for stock in stocklist:
        pos=stocklist.index(stock)
        portion=portionlist[pos]
        sp[stock]=closeprice[stock]*portion

    #逐行汇总汇总，形成每日投资组合的价格
    #在同一行中对各个列的数值计算：axis=1
    sp['PORTFOLIO']=sp.apply(lambda row: sum(row), axis =1)
    ret_pf=pd.DataFrame(sp['PORTFOLIO'].pct_change())*100.0
    ret_pf=ret_pf.dropna()
    
    #获得期间的无风险收益率  
    try:      
        rf_df=get_ff_factors(startdate,enddate,scope,'FF3',freq)
    except:
        print("Error #5 (sharpe_ratio): RF server did not respond")
        return None,None        

    if rf_df is None:
        print("Error #6 (sortino_ratio): RF server did not respond")
        return None,None        
    if len(rf_df) == 0:
        print("Error #7 (sortino_ratio): RF server returned empty data")
        return None,None 
    
    #强制转换索引格式，彻底消除下面并表的潜在隐患
    rf_df['ffdate']=rf_df.index.astype('str')
    rf_df['ffdate']=pd.to_datetime(rf_df['ffdate'])
    rf_df.set_index(['ffdate'],inplace=True)
    
    #合并rf_df与ret_pf
    reg=pd.merge(ret_pf,rf_df,how='inner',left_index=True,right_index=True)
    reg['Ret-RF']=reg['PORTFOLIO']-reg['RF']
    reg=reg.dropna()
    
    #计算风险溢价Ret-RF均值和下偏标准差LPSD
    ret_rf_mean=reg['Ret-RF'].mean()
    reg2=reg[reg['Ret-RF'] < 0]
    ret_rf_lpsd=reg2['Ret-RF'].std()
    
    #计算索梯诺指数
    sr=ret_rf_mean/ret_rf_lpsd
    
    #打印报告
    if printout == True:    
        date_start=str(reg.index[0].year)+'-'+str(reg.index[0].month)+ \
            '-'+str(reg.index[0].day)
        date_end=str(reg.index[-1].year)+'-'+str(reg.index[-1].month)+ \
            '-'+str(reg.index[-1].day)            
        print("\n===== 风险调整收益率 =====")
        print("投资组合：",portfolio)
        print("计算期间：",date_start,"至",date_end, \
              "(可用日期)")
        print("风险溢价均值(%)：",round(ret_rf_mean,4))
        print("索替诺比率(%)：",round(sr,4))
        
        import datetime as dt; today=dt.date.today()
        print("*数据来源：雅虎财经，"+str(today))
    
    return sr,ret_rf_mean


if __name__=='__main__':
    portfolio={'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    sr1,rp1=sortino_ratio_portfolio(portfolio,'2019-01-01','2019-08-03')

#==============================================================================
def jensen_alpha_portfolio(portfolio,start,end,printout=True):
    """
    功能：按天计算一个投资组合的阿尔法指数
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合，开始日期，结束日期
    输出：阿尔法指数
    """

    #仅为测试用
    #portfolio={'Market':('China','000001.SS'),'600519.SS':1.0}
    #start='2019-01-01'
    #end  ='2019-01-31'
    
    freq='daily'
    keylist=list(portfolio.keys())
    scope=portfolio[keylist[0]][0]
    mktidx=portfolio[keylist[0]][1]
    
    #从字典中提取信息
    slist=[]
    plist=[]
    for key,value in portfolio.items():
        slist=slist+[key]
        plist=plist+[value]
    stocklist=slist[1:]    
    portionlist=plist[1:]
    
    #检查份额配比是否合理
    """
    if round(sum(portionlist),1) != 1.0:
        print("Error #1 (jensen_alpha): Incorrect total of portions.")
        return None,None
    """
    
    #抓取指数和股票价格
    tickerlist=[mktidx]+stocklist
    import pandas as pd
    try:
        startdate=pd.to_datetime(start)
        enddate=pd.to_datetime(end)
    except:
        print("Error #2 (jensen_alpha): Incorrect start/end date(s).")
        return None,None        
        
    import pandas_datareader as pdr
    try:
        price=pdr.DataReader(tickerlist,'yahoo',start=startdate,end=enddate)
    except:
        print("Error #3 (jensen_alpha): Server did not respond.")
        return None,None
    
    if len(price) == 0:
        print("Error #4 (jensen_alpha): Server returned empty data.")
        return None,None
        
    #提取股指和投资组合中各个股票的收盘价    
    closeprice=price['Close'] 

    #将股价乘以各自的份额，放入新的表sp中  
    sp=pd.DataFrame(columns=stocklist)
    for stock in stocklist:
        pos=stocklist.index(stock)
        portion=portionlist[pos]
        sp[stock]=closeprice[stock]*portion

    #逐行汇总汇总，形成每日投资组合的价格
    #在同一行中对各个列的数值计算：axis=1
    sp['PORTFOLIO']=sp.apply(lambda row: sum(row), axis =1)
    ret_pf=pd.DataFrame(sp['PORTFOLIO'].pct_change())*100.0
    ret_pf=ret_pf.dropna()
    
    #获得期间的无风险收益率        
    rf_df=get_ff_factors(startdate,enddate,scope,'FF3',freq)
    #强制转换索引格式，彻底消除下面并表的潜在隐患
    rf_df['ffdate']=rf_df.index.astype('str')
    rf_df['ffdate']=pd.to_datetime(rf_df['ffdate'])
    rf_df.set_index(['ffdate'],inplace=True)
    
    if rf_df is None:
        print("Error #5 (jensen_alpha): RF server did not respond.")
        return None,None        
    if len(rf_df) == 0:
        print("Error #6 (jensen_alpha): RF server returned empty data.")
        return None,None 
    
    #合并rf_df与ret_pf
    reg=pd.merge(ret_pf,rf_df,how='inner',left_index=True,right_index=True)
    reg['Ret-RF']=reg['PORTFOLIO']-reg['RF']
    reg=reg.dropna()
    if len(reg) == 0:
        print("Error #7 (jensen_alpha): Empty data for regression.")
        return None,None     
    ret_rf_mean=reg['Ret-RF'].mean()
    
    #使用CAPM回归计算投资组合的贝塔系数，这里得到的alpha就是Jensen's alpha
    from scipy import stats
    output=stats.linregress(reg['Mkt-RF'],reg['Ret-RF'])
    (beta,alpha,r_value,p_value,std_err)=output 
    
    #打印报告
    if printout == True:
        date_start=str(reg.index[0].year)+'-'+str(reg.index[0].month)+ \
            '-'+str(reg.index[0].day)
        date_end=str(reg.index[-1].year)+'-'+str(reg.index[-1].month)+ \
            '-'+str(reg.index[-1].day)            
        print("\n===== 风险调整收益率 =====")
        print("投资组合：",portfolio)
        print("计算期间：",date_start,"至",date_end, \
              "(可用日期)")
        print("风险溢价均值(%)：",round(ret_rf_mean,4))
        print("詹森阿尔法(%)：",round(alpha,4))
        
        import datetime as dt; today=dt.date.today()
        print("*数据来源：雅虎财经，"+str(today))        
    
    return alpha,ret_rf_mean


if __name__=='__main__':
    portfolio={'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    alpha1=jensen_alpha_portfolio(portfolio,'2019-01-01','2019-08-03')

#==============================================================================
def calc_monthly_date_range(start,end):
    """
    功能：返回两个日期之间各个月份的开始和结束日期
    输入：开始/结束日期
    输出：两个日期之间各个月份的开始和结束日期元组对列表
    """
    #测试用
    #start='2019-01-05'
    #end='2019-06-25'    
    
    import pandas as pd
    startdate=pd.to_datetime(start)
    enddate=pd.to_datetime(end)

    mdlist=[]
    #当月的结束日期
    syear=startdate.year
    smonth=startdate.month
    import calendar
    sdays=calendar.monthrange(syear,smonth)[1]
    from datetime import date
    slastday=pd.to_datetime(date(syear,smonth,sdays))

    if slastday > enddate: slastday=enddate
    
    #加入第一月的开始和结束日期
    import bisect
    bisect.insort(mdlist,(startdate,slastday))
    
    #加入结束月的开始和结束日期
    eyear=enddate.year
    emonth=enddate.month
    efirstday=pd.to_datetime(date(eyear,emonth,1))   
    if startdate < efirstday:
        bisect.insort(mdlist,(efirstday,enddate))
    
    #加入期间内各个月份的开始和结束日期
    from dateutil.relativedelta import relativedelta
    next=startdate+relativedelta(months=+1)
    while next < efirstday:
        nyear=next.year
        nmonth=next.month
        nextstart=pd.to_datetime(date(nyear,nmonth,1))
        ndays=calendar.monthrange(nyear,nmonth)[1]
        nextend=pd.to_datetime(date(nyear,nmonth,ndays))
        bisect.insort(mdlist,(nextstart,nextend))
        next=next+relativedelta(months=+1)
    
    return mdlist

if __name__=='__main__':
    mdp1=calc_monthly_date_range('2019-01-01','2019-06-30')
    mdp2=calc_monthly_date_range('2000-01-01','2000-06-30')   #闰年
    mdp3=calc_monthly_date_range('2018-09-01','2019-03-31')   #跨年
    
    for i in range(0,len(mdp1)):
        start=mdp1[i][0]
        end=mdp1[i][1]
        print("start =",start,"end =",end)


#==============================================================================
def calc_yearly_date_range(start,end):
    """
    功能：返回两个日期之间各个年度的开始和结束日期
    输入：开始/结束日期
    输出：两个日期之间各个年度的开始和结束日期元组对列表
    """
    #测试用
    #start='2013-01-01'
    #end='2019-08-08'    
    
    import pandas as pd
    startdate=pd.to_datetime(start)
    enddate=pd.to_datetime(end)

    mdlist=[]
    #当年的结束日期
    syear=startdate.year
    from datetime import date
    slastday=pd.to_datetime(date(syear,12,31))

    if slastday > enddate: slastday=enddate
    
    #加入第一年的开始和结束日期
    import bisect
    bisect.insort(mdlist,(startdate,slastday))
    
    #加入结束年的开始和结束日期
    eyear=enddate.year
    efirstday=pd.to_datetime(date(eyear,1,1))   
    if startdate < efirstday:
        bisect.insort(mdlist,(efirstday,enddate))
    
    #加入期间内各个年份的开始和结束日期
    from dateutil.relativedelta import relativedelta
    next=startdate+relativedelta(years=+1)
    while next < efirstday:
        nyear=next.year
        nextstart=pd.to_datetime(date(nyear,1,1))
        nextend=pd.to_datetime(date(nyear,12,31))
        bisect.insort(mdlist,(nextstart,nextend))
        next=next+relativedelta(years=+1)
    
    return mdlist

if __name__=='__main__':
    mdp1=calc_yearly_date_range('2013-01-05','2019-06-30')
    mdp2=calc_yearly_date_range('2000-01-01','2019-06-30')   #闰年
    mdp3=calc_yearly_date_range('2018-09-01','2019-03-31')   #跨年
    
    for i in range(0,len(mdp1)):
        start=mdp1[i][0]
        end=mdp1[i][1]
        print("start =",start,"end =",end)

#==============================================================================
def plot_rar_monthly(portfolio,start,end,rar_type):
    """
    功能：将风险调整收益率和风险溢价逐月绘图对比
    输入：投资组合，开始/结束日期，风险调整收益指数类别
    输出：风险调整收益率和风险溢价的逐月数据框
    显示：按月绘图投资组合的风险调整收益率和风险溢价
    """
    #仅为测试用
    #portfolio={'Market':('US','^GSPC'),'JD':0.3,'BABA':0.7}
    #start='2019-01-01'
    #end='2019-03-31'
    #rar_type='sortino_ratio'    
    
    #各项函数参数检查
    #从字典中提取信息
    plist=[]
    for key,value in portfolio.items():
        plist=plist+[value]
    #portionlist=plist[1:]
    
    #检查1：投资组合各个成分股份额的合理性
    """
    if round(sum(portionlist),1) != 1.0:
        print("Error #1(plot_rar_monthly): Incorrect total of portions")
        return None    
    """
    
    #检查2：开始/结束日期大小
    import pandas as pd
    try:
        startdate=pd.to_datetime(start)
        enddate=pd.to_datetime(end)
    except:
        print("Error #2(plot_rar_monthly): Incorrect start/end date(s)")
        return None
    if startdate >= enddate:
        print("Error #3(plot_rar_monthly): start date should be earlier")
        return None        

    #检查3：支持的rar_type
    rar_list=['treynor_ratio','sharpe_ratio','sortino_ratio','jensen_alpha']
    if rar_type not in rar_list:
        print("Error #4 (draw_rar_monthly): not supported rar type")
        print("Supported rar type:",rar_list)              
        return None         

    #拆分start/end之间的各个年份和月份
    mdlist=calc_monthly_date_range(start,end)
    if len(mdlist) == 0:
        print("Error #5(plot_rar_monthly): start/end dates inappropriate")
        return None          

    #用于保存risk premium和rar
    print("\nCalculating monthly",rar_type,"from",start,"to",end,"......")
    rarfunc=rar_type+'_portfolio'
    rars=pd.DataFrame(columns=('YM','rp','rar'))
    for i in range(0,len(mdlist)):
        start=mdlist[i][0]
        YM=start.strftime("%Y-%m")
        print(YM,end=' ')
        end=mdlist[i][1]
        rar,rp=eval(rarfunc)(portfolio,start,end,printout=False)
        
        row=pd.Series({'YM':YM,'rp':rp,'rar':rar})
        rars=rars.append(row,ignore_index=True)         
    print("completed.")
    rars.set_index('YM',inplace=True)    
    #绘图
    import matplotlib.pyplot as plt
    plt.plot(rars['rp'],label='risk_premium',c='blue',marker='*',ls=':',lw=3)
    plt.plot(rars['rar'],label=rar_type,c='r',lw=3,marker='o')
    plt.axhline(y=0.0,color='black',linestyle=':',lw=1) 
    titletxt="投资组合的风险调整收益"
    plt.title(titletxt)
    plt.ylabel('收益率(%)')
    plt.xticks(rotation=45)
    plt.legend(loc='best')

    import datetime as dt; today=dt.date.today() 
    footnote="数据来源：雅虎财经，"+str(today)
    plt.xlabel(footnote)   
    
    plt.show()

    return


if __name__=='__main__':
    portfolio={'Market':('US','^GSPC'),'VIPS':0.1,'PDD':0.2,'JD':0.3,'BABA':0.4}
    plot_rar_monthly(portfolio,'2019-01-01','2019-06-30','treynor_ratio') 

    portfolio={'Market':('US','^GSPC'),'AAPL':1.0}
    plot_rar_monthly(portfolio,'2017-01-01','2017-12-31','sharpe_ratio')       
#==============================================================================
#==============================================================================
def plot_rar_annual(portfolio,start,end,rar_type):
    """
    功能：将风险调整收益率和风险溢价逐年绘图对比
    输入：投资组合，开始/结束日期，风险调整收益指数类别
    输出：风险调整收益率和风险溢价的逐年数据框
    显示：按年绘图投资组合的风险调整收益率和风险溢价
    """
    #仅为测试用
    #portfolio={'Market':('US','^GSPC'),'JD':0.3,'BABA':0.7}
    #start='2013-01-01'
    #end='2018-12-31'
    #rar_type='sortino_ratio'    
    
    #各项函数参数检查
    #从字典中提取信息
    plist=[]
    for key,value in portfolio.items():
        plist=plist+[value]
    #portionlist=plist[1:]
    
    #检查1：投资组合各个成分股份额的合理性
    """
    if round(sum(portionlist),1) != 1.0:
        print("Error #1(plot_rar_annual): Incorrect total of portions")
        return None    
    """
    
    #检查2：开始/结束日期大小
    import pandas as pd
    try:
        startdate=pd.to_datetime(start)
        enddate=pd.to_datetime(end)
    except:
        print("Error #2(plot_rar_annual): Incorrect start/end date(s)")
        return None
    if startdate >= enddate:
        print("Error #3(plot_rar_annual): start date should be earlier")
        return None        

    #检查3：支持的rar_type
    rar_list=['treynor_ratio','sharpe_ratio','sortino_ratio','jensen_alpha']
    if rar_type not in rar_list:
        print("Error #4(plot_rar_annual): not supported rar type")
        print("Supported rar type:",rar_list)              
        return None         

    #拆分start/end之间的各个年份和月份
    mdlist=calc_yearly_date_range(start,end)
    if len(mdlist) == 0:
        print("Error #5(plot_rar_annual): start/end dates inappropriate")
        return None          

    #用于保存risk premium和rar
    print("\nCalculating yearly",rar_type,"from",start,"to",end,"......")
    rarfunc=rar_type+'_portfolio'
    rars=pd.DataFrame(columns=('YR','rp','rar'))
    for i in range(0,len(mdlist)):
        start=mdlist[i][0]
        YR=start.strftime("%Y")
        print(YR,end=' ')
        end=mdlist[i][1]
        rar,rp=eval(rarfunc)(portfolio,start,end,printout=False)
        
        row=pd.Series({'YR':YR,'rp':rp,'rar':rar})
        rars=rars.append(row,ignore_index=True)         
    print("completed.")
    rars.set_index('YR',inplace=True)    
    #绘图
    import matplotlib.pyplot as plt
    plt.plot(rars['rp'],label='risk_premium',c='blue',marker='*',ls=':',lw=3)
    plt.plot(rars['rar'],label=rar_type,c='r',lw=3,marker='o')
    plt.axhline(y=0.0,color='black',linestyle=':',lw=1) 
    titletxt="投资组合的风险调整收益"
    plt.title(titletxt)
    plt.ylabel('收益率(%)')
    plt.xticks(rotation=45)
    plt.legend(loc='best')
    
    import datetime as dt; today=dt.date.today() 
    footnote="数据来源：雅虎财经，"+str(today)
    plt.xlabel(footnote)
    
    plt.show()

    return


if __name__=='__main__':
    portfolio={'Market':('US','^GSPC'),'VIPS':0.1,'PDD':0.2,'JD':0.3,'BABA':0.4}
    plot_rar_annual(portfolio,'2013-01-01','2019-06-30','treynor_ratio') 

    portfolio={'Market':('US','^GSPC'),'AAPL':1.0}
    plot_rar_annual(portfolio,'2015-01-01','2017-12-31','sharpe_ratio')       
#==============================================================================





