import tkinter as tk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasAgg,FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import settings
import os
import finance



#Takes user's mouse clicks to decide how they interact with the UI
def mousePressed(event, data):
    #decides where user goes from landing page
    if data.ratioAnalysis==False and data.portfolioBuilder==False and data.stockPerformance == False and data.start==True:
        if data.height*3/8<event.y<data.height*5/8:
            if data.width*0.5/12<event.x<data.width*3.75/12:
                data.ratioAnalysis=True
            if data.width*4.25/12<event.x<data.width*7.75/12:
                data.stockPerformance = True
            if data.width*8.25/12<event.x<data.width*11.5/12:
                data.portfolioBuilder=True    
    #Chooses what mouseclicks in the stock performance page do (regarding which stocks are toggled etc)
    elif data.stockPerformance==True and data.start == True and data.ratioAnalysis==False and data.portfolioBuilder==False:
        if data.width/100<event.x<data.width/6 and data.height*13/15<event.y<data.height*14/15:
            data.stockPerformance=False
        if event.x > data.startX and event.x < data.startX + 10:
            for i in range(len(data.startY)):
                if event.y > data.startY[i] and event.y < (data.startY[i] + 10):
                    count = data.stockPerformanceToggle.count(True)
                    if data.stockPerformanceToggle[i]==False and count<=1:    
                        data.stockPerformanceToggle[i] = True
                    else:
                        data.stockPerformanceToggle[i] = False
        if data.width*1.45/4<event.x<data.width*2.25/4 and data.height*1.5/4<event.y<data.height*2.1/4:
            historicalPriceData = []
            day = []
            compNames = []
            for i in range (len(data.stockPerformanceToggle)):
                if data.stockPerformanceToggle[i]==True:
                    processed = finance.processDailyStockPrice(data.companies[i])
                    if len(day) == 0:
                        day = processed[0]
                    historicalPriceData.append(processed[1])
                    compNames.append(data.companies[i])
            if len(historicalPriceData) > 0:
                finance.historicalPriceGraph(day,historicalPriceData,compNames,data.currentTimePeriod)
        if data.width*8/10<event.x<data.width*8/10+15:
            for i in range(len(data.timePeriod)):
                if data.yMargin[i]<event.y<data.yMargin[i]+15 and data.currentTimePeriod not in data.timePeriod[i]:
                    data.currentTimePeriod=data.timePeriod[i]
                elif data.yMargin[i]<event.y<data.yMargin[i]+15 and data.currentTimePeriod in data.timePeriod[i]:
                    data.currentTimePeriod="hi"

    #In the ratio analysis page this decides which graph is called or which stock is toggled based off of mouse clicks
    elif data.ratioAnalysis==True and data.moreInfo==False:
        if data.width*3.5/5<event.x<data.width*4.5/5 and data.height/15-20<event.y<data.height/15+20:
            data.moreInfo=True
        if data.width/100<event.x<data.width/6 and data.height*13/15<event.y<data.height*14/15:
            data.ratioAnalysis=False
        if data.width*2/3<event.x<data.width*7/8 and data.height*2.6/5<event.y<data.height*8.6/10:
            companyComparison=[]
            indices = [j for j, x in enumerate(data.stockToggle) if x == True]
            companyComparison=[]
            for l in range (len(indices)):
                companyComparison.append(data.companies[indices[l]])
            finance.currRatioGraph(companyComparison)
        if data.width*1/8<event.x<data.width*1/3 and data.height*2.6/5<event.y<data.height*8.6/10:
            companyComparison=[]
            indices = [j for j, x in enumerate(data.stockToggle) if x == True]
            companyComparison=[]
            for l in range (len(indices)):
                companyComparison.append(data.companies[indices[l]])
            finance.DERatioGraph(companyComparison)
        if data.width*9.5/24<event.x<data.width*14.5/24 and data.height*2.6/5<event.y<data.height*8.6/10:
            companyComparison=[]
            indices = [j for j, x in enumerate(data.stockToggle) if x == True]
            companyComparison=[]
            for l in range (len(indices)):
                companyComparison.append(data.companies[indices[l]])
            finance.quickRatio(companyComparison)
        if data.width*1/8<event.x<data.width*1/3 and data.height*1/5<event.y<data.height*1/2:
            companyComparison=[]
            indices = [j for j, x in enumerate(data.stockToggle) if x == True]
            companyComparison=[]
            for l in range (len(indices)):
                companyComparison.append(data.companies[indices[l]])
            finance.debtCapitalGraph(companyComparison)
        if data.width*2/3<event.x<data.width*7/8 and data.height*1/5<event.y<data.height*1/2:
            companyComparison=[]
            indices = [j for j, x in enumerate(data.stockToggle) if x == True]
            companyComparison=[]
            for l in range (len(indices)):
                companyComparison.append(data.companies[indices[l]])
            finance.cashRatio(companyComparison)
        if data.width*9.5/24<event.x<data.width*14.5/24 and data.height*1/5<event.y<data.height*1/2:
            companyComparison=[]
            indices = [j for j, x in enumerate(data.stockToggle) if x == True]
            companyComparison=[]
            for l in range (len(indices)):
                companyComparison.append(data.companies[indices[l]])
            finance.returnOnEquityGraph(companyComparison)
        if event.x > data.startX and event.x < data.startX + 10:
            for i in range(len(data.startY)):
                if event.y > data.startY[i] and event.y < (data.startY[i] + 10):
                    if data.stockToggle[i]==False:
                            data.stockToggle[i] = True
                    else:
                        data.stockToggle[i] = False
    #In the more info page allows a back button
    if data.moreInfo==True:
        if data.width/100<event.x<data.width/6 and data.height*13/15<event.y<data.height*14/15:
            data.moreInfo=False
            data.ratioAnalysis=True
    #In the portfolio builder decides what the clicks do
    if data.portfolioBuilder==True and data.start==True:
        if event.x > data.width/10 and event.x < data.width/10 + 15:
            for i in range(len(data.yMargin)):
                if event.y > data.yMargin[i] and event.y < (data.yMargin[i] + 15):
                    data.currentRisk = data.riskLevel[i]
        if event.x > data.width*2.7/4 and event.x < data.width*2.7/4 + 15:
            for i in range(len(data.startY)):
                if event.y > data.startY[i] and event.y < (data.startY[i] + 10): 
                    if data.companyToggle[i]==False:
                        data.companyToggle[i] = True
                    else:
                        data.companyToggle[i] = False
        if data.width*1.45/4<event.x<data.width*2.25/4 and data.height*1.5/4<event.y<data.height*2.1/4 \
        and data.currentRisk != "" and True in data.companyToggle:
            indices = [j for j, x in enumerate(data.companyToggle) if x == True]
            graphCompany = []
            for h in range(len(indices)):
                graphCompany.append(data.companies[indices[h]])
            if data.currentRisk == "Low":
                dist, names,wtdAverage,wtdStd = finance.getPortfolio(graphCompany,data.rfr,0.9)
                finance.makePortfolio(dist,names,wtdAverage,wtdStd)
            elif data.currentRisk == "Medium":
                dist, names,wtdAverage,wtdStd = finance.getPortfolio(graphCompany,data.rfr,1)
                finance.makePortfolio(dist,names,wtdAverage,wtdStd)
            else: 
                dist, names,wtdAverage,wtdStd = finance.getPortfolio(graphCompany,data.rfr,1.1)
                finance.makePortfolio(dist,names,wtdAverage,wtdStd)
        if data.width/100<event.x<data.width/6 and data.height*13/15<event.y<data.height*14/15:
            data.portfolioBuilder=False
            data.risk = ""

