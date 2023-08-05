# -*- coding: utf-8 -*-
"""
本模块功能：SIAT公共基础函数
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2019年7月16日
最新修订日期：2020年3月28日
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
def ectranslate(eword):
    """
    翻译英文专业词汇至中文，便于显示或绘图时输出中文而不是英文。
    输入：英文专业词汇。输出：中文专业词汇
    """
    import pandas as pd
    ecdict=pd.DataFrame([
        ['High','最高价'],['Low','最低价'],['Open','开盘价'],['Close','收盘价'],
        ['Volume','成交量'],['Adj Close','调整收盘价'],['Daily Ret','日收益率'],
        ['Daily Ret%','日收益率%'],['Daily Adj Ret','调整日收益率'],
        ['Daily Adj Ret%','调整日收益率%'],['log(Daily Ret)','对数日收益率'],
        ['log(Daily Adj Ret)','对数调整日收益率'],['Weekly Ret','周收益率'],
        ['Weekly Ret%','周收益率%'],['Weekly Adj Ret','周调整收益率'],
        ['Weekly Adj Ret%','周调整收益率%'],['Monthly Ret','月收益率'],
        ['Monthly Ret%','月收益率%'],['Monthly Adj Ret','月调整收益率'],
        ['Monthly Adj Ret%','月调整收益率%'],['Quarterly Ret','季度收益率'],
        ['Quarterly Ret%','季度收益率%'],['Quarterly Adj Ret','季度调整收益率'],
        ['Quarterly Adj Ret%','季度调整收益率%'],['Annual Ret','年收益率'],
        ['Annual Ret%','年收益率%'],['Annual Adj Ret','年调整收益率'],
        ['Annual Adj Ret%','年调整收益率%'],['Exp Ret','扩展收益率'],
        ['Exp Ret%','扩展收益率%'],['Exp Adj Ret','扩展调整收益率'],
        ['Exp Adj Ret%','扩展调整收益率%'],
        
        ['Weekly Price Volatility','周股价波动风险'],
        ['Weekly Adj Price Volatility','周调整股价波动风险'],
        ['Monthly Price Volatility','月股价波动风险'],
        ['Monthly Adj Price Volatility','月调整股价波动风险'],
        ['Quarterly Price Volatility','季股价波动风险'],
        ['Quarterly Adj Price Volatility','季调整股价波动风险'],
        ['Annual Price Volatility','年股价波动风险'],
        ['Annual Adj Price Volatility','年调整股价波动风险'],  
        ['Exp Price Volatility','扩展股价波动风险'], 
        ['Exp Adj Price Volatility','扩展调整股价波动风险'],
        
        ['Weekly Ret Volatility','周收益率波动风险'],
        ['Weekly Ret Volatility%','周收益率波动风险%'],
        ['Weekly Adj Ret Volatility','周调整收益率波动风险'],
        ['Weekly Adj Ret Volatility%','周调整收益率波动风险%'],
        ['Monthly Ret Volatility','月收益率波动风险'],
        ['Monthly Ret Volatility%','月收益率波动风险%'],
        ['Monthly Adj Ret Volatility','月调整收益波动风险'],
        ['Monthly Adj Ret Volatility%','月调整收益波动风险%'],
        ['Quarterly Ret Volatility','季收益率波动风险'],
        ['Quarterly Ret Volatility%','季收益率波动风险%'],
        ['Quarterly Adj Ret Volatility','季调整收益率波动风险'],
        ['Quarterly Adj Ret Volatility%','季调整收益率波动风险%'],
        ['Annual Ret Volatility','年收益率波动风险'],
        ['Annual Ret Volatility%','年收益率波动风险%'],
        ['Annual Adj Ret Volatility','年调整收益率波动风险'], 
        ['Annual Adj Ret Volatility%','年调整收益率波动风险%'], 
        ['Exp Ret Volatility','扩展收益率波动风险'], 
        ['Exp Ret Volatility%','扩展收益率波动风险%'],
        ['Exp Adj Ret Volatility','扩展调整收益率波动风险'],        
        ['Exp Adj Ret Volatility%','扩展调整收益率波动风险%'],
        
        ['Weekly Ret LPSD','周收益率波动损失风险'],
        ['Weekly Ret LPSD%','周收益率波动损失风险%'],
        ['Weekly Adj Ret LPSD','周调整收益率波动损失风险'],
        ['Weekly Adj Ret LPSD%','周调整收益率波动损失风险%'],
        ['Monthly Ret LPSD','月收益率波动损失风险'],
        ['Monthly Ret LPSD%','月收益率波动损失风险%'],
        ['Monthly Adj Ret LPSD','月调整收益波动损失风险'],
        ['Monthly Adj Ret LPSD%','月调整收益波动损失风险%'],
        ['Quarterly Ret LPSD','季收益率波动损失风险'],
        ['Quarterly Ret LPSD%','季收益率波动损失风险%'],
        ['Quarterly Adj Ret LPSD','季调整收益率波动损失风险'],
        ['Quarterly Adj Ret LPSD%','季调整收益率波动损失风险%'],
        ['Annual Ret LPSD','年收益率波动损失风险'],
        ['Annual Ret LPSD%','年收益率波动损失风险%'],
        ['Annual Adj Ret LPSD','年调整收益率波动损失风险'], 
        ['Annual Adj Ret LPSD%','年调整收益率波动损失风险%'], 
        ['Exp Ret LPSD','扩展收益率波动损失风险'], 
        ['Exp Ret LPSD%','扩展收益率波动损失风险%'],
        ['Exp Adj Ret LPSD','扩展调整收益率波动损失风险'],        
        ['Exp Adj Ret LPSD%','扩展调整收益率波动损失风险%'],
        
        ['ESGscore','ESG风险'],['ESGpercentile','ESG风险行业分位数%'],['ESGperformance','ESG风险评价'],
        ['EPscore','环保风险'],['EPpercentile','环保风险分位数%'],
        ['CSRscore','社会责任风险'],['CSRpercentile','社会责任风险分位数%'],
        ['CGscore','公司治理风险'],['CGpercentile','公司治理风险分位数%'],
        ['Peer Group','业务分类'],['Count','数目']
        
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
        ['QCOM','高通'],['BAC','美国银行'],
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
    print(codetranslate('000002.SZ'))
    print(codetranslate('9988.HK'))

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
def tickers_check(tickers, source="yahoo"):
    """
    检查证券代码列表，对于大陆证券代码、香港证券代码和东京证券代码进行修正。
    输入：证券代码列表tickers，数据来源source。
    上交所证券代码后缀为.SS或.SH或.ss或.sh，深交所证券代码为.SZ或.sz
    港交所证券代码后缀为.HK，截取数字代码后4位
    东京证交所证券代码后缀为.T，截取数字代码后4位
    source：yahoo或tushare
    返回：证券代码列表，字母全部转为大写。若是大陆证券返回True否则返回False。
    若选择yahoo数据源，上交所证券代码转为.SS；
    若选择tushare数据源，上交所证券代码转为.SH
    """
    #检查列表是否为空
    if tickers[0] is None:
        print("*** 错误#1(tickers_check)，空的证券代码列表:",tickers)
        return None         
    
    tickers_new=[]
    for t in tickers:
        _, t_new = ticker_check(t, source=source)
        tickers_new.append(t_new)
    
    #返回：基于数据源/交易所格式修正后的证券代码
    return tickers_new

#测试各种情形
if __name__=='__main__':
    tickers=tickers_check(["600519.sh","000002.sz"],"yahoo")
    print(tickers)
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
def date_adjust(basedate, adjust=0):
    """
    功能：将给定日期向前或向后调整特定的天数
    输入：基础日期，需要调整的天数。
    basedate: 基础日期。
    adjust：需要调整的天数，负数表示向前调整，正数表示向后调整。
    输出：调整后的日期。
    """
    #检查基础日期的合理性
    import pandas as pd    
    try:
        bd=pd.to_datetime(basedate)
    except:
        print("*** 错误#1(date_adjust)，无效的日期:",basedate)
        return None

    #调整日期
    from datetime import timedelta
    nd = bd+timedelta(days=adjust)    
    
    #重新提取日期
    newdate=nd.date()   
    return str(newdate)
 
if __name__ =="__main__":
    basedate='2020-3-17' 
    adjust=-365    
    newdate = date_adjust(basedate, adjust)
    print(newdate)    

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
def get_prices(tickers, fromdate, todate):
    """
    功能：从雅虎财经抓取多个证券价格或指数价格
    输入：证券代码列表，开始日期，结束日期
    tickers: 证券代码列表。
    大陆股票代码加上后缀.SZ或.SS，港股代码去掉前导0加后缀.HK
    fromdate: 样本开始日期。
    todate: 样本结束日期。既可以是今天日期，也可以是一个历史日期   
    
    输出：多元证券价格序列，按照日期升序排列。原汁原味的抓取数据
    *Close price adjusted for splits.
    **Adjusted close price adjusted for both dividends and splits. 
    """

    #仅支持证券代码列表
    if not isinstance(ticker,list):
        print("*** 错误#1(get_price)，仅支持证券代码列表!")        
        return None     
    
    #校验证券代码列表
    tickers_new=tickers_check(tickers, source="yahoo")

    #检查期间合理性
    result,start,end=check_period(fromdate,todate)
    if result is None:
        print("*** 错误#2(get_prices)，无效的日期或期间!")        
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
        prices=data.DataReader(tickers_new,'yahoo',start,end)
    except:
        print("*** 错误#4(get_prices)，抓取证券价格失败!")        
        print("信息:",tickers_new,fromdate,todate) 
        print("可能的原因:")
        print("  1)网络连接不稳定.")
        print("  2)证券代码无效.")
        print("  3)所选证券期间内暂停交易或退市.")
        return None            
    
    #抓取未失败但返回空数据
    if len(prices)==0:
        print("*** 错误#5(get_prices)，未能抓取到有效价格信息!")
        return None         
    
    #生成字符串型的日期字段date，方便以后使用
    prices['datetmp']=prices.index
    prices['date']=prices['datetmp'].apply(lambda x:x.date())
    del prices['datetmp']

    #加入星期几
    price["Weekday"]=price.index.weekday + 1  
    
    return prices

if __name__ =="__main__":
    df=get_prices(['000002.SZ','600266.SS'],'2020-1-1','2020-3-31')
    print(price['Close']['^HSI'].tail(10))

#==============================================================================
def calc_daily_return(pricedf):
    """
    功能：基于从雅虎财经抓取的单个证券价格数据集计算其日收益率
    输入：从雅虎财经抓取的单个证券价格数据集pricedf，基于收盘价或调整收盘价进行计算
    输出：证券日收益率序列，按照日期升序排列。
    """
    import numpy as np    
    #计算算术日收益率：基于收盘价
    pricedf["Daily Ret"]=pricedf['Close'].pct_change()
    pricedf["Daily Ret%"]=pricedf["Daily Ret"]*100.0
    
    #计算算术日收益率：基于调整收盘价
    pricedf["Daily Adj Ret"]=pricedf['Adj Close'].pct_change()
    pricedf["Daily Adj Ret%"]=pricedf["Daily Adj Ret"]*100.0
    
    #计算对数日收益率
    pricedf["log(Daily Ret)"]=np.log(pricedf["Daily Ret"]+1)
    pricedf["log(Daily Adj Ret)"]=np.log(pricedf["Daily Adj Ret"]+1)
    
    return pricedf 
    

if __name__ =="__main__":
    ticker='AAPL'
    fromdate='2018-1-1'
    todate='2020-3-16'
    pricedf=get_price(ticker, fromdate, todate)
    drdf=calc_daily_return(pricedf)    
    

#==============================================================================
def calc_rolling_return(drdf, period="Weekly"):
    """
    功能：基于单个证券的日收益率数据集, 计算其滚动期间收益率
    输入：
    单个证券的日收益率数据集drdf。
    期间类型period，默认为每周。
    输出：期间滚动收益率序列，按照日期升序排列。
    """
    #检查period类型
    periodlist = ["Weekly","Monthly","Quarterly","Annual"]
    if not (period in periodlist):
        print("*** 错误#1(calc_rolling_return)，仅支持期间类型：",periodlist)
        return None

    #换算期间对应的实际交易天数
    perioddays=[5,21,63,252]
    rollingnum=perioddays[periodlist.index(period)]    
    
    #计算滚动收益率：基于收盘价
    retname1=period+" Ret"
    retname2=period+" Ret%"
    import numpy as np
    drdf[retname1]=np.exp(drdf["log(Daily Ret)"].rolling(rollingnum).sum())-1.0
    drdf[retname2]=drdf[retname1]*100.0
    
    #计算滚动收益率：基于调整收盘价
    retname3=period+" Adj Ret"
    retname4=period+" Adj Ret%"
    drdf[retname3]=np.exp(drdf["log(Daily Adj Ret)"].rolling(rollingnum).sum())-1.0
    drdf[retname4]=drdf[retname3]*100.0
    
    return drdf

if __name__ =="__main__":
    ticker='000002.SZ'
    period="Weekly"
    prdf=calc_rolling_return(drdf, period) 
    prdf=calc_rolling_return(drdf, "Monthly")
    prdf=calc_rolling_return(drdf, "Quarterly")
    prdf=calc_rolling_return(drdf, "Annual")

#==============================================================================
def calc_expanding_return(drdf,basedate):
    """
    功能：基于日收益率数据集，从起始日期开始到结束日期的扩展窗口收益率序列。
    输入：
    日收益率数据集drdf。
    输出：期间累计收益率序列，按照日期升序排列。
    """
    
    #计算累计收益率：基于收盘价
    retname1="Exp Ret"
    retname2="Exp Ret%"
    import numpy as np
    drdf[retname1]=np.exp(drdf[drdf.index >= basedate]["log(Daily Ret)"].expanding(min_periods=1).sum())-1.0
    drdf[retname2]=drdf[retname1]*100.0  
    
    #计算累计收益率：基于调整收盘价
    retname3="Exp Adj Ret"
    retname4="Exp Adj Ret%"
    drdf[retname3]=np.exp(drdf[drdf.index >= basedate]["log(Daily Adj Ret)"].expanding(min_periods=1).sum())-1.0
    drdf[retname4]=drdf[retname3]*100.0  
    
    return drdf

if __name__ =="__main__":
    ticker='000002.SZ'
    basedate="2019-1-1"
    erdf=calc_expanding_return(prdf,basedate)  

#==============================================================================
def rolling_price_volatility(df, period="Weekly"):
    """
    功能：基于单个证券价格的期间调整标准差, 计算其滚动期间价格风险
    输入：
    单个证券的日价格数据集df。
    期间类型period，默认为每周。
    输出：期间滚动价格风险序列，按照日期升序排列。
    """
    #检查period类型
    periodlist = ["Weekly","Monthly","Quarterly","Annual"]
    if not (period in periodlist):
        print("*** 错误#1(calc_rolling_volatility)，仅支持期间类型：",periodlist)
        return None

    #换算期间对应的实际交易天数
    perioddays=[5,21,63,252]
    rollingnum=perioddays[periodlist.index(period)]    
    
    #计算滚动期间的调整标准差价格风险：基于收盘价
    retname1=period+" Price Volatility"
    import numpy as np
    df[retname1]=df["Close"].rolling(rollingnum).apply(lambda x: np.std(x,ddof=1)/np.mean(x)*np.sqrt(len(x)))
    
    #计算滚动期间的调整标准差价格风险：基于调整收盘价
    retname3=period+" Adj Price Volatility"
    df[retname3]=df["Adj Close"].rolling(rollingnum).apply(lambda x: np.std(x,ddof=1)/np.mean(x)*np.sqrt(len(x)))
    
    return df

if __name__ =="__main__":
    period="Weekly"
    df=get_price('000002.SZ','2018-1-1','2020-3-16')
    vdf=rolling_price_volatility(df, period) 

#==============================================================================
def expanding_price_volatility(df,basedate):
    """
    功能：基于日价格数据集，从起始日期开始到结束日期调整价格风险的扩展窗口序列。
    输入：
    日价格数据集df。
    输出：期间扩展调整价格风险序列，按照日期升序排列。
    """
    
    #计算扩展窗口调整价格风险：基于收盘价
    retname1="Exp Price Volatility"
    import numpy as np
    df[retname1]=df[df.index >= basedate]["Close"].expanding(min_periods=1).apply(lambda x: np.std(x,ddof=1)/np.mean(x)*np.sqrt(len(x)))
    
    #计算扩展窗口调整价格风险：基于调整收盘价
    retname3="Exp Adj Price Volatility"
    df[retname3]=df[df.index >= basedate]["Adj Close"].expanding(min_periods=1).apply(lambda x: np.std(x,ddof=1)/np.mean(x)*np.sqrt(len(x)))
    
    return df

if __name__ =="__main__":
    df=get_price('000002.SZ','2018-1-1','2020-3-16')    
    evdf=expanding_price_volatility(df)  


#==============================================================================
def rolling_ret_volatility(df, period="Weekly"):
    """
    功能：基于单个证券的期间收益率, 计算其滚动收益率波动风险
    输入：
    单个证券的期间收益率数据集df。
    期间类型period，默认为每周。
    输出：滚动收益率波动风险序列，按照日期升序排列。
    """
    #检查period类型
    periodlist = ["Weekly","Monthly","Quarterly","Annual"]
    if not (period in periodlist):
        print("*** 错误#1(rolling_ret_volatility)，仅支持期间类型：",periodlist)
        return None

    #换算期间对应的实际交易天数
    perioddays=[5,21,63,252]
    rollingnum=perioddays[periodlist.index(period)]    
    
    #计算滚动标准差：基于普通收益率
    periodret=period+" Ret"
    retname1=period+" Ret Volatility"
    retname2=retname1+'%'
    import numpy as np
    df[retname1]=df[periodret].rolling(rollingnum).apply(lambda x: np.std(x,ddof=1))
    df[retname2]=df[retname1]*100.0
    
    #计算滚动标准差：基于调整收益率
    periodadjret=period+" Adj Ret"
    retname3=period+" Adj Ret Volatility"
    retname4=retname3+'%'
    df[retname3]=df[periodadjret].rolling(rollingnum).apply(lambda x: np.std(x,ddof=1))
    df[retname4]=df[retname3]*100.0
    
    return df

if __name__ =="__main__":
    period="Weekly"
    pricedf=get_price('000002.SZ','2018-1-1','2020-3-16')
    retdf=calc_daily_return(pricedf)
    vdf=rolling_ret_volatility(retdf, period) 

#==============================================================================
def expanding_ret_volatility(df,basedate):
    """
    功能：基于日收益率数据集，从起始日期basedate开始的收益率波动风险扩展窗口序列。
    输入：
    日收益率数据集df。
    输出：扩展调整收益率波动风险序列，按照日期升序排列。
    """
    
    #计算扩展窗口调整收益率波动风险：基于普通收益率
    retname1="Exp Ret Volatility"
    retname2="Exp Ret Volatility%"
    import numpy as np
    df[retname1]=df[df.index >= basedate]["Daily Ret"].expanding(min_periods=1).apply(lambda x: np.std(x,ddof=1)*np.sqrt(len(x)))
    df[retname2]=df[retname1]*100.0
    
    #计算扩展窗口调整收益率风险：基于调整收益率
    retname3="Exp Adj Ret Volatility"
    retname4="Exp Adj Ret Volatility%"
    df[retname3]=df[df.index >= basedate]["Daily Adj Ret"].expanding(min_periods=1).apply(lambda x: np.std(x,ddof=1)*np.sqrt(len(x)))
    df[retname4]=df[retname3]*100.0
    
    return df

if __name__ =="__main__":
    basedate='2019-1-1'
    pricedf=get_price('000002.SZ','2018-1-1','2020-3-16')    
    retdf=calc_daily_return(pricedf)
    evdf=expanding_ret_volatility(retdf,'2019-1-1')  

#==============================================================================
def lpsd(ds):
    """
    功能：基于给定数据序列计算其下偏标准差。
    输入：
    数据序列ds。
    输出：序列的下偏标准差。
    """
    import numpy as np
    #若序列长度为0则直接返回数值型空值
    if len(ds) == 0: return np.NaN
    
    #求均值
    import numpy as np
    miu=np.mean(ds)
    
    #计算根号内的下偏平方和
    sum=0; ctr=0
    for s in list(ds):
        if s < miu:
            sum=sum+pow((s-miu),2)
            ctr=ctr+1
    
    #下偏标准差
    if ctr > 1:
        result=np.sqrt(sum/(ctr-1))
    elif ctr == 1: result=np.NaN
    else: result=np.NaN
        
    return result
    
if __name__ =="__main__":
    df=get_price("000002.SZ","2020-1-1","2020-3-16")
    print(lpsd(df['Close']))

#==============================================================================
def rolling_ret_lpsd(df, period="Weekly"):
    """
    功能：基于单个证券期间收益率, 计算其滚动收益率损失风险。
    输入：
    单个证券的期间收益率数据集df。
    期间类型period，默认为每周。
    输出：滚动收益率的下偏标准差序列，按照日期升序排列。
    """
    #检查period类型
    periodlist = ["Weekly","Monthly","Quarterly","Annual"]
    if not (period in periodlist):
        print("*** 错误#1(rolling_ret_lpsd)，仅支持期间类型：",periodlist)
        return None

    #换算期间对应的实际交易天数
    perioddays=[5,21,63,252]
    rollingnum=perioddays[periodlist.index(period)]    
    
    #计算滚动下偏标准差：基于普通收益率
    periodret=period+" Ret"
    retname1=period+" Ret LPSD"
    retname2=retname1+'%'
    #import numpy as np
    df[retname1]=df[periodret].rolling(rollingnum).apply(lambda x: lpsd(x))
    df[retname2]=df[retname1]*100.0
    
    #计算滚动下偏标准差：基于调整收益率
    periodadjret=period+" Adj Ret"
    retname3=period+" Adj Ret LPSD"
    retname4=retname3+'%'
    df[retname3]=df[periodadjret].rolling(rollingnum).apply(lambda x: lpsd(x))
    df[retname4]=df[retname3]*100.0
    
    return df

if __name__ =="__main__":
    period="Weekly"
    pricedf=get_price('000002.SZ','2018-1-1','2020-3-16')
    retdf=calc_daily_return(pricedf)
    vdf=rolling_ret_lpsd(retdf, period) 

#==============================================================================
def expanding_ret_lpsd(df,basedate):
    """
    功能：基于日收益率数据集，从起始日期basedate开始的收益率损失风险扩展窗口序列。
    输入：
    日收益率数据集df。
    输出：扩展调整收益率波动风险序列，按照日期升序排列。
    """
    
    #计算扩展窗口调整收益率下偏标准差：基于普通收益率
    retname1="Exp Ret LPSD"
    retname2=retname1+'%'
    import numpy as np
    df[retname1]=df[df.index >= basedate]["Daily Ret"].expanding(min_periods=1).apply(lambda x: lpsd(x)*np.sqrt(len(x)))
    df[retname2]=df[retname1]*100.0
    
    #计算扩展窗口调整下偏标准差：基于调整收益率
    retname3="Exp Adj Ret LPSD"
    retname4=retname3+'%'
    df[retname3]=df[df.index >= basedate]["Daily Adj Ret"].expanding(min_periods=1).apply(lambda x: lpsd(x)*np.sqrt(len(x)))
    df[retname4]=df[retname3]*100.0
    
    return df

if __name__ =="__main__":
    basedate='2019-1-1'
    pricedf=get_price('000002.SZ','2018-1-1','2020-3-16')    
    retdf=calc_daily_return(pricedf)
    evdf=expanding_ret_lpsd(retdf,'2019-1-1')  
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
               power=0,datatag1=False,datatag2=False,yscalemax=5,zeroline=False):
    """
    功能：绘制两个证券的折线图。如果power=0不绘制趋势图，否则绘制多项式趋势图
    假定：数据表有索引，且已经按照索引排序
    输入：
    证券1：数据表df1，证券代码ticker1，列名1，列名标签1；
    证券2：数据表df2，证券代码ticker2，列名2，列名标签2；
    标题titletxt，脚注footnote；是否在图中标记数据datatag；趋势图的多项式次数power
    输出：若两个证券数据均值差距超过yscalemax，绘制双轴折线图，否则绘制同轴折线图
    返回值：无
    """
    #算法需要不断改进：判断两个证券的数据均值差距
    #mean1=df1[colname1].mean(); mean2=df2[colname2].mean()
    #yscale=abs(mean1 - mean2)/min(abs(mean1),abs(mean2))
    max1=df1[colname1].max(); min1=df1[colname1].min()
    max2=df2[colname2].max(); min2=df2[colname2].min()
    #判断最高点的差距：
    try:
        yscale1=max(abs(max1),abs(max2))/min(abs(max1),abs(max2))
    except:
        yscale1=1
    #判断最低点的差距：
    try:
        yscale2=max(abs(min1),abs(min2))/min(abs(min1),abs(min2))
    except:
        yscale2=1
    #取差距的较大者
    yscale=max(yscale1,yscale2)
    
    if yscale > yscalemax: uniyaxis=False  #双y轴        
    else: uniyaxis=True   #单一y轴  
    
    if uniyaxis:            
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





#==============================================================================
