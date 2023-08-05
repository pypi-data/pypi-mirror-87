# -*- coding: utf-8 -*-
"""
本模块功能：债券，基础层函数
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2020年1月8日
最新修订日期：2020年5月10日
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
def macD0(c,y,F,n):
    """
    功能：计算债券的麦考莱久期期数
    输入参数：
    1、每期票面利率c
    2、每期到期收益率y，市场利率，贴现率
    3、票面价值F
    3、到期期数n
    输出：麦考莱久期的期数（不一定是年数）
    """
    #生成期数序列
    import pandas as pd
    t=pd.Series(range(1,(n+1)))
    
    #计算未来票息和面值的现值
    p=sum(c*F/(1+y)**t)+F/(1+y)**len(t)
    #计算未来票息和面值的加权现值
    wp=sum(c*F*t/(1+y)**t)+F*len(t)/(1+y)**len(t)
    
    return wp/p    

if __name__=='__main__':
    c=0.08/2; y=0.1/2; n=6; F=100
    print(macD0(c,y,F,n))
#==============================================================================
def macD(cr,ytm,nyears,ctimes=2,fv=100):
    """
    功能：计算债券的麦考莱久期年数
    输入参数：
    1、年票面利率cr
    2、年到期收益率ytm，市场利率，贴现率
    3、到期年数nyears
    4、每年付息次数ctimes
    5、票面价值fv
    输出：麦考莱久期（年数）
    """
    
    #转换为每期付息的参数
    c=cr/ctimes; y=ytm/ctimes; F=fv; n=nyears*ctimes
    
    #计算麦考莱久期期数
    d=macD0(c,y,F,n)
    #转换为麦考莱久期年数：年数=期数/每年付息次数
    D=round(d/ctimes,2)
    
    return D                    

if __name__=='__main__':
    cr=0.08; ytm=0.1; nyears=3; ctimes=2; fv=100
    print(macD(cr,ytm,nyears))

#==============================================================================
def MD0(c,y,F,n):
    """
    功能：计算债券的修正久期期数
    输入参数：
    1、每期票面利率c
    2、每期到期收益率y，市场利率，贴现率
    3、票面价值F
    4、到期期数n
    输出：修正久期期数（不一定是年数）
    """
    #修正麦考莱久期
    md=macD0(c,y,F,n)/(1+y)
    
    return md

if __name__=='__main__':
    c=0.08/2; y=0.1/2; n=6; F=100
    print(MD0(c,y,F,n))    
    
#==============================================================================
def MD(cr,ytm,nyears,ctimes=2,fv=100):
    """
    功能：计算债券的修正久期年数
    输入参数：
    1、年票面利率cr
    2、年到期收益率ytm，市场利率，贴现率
    3、到期年数nyears
    4、每年付息次数ctimes
    5、票面价值fv
    输出：修正久期（年数）
    """
    
    #转换为每期付息的参数
    c=cr/ctimes; y=ytm/ctimes; F=fv; n=nyears*ctimes
    
    #计算久期期数
    d=MD0(c,y,F,n)
    #转换为久期年数：年数=期数/每年付息次数
    D=round(d/ctimes,2)
    
    return D                    

if __name__=='__main__':
    cr=0.08; ytm=0.1; nyears=3; ctimes=2; fv=100
    print(MD(cr,ytm,nyears))


    
#==============================================================================
def DD0(c,y,F,n):
    """
    功能：计算债券的美元久期期数
    输入参数：
    1、每期票面利率c
    2、每期到期收益率y，市场利率，贴现率
    3、票面价值F
    4、到期期数n
    输出：美元久期期数（不一定是年数）
    """
    #生成期数序列
    import pandas as pd
    t=pd.Series(range(1,(n+1)))
    
    #计算现值
    p=sum(c*F/(1+y)**t)+F/(1+y)**len(t)
    #美元久期期数
    dd=MD0(c,y,F,n)*p
    
    return dd

if __name__=='__main__':
    c=0.08/2; y=0.1/2; n=6; F=100
    print(DD0(c,y,F,n))    
    
#==============================================================================    
def DD(cr,ytm,nyears,ctimes=2,fv=100):
    """
    功能：计算债券的美元久期年数
    输入参数：
    1、年票面利率cr
    2、年到期收益率ytm，市场利率，贴现率
    3、到期年数nyears
    4、每年付息次数ctimes
    5、票面价值fv
    输出：美元久期（年数）
    """
    
    #转换为每期付息的参数
    c=cr/ctimes; y=ytm/ctimes; F=fv; n=nyears*ctimes
    
    #计算久期期数
    d=DD0(c,y,F,n)
    #转换为久期年数：年数=期数/每年付息次数
    D=round(d/ctimes,2)
    
    return D                    

if __name__=='__main__':
    cr=0.08; ytm=0.1; nyears=3; ctimes=2; fv=100
    print(DD(cr,ytm,nyears))

#==============================================================================    
def ED0(c,y,F,n,per):
    """
    功能：计算债券的有效久期期数
    输入参数：
    1、每期票面利率c
    2、每期到期收益率y，市场利率，贴现率
    3、票面价值F
    4、到期期数n
    5、到期收益率的变化幅度，1个基点=0.01%=0.0001
    输出：有效久期期数（不一定是年数）
    """
    #生成期数序列
    import pandas as pd
    t=pd.Series(range(1,(n+1)))
    
    #计算到期收益率变化前的现值
    p0=sum(c*F/(1+y)**t)+F/(1+y)**len(t)
    #计算到期收益率增加一定幅度后的现值
    p1=sum(c*F/(1+y+per)**t)+F/(1+y+per)**len(t)
    #计算到期收益率减少同等幅度后的现值
    p2=sum(c*F/(1+y-per)**t)+F/(1+y-per)**len(t)
    #久期期数
    ed=(p2-p1)/(2*p0*per)
    
    return ed

if __name__=='__main__':
    c=0.08/2; y=0.1/2; n=6; F=100; per=0.001/2
    print(ED0(c,y,F,n,per))    
    
#==============================================================================    
def ED(cr,ytm,nyears,peryear,ctimes=2,fv=100):
    """
    功能：计算债券的有效久期年数
    输入参数：
    1、年票面利率cr
    2、年到期收益率ytm，市场利率，贴现率
    3、到期年数nyears
    4、年到期收益率变化幅度peryear
    5、每年付息次数ctimes
    6、票面价值fv
    输出：有效久期（年数）
    """
    
    #转换为每期付息的参数
    c=cr/ctimes; y=ytm/ctimes; per=peryear/ctimes; F=fv; n=nyears*ctimes
    
    #计算久期期数
    d=ED0(c,y,F,n,per)
    #转换为久期年数：年数=期数/每年付息次数
    D=round(d/ctimes,2)
    
    return D                    

if __name__=='__main__':
    cr=0.08; ytm=0.1; nyears=3; ctimes=2; fv=100; peryear=0.001
    print(ED(cr,ytm,nyears,peryear))
    
    cr=0.095; ytm=0.1144; nyears=8; ctimes=2; fv=1000; peryear=0.0005
    print(ED(cr,ytm,nyears,peryear))    
#==============================================================================    
def CFD0(c,y,F,n):
    """
    功能：计算债券的封闭式久期期数
    输入参数：
    1、每期票面利率c
    2、每期到期收益率y，市场利率，贴现率
    3、票面价值F
    4、到期期数n
    输出：久期期数（不一定是年数）
    """
    #生成期数序列
    import pandas as pd
    t=pd.Series(range(1,(n+1)))
    
    #计算到期收益率变化前的现值
    p=sum(c*F/(1+y)**t)+F/(1+y)**len(t)
    
    #计算分子第1项
    nm1=(c*F) * ((1+y)**(n+1)-(1+y)-y*n) / ((y**2)*((1+y)**n))
    #计算分子第2项
    nm2=F*(n/((1+y)**n))
    
    #计算封闭式久期
    cfd=(nm1+nm2)/p
    
    return cfd

if __name__=='__main__':
    c=0.095/2; y=0.1144/2; n=16; F=1000
    print(CFD0(c,y,F,n))    
#==============================================================================    
def CFD(cr,ytm,nyears,ctimes=2,fv=100):
    """
    功能：计算债券的封闭式年数
    输入参数：
    1、年票面利率cr
    2、年到期收益率ytm，市场利率，贴现率
    3、到期年数nyears
    4、每年付息次数ctimes
    5、票面价值fv
    输出：久期（年数）
    """
    
    #转换为每期付息的参数
    c=cr/ctimes; y=ytm/ctimes; F=fv; n=nyears*ctimes
    
    #计算久期期数
    d=CFD0(c,y,F,n)
    #转换为久期年数：年数=期数/每年付息次数
    cfd=round(d/ctimes,2)
    
    return cfd                    

if __name__=='__main__':
    cr=0.08; ytm=0.1; nyears=3; ctimes=2; fv=100
    print(CFD(cr,ytm,nyears))
#==============================================================================    
def C0(c,y,F,n):
    """
    功能：计算债券的凸度期数
    输入参数：
    1、每期票面利率c
    2、每期到期收益率y，市场利率，贴现率
    3、票面价值F
    4、到期期数n
    输出：到期收益率变化幅度为per时债券价格的变化幅度
    """    
    #生成期数序列
    import pandas as pd
    t=pd.Series(range(1,(n+1)))
    
    #计算未来现金流的现值
    p=sum(c*F/(1+y)**t)+F/(1+y)**len(t)
    #计算未来现金流的加权现值：权重为第t期的(t**2+t)
    w2p=sum(c*F*(t**2+t)/(1+y)**t)+F*(len(t)**2+len(t))/(1+y)**len(t)
    #计算凸度
    c0=w2p/(p*(1+y)**2)
    
    return c0

if __name__=='__main__':
    c=0.08/2; y=0.1/2; n=6; F=100
    print(C0(c,y,F,n)) 
#==============================================================================    
def convexity(cr,ytm,nyears,ctimes=2,fv=100):
    """
    功能：计算债券的凸度年数
    输入参数：
    1、年票面利率cr
    2、年到期收益率ytm，市场利率，贴现率
    3、到期年数nyears
    4、每年付息次数ctimes
    5、票面价值fv
    输出：凸度（年数）
    """
    #转换为每期付息的参数
    c=cr/ctimes; y=ytm/ctimes; F=fv; n=nyears*ctimes
    
    #计算凸度期数
    c=C0(c,y,F,n)
    #转换为凸度年数：年数=期数/每年付息次数**2
    cyears=round(c/ctimes**2,2)
    
    return cyears                    

if __name__=='__main__':
    cr=0.08; ytm=0.1; nyears=3; ctimes=2; fv=100
    print(convexity(cr,ytm,nyears))
#==============================================================================    
def ytm_risk(cr,ytm,nyears,peryear,ctimes=2,fv=100):
    """
    功能：计算债券的利率风险，即市场利率（到期收益率）变动将带来的债券价格变化率
    输入参数：
    1、年票面利率cr
    2、年到期收益率ytm，市场利率，贴现率
    3、到期年数nyears
    4、每期到期收益率（市场利率）变化的幅度per，100个基点=1%
    5、每年付息次数ctimes
    6、票面价值fv
    输出：到期收益率变化幅度导致的债券价格变化率
    """
    #转换为每期付息的参数
    c=cr/ctimes; y=ytm/ctimes; F=fv; n=nyears*ctimes
    
    #计算到期收益率变化对债券价格的影响：第1部分
    b0=-MD0(c,y,F,n)/2*peryear
    #计算到期收益率变化对债券价格的影响：第2部分
    b1=(0.5*C0(c,y,F,n)/ctimes**2)*peryear**2
    #债券价格的变化率
    p_pct=round(b0+b1,4)
        
    return p_pct

if __name__=='__main__':
    cr=0.08; ytm=0.1; nyears=3; peryear=0.01
    print(ytm_risk(cr,ytm,nyears,peryear))        

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
def print_progress_bar(current,startnum,endnum):
    """
    功能：打印进度数值，每个10%打印一次，不换行
    """
    for i in [9,8,7,6,5,4,3,2,1]:
        if current == int((endnum - startnum)/10*i)+1: 
            print(str(i)+'0%',end=' '); break
        elif current == int((endnum - startnum)/100*i)+1: 
            print(str(i)+'%',end=' '); break
    if current == 2: print('0%',end=' ')

if __name__ =="__main__":
    startnum=2
    endnum=999
    L=range(2,999)
    for c in L: print_progress_bar(c,startnum,endnum)

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
    #设定xy轴的范围
    plt.xlim(min(df.index),max(df.index))
    #plt.ylim(min(df[colname]),max(df[colname]))        
        
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
    plt.ylabel(ylabeltxt)
    plt.xlabel(footnote,fontsize=9)
    plt.title(titletxt,fontsize=12)
    plt.tick_params(labelsize=8)
    
    plt.tight_layout()
    plt.show()
    plt.close()
    return

if __name__ =="__main__":
    plot_line(df,'Close',"收盘价","价格","万科股票","数据来源：雅虎财经",power=4)

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
    #plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    
    plt.title(titletxt, fontsize=12)
    plt.show()
    
    return


if __name__ =="__main__":
    pass
    """
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
    """
#==============================================================================    
def interbank_bond_issue_detail(fromdate,todate):
    """
    功能：获得银行间债券市场发行明细
    输入：开始日期fromdate，截止日期todate
    """
    #检查期间的合理性
    result,start,end=check_period(fromdate, todate)
    if result is None:
        print("...Error(interbank_bond_issue_detail), invalid period:",fromdate,todate)
        return None
    
    #####银行间市场的债券发行数据
    import akshare as ak
    #获得债券发行信息第1页
    print("\n...Searching for bond issuance: ",end='')
    bond_issue=ak.get_bond_bank(page_num=1)    

    import pandas as pd
    from datetime import datetime
    #获得债券发行信息后续页
    maxpage=999
    for pn in range(2,maxpage):
        print_progress_bar(pn,2,maxpage)
        try:
            #防止中间一次失败导致整个过程失败
            bi=ak.get_bond_bank(page_num=pn)
            bond_issue=bond_issue.append(bi)
        except:
            #后续的网页已经变得无法抓取
            print("...Unexpected get_bond_bank(interbank_bond_issue_detail), page_num",pn)
            break        
        
        #判断是否超过了开始日期
        bistartdate=bi.tail(1)['releaseTime'].values[0]
        bistartdate2=pd.to_datetime(bistartdate)
        if bistartdate2 < start: break
    print(" Done!")        
    
    #删除重复项，按日期排序
    bond_issue.drop_duplicates(keep='first',inplace=True)
    bond_issue.sort_values(by=['releaseTime'],ascending=[False],inplace=True)    
    #转换日期项
    lway1=lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S')
    bond_issue['releaseTime2']=bond_issue['releaseTime'].apply(lway1)    
    
    #提取年月日信息
    lway2=lambda x: x.year
    bond_issue['releaseYear']=bond_issue['releaseTime2'].map(lway2).astype('str')
    lway3=lambda x: x.month
    bond_issue['releaseMonth']=bond_issue['releaseTime2'].map(lway3).astype('str')
    lway4=lambda x: x.day
    bond_issue['releaseDay']=bond_issue['releaseTime2'].map(lway4).astype('str')
    lway5=lambda x: x.weekday() + 1
    bond_issue['releaseWeekDay']=bond_issue['releaseTime2'].map(lway5).astype('str')
    lway6=lambda x: x.date()
    bond_issue['releaseDate']=bond_issue['releaseTime2'].map(lway6).astype('str')
    
    #过滤日期
    bond_issue=bond_issue.reset_index(drop = True)
    bond_issue1=bond_issue.drop(bond_issue[bond_issue['releaseTime2']<start].index)
    bond_issue1=bond_issue1.reset_index(drop = True)
    bond_issue2=bond_issue1.drop(bond_issue1[bond_issue1['releaseTime2']>end].index)
    bond_issue2=bond_issue2.reset_index(drop = True)
    #转换字符串到金额
    bond_issue2['issueAmount']=bond_issue2['firstIssueAmount'].astype('float64')
    
    return bond_issue2
    
if __name__=='__main__':
    fromdate='2020-4-25'    
    todate='2020-4-28'
    ibbi=interbank_bond_issue_detail(fromdate,todate)
    
#==============================================================================
def save_to_excel(df,filedir,excelfile,sheetname="Sheet1"):
    """
    函数功能：将df保存到Excel文件。
    如果目录不存在提示出错；如果Excel文件不存在则创建之文件并保存到指定的sheet；
    如果Excel文件存在但sheet不存在则增加sheet并保存df内容，原有sheet内容不变；
    如果Excel文件和sheet都存在则追加df内容到已有sheet的末尾
    输入参数：
    df: 数据框
    filedir: 目录
    excelfile: Excel文件名，不带目录，后缀为.xls或.xlsx
    sheetname：Excel文件中的sheet名
    输出：
    保存df到Excel文件
    无返回数据
    
    注意：如果df中含有以文本表示的数字，写入到Excel会被自动转换为数字类型保存。
    从Excel中读出后为数字类型，因此将会与df的类型不一致
    """

    #检查目录是否存在
    import os
    try:
        os.chdir(filedir)
    except:
        print("Error #1(save_to_excel): folder does not exist")        
        print("Information:",filedir)  
        return
                
    #取得df字段列表
    dflist=df.columns
    #合成完整的带目录的文件名
    filename=filedir+'/'+excelfile
    
    import pandas as pd
    try:
        file1=pd.ExcelFile(excelfile)
    except:
        #不存在excelfile文件，直接写入
        df.to_excel(filename,sheet_name=sheetname, \
                       header=True,encoding='utf-8')
        print("***Results saved in",filename,"@ sheet",sheetname)
        return
    else:
        #已存在excelfile文件，先将所有sheet的内容读出到dict中        
        dict=pd.read_excel(file1, None)
    file1.close()
    
    #获得所有sheet名字
    sheetlist=list(dict.keys())
    
    #检查新的sheet名字是否已存在
    try:
        pos=sheetlist.index(sheetname)
    except:
        #不存在重复
        dup=False
    else:
        #存在重复，合并内容
        dup=True
        #合并之前可能需要对df中以字符串表示的数字字段进行强制类型转换.astype('int')
        df1=dict[sheetlist[pos]][dflist]
        dfnew=pd.concat([df1,df],axis=0,ignore_index=True)        
        dict[sheetlist[pos]]=dfnew
    
    #将原有内容写回excelfile    
    result=pd.ExcelWriter(filename)
    for s in sheetlist:
        df1=dict[s][dflist]
        df1.to_excel(result,s,header=True,index=True,encoding='utf-8')
    #写入新内容
    if not dup: #sheetname未重复
        df.to_excel(result,sheetname,header=True,index=True,encoding='utf-8')
    try:
        result.save()
        result.close()
    except:
        print("Error #2(save_to_excel): writing file permission denied")
        print("Information:",filename)  
        return
    print("***Results saved in",filename,"@ sheet",sheetname)
    return       