#Stock Performance Page
def drawStockPerformance(canvas,data):
    canvas.delete("all")
    canvas.create_rectangle(0,0,data.width,data.height,fill = "#4094c9")
    canvas.create_rectangle(data.width/100,data.height*13/15,
                            data.width/6,data.height*14/15,fill = "white")
    canvas.create_rectangle(data.width*1.45/4,data.height*1.5/4,
                        data.width*2.25/4,data.height*2.1/4,fill= "white")
    canvas.create_text(data.width/11.8,data.height*13.5/15,
        text = "Go Back",font = ("Avenir",37))
    canvas.create_text(data.width*7/8,data.height*1.25/8,
        text = "Predicted Stock\nTimeline",font = ("Avenir",25),justify='center')
    canvas.create_text(data.width*2.8/6,data.height*7/8,
        text = "Choose at most two stocks\nand optionally a forecast timeline",font = ("Avenir",25),justify = 'center')

    #Boxes for stocks
    for i in range(len(data.companies)):
        if data.stockPerformanceToggle[i]==True:
            canvas.create_rectangle(data.startX, data.startY[i], data.startX + 10, data.startY[i] + 10, 
                fill = "black", width = 2)
        else:
            canvas.create_rectangle(data.startX, data.startY[i], data.startX + 10, data.startY[i] + 10, 
                fill = "white", width = 2)
        canvas.create_text(data.startX + 15, data.startY[i]+3, text=data.companies[i], font = ("Avenir",25),anchor = "w")
        canvas.create_line(0,data.height*1.2/6,data.width,data.height*1.2/6,width = 3)
    canvas.create_text(data.width*1.9/4,data.height*1/12,
        text = "Stock Performance", font = ("Avenir",40),justify="center")
    canvas.create_text(data.width*0.8/12,data.height*1.25/8,
        text="Stock\nChoices",font = ("Avenir",25),justify="center")
    canvas.create_text(data.width*1.85/4,data.height*1.8/4,
        text = "Click To\nView Data",font = ("Avenir",30),justify = 'center')
    #Circles for risk
    for i in range(len(data.timePeriod)):
        if(data.timePeriod[i] == data.currentTimePeriod):
            canvas.create_oval(data.width*8/10, data.yMargin[i], data.width*8/10+15, data.yMargin[i] + 15, 
            fill = "black", width = 2)
        else:
            canvas.create_oval(data.width*8/10, data.yMargin[i], data.width*8/10+15, data.yMargin[i]+15, 
            fill = "white", width = 2)
        canvas.create_text(data.width*8.19/10, data.yMargin[i]+5, text=data.timePeriod[i], font = ("Avenir",35),anchor = "w")

