import sys
import os
import csv
import math
import time
import numpy as np
import settings
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import random
import copy


global BSData
BSData = dict()

#Calculates the expected returns, volatility, and ewma based off which stock name is sent in
def processStockPrice(stock):
    pathname = './data/' + stock + '/' + stock + '_Price.csv'
    with open(pathname, 'r', encoding = 'utf-8') as g:
        price = list(csv.reader(g, delimiter=";"))
    rows = len(price)
    cols = len(price[0])
    finalPrice = []
    closePrice = []
    for row in range (rows):
        for col in range(cols):
            if row == 0:
                continue
            parts = price[row][col].split(",")
            finalPrice.append(parts[0])
            finalPrice.append(parts[4])
            closePrice.append(float(parts[4]))
    changeInPrice = []
    prices=np.array([closePrice],dtype=float)
    percentChangeInPrice = []
    for i in range (len(closePrice)):
        if i == 0:
            continue
        changePrice = ((closePrice[i]-closePrice[i-1])/abs(closePrice[i-1]))*100
        percentChangeInPrice.append(changePrice)
    percentChangeArr = np.array([percentChangeInPrice],dtype = float)
    std = np.std(percentChangeArr,axis=1)
    averageChange = np.mean(percentChangeArr,axis = 1)

    #Exponential Weighted Moving Average (EWMA)
    logReturns = 0
    smoothingConstant = 0.94
    EWMA = 0
    #Risk metric
    for i in range(len(closePrice)):
        if i ==0:
            continue
        logReturns = math.log(abs(closePrice[i]/closePrice[i-1]))
        logReturns=logReturns**2
        weights = (1-smoothingConstant)*(smoothingConstant**(i-1))
        EWMA += logReturns*weights

    return [float(averageChange[0]),float(std[0]),float(EWMA)]

#Finds the day and close price from each stocks historical price data CSV
def processDailyStockPrice(stock):
    pathname = './data/' + stock + '/' + stock + '_Price.csv'
    with open(pathname, 'r', encoding = 'utf-8') as g:
        price = list(csv.reader(g, delimiter=";"))
    rows = len(price)
    cols = len(price[0])
    finalPrice = []
    closePrice = []
    day = []
    for row in range (rows):
        for col in range(cols):
            if row == 0:
                continue
            parts = price[row][col].split(",")
            day.append(parts[0])
            closePrice.append(float(parts[4]))
    return (day,closePrice)

#Processes the balances sheet into a list that is more readable
def processBalanceSheet(stock):
    path = './data/' + stock + '/' + stock + '_BS.csv'
    with open(path, 'r') as f:
        balanceSheet = list(csv.reader(f, delimiter=";"))
    rows = len(balanceSheet)
    cols = len(balanceSheet[0])
    final = []
    for row in range(rows):
        for col in range(cols):
            parts = balanceSheet[row][col].split(",")
            for i in range (len(parts)):
                #if the data is empty fill it with a value of 0.0 instead of a "-"
                if parts[i] == "-":
                    parts[i] = 0.0
            final.append(parts)
    return final

#calculates the new indexes and price for future stock prices
def forecastGraph(closePrice,fcperiod,name):
    lastPrice = closePrice[-1]
    if fcperiod == "1 Month":
        periodLength = 22
    elif fcperiod == "3 Months":
        periodLength = 66
    elif fcperiod == "6 Months":
        periodLength = 125
    else: 
        periodLength = 251
    newind = range(250,251+periodLength)
    er, sd, ewma = processStockPrice(name)
    DE = DERatio(name)
    cash = curCashRatio(name)
    def getNextPrice(oldPrice,DE,cash,er,ewma,sd):
        performance = 0
        #Bad cash ratio
        if(cash < 1):
            performance -= 4
        else: 
            performance += 2
        #Good DE Ratio
        if(DE < 0.4):
            performance += 5
        elif(DE > 0.6):
            performance -= min(DE*5,6)
        #Mimic real behavior
        noise = np.random.normal(er,sd,1)
        change = min(random.randint(1,10)*er*(ewma*performance)+noise,0.04*oldPrice)
        return(oldPrice+change)
    futurePrice = [lastPrice]
    for i in range(len(newind)):
        if i == 0: 
            pass
        else:
            futurePrice.append(getNextPrice(futurePrice[i-1],DE,cash,er,ewma,sd))
    return(newind,futurePrice)


