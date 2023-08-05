# -*- coding: utf-8 -*-
"""
本模块功能：证券资产的流动性风险与溢价
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2019年6月18日
最新修订日期：2020年7月16日
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
def ectranslate(eword):
    """
    翻译英文专业词汇至中文，便于显示或绘图时输出中文而不是英文。
    输入：英文专业词汇。输出：中文专业词汇
    """
    import pandas as pd
    ecdict=pd.DataFrame([
        ['roll_spread','罗尔价差比率'],['amihud_illiquidity','阿米胡德非流动性'],
        ['ps_liquidity','P-S流动性'],
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
def tickertranslate(code):
    """
    翻译证券代码为证券名称。
    输入：证券代码。输出：证券名称
    """
    import pandas as pd
    codedict=pd.DataFrame([
        ['000002.SZ','万科地产A股'],['600266.SS','北京城建A股'],
        ['600519.SS','茅台酒A股'],['601398.SS','工商银行A股'],
        ['601939.SS','建设银行A股'],['601288.SS','农业银行A股'],
        ['601988.SS','中国银行A股'],['601857.SS','中国石油A股'],
        ['000651.SZ','格力电器A股'],['000333.SZ','美的集团A股'],
        
        ['AAPL','苹果'],['MSFT','微软'],['AMZN','亚马逊'],['JD','京东'],
        ['FB','脸书'],['BABA','阿里巴巴美股'],['PTR','中石油美股'],
        ['ZM','ZOOM'],['C','花旗集团'],['F','福特汽车'],['GOOG','谷歌'],
        ['KO','可口可乐'],['PEP','百事可乐'],['IBM','国际商用机器'],
        ['HPQ','惠普'],['BA','波音'],['GM','通用汽车'],['INTC','英特尔'],
        ['AMD','超威半导体'],['NVDA','英伟达'],['PFE','辉瑞制药'],
        ['BILI','哔哩哔哩'],['TAL','好未来'],['EDU','新东方'],['VIPS','唯品会'],
        ['SINA','新浪网'],['BIDU','百度'],['NTES','网易'],['PDD','拼多多'],
        ['COST','好事多'],['WMT','沃尔玛'],['DIS','迪士尼'],['GS','高盛'],
        ['QCOM','高通'],['BAC','美国银行'],['TWTR','推特'],
        ['JPM','摩根大通'],['WFC','富国银行'],['GS','高盛集团'],['MS','摩根示丹利'],
        ['USB','美国合众银行'],['TD','道明银行'],['PNC','PNC金融'],['BK','纽约梅隆银行'],
        
        ['0700.HK','港股腾讯控股'],['9988.HK','阿里巴巴港股'],
        ['1810.HK','港股小米'],['0992.HK','港股联想'],['1398.HK','工商银行港股'],
        ['0939.HK','建设银行港股'],['1288.HK','农业银行港股'],
        ['3988.HK','中国银行港股'],['0857.HK','中国石油港股'],
        ['0005.HK','港股汇丰控股'],['2888.HK','港股渣打银行'],
        
        ['6758.T','日股索尼'],['4911.T','日股资生堂'],['8306.T','三菱日联金融'],
        ['7203.T','日股丰田汽车'],['7267.T','日股本田汽车'],
        ['7201.T','日股日产汽车'],['8411.T','日股瑞穗金融'],['7182.T','日本邮政银行'],
        
        ['TCS.NS','印度股塔塔咨询'],['005930.KS','韩股三星电子'],
        ['UBSG.SW','瑞士股瑞银'],['UG.PA','法国股标致雪铁龙'],
        ['DAI.DE','德国股奔驰汽车'],
        ['BMW.DE','德国股宝马汽车']
        ], columns=['code','codename'])

    try:
        codename=codedict[codedict['code']==code]['codename'].values[0]
    except:
        #未查到翻译词汇，返回原词
        codename=code
   
    return codename

if __name__=='__main__':
    code='GOOG'
    print(tickertranslate('000002.SZ'))
    print(tickertranslate('9988.HK'))

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
        return False,None,None         
    try:
        end=pd.to_datetime(todate)
    except:
        print("Error #2(check_period): invalid date:",todate)
        return False,None,None          
    if start > end:
        print("Error #3(check_period): invalid period: from",fromdate,"to",todate)
        return False,None,None     

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
def get_portfolio_prices(portfolio,fromdate,todate):
    """
    功能：抓取投资组合portfolio的每日价值和FF3各个因子
    输入：投资组合portfolio，开始日期，结束日期
    fromdate: 样本开始日期。格式：'YYYY-MM-DD'
    todate: 样本结束日期。既可以是今天日期，也可以是一个历史日期    
    
    输出：投资组合的价格序列，按照日期升序排列
    """
    
    #仅为调试用的函数入口参数，正式使用前需要注释掉！
    """
    portfolio={'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    fromdate='2019-8-1'
    todate  ='2019-8-31'
    """
    #解构投资组合
    _,mktidx,tickerlist,sharelist=decompose_portfolio(portfolio)
    
    #检查股票列表个数与份额列表个数是否一致
    if len(tickerlist) != len(sharelist):
        print("#Error(get_portfolio_prices): numbers of stocks and shares mismatch.")
        return None        
    
    #从雅虎财经抓取股票价格
    p=get_prices_yahoo(tickerlist,fromdate,todate)
    
    import pandas as pd
    #计算投资组合的开盘价
    op=p['Open']
    #计算投资组合的价值
    oprice=pd.DataFrame(op.dot(sharelist))
    oprice.rename(columns={0: 'Open'}, inplace=True)    

    #计算投资组合的收盘价
    cp=p['Close']
    #计算投资组合的价值
    cprice=pd.DataFrame(cp.dot(sharelist))
    cprice.rename(columns={0: 'Close'}, inplace=True) 
    
    #计算投资组合的调整收盘价
    acp=p['Adj Close']
    #计算投资组合的价值
    acprice=pd.DataFrame(acp.dot(sharelist))
    acprice.rename(columns={0: 'Adj Close'}, inplace=True) 
    
    #计算投资组合的交易量
    vol=p['Volume']
    #计算投资组合的价值
    pfvol=pd.DataFrame(vol.dot(sharelist))
    pfvol.rename(columns={0: 'Volume'}, inplace=True) 
    
    #计算投资组合的交易金额
    for t in tickerlist:
        p['Amount',t]=p['Close',t]*p['Volume',t]
    amt=p['Amount']
    #计算投资组合的价值
    pfamt=pd.DataFrame(amt.dot(sharelist))
    pfamt.rename(columns={0: 'Amount'}, inplace=True) 

    #合成开盘价、收盘价、调整收盘价、交易量和交易金额
    pf1=pd.merge(oprice,cprice,how='inner',left_index=True,right_index=True)    
    pf2=pd.merge(pf1,acprice,how='inner',left_index=True,right_index=True)
    pf3=pd.merge(pf2,pfvol,how='inner',left_index=True,right_index=True)
    pf4=pd.merge(pf3,pfamt,how='inner',left_index=True,right_index=True)
    pf4['Ret%']=pf4['Close'].pct_change()*100.0

    #获得期间的市场收益率：假设无风险收益率非常小，可以忽略
    m=get_prices_yahoo(mktidx,fromdate,todate)
    m['Mkt-RF']=m['Close'].pct_change()*100.0
    m['RF']=0.0
    rf_df=m[['Mkt-RF','RF']]
    
    #合并pf4与rf_df
    prices=pd.merge(pf4,rf_df,how='left',left_index=True,right_index=True)

    #提取日期和星期几
    prices['Date']=prices.index.strftime("%Y-%m-%d")
    prices['Weekday']=prices.index.weekday+1

    prices['Portfolio']=str(tickerlist)
    prices['Shares']=str(sharelist)
    prices['Adjustment']=prices.apply(lambda x: \
          False if x['Close']==x['Adj Close'] else True, axis=1)

    pfdf=prices[['Portfolio','Shares','Date','Weekday', \
                 'Open','Close','Adj Close','Adjustment', \
                'Volume','Amount','Ret%','Mkt-RF','RF']]  

    return pfdf      


#==============================================================================
def sample_selection(df,start,end):
    """
    功能：根据日期范围start/end选择数据集df的子样本，并返回子样本
    """
    flag,start2,end2=check_period(start,end)
    df_sub=df[df.index >= start2]
    df_sub=df_sub[df_sub.index <= end2]
    
    return df_sub
    
if __name__=='__main__':
    portfolio={'Market':('US','^GSPC'),'AAPL':1.0}
    market,mktidx,tickerlist,sharelist=decompose_portfolio(portfolio)
    start='2020-1-1'; end='2020-3-31'
    pfdf=get_portfolio_prices(tickerlist,sharelist,start,end)
    start2='2020-1-10'; end2='2020-3-18'
    df_sub=sample_selection(pfdf,start2,end2)    
    
#==============================================================================        
def calc_roll_spread(pfdf):
    """
    功能：从给定的股票或投资组合portfolio的数据集df中按期间计算罗尔价差
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合价格df，单一数据集有利于计算滚动指数
    输出：罗尔价差%
    注意：不包括爬虫部分
    """
    sp=pfdf.copy()
    #计算价格序列的价差
    sp['dP']=sp['Close'].diff()
    sp['dP_1']=sp['dP'].shift(1)
    sp2=sp[['Close','dP','dP_1']].copy()      
    sp2.dropna(inplace=True)
    if len(sp2) == 0: return None

    #计算指标，注意cov函数的结果是一个矩阵
    import numpy as np
    rs_cov=abs(np.cov(sp2['dP'],sp2['dP_1'])[0,1])    
    #计算价格均值
    p_mean=sp2['Close'].mean()    
    rs=2*np.sqrt(rs_cov)/p_mean 

    rs_pct=round(rs*100.0,4)
    return rs_pct

if __name__=='__main__':
    pf={'Market':('US','^GSPC'),'AAPL':1.0}
    start='2020-1-1'; end='2020-3-31'
    pfdf=get_portfolio_prices(pf,start,end)
    rs=calc_roll_spread(pfdf)

#==============================================================================    
def roll_spread_portfolio(portfolio,start,end,printout=True):
    """
    功能：按期间计算一个投资组合的罗尔价差，并输出结果
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合，开始日期，结束日期，是否打印结果(默认打印)
    输出：罗尔价差%
    注意：含爬虫部分，调用其他函数
    """

    #仅为测试用
    #portfolio={'Market':('US','^GSPC'),'EDU':0.7,'TAL':0.3}
    #start='2019-06-01'
    #end  ='2019-06-30'

    #检查日期和期间的合理性
    flag,start2,end2=check_period(start,end)
    if not flag:
        print("#Error(roll_spread_portfolio): invalid period for,", start, end)
        return None
    
    #抓取股票价格，构建投资组合价格
    sp=get_portfolio_prices(portfolio,start2,end2)

    #计算罗尔价差指标
    rs_pct=calc_roll_spread(sp)
    
    #打印报告
    if printout == True:
        date_start=str(sp.index[0].year)+'-'+str(sp.index[0].month)+ \
            '-'+str(sp.index[0].day)
        date_end=str(sp.index[-1].year)+'-'+str(sp.index[-1].month)+ \
            '-'+str(sp.index[-1].day)            
        print("\n===== 投资组合的流动性风险 =====")
        print("投资组合:",portfolio)
        print("计算期间:",date_start,"to",date_end, \
                  "(可用日期)")
        print("罗尔价差%:",rs_pct)
    
    return rs_pct

if __name__=='__main__':
    pf_aapl={'Market':('US','^GSPC'),'AAPL':1.0}
    rs_aapl=roll_spread_portfolio(pf_aapl,'2019-01-01','2019-01-31')    
    
    pfA={'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    rsA=roll_spread_portfolio(pfA,'2019-01-01','2019-01-31')    
    
#==============================================================================        
def calc_amihud_illiquidity(pfdf):
    """
    功能：从给定的投资组合pfdf中计算阿米胡德非流动性
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合价格pfdf
    输出：阿米胡德非流动性
    注意：不包括爬虫部分
    """
    sp=pfdf.copy()
    #计算阿米胡德非流动性
    sp2=sp[['Ret%','Amount']]
    sp2=sp2.dropna()
    if len(sp2) == 0: return None
    
    import numpy as np
    sp2['Ret/Amt']=np.abs(sp2['Ret%'])/np.log10(sp2['Amount'])
    amihud=round(sp2['Ret/Amt'].mean(),4)
    
    return amihud

if __name__=='__main__':
    pf={'Market':('US','^GSPC'),'AAPL':1.0}
    start='2020-1-1'; end='2020-3-31'
    pfdf=get_portfolio_prices(pf,start,end)
    amihud=calc_amihud_illiquidity(pfdf)

#==============================================================================    
def amihud_illiquidity_portfolio(portfolio,start,end,printout=True):
    """
    功能：按天计算一个投资组合的阿米胡德非流动性指数
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合，开始日期，结束日期，是否打印结果
    输出：阿米胡德非流动性指数
    注意：含爬虫部分，调用其他函数
    """

    #仅为测试用
    #portfolio={'Market':('US','^GSPC'),'EDU':0.7,'TAL':0.3}
    #start='2019-06-01'
    #end  ='2019-06-30'

    #检查日期和期间的合理性
    flag,start2,end2=check_period(start,end)
    if not flag:
        print("#Error(amihud_illiquidity_portfolio): invalid period for,", start, end)
        return None

    #抓取股票价格，构建投资组合价格
    sp=get_portfolio_prices(portfolio,start2,end2)

    #计算指标
    amihud=calc_amihud_illiquidity(sp)
    
    #打印报告
    if printout == True:
        date_start=str(sp.index[0].year)+'-'+str(sp.index[0].month)+ \
            '-'+str(sp.index[0].day)
        date_end=str(sp.index[-1].year)+'-'+str(sp.index[-1].month)+ \
            '-'+str(sp.index[-1].day)            
        print("\n===== 投资组合的流动性风险 =====")
        print("投资组合:",portfolio)
        print("计算期间:",date_start,"to",date_end, \
                  "(可用日期)")
        print("阿米胡德非流动性:",amihud,"(对数算法)")
    
    return amihud

if __name__=='__main__':
    pf_aapl={'Market':('US','^GSPC'),'AAPL':1.0}
    amihud_aapl=amihud_illiquidity_portfolio(pf_aapl,'2019-01-01','2019-01-31')    

#==============================================================================        
def calc_ps_liquidity(pfdf):
    """
    功能：从给定的投资组合pfdf中计算帕斯托-斯坦堡流动性，原始公式
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合价格df
    输出：帕斯托-斯坦堡流动性
    注意：不包括爬虫部分
    """
    reg=pfdf.copy()
    
    reg['Ret-RF']=reg['Ret%']-reg['RF']
    reg['Ret-RF_1']=reg['Ret-RF'].shift(1)
    reg['Mkt']=reg['Mkt-RF']+reg['RF']
    reg['Mkt_1']=reg['Mkt'].shift(1)
    reg['Amount_1']=reg['Amount'].shift(1)
    
    import numpy as np
    reg1=reg[['Ret-RF','Mkt_1','Ret-RF_1','Amount_1']]
    reg1=reg1.dropna()
    if len(reg1) == 0: return None
    reg1['signAmt_1']=np.sign(reg1['Ret-RF_1'])*np.log10(reg1['Amount_1'])
    reg2=reg1[['Ret-RF','Mkt_1','signAmt_1']].copy()
    
    #回归前彻底删除带有NaN和inf等无效值的样本，否则回归中可能出错
    reg2=reg2[~reg2.isin([np.nan, np.inf, -np.inf]).any(1)].dropna()
    if len(reg2) == 0: return None
    
    ##计算帕斯托-斯坦堡流动性PSL
    import statsmodels.api as sm
    y=reg2['Ret-RF']
    X=reg2[['Mkt_1','signAmt_1']]
    X1=sm.add_constant(X)
    results=sm.OLS(y,X1).fit() 
    [alpha,beta,psl]=results.params
    
    return round(psl,4)

if __name__=='__main__':
    pf={'Market':('US','^GSPC'),'AAPL':1.0}
    start='2020-1-1'; end='2020-3-31'
    pfdf=get_portfolio_prices(pf,start,end)
    psl=calc_ps_liquidity(pfdf)

#==============================================================================        
def calc_ps_liquidity_modified(pfdf):
    """
    功能：从给定的投资组合pfdf中计算修正的帕斯托-斯坦堡流动性
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合价格df
    输出：修正的帕斯托-斯坦堡流动性，符号内含
    注意：不包括爬虫部分
    """
    reg=pfdf.copy()
    
    reg['Ret-RF']=reg['Ret%']-reg['RF']
    reg['Ret-RF_1']=reg['Ret-RF'].shift(1)
    reg['Mkt']=reg['Mkt-RF']+reg['RF']
    reg['Mkt_1']=reg['Mkt'].shift(1)
    reg['Amount_1']=reg['Amount'].shift(1)
    
    import numpy as np
    reg1=reg[['Ret-RF','Mkt_1','Ret-RF_1','Amount_1']]
    reg1=reg1.dropna()
    if len(reg1) == 0: return None
    
    #修正psl，符号内含
    #reg1['signAmt_1']=np.sign(reg1['Ret-RF_1'])*np.log10(reg1['Amount_1'])
    reg1['signAmt_1']=np.log10(reg1['Amount_1'])
    reg2=reg1[['Ret-RF','Mkt_1','signAmt_1']].copy()
    
    #回归前彻底删除带有NaN和inf等无效值的样本，否则回归中可能出错
    reg2=reg2[~reg2.isin([np.nan, np.inf, -np.inf]).any(1)].dropna()
    if len(reg2) == 0: return None
    
    ##计算帕斯托-斯坦堡流动性PSL
    import statsmodels.api as sm
    y=reg2['Ret-RF']
    X=reg2[['Mkt_1','signAmt_1']]
    X1=sm.add_constant(X)
    results=sm.OLS(y,X1).fit() 
    [alpha,beta,psl]=results.params
    
    return round(psl,4)

if __name__=='__main__':
    pf={'Market':('US','^GSPC'),'AAPL':1.0}
    start='2020-1-1'; end='2020-3-31'
    pfdf=get_portfolio_prices(pf,start,end)
    psl=calc_ps_liquidity_modified(pfdf)

#==============================================================================    
def ps_liquidity_portfolio(portfolio,start,end,printout=True):
    """
    功能：按天计算一个投资组合的帕斯托-斯坦堡流动性
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合，开始日期，结束日期，是否打印结果
    输出：帕斯托-斯坦堡流动性
    注意：含爬虫部分，调用其他函数
    """

    #仅为测试用
    #portfolio={'Market':('US','^GSPC'),'EDU':0.7,'TAL':0.3}
    #start='2019-06-01'
    #end  ='2019-06-30'

    #检查日期和期间的合理性
    flag,start2,end2=check_period(start,end)
    if not flag:
        print("#Error(amihud_illiquidity_portfolio): invalid period for,", start, end)
        return None

    #抓取股票价格，构建投资组合价格
    sp=get_portfolio_prices(portfolio,start2,end2)

    #计算帕斯托-斯坦堡流动性
    psl=calc_ps_liquidity(sp)
    
    #打印报告
    if printout == True:
        date_start=str(sp.index[0].year)+'-'+str(sp.index[0].month)+ \
            '-'+str(sp.index[0].day)
        date_end=str(sp.index[-1].year)+'-'+str(sp.index[-1].month)+ \
            '-'+str(sp.index[-1].day)            
        print("\n===== 投资组合的流动性风险 =====")
        print("投资组合:",portfolio)
        print("计算期间:",date_start,"to",date_end, \
                  "(可用日期)")
        print("Pastor-Stambaugh流动性:",psl,"(对数算法)")
    
    return psl

if __name__=='__main__':
    pf_aapl={'Market':('US','^GSPC'),'AAPL':1.0}
    psl_aapl=ps_liquidity_portfolio(pf_aapl,'2019-01-01','2019-01-31')    

    
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
    if (power > 0) and (power <= len(df)):
        try:
            #生成行号，借此将横轴的日期数量化，以便拟合
            df['id']=range(len(df))
        
            #设定多项式拟合，power为多项式次数
            import numpy as np
            parameter = np.polyfit(df.id, df[colname], power)
            f = np.poly1d(parameter)
            plt.plot(df.index, f(df.id),"r--", label="趋势线")
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
    
    plot_line(pfdf,'Close',"收盘价","价格","万科股票","数据来源：雅虎财经",power=4)

#==============================================================================
def plot_liquidity_monthly(portfolio,start,end,liquidity_type):
    """
    功能：将资产流动性指标逐月绘图对比
    输入：投资组合，开始/结束日期，流动性指标类别
    输出：流动性指标的逐月数据框
    显示：按月绘图投资组合的流动性指标
    """
    #仅为测试用
    #portfolio={'Market':('US','^GSPC'),'JD':0.3,'BABA':0.7}
    #start='2019-01-01'
    #end='2019-03-31'
    #liquidity_type='roll_spread'    

    #检查日期和期间的合理性
    flag,start2,end2=check_period(start,end)
    if not flag:
        print("#Error(plot_liquidity_monthly): invalid period for,", start, end)
        return None

    #检查：支持的liquidity_type
    liquidity_list=['roll_spread','amihud_illiquidity','ps_liquidity']
    if liquidity_type not in liquidity_list:
        print("#Error(plot_liquidity_monthly): not supported liquidity type")
        print("Supported liquidity type:",liquidity_list)              
        return None         

    #抓取投资组合信息
    print("\n... Searching for portfolio information ...")
    df=get_portfolio_prices(portfolio,start,end)

    #拆分start/end之间的各个年份和月份
    mdlist=calc_monthly_date_range(start,end)
    if len(mdlist) == 0:
        print("#Error(plot_liquidity_monthly): start/end dates inappropriate")
        return None          

    #用于保存流动性指标
    import pandas as pd
    print("... Calculating monthly",liquidity_type,"...")
    rarfunc='calc_'+liquidity_type
    rars=pd.DataFrame(columns=('YM','rar'))
    zeroline=False
    for i in range(0,len(mdlist)):
        startym=mdlist[i][0]
        YM=startym.strftime("%Y-%m")
        #print(YM,end=' ')
        endym=mdlist[i][1]
        pfdf=sample_selection(df,startym,endym)
        rar=eval(rarfunc)(pfdf)
        if rar is None: continue
        
        if rar < 0: zeroline=True
        row=pd.Series({'YM':YM,'rar':rar})
        rars=rars.append(row,ignore_index=True)         
    #print("completed.")
    rars.set_index('YM',inplace=True)    
    
    #绘图
    colname='rar'
    collabel=ectranslate(liquidity_type)
    ylabeltxt=ectranslate(liquidity_type)
    titletxt="证券流动性风险的月度指标"
    
    _,_,tickerlist,sharelist=decompose_portfolio(portfolio)
    if len(tickerlist)==1:
        product=str(tickerlist)
    else:
        product=str(tickerlist)+' in '+str(sharelist)
    import datetime as dt; today=dt.date.today()
    footnote="证券="+product+"\n数据来源：雅虎财经, "+str(today)
    datatag=False
    power=4
    plot_line(rars,colname,collabel,ylabeltxt,titletxt,footnote,datatag, \
              power,zeroline)

    return rars


if __name__=='__main__':
    portfolio={'Market':('US','^GSPC'),'AAPL':1.0}
    start='2019-01-01'; end='2020-6-30'
    liquidity_type='roll_spread'
    liq1=plot_liquidity_monthly(portfolio,start,end,liquidity_type)       
    liquidity_type='amihud_illiquidity'
    liq2=plot_liquidity_monthly(portfolio,start,end,liquidity_type) 
    liquidity_type='ps_liquidity'
    liq3=plot_liquidity_monthly(portfolio,start,end,liquidity_type) 

    pf1={'Market':('US','^GSPC'),'VIPS':0.1,'PDD':0.2,'JD':0.3,'BABA':0.4}
    al1=plot_liquidity_monthly(pf1,start,end,'roll_spread') 

    pf2={'Market':('US','^GSPC'),'^GSPC':1.0}
    al2=plot_liquidity_monthly(pf2,start,end,'roll_spread')
    al3=plot_liquidity_monthly(pf2,start,end,'amihud_illiquidity')
    al4=plot_liquidity_monthly(pf2,start,end,'ps_liquidity')

#==============================================================================
def plot_liquidity_annual(portfolio,start,end,liquidity_type):
    """
    功能：将流动性指标逐年绘图对比
    输入：投资组合，开始/结束日期，流动性指标类别
    输出：流动性指标的逐年数据框
    显示：按年绘图投资组合的流动性指标
    """
    #仅为测试用
    #portfolio={'Market':('US','^GSPC'),'TSLA':1.0}
    #start='2009-07-01'
    #end='2019-06-30'
    #liquidity_type='roll_spread'    

    #检查日期和期间的合理性
    flag,start2,end2=check_period(start,end)
    if not flag:
        print("#Error(plot_liquidity_annual): invalid period for,", start, end)
        return None

    #检查：支持的liquidity_type
    liquidity_list=['roll_spread','amihud_illiquidity','ps_liquidity']
    if liquidity_type not in liquidity_list:
        print("#Error(plot_liquidity_annual): not supported liquidity type")
        print("Supported liquidity type:",liquidity_list)              
        return None         

    #抓取投资组合信息
    print("\n... Searching for portfolio information ...")
    df=get_portfolio_prices(portfolio,start,end)

    #拆分start/end之间的各个年份和月份
    mdlist=calc_yearly_date_range(start,end)
    if len(mdlist) == 0:
        print("#Error(plot_liquidity_annual): start/end dates inappropriate")
        return None          

    #用于保存指标
    print("... Calculating annual",liquidity_type,"...")
    rarfunc='calc_'+liquidity_type
    import pandas as pd
    rars=pd.DataFrame(columns=('YR','liquidity'))
    zeroline=False   
    for i in range(0,len(mdlist)):
        startyr=mdlist[i][0]
        YR=startyr.strftime("%Y")
        #print(YR,end=' ')
        endyr=mdlist[i][1]
        pfdf=sample_selection(df,startyr,endyr)
        rar=eval(rarfunc)(pfdf)        
        if rar is not None:     
            if rar < 0: zeroline=True
            row=pd.Series({'YR':YR,'liquidity':rar})
            rars=rars.append(row,ignore_index=True)         
    rars.set_index('YR',inplace=True)    
    
    #绘图
    colname='liquidity'
    collabel=ectranslate(liquidity_type)
    ylabeltxt=ectranslate(liquidity_type)
    titletxt="证券流动性风险的年度指标"

    _,_,tickerlist,sharelist=decompose_portfolio(portfolio)
    if len(tickerlist)==1:
        product=str(tickerlist)
    else:
        product=str(tickerlist)+' in '+str(sharelist)
    
    import datetime as dt; today=dt.date.today()
    footnote="证券="+product+"\n数据来源：雅虎财经, "+str(today)    
    datatag=False
    power=4
    plot_line(rars,colname,collabel,ylabeltxt,titletxt,footnote,datatag, \
              power,zeroline)

    return rars


if __name__=='__main__':
    portfolio={'Market':('US','^GSPC'),'AAPL':1.0}
    start='2010-01-01'
    end='2019-12-31'
    liquidity_type='roll_spread'
    al1=plot_liquidity_annual(portfolio,start,end,liquidity_type)  
    
    portfolio={'Market':('US','^GSPC'),'VIPS':0.1,'PDD':0.2,'JD':0.3,'BABA':0.4}
    start='2013-01-01'
    end='2019-06-30'    
    al2=plot_liquidity_annual(portfolio,start,end,liquidity_type) 


#==============================================================================
def draw_liquidity(liqs):
    """
    功能：绘制滚动窗口曲线
    输入：滚动数据df，内含投资组合Portfolio和指数名称Type
    """
    
    import matplotlib.pyplot as plt    
    plt.figure(figsize=(8,5))

    portfolio=liqs['Portfolio'][0]
    colname='Ratio'
    collabel=ectranslate(liqs['Type'][0])
    ylabeltxt=ectranslate(liqs['Type'][0])
    titletxt="证券流动性风险的滚动趋势"
    
    _,_,tickerlist,sharelist=decompose_portfolio(portfolio)
    if len(tickerlist)==1:
        product=str(tickerlist)
    else:
        product=str(tickerlist)+' in '+str(sharelist)
    
    import datetime as dt; today=dt.date.today()
    footnote="证券="+product+"\n数据来源：雅虎财经, "+str(today)    
    datatag=False
    power=4
    
    zeroline=False
    neg_liqs=liqs[liqs['Ratio'] < 0]
    if len(neg_liqs) > 0: zeroline=True
    
    plot_line(liqs,colname,collabel,ylabeltxt,titletxt,footnote,datatag, \
              power,zeroline)

    return

#==============================================================================
def liquidity_rolling(portfolio,start,end,liquidity_type, \
                      window=30,graph=True):
    """
    功能：滚动计算一个投资组合的流动性风险
    投资组合的结构：{'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    输入：投资组合，开始日期，结束日期，指数名称，滚动窗口宽度(天数)
    输出：流动性风险
    注意：因需要滚动计算，开始和结束日期之间需要拉开距离
    """

    #检查日期和期间的合理性
    flag,start2,end2=check_period(start,end)
    if not flag:
        print("#Error(plot_liquidity_monthly): invalid period for,", start, end)
        return None

    #检查：支持的liquidity_type
    liquidity_list=['roll_spread','amihud_illiquidity','ps_liquidity']
    if liquidity_type not in liquidity_list:
        print("#Error(plot_liquidity_monthly): not supported liquidity type")
        print("Supported liquidity type:",liquidity_list)              
        return None         

    #抓取投资组合信息
    print("\n... Searching information for portfolio:",portfolio)
    reg=get_portfolio_prices(portfolio,start,end)
    
    #滚动计算
    print("... Calculating its rolling ratios:",liquidity_type)
    import pandas as pd; import numpy as np
    datelist=reg.index.to_list()
    calc_func='calc_'+liquidity_type
    
    liqs=pd.DataFrame(columns=('Portfolio','Date','Ratio','Type')) 
    for i in np.arange(0,len(reg)):
        i1=i+window
        if i1 >= len(reg): break
        
        #构造滚动窗口
        windf=reg[reg.index >= datelist[i]]
        windf=windf[windf.index < datelist[i1]]
        #print(i,datelist[i],i1,datelist[i1],len(windf))
        
        #使用滚动窗口计算
        liq=eval(calc_func)(windf)
        
        #记录计算结果
        row=pd.Series({'Portfolio':portfolio,'Date':datelist[i1-1],'Ratio':liq,'Type':liquidity_type})
        liqs=liqs.append(row,ignore_index=True)        
    
    liqs.set_index(['Date'],inplace=True) 
    
    #第6步：绘图
    if graph == True:
        draw_liquidity(liqs)
    
    return liqs


if __name__=='__main__':
    portfolio={'Market':('US','^GSPC'),'AAPL':0.5,'MSFT':0.3,'IBM':0.2}
    start='2019-1-1'
    end='2019-6-30'
    window=30
    graph=True    
    liquidity_type='roll_spread'
    liqs=liquidity_rolling(portfolio,start,end,liquidity_type)


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
    plt.figure(figsize=(8,6))
    #设置绘图时的汉字显示
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体
    # 解决保存图像时'-'显示为方块的问题
    plt.rcParams['axes.unicode_minus'] = False  
    
    #证券1：先绘制折线图
    plt.plot(df1.index,df1[colname1],'-',label=tickertranslate(str(ticker1))+'('+label1+')', \
             linestyle='-',linewidth=3)
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
            plt.plot(df1.index, f(df1.id),"r--", label=tickertranslate(str(ticker1))+"(趋势线)")
        except: pass
    
    #证券2：先绘制折线图
    plt.plot(df2.index,df2[colname2],'-',label=tickertranslate(str(ticker2))+'('+label2+')', \
             color='blue',linestyle='-.',linewidth=3)
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
            plt.plot(df2.index, f(df2.id),"r:", label=tickertranslate(str(ticker2))+"(趋势线)")
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
    pass

#==============================================================================
def compare_liquidity_rolling(portfolio1,portfolio2,start,end,liquidity_type,window=30):
    """
    功能：比较两个投资组合portfolio1和portfolio2在start至end期间的流动性指标liquidity_type
    """
    #投资组合1
    liqs1=liquidity_rolling(portfolio1,start,end,liquidity_type, \
                      window=window,graph=False)
    colname1='Ratio'
    label1=ectranslate(liquidity_type)
    datatag1=False
    
    zeroline=False
    neg_liqs1=liqs1[liqs1['Ratio'] < 0]
    if len(neg_liqs1) > 0: zeroline=True
   
    #投资组合2
    liqs2=liquidity_rolling(portfolio2,start,end,liquidity_type, \
                      window=window,graph=False)
    colname2='Ratio'
    label2=ectranslate(liquidity_type)
    datatag2=False
    
    zeroline=False
    neg_liqs2=liqs2[liqs2['Ratio'] < 0]
    if len(neg_liqs2) > 0: zeroline=True

    #绘图    
    ylabeltxt=ectranslate(liquidity_type)
    titletxt="证券流动性风险的滚动趋势比较"
    
    _,_,tickerlist1,sharelist1=decompose_portfolio(portfolio1)
    if len(tickerlist1)==1:
        product1=str(tickerlist1)
    else:
        product1=str(tickerlist1)+' in '+str(sharelist1)    
    _,_,tickerlist2,sharelist2=decompose_portfolio(portfolio2)
    if len(tickerlist2)==1:
        product2=str(tickerlist2)
    else:
        product2=str(tickerlist2)+' in '+str(sharelist2)     
    
    import datetime as dt; today=dt.date.today()
    footnote="证券1="+product1+"\n证券2="+product2+ \
            "\n数据来源：雅虎财经, "+str(today)
    power=4

    plot_line2_coaxial(liqs1,"证券1",colname1,label1, \
                       liqs2,"证券2",colname2,label2, \
                ylabeltxt,titletxt,footnote,power,datatag1,datatag2,zeroline)
    return
    
    

if __name__ =="__main__":
    portfolio1={'Market':('US','^GSPC'),'PDD':1.0}
    portfolio2={'Market':('US','^GSPC'),'BILI':1.0}
    start='2020-1-01'
    end='2020-6-30'
    window=21
    graph=False
    liquidity_type='roll_spread'   
    compare_liquidity_rolling(portfolio1,portfolio2,start,end,liquidity_type)

    liquidity_type='amihud_illiquidity'   
    compare_liquidity_rolling(portfolio1,portfolio2,start,end,liquidity_type)    

    liquidity_type='ps_liquidity'   
    compare_liquidity_rolling(portfolio1,portfolio2,start,end,liquidity_type)    
#==============================================================================


#==============================================================================