#Unused timer fired function
def timerFired(data):
    pass

#Used to start program
def keyPressed(event, data):
    if event.keysym=="Return":
        data.start=True
          
#Draws initial page
def drawStartScreen(canvas,data):
    canvas.create_rectangle(0,0,
                            data.width,data.height,fill="#96c5d0")
    canvas.create_text(data.width/2,data.height/4,
        text = "Stock Data Analysis Tool",font = ("Avenir", 80))
    canvas.create_text(data.width/2,data.height*2/3,
        text = ("Press Enter to begin"),font = ("Avenir", 40))
    canvas.create_text(data.width/2,data.height*1.5/4,
        text = ("by Derek Li"), font = ("Avenir", 40))

#Landing page after user clicks "Enter"
def drawLandingScreen(canvas,data):
    canvas.delete("all")
    canvas.create_rectangle(0,0,
                            data.width,data.height,fill="#3895af")
    canvas.create_text(data.width/2,data.height*1/4,
        text = "Select What You'd Like",font = ("Avenir", 30))
    canvas.create_rectangle(data.width*0.5/12,data.height*3/8,data.width*3.75/12,data.height*5/8,fill = "white")
    canvas.create_rectangle(data.width*4.25/12,data.height*3/8,data.width*7.75/12,data.height*5/8,fill = "white")
    canvas.create_rectangle(data.width*8.25/12,data.height*3/8,data.width*11.5/12,data.height*5/8,fill = 'white')
    canvas.create_text(data.width*2.125/12,data.height*1/2,
        text="Ratio\nAnalysis",font = ("Avenir",40),justify='center')
    canvas.create_text(data.width*6/12,data.height*1/2,
        text="Stock\nPerformance",font = ("Avenir",40),justify='center')
    canvas.create_text(data.width*9.875/12,data.height*1/2,
        text="Portfolio\nBuilder",font = ("Avenir",40),justify='center')

