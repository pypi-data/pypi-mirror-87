# -*- coding: utf-8 -*-
"""
本模块功能：绘制折线图
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2020年9月16日
最新修订日期：2020年9月16日
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
def draw_lines(df,y_label,x_label,axhline_value,axhline_label,title_txt, \
               data_label=True):
    """
    函数功能：根据df的内容绘制折线图
    输入参数：
    df：数据框。有几个字段就绘制几条折现。必须索引，索引值将作为X轴标记点
    axhline_label: 水平辅助线标记。如果为空值则不绘制水平辅助线
    axhline_value: 水平辅助线的y轴位置
    y_label：y轴标记
    x_label：x轴标记
    title_txt：标题。如需多行，中间用\n分割
    
    输出：
    绘制折线图
    无返回数据
    """
    import matplotlib.pyplot as plt

    #取得df字段名列表
    collist=df.columns.values.tolist()  
    
    #绘制折线图    
    for c in collist:
        plt.plot(df[c],label=c,lw=3)
        #为折线加数据标签
        if data_label==True:
            for a,b in zip(df.index,df[c]):
                plt.text(a,b+0.02,str(round(b,2)), \
                         ha='center',va='bottom',fontsize=7)
    
    #绘制水平辅助线
    if axhline_label !="":
        plt.axhline(y=axhline_value,label=axhline_label,color='green',linestyle=':')  
    
    #坐标轴标记
    plt.ylabel(y_label,fontweight='bold')
    if x_label != "":
        plt.xlabel(x_label,fontweight='bold')
    #图示标题
    plt.title(title_txt,fontweight='bold')
    plt.xticks(rotation=45)
    plt.legend(loc='best')
    plt.show()
    
    return    
    
if __name__=='__main__':
    title_txt="Stock Risk \nCAPM Beta Trends"
    draw_lines(df,"market line",1.0,"Beta coefficient","",title_txt)    

#==============================================================================
def plot_barh(df,colname,titletxt,footnote,datatag=True, \
              colors=['r','g','b','c','m','y','aquamarine','dodgerblue', \
              'deepskyblue','silver'],tag_offset=0.05):
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
    
    #xmin=int(min(df[colname]))
    xmin0=min(df[colname])
    if xmin0 > 0:
        xmin=xmin0*0.8
    else:
        xmin=xmin0*1.05
    #xmax=(int(max(df[colname]))+1)*1.1
    xmax0=max(df[colname])
    if xmax0 > 0:
        xmax=xmax0*1.2
    else:
        xmax=xmax0*0.8
    plt.xlim([xmin,xmax])
    
    tag_off=tag_offset * xmax
    for x,y in enumerate(list(df[colname])):
        #plt.text(y+0.1,x,'%s' % y,va='center')
        plt.text(y+tag_off,x,'%s' % y,va='center')

    yticklist=list(df.index)
    yticknames=[]
    for yt in yticklist:
        ytname=codetranslate(yt)
        yticknames=yticknames+[ytname]
    plt.yticks(df.index,yticknames)

    plt.show(); plt.close()
    
    return

#==============================================================================
def ectranslate(eword):
    """
    翻译英文词汇至中文，便于显示或绘图时输出中文而不是英文。
    输入：英文词汇。输出：中文词汇
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
        
        ['ESGscore','ESG风险'],['ESGpercentile','ESG风险行业分位数%'], \
        ['ESGperformance','ESG风险评价'],
        ['EPscore','环保风险'],['EPpercentile','环保风险分位数%'],
        ['CSRscore','社会责任风险'],['CSRpercentile','社会责任风险分位数%'],
        ['CGscore','公司治理风险'],['CGpercentile','公司治理风险分位数%'],
        ['Peer Group','业务分类'],['Count','数目'],
        
        ['zip','邮编'],['sector','领域'],['fullTimeEmployees','全职员工数'],
        ['longBusinessSummary','业务介绍'],['city','城市'],['phone','电话'],
        ['state','州/省'],['country','国家/地区'],['companyOfficers','高管'],
        ['website','官网'],['address1','地址1'],['industry','行业'],
        ['previousClose','上个收盘价'],['regularMarketOpen','正常市场开盘价'],
        ['twoHundredDayAverage','200天均价'],['fax','传真'], 
        ['trailingAnnualDividendYield','年化股利率TTM'],
        ['payoutRatio','股息支付率'],['volume24Hr','24小时交易量'],
        ['regularMarketDayHigh','正常市场日最高价'],
        ['averageDailyVolume10Day','10天平均日交易量'],['totalAssets','总资产'],
        ['regularMarketPreviousClose','正常市场上个收盘价'],
        ['fiftyDayAverage','50天平均股价'],
        ['trailingAnnualDividendRate','年化每股股利金额TTM'],['open','当日开盘价'],
        ['averageVolume10days','10日平均交易量'],['expireDate','失效日'],
        ['yield','收益率'],['dividendRate','每股股利金额'],
        ['exDividendDate','股利除息日'],['beta','贝塔系数'],
        ['startDate','开始日期'],['regularMarketDayLow','正常市场日最低价'],
        ['priceHint','价格提示'],['currency','交易币种'],
        ['trailingPE','市盈率TTM'],['regularMarketVolume','正常市场交易量'],
        ['marketCap','市值'],['averageVolume','平均交易量'],
        ['priceToSalesTrailing12Months','市销率TTM'],['dayLow','当日最低价'],
        ['ask','卖出价'],['askSize','卖出价股数'],['volume','当日交易量'],
        ['fiftyTwoWeekHigh','52周最高价'],['forwardPE','预期市盈率'],
        ['fiveYearAvgDividendYield','5年平均股利率'],
        ['fiftyTwoWeekLow','52周最低价'],['bid','买入价'],
        ['tradeable','今日是否可交易'],['dividendYield','股利率'],
        ['bidSize','买入价股数'],['dayHigh','当日最高价'],
        ['exchange','交易所'],['shortName','简称'],['longName','全称'],
        ['exchangeTimezoneName','交易所时区'],
        ['exchangeTimezoneShortName','交易所时区简称'],['quoteType','证券类别'],
        ['symbol','证券代码'],['messageBoardId','证券留言板编号'],
        ['market','证券市场'],['annualHoldingsTurnover','一年內转手率'],
        ['enterpriseToRevenue','企业价值/销售收入'],['beta3Year','3年贝塔系数'],
        ['profitMargins','净利润率'],['enterpriseToEbitda','企业价值/EBITDA'],
        ['52WeekChange','52周股价变化率'],['morningStarRiskRating','晨星风险评级'],
        ['forwardEps','预期每股收益'],['revenueQuarterlyGrowth','季营收增长率'],
        ['sharesOutstanding','流通在外股数'],['fundInceptionDate','基金成立日'],
        ['annualReportExpenseRatio','年报费用比率'],['bookValue','每股净资产'],
        ['sharesShort','卖空股数'],['sharesPercentSharesOut','卖空股数/流通股数'],
        ['lastFiscalYearEnd','上个财年截止日期'],
        ['heldPercentInstitutions','机构持股比例'],
        ['netIncomeToCommon','归属普通股股东净利润'],['trailingEps','每股收益TTM'],
        ['lastDividendValue','上次股利价值'],
        ['SandP52WeekChange','标普指数52周变化率'],['priceToBook','市净率'],
        ['heldPercentInsiders','内部人持股比例'],['priceToBook','市净率'],
        ['nextFiscalYearEnd','下个财年截止日期'],
        ['mostRecentQuarter','上个财季截止日期'],['shortRatio','空头净额比率'],
        ['sharesShortPreviousMonthDate','上月做空日期'],
        ['floatShares','可交易股数'],['enterpriseValue','企业价值'],
        ['threeYearAverageReturn','3年平均回报率'],['lastSplitDate','上个拆分日期'],
        ['lastSplitFactor','上次拆分比例'],
        ['earningsQuarterlyGrowth','季盈余增长率'],['dateShortInterest','做空日期'],
        ['pegRatio','市盈率与增长比率'],['shortPercentOfFloat','空头占可交易股票比例'],
        ['sharesShortPriorMonth','上月做空股数'],
        ['fiveYearAverageReturn','5年平均回报率'],['regularMarketPrice','正常市场价'],
        ['logo_url','商标图标网址']    
        
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
        
        ['000012.SS','上证国债指数'],['000013.SS','上证企业债指数'],
        ['000832.SS','中证可转债指数'],['399481.SZ','深证企业债指数'],
        
        ['^IRX','三个月美债利率'],['^FVX','五年美债利率'],
        ['^TNX','十年期美债利率'],['^TYX','三十年美债利率'],
        
        ["510050.SS",'上证50ETF基金'],['510880.SS','上证红利ETF基金'],
        ["510180.SS",'上证180ETF基金'],['159901.SZ','深证100ETF基金'],
        ["159902.SZ",'深证中小板ETF基金'],['159901.SZ','深证100ETF基金'],
        ["SPY",'SPDR SP500 ETF'],['SPYD','SPDR SP500 Div ETF'],
        ["SPYG",'SPDR SP500 Growth ETF'],['SPYV','SPDR SP500 Value ETF'],
        ["VOO",'Vanguard SP500 ETF'],['VOOG','Vanguard SP500 Growth ETF'],
        ["VOOV",'Vanguard SP500 Value ETF'],['IVV','iShares SP500 ETF'],        
        ["DGT",'SPDR Global Dow ETF'],['ICF','iShares C&S REIT ETF'], 
        ["FRI",'FT S&P REIT Index Fund'],
        
        ["HG=F",'COMEX Copper Future'],["CL=F",'NYM Crude Oil Future'],
        ["S=F",'CBT Soybean Future'],["C=F",'CBT Corn Future'],
        ["ES=F",'CME SP500 Future'],["YM=F",'CBT DJI Future'],
        ["NQ=F",'CME NASDAQ100 Future'],["RTY=F",'Russell 2K Future'],
        ["ZB=F",'US T-Bond Future'],["ZT=F",'2y US T-Note Future'],
        ["ZF=F",'5y US T-Note Future'],["ZN=F",'10y US T-Note Future'],
        
        ['000002.SZ','万科地产A股'],['600266.SS','北京城建A股'],
        ['600519.SS','茅台酒A股'],
        ['601398.SS','工商银行A股'],['601939.SS','建设银行A股'],
        ['601288.SS','农业银行A股'],['601988.SS','中国银行A股'],
        ['601857.SS','中国石油A股'],
        ['000651.SZ','格力电器A股'],['000333.SZ','美的集团A股'],
        
        ['AAPL','苹果'],['MSFT','微软'],['AMZN','亚马逊'],['JD','京东美股'],
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
        ['Vipshop','唯品会'],['Amazon','亚马逊'],['Alibaba','阿里巴巴美股'],
        ['eBay','易贝'],['Pinduoduo','拼多多'],
        ['Apple','苹果'],['Berkshire','伯克希尔'],['Microsoft','微软'],
        ['LLY','礼来制药'],['Eli','礼来制药'],
        ['JNJ','强生制药'],['Johnson','强生制药'],
        ['VRTX','福泰制药'],['Vertex','福泰制药'],
        ['PFE','辉瑞制药'],['Pfizer','辉瑞制药'],
        ['MRK','默克制药'],['Merck','默克制药'],
        ['NVS','诺华制药'],['Novartis','诺华制药'],
        ['AMGN','安进制药'],['Amgen','安进制药'],
        ['SNY','赛诺菲制药'],['Sanofi','赛诺菲制药'],
        ['NBIX','神经分泌生物'],['Neurocrine','神经分泌生物'],
        ['REGN','再生元制药'],['Regeneron','再生元制药'],
        ['PRGO','培瑞克制药'],['Perrigo','培瑞克制药'],
        
        
        ['0700.HK','港股腾讯控股'],['9988.HK','阿里巴巴港股'],['9618.HK','京东港股'],
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