#Graphs the historical price data of stocks and the predicted future values
def historicalPriceGraph(day,data,compnames,fcperiod):
    ind = range(1,251)
    if fcperiod != "hi" and len(compnames)>1:
        a = compnames[0]
        b = compnames[1]
        compnames = [a,a,b,b]
    for i in range(len(data)):
        if fcperiod != "hi":
            futureinds,futurePrice = forecastGraph(data[i],fcperiod,compnames[i])
            plt.plot(futureinds,futurePrice)
        plt.plot(ind,data[i])
    plt.title("Historical Price")
    plt.legend(compnames)
    plt.xlabel("Days since 11/29/2016")
    plt.ylabel("Price")
    plt.show()

#Current Ratio x Year Graph
#Total Current Assets/Total Liabilities = Current Ratio
def currRatioGraph(stocks):
    for stock in stocks:
        xValCurrRatio = []
        yValCurrRatio = []
        currentStock(stock)
        final = BSData[stock]
        for i in range(len(final[0])):
            if i==0:
                continue
            if float(final[35][i])==0:
                continue
            else:
                xValCurrRatio.append(int(final[0][i]))
                currentRatio=float(final[11][i])/float(final[35][i])
                yValCurrRatio.append(currentRatio)
        plt.plot(xValCurrRatio,yValCurrRatio,label = stock)
    plt.title("Current Ratio by Year")
    plt.legend()
    plt.xlabel("Years")
    plt.ylabel("Current Ratio")
    plt.show()

#Return on Equity X Year Graph
#Net Income/Shareholder's Equity
def returnOnEquityGraph(stocks):
    for stock in stocks:
        xValROE = []
        yValROE = []
        currentStock(stock)
        final = BSData[stock]
        for i in range(len(final[0])):
            if i==0:
                continue
            if float(final[43][i])==0:
                continue
            else:
                xValROE.append(int(final[0][i]))
                ROE=(float(final[40][i]))/(float(final[43][i]))
                yValROE.append(ROE)
        plt.plot(xValROE,yValROE,label = stock)
    plt.title("Return On Equity by Year")
    plt.legend()
    plt.xlabel("Years")
    plt.ylabel("Return On Equity")
    plt.show()

#Debt to Capital X Year Graph
#Short and long term liabilities/Total Capital
def debtCapitalGraph(stocks):
    for stock in stocks:
        xValDC = []
        yValDC = []
        currentStock(stock)
        final = BSData[stock]
        for i in range(len(final[0])):
            if i==0:
                continue
            if float(final[35][i])+float(final[43][i])+float(final[39][i])+float(final[32][i])+float(final[36][i])==0:
                continue
            else:
                xValDC.append(int(final[0][i]))
                tl = float(final[35][i])
                eq = float(final[43][i])
                cs = float(final[39][i])
                ld = float(final[32][i])
                mi = float(final[36][i])
                DC = tl/(eq+cs+ld+mi)
                yValDC.append(DC)
        plt.plot(xValDC,yValDC,label = stock)
    plt.title("Debt to Capital Ratio by Year")
    plt.legend()
    plt.xlabel("Years")
    plt.ylabel("Debt Capital Ratio")
    plt.show()

#D/E Ratio x Year Graph
#Total Liabilities/Stockholder Equity
def DERatioGraph(stocks):
    for stock in stocks:
        xValDE = []
        yValDE = []
        currentStock(stock)
        final = BSData[stock]
        for i in range(len(final[0])):
            if i==0:
                continue
            if float(final[43][i])==0:
                continue
            else:
                xValDE.append(int(final[0][i]))
                DE=float(final[35][i])/float(final[43][i])
                yValDE.append(DE)
        plt.plot(xValDE,yValDE,label = stock)
    plt.title("Debt to Equity Ratio by Year")
    plt.legend()
    plt.xlabel("Years")
    plt.ylabel("DE")
    plt.show()