#Draw rational analysis page
def drawRatioAnalysis(canvas,data):
    canvas.delete("all")
    canvas.create_rectangle(0,0,
                            data.width,data.height,fill="#6990ae")
    canvas.create_rectangle(data.width*3.5/5,data.height/15-20,
                            data.width*4.5/5,data.height/15+20,fill = "white")
    canvas.create_rectangle(data.width/100,data.height*13/15,
                            data.width/6,data.height*14/15,fill = "white")
    canvas.create_rectangle(data.width*1/8,data.height*1/5,
                            data.width*1/3,data.height*1.5/3,fill="white")
    canvas.create_rectangle(data.width*2/3,data.height*1/5,
                            data.width*7/8,data.height*1.5/3,fill="white")
    canvas.create_rectangle(data.width*9.5/24,data.height*1/5,
                            data.width*14.5/24,data.height/2,fill="white")
    canvas.create_rectangle(data.width*9.5/24,data.height*2.6/5,
                            data.width*14.5/24,data.height*8.6/10,fill="white")
    canvas.create_rectangle(data.width*1/8,data.height*2.6/5,
                            data.width*1/3,data.height*8.6/10,fill="white")
    canvas.create_rectangle(data.width*2/3,data.height*2.6/5,
                            data.width*7/8,data.height*8.6/10,fill="white")
    canvas.create_text(data.width*18.5/24,data.height*6.975/10,
        text = "Current Ratio\nGraph",font=("Avenir",25),justify = "center")
    canvas.create_text(data.width*5.5/24,data.height*6.975/10,
        text = "D/E Ratio\nGraph",font=("Avenir",25),justify = "center")
    canvas.create_text(data.width*12/24,data.height*6.975/10,
        text = "Quick Ratio\nGraph",font=("Avenir",25),justify = "center")
    canvas.create_text(data.width*4/5,data.height/15,
        text = "More Info", font = ("Avenir",40))
    canvas.create_text(data.width/11.8,data.height*13.5/15,
        text = "Go Back",font = ("Avenir",37))
    canvas.create_text(data.width*5.5/24,(data.height*1/5+data.height*1/2)/2,
        text = "Debt to Capital \nRatio Graph",font = ("Avenir",25),justify = "center")
    canvas.create_text((data.width*2/3+data.width*7/8)/2,(data.height*1/5+data.height*1/2)/2,
        text = "Cash Ratio\nGraph",font = ("Avenir",25),justify = "center")
    canvas.create_text(data.width*1/2,(data.height*1/5+data.height*1/2)/2,
        text = "Return on Equity\nGraph",font = ("Avenir",25),justify = "center")
    canvas.create_text(data.width/2,data.height/15,
        text = "Ratio Analysis", font = ("Avenir",40),justify = 'center')
    closetMiddle = data.margin + data.listWidth/2
    canvas.create_text(data.margin*0.5 + data.listWidth/2, data.height*1.1/6, 
        text = "Stock\nChoices", fill = "black",font = ("Avenir",25),justify = "center")
    #Boxes for stocks
    for i in range(len(data.companies)):
        if data.stockToggle[i]==True:
            canvas.create_rectangle(data.startX, data.startY[i], data.startX + 10, data.startY[i] + 10, 
                fill = "black", width = 2)
        else:
            canvas.create_rectangle(data.startX, data.startY[i], data.startX + 10, data.startY[i] + 10, 
                fill = "white", width = 2)
        canvas.create_text(data.startX + 12, data.startY[i]+5, text=data.companies[i], font = ("Avenir",25),anchor = "w")
        canvas.create_line(0,data.height*0.8/6,data.width,data.height*0.8/6,width = 3)
        canvas.create_line(data.width/50,data.height*1.35/6,data.width*0.7/6,data.height*1.35/6,width = 3)

#Definitions page
def drawMoreInfo(canvas,data):
    canvas.delete("all")
    canvas.create_rectangle(0,0,
                            data.width,data.height,fill="#6990ae")
    canvas.create_rectangle(data.width/100,data.height*13/15,
                            data.width/6,data.height*14/15,fill = "white")
    canvas.create_text(data.width/2,data.height/25,
        text = "More Info", font = ("Avenir",40),justify = 'center')
    canvas.create_text(data.width/2,data.height/8,
        text = "Debt to Capital Ratio: The debt-to-capital ratio is a measurement of a company's\nfinancial leverage. The debt-to-capital ratio is calculated by taking the company's\ndebt, including both short- and long-term liabilities and dividing it by the total capital.",font = ("Avenir",25),justify = 'center')
    canvas.create_text(data.width/2,data.height*2/8,
        text = "Return On Equity: ROE is a profitability ratio that measures the ability of a firm\nto generate profits from its shareholders investments in the company.",font = ("Avenir",25),justify = 'center')
    canvas.create_text(data.width/2,data.height*3/8,
        text = "Cash Ratio: The cash ratio is the ratio of a company's total cash and cash\nequivalents to its current liabilities. The metric calculates a company's ability to repay\nits short-term debt",font = ("Avenir",25),justify='center')
    canvas.create_text(data.width/2,data.height*4/8,
        text = "Debt to Equity Ratio: The D/E ratio is a financial ratio indicating the relative\nproportion of shareholders' equity and debt used to finance a company's assets",font = ("Avenir",25),justify = 'center')
    canvas.create_text(data.width/2,data.height*5/8,
        text = "Quick Ratio: The quick ratio is an indicator of a company’s short-term liquidity,\nand measures a company’s ability to meet its short-term obligations with its most\nliquid assets.",font = ("Avenir",25),justify = 'center')
    canvas.create_text(data.width/2,data.height*6.25/8,
        text = "Current Ratio: The current ratio is a liquidity ratio that measures a company's\nability to pay short-term and long-term obligations.To gauge this ability, the current\nratio considers the current total assets of a company (both liquid and illiquid) relative\nto that company's current total liabilities.",font = ("Avenir",25),justify = 'center')
    canvas.create_text(data.width/11.8,data.height*13.5/15,
        text = "Go Back",font = ("Avenir",37))

