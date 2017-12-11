import os
import finance

#Initializes variables that are used later
def init(data):
    data.companies = next(os.walk('./data'))[1]
    data.startY = range(200,700,30)
    data.rfr = 0.0175
    global currStockName
    currStockName = data.companies[0]
    data.start = False
    data.landingScreen = False
    data.ratioAnalysis= False
    data.portfolioBuilder=False
    data.moreInfo=False
    data.stockPerformance=False
    data.risk=""
    data.margin = 20
    data.listWidth = 120
    data.startText = 40
    data.currStockName = data.companies[0]
    data.startX = data.margin + data.listWidth/9
    data.currentRisk = ''
    data.riskLevel = ["Low","Medium","High"]
    data.yMargin = range(200,700,150)
    data.companyToggle = [False]*len(data.companies)
    data.stockToggle = [False]*len(data.companies)
    data.stockPerformanceToggle = [False]*len(data.companies)
    data.currChart = ""
    data.time=0
    data.callChart = [finance.debtCapitalGraph,finance.returnOnEquityGraph,finance.cashRatio,finance.DERatioGraph,finance.quickRatio,finance.currRatioGraph]
    data.chart = ["Debt to Capital Ratio Graph", "Return on Equity Graph", "Cash Ratio Graph",
            "D/E Ratio Graph","Quick Ratio Graph","Current Ratio Graph"]
    data.timePeriod = ["1 Month","3 Months","6 Months", "1 Year"]
    data.currentTimePeriod = "hi"
    data.dailyStockPrice = []