#Cash Ratio X Years Graph
#Cash/Current Liabilities
def cashRatio(stocks):
    for stock in stocks:
        xValCashRatio = []
        yValCashRatio = []
        currentStock(stock)
        final = BSData[stock]
        for i in range(len(final[0])):
            if i==0:
                continue
            if float(final[28][i])==0:
                continue
            else:
                xValCashRatio.append(int(final[0][i]))
                CR=(float(final[2][i]))/(float(final[28][i]))
                yValCashRatio.append(CR)
        plt.plot(xValCashRatio,yValCashRatio,label = stock)
    plt.legend()
    plt.title("Cash Ratio by Year")
    plt.xlabel("Years")
    plt.ylabel("Quick Ratio")
    plt.show()

#Quick Ratio x Years Graph
#(Current Assets-Inventory)/Total Liabilities
def quickRatio(stocks):
    for stock in stocks:
        xValquickRatio = []
        yValquickRatio = []
        currentStock(stock)
        final = BSData[stock]
        for i in range(len(final[0])):
            if i==0:
                continue
            if float(final[35][i])==0:
                continue
            else:
                xValquickRatio.append(int(final[0][i]))
                quickRatio=(float(final[11][i])-float(final[5][i]))/float(final[35][i])
                yValquickRatio.append(quickRatio)
        plt.plot(xValquickRatio,yValquickRatio,label = stock)
    plt.title("Cash Ratio by Year")
    plt.legend()
    plt.xlabel("Years")
    plt.ylabel("Quick Ratio")
    plt.show()

#Processes the stock name if they have not already been processed
def currentStock(name):
    global BSData
    if name not in BSData:
        BSData[name] = processBalanceSheet(name)
    else:
        pass

#Calculates the most recent cash ratio of the stock
def curCashRatio(stock):
    currentStock(stock)
    final = BSData[stock]
    i = len(final[0])-1
    while True:
        if final[28][i] != 0: 
            return(float(final[2][i])/float(final[28][i]))
        i -= 1

#Calculates the most recent DE ratio of the stock
def DERatio(stock):
    currentStock(stock)
    final = BSData[stock]
    i = len(final[0])-1
    while True:
        if final[43][i] != 0: 
            return(float(final[35][i])/float(final[43][i]))
        i -= 1

#Determines the distribution of how the portfolio should be divided by company
#Also returns the expected return and volatility level of the companies
def getPortfolio(companies,riskFree,tgt):
    distribution = [0]*(len(companies)+1)
    expectedReturn=[]
    std = []
    minStockPortion = 0.05
    if (len(companies) == 1):
        maxStockPortion = 1/float(len(companies))
    else:
        maxStockPortion = 1/(float(len(companies))-1)
    scores = []

    for i in range(len(companies)):
        processed = processStockPrice(companies[i])
        expectedReturn.append(processed[0])
        std.append(processed[1])

    temp = copy.deepcopy(expectedReturn)
    for k in range (len(companies)):
        maxStockPortion = (1 - sum(distribution))/float(len(temp))
        high = max(temp)
        ind = expectedReturn.index(high)
        if(std[ind]<tgt):
            distribution[ind]=maxStockPortion
        else:
            distribution[ind]=minStockPortion
        temp.remove(high)
    weightedAverage = 0
    weightedStd = 0
    for l in range(len(companies)):
        weightedAverage += expectedReturn[l]*distribution[l]
        weightedStd += (std[l]**2)*(distribution[l]**2)
    weightedStd = weightedStd**0.5

    #T-Bill calculation 
    distribution[len(companies)]=1-sum(distribution)
    companies.append("T-Bills")
    return (distribution,companies,weightedAverage,weightedStd)


#Makes the porfolio into a pie chart based off of the values that are calculated in getPortfolio
def makePortfolio(props,companies,weightedAverage,weightedStd):
    if round(props[-1],3)==0:
        companies.pop()
        props.pop()
    labels = companies
    fig1, ax1 = plt.subplots()
    ax1.pie(props, labels=labels, autopct='%1.1f%%', startangle=90,shadow = False)
    ax1.axis('equal')  
    plt.title("Expected Returns: "+ str(round(weightedAverage*100,4)) + "% | Volatility Rate: " + str(round(weightedStd*100,4))+"%")
    plt.show()