#Draws portfolio builder
def drawPortfolioBuilder(canvas,data):
    canvas.delete("all")
    canvas.create_rectangle(0,0,
                            data.width,data.height,fill="#697fae")
    canvas.create_rectangle(data.width/100,data.height*13/15,
                            data.width/6,data.height*14/15,fill = "white")
    canvas.create_rectangle(data.width*1.45/4,data.height*1.5/4,
                            data.width*2.25/4,data.height*2.1/4,fill= "white")
    canvas.create_text(data.width*1/5,data.height/8,
        text = "How Much Risk Are\nYou Willing to Take On?",font = ("Avenir",30),justify = 'center')
    canvas.create_text(data.width/11.8,data.height*13.5/15,
        text = "Go Back",font = ("Avenir",37))
    canvas.create_text(data.width*7/10,data.height/8,
        text = "What Stocks Would\nYou Like In Your Portfolio?",font = ("Avenir",30),justify = 'center')
    canvas.create_text(data.width*1.85/4,data.height*1.8/4,
        text = "Click To\nContinue",font = ("Avenir",30),justify = 'center')
    canvas.create_text(data.width*2.8/6,data.height*7/8,
        text = "Click risk level and at least one\nstock before getting recommendation",font = ("Avenir",25),justify = 'center')

    #Circles for risk
    for i in range(len(data.riskLevel)):
        if(data.riskLevel[i] == data.currentRisk):
            canvas.create_oval(data.width/10, data.yMargin[i], data.width/10+15, data.yMargin[i] + 15, 
            fill = "black", width = 2)
        else:
            canvas.create_oval(data.width/10, data.yMargin[i], data.width/10+15, data.yMargin[i]+15, 
            fill = "white", width = 2)
        canvas.create_text(data.width/10+20, data.yMargin[i]+8, text=data.riskLevel[i], font = ("Avenir",35),anchor = "w")

    #Boxes for stocks
    for i in range(len(data.companies)):
        if data.companyToggle[i]==True:
            canvas.create_rectangle(data.width*2.7/4, data.startY[i], data.width*2.7/4+10, data.startY[i] + 10, 
                fill = "black", width = 2)
        else:
            canvas.create_rectangle(data.width*2.7/4, data.startY[i], data.width*2.7/4+10, data.startY[i] + 10, 
                fill = "white", width = 2)
        canvas.create_text(data.width*2.7/4+15, data.startY[i]+5, text=data.companies[i], font = ("Avenir",25),anchor = "w")
        canvas.create_line(0,data.height*1.2/6,data.width,data.height*1.2/6,width = 3)

#Calls all draw functions if their respective buttons are clicked on and the boolean's are changed to True
def redrawAll(canvas, data):
    drawStartScreen(canvas,data)
    if data.start==True:
        drawLandingScreen(canvas,data)
        if data.ratioAnalysis==True:
            drawRatioAnalysis(canvas,data)
            if data.moreInfo==True:
                drawMoreInfo(canvas,data)
        if data.stockPerformance==True:
            drawStockPerformance(canvas,data)
        if data.portfolioBuilder==True:
            drawPortfolioBuilder(canvas,data)

####################################
# use the run function as-is
####################################
#Run funcion is from the course website
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete('ALL')
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    settings.init(data)
    # create the root and the canvas
    root = tk.Tk()
    canvas = tk.Canvas(root, width=data.width, height=data.height)
    canvas.pack()

    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
