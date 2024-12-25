from cmu_graphics import *
import os
import csv
from datetime import datetime
from types import SimpleNamespace
import Get_Data
import startEndLogics
import OOPLogics
import DrawIndicators, drawBoxPlot, DrawAnnotation

def onAppStart(app):
    app.userName, app.userPassword = getUserCredentials()
    app.registered = False if app.userName == '' else True
    app.gameSettingPage = True
    app.loggedIn = False
    app.account = OOPLogics.Account(0,1000000)
    app.stockfile = None
    app.goldChosen = False
    app.oilChosen = False
    app.appleChosen = False
    app.existingData = [] # the data excerpt according to User Input
    app.startDate = None
    app.endDate = None
    app.todayIndex = 0
    app.gameStart = False
    app.gamePaused = False
    app.gameOver = False
    app.showGameInfo = False # inside game board
    app.stepsPerSecond = 2

    app.mousex = None # see drawMouse
    app.mousey = None
    app.presentingData = [] # data that need to be drawn on the game board
    app.dataForGame = None # all data will be presented (from start to end)
    app.filteredData = app.highPrices = app.lowPrices = app.openPrices = app.closePrices = None
    app.tupleData = app.dataForIndicators = None
    app.MA5=app.MA10=app.MA25 = app.EMA12 = app.EMA26 =app.RSI = app.MACD = app.signal = None
    
    app.MA5Check = False # check box
    app.MA10Check = False
    app.MA25Check = False
    app.SMAinstruction = False # to instruction screen
    app.EMA12Check = app.EMA26Check = False
    app.EMAinstruction = False
    app.MACDCheck = False
    app.MACDinstruction = False
    app.RSICheck = False
    app.RSIinstruction = False
    app.checkbox = [app.MA5Check, app.MA10Check, app.MA25Check, app.EMA12Check, 
                    app.EMA26Check, app.RSICheck, app.MACDCheck]
    app.upperIndicators = [app.MA5Check, app.MA10Check, app.MA25Check, app.EMA12Check, app.EMA26Check]
    app.lowerIndicators = [app.RSICheck, app.MACDCheck]
    app.upperIndicatorNames = ['MA5', 'MA10','MA25','EMA12','EMA26']
    app.lowerIndicatorNames = ['RSI', 'MACD']

    app.annotating = False
    app.diagonal = app.dashedSquare = app.arrow = app.clearAll = False
    app.annotation = [app.diagonal, app.dashedSquare, app.arrow, app.clearAll]
    app.dashedRects = []
    app.diagonals = []
    app.arrows = [] # store simple namespace
    app.dragging = False
    app.startpoint = None, None # for annotation
    app.endpoint = None, None # for annotation
    app.zoomingin = app.zoomingout = False

    app.AITrader = OOPLogics.Account(0,1000000)

# https://www.geeksforgeeks.org/os-module-python-examples/
def getUserCredentials():
    if os.path.exists('userCredentials.txt'):
        file = open('userCredentials.txt', 'r')
        lines = file.readlines()
        if len(lines) >= 2:
            userName = lines[0].strip()
            userPassword = lines[1].strip()
            return userName, userPassword
        else:
            userName = ''
            userPassword = ''
            return userName, userPassword
    else:
        userName = ''
        userPassword = ''
        return userName, userPassword

# create userfile (if not created before, write such file, 
#                  if created, then use this path to match the login info)
if not os.path.exists('userCredentials.txt'):
    file = open('userCredentials.txt','w')
    file.close()

#############################################################################################
##### create local file and sign in check ###################################################
#############################################################################################
# learn from https://www.geeksforgeeks.org/os-module-python-examples/
currentWorkingDirectory = os.getcwd() 
directory = 'userCredentials'
parent_dir = currentWorkingDirectory
directory_path = os.path.join(parent_dir, directory)
os.makedirs(directory_path, exist_ok=True) #if already exists, skip
def logIn(app):
    if app.registered and not app.loggedIn:
        inputUsername = app.getUserInput('Enter your username: ')
        inputPassword = app.getUserInput('Enter your password: ')
        if app.userNum == 1:
            file.open('userCredentials.txt', 'r')
            for row in file:
                check = row.split(',')
                checkusername = check[0]
                checkpassword = check[1]
                if checkusername == inputUsername:
                    if checkpassword == inputPassword:
                        app.loggedIn = True
                        break
        else:
            pass

#############################################################################################
##### game setting page controllers #########################################################
#############################################################################################

def drawGameSettingPage(app):
    logoUrl = 'pictures/Logo.png'
    if app.registered == False: # never played before
        drawImage(logoUrl, 0,0,width = app.width, height = app.height)
        drawLabel("Mock Trading", app.width/2, 150, fill = 'orange', border = 'orange', 
                font = 'orbitron', bold = True, size = 80, italic = True)
        drawRect(app.width/2,app.height/2,200,100,fill = 'white', border = 'black', align = 'center')
        drawLabel('Create New Account', app.width/2, app.height/2, align = 'center', size = 19)
    else:
        if app.loggedIn == False: # have an account, can log in (or create a new one/not written yet)
            drawImage(logoUrl, 0,0,width = app.width, height = app.height)
            drawLabel("Mock Trading", app.width/2, 150, fill = 'orange', border = 'orange', 
                    font = 'orbitron', bold = True, size = 80, italic = True)
            drawRect(app.width/2,app.height/2,200,100,fill = 'white', border = 'black', align = 'center')
            drawLabel('Log in to your account', app.width/2,app.height/2, align = 'center', size = 19)

        else: #game setting board
            drawRect(0,0,app.width, app.height, fill = 'papayaWhip')
            drawLabel(f'Hi, {app.userName}', app.width/2, 350, size = 20)
            drawLabel(f'Your account: {app.account.account}', app.width/2, app.height/2+45, size = 20)
            drawLabel('Start A New Game', app.width/2, app.height/2 + 100, align = 'center', size = 16)
            drawRect(app.width/2, app.height/2+100, 150, 50,  fill = None, border = 'black', align = 'center')

            #instructions header
            drawLabel('Before start, you should know...', 35+250, 40, align = 'center', size = 30)
            drawRect(35,60, 500, 270, border = 'darkGreen', fill = 'white',borderWidth = 5)
            drawLabel('This is a game to mock trading, using past stock data.', 45, 80, align = 'left',
                    fill = 'black', size = 18)
            drawLabel('If you are new to stock, start with the boxes on the right', 45, 100, align = 'left', 
                    fill = 'black', size = 18)
            drawLabel('side to learn the basic components of a stock plot.', 45, 120, align = 'left', 
                    fill = 'black', size = 18)
            drawLabel('Choose one of the stock, and click on [Start A New Game].', 45, 140, align = 'left', 
                    fill = 'black', size = 18)
            drawLabel('Then, enter a start and end date from 2006-1-20 to 2024-3-1.', 45, 160, align = 'left', 
                    fill = 'black', size = 18)
            drawLabel('Two dates are at least 60 days apart.',45, 180, align = 'left', 
                    fill = 'black', size = 18)
            drawLabel('After you have an idea of the box plot, you will be able to', 45, 200, align = 'left', 
                    fill = 'black', size = 18)
            drawLabel('understand more components of a stock, including indicators,', 45, 220, align = 'left', 
                    fill = 'black', size = 18)
            drawLabel('buy and selling points, etc. After you start the game, ',45, 240, align = 'left', 
                    fill = 'black', size = 18)
            drawLabel('click on the --Dashed Boxes-- to get more explanations.', 45, 260, align = 'left', 
                    fill = 'black', size = 18)
            drawLabel('An auto trader will start to trade with you, you can compare',45, 280, align = 'left',
                    fill = 'black', size = 18)
            drawLabel('your decisions with its and improve your strategies.',45, 300, align = 'left', 
                    fill = 'black', size = 18)
            
            drawBoxPlotExplanation(app)

            # choose a stock
            border = 'gold' # gold spot
            if app.goldChosen == True: border = 'black'
            drawRect(app.width/4, app.height*4/5, 110, 50, fill = 'gold', 
                    align = 'center',border = border)
            drawLabel('Gold', app.width/4, app.height*4/5, size = 20, align = 'center')

            border = 'darkSeaGreen' # oil
            if app.oilChosen == True: border = 'black'
            drawRect(app.width*2/4, app.height*4/5, 110, 50, fill = 'darkSeaGreen', 
                    align = 'center',border = border)
            drawLabel('Oil', app.width*2/4, app.height*4/5, size = 20, align = 'center')

            border = 'lightPink' # apple
            if app.appleChosen == True: border = 'black'
            drawRect(app.width*3/4, app.height*4/5, 110, 50, fill = 'lightPink', 
                    align = 'center',border = border)
            drawLabel('Apple', app.width*3/4, app.height*4/5, size = 20, align = 'center')
            
    if thereIsUnfinishedGame(app,app.account):
        drawRect(app.width/2, app.height/2+150, 110, 50, fill = 'peachPuff', align = 'center')
        drawLabel('Continue Last Game', app.width/2, app.height/2+150, align = 'center')
    
def thereIsUnfinishedGame(app, account):
    return app.gamePaused == True and app.gameStart == True


def drawBoxPlotExplanation(app):
    drawRect(735, 200, 50, 150, fill = 'green', align = 'center')
    drawLine(735, 125, 735, 100, fill = 'green')
    drawLine(735, 350, 735, 275, fill = 'green')
    drawLabel('Close Price',670,88,size = 16)
    drawLine(735,125,670,100, dashes = True)
    drawLabel('Open Price', 680, 302, size = 16)
    drawLine(735,275,680,290, dashes = True)

    drawRect(795, 250, 50, 100, fill = 'red', align = 'center')
    drawLine(795, 200, 795, 180, fill = 'red')
    drawLine(795, 300, 795, 320, fill = 'red')
    drawLabel('Close Price',840,330,size = 16)
    drawLine(795,300,830,320, dashes = True)
    drawLabel('Open Price', 850, 170, size = 16)
    drawLine(795,200,830,180, dashes = True)
    
    drawLabel('Highest Price in the day', 765, 65 ,size = 16)
    drawLine(735,100,765,75, dashes = True)
    drawLabel('Lowest Price in the day', 760, 375, size = 16)
    drawLine(735,350, 760, 370, dashes = True)
    drawLabel('Red: Price falls', 900, 250, size = 16)
    drawLabel('(Open > Close)', 900, 270, size = 16)
    drawLabel('Green: Price rises', 630, 200, size = 16)
    drawLabel('(Close > Open)', 630, 220, size = 16)

def start_onMousePress(app, mouseX, mouseY):
    if app.registered == False:
        if clickOnCreateNewAccount(app, mouseX, mouseY):
                app.userName = app.getTextInput("Enter your username:")
                app.userPassword = app.getTextInput("Enter your password:")
                file = open('userCredentials.txt','w')
                file.write(app.userName + '\n')
                file.write(app.userPassword + '\n')
                file.close()
                if app.userName and app.userPassword:
                    app.registered = True
    elif app.registered and clickOnLogIn(app, mouseX, mouseY):
        input = app.getTextInput("Enter your username:")
        if input == app.userName:
            password = app.getTextInput("Enter your password:")
            if  password == app.userPassword:
                app.loggedIn = True
    elif app.loggedIn:
        if clickOnStartNewGame(app, mouseX, mouseY):
            if app.stockfile == None: # set default stock file
                app.stockfile = 'Gold historical data/XAU_USD Historical Data (1).csv'
                app.goldChosen = True
            while app.startDate is None or not startEndLogics.validstart(app.startDate):
                app.startDate = app.getTextInput('Enter a start date (YYYY-MM-DD):')
            while app.endDate is None or not startEndLogics.validend(app, app.endDate):
                app.endDate = app.getTextInput('Enter an end date (YYYY-MM-DD):')
            app.gameStart = True
            app.gamePaused = False
            app.filteredData, app.highPrices, app.lowPrices, app.openPrices, app.closePrices, app.tupleData= Get_Data.getData(app, app.stockfile)
            app.MA5, app.MA10, app.MA25, app.RSI, app.EMA12, app.EMA26, app.MACD, app.signal= Get_Data.getIndicators(app)
            setActiveScreen('game')
        elif clickOnApple(mouseX, mouseY):
            app.appleChosen = not app.appleChosen
            if app.appleChosen == True:
                app.stockfile = "Gold historical data/Apple Stock Price History.csv"
                app.goldChosen = app.oilChosen = False
        elif clickOnOil(mouseX, mouseY):
            app.oilChosen = not app.oilChosen
            if app.oilChosen == True:
                app.stockfile = 'Gold historical data/Oil-Dri Of America Stock Price History.csv'
                app.goldChosen = app.appleChosen = False
        elif clickOnGold(mouseX,mouseY):
            app.goldChosen = not app.goldChosen
            if app.goldChosen == True:
                app.stockfile = 'Gold historical data/XAU_USD Historical Data (1).csv'
            app.oilChosen = app.appleChosen = False
        elif app.gameStart == True and clickOnContinueGame(app, mouseX, mouseY):
            app.gamePaused = False
            setActiveScreen('game')

def clickOnContinueGame(app,mouseX, mouseY):
    return app.width/2-55 <= mouseX <= app.width/2+55 and app.height/2+100<= mouseY<= app.height/2+200
def clickOnApple(mouseX, mouseY):
    return 695 <= mouseX <= 805 and 495 <= mouseY <=545
def clickOnOil(mouseX, mouseY):
    return 445<= mouseX <= 555 and 495 <= mouseY <=545
def clickOnGold(mouseX,mouseY):
    return 195 <= mouseX <= 305 and 495 <= mouseY <=545
def clickOnStartNewGame(app, mouseX, mouseY):
    return (app.width/2 -75 <=mouseX <= app.width/2 + 75 ) and (app.height/2+75 <= mouseY <= app.height/2 + 125)
def clickOnCreateNewAccount(app, mouseX, mouseY):
    return (app.width/2 -100 <=mouseX <= app.width/2 + 100 ) and (app.height/2-50 <= mouseY <= app.height/2 + 50)
def clickOnLogIn(app, mouseX, mouseY):
    return (app.width/2 -100 <=mouseX <= app.width/2 + 100 ) and (app.height/2-50 <= mouseY <= app.height/2 + 50)



#############################################################################################
##### game page controllers and drawers #####################################################
#############################################################################################

def drawMiddlePart(app): # changing box plot and SMA, EMA, bollinger bonds
    if app.gameStart:
        drawBoxPlot.drawBoxPlot(app, app.presentingData)
        drawUpperIndicator(app)

def drawUpperIndicator(app):
    if app.MA5Check == True:
        DrawIndicators.drawSMA(app, 5)
    if app.MA10Check == True:
        DrawIndicators.drawSMA(app, 10)
    if app.MA25Check == True:
        DrawIndicators.drawSMA(app, 25)
    if app.EMA12Check == True:
        DrawIndicators.drawEMA(app, 12)
    if app.EMA26Check == True:
        DrawIndicators.drawEMA(app, 26)

def drawLowerIndicators(app):
    drawLine(100, 500, 800, 500) # lower line
    if app.RSICheck == True:
        DrawIndicators.drawRSI(app)
    if app.MACDCheck == True:
        DrawIndicators.drawMACD(app)
        DrawIndicators.drawSignal(app)

def drawLeftSideButtons(app):
    drawRect(5,5,50,50,fill = 'red') # pause button
    drawLabel('Pause', 30, 30, bold = True, fill= 'white', align = 'center')
    drawLine(100, 0, 100, app.height)
    
    # SMAs
    drawRect(5,90,90,55, dashes = True, fill = None, border = 'grey')
    drawLabel('SMA',50, 117.5)

    fill = 'lightYellow' if app.MA5Check == True else None
    drawRect(5, 150, 90, 55,border = 'black', fill = fill)
    drawLabel('MA5',50, 177.5)

    fill = 'lemonChiffon' if app.MA10Check == True else None
    drawRect(5, 205, 90, 55,border = 'black', fill = fill)
    drawLabel('MA10',50, 232.5)

    fill = 'moccasin' if app.MA25Check == True else None
    drawRect(5, 260, 90, 55,border = 'black', fill = fill)
    drawLabel('MA25',50, 287.5)

    drawRect(5,320,90,55, dashes = True, fill = None, border = 'grey')
    drawLabel('EMA',50, 347.5)

    fill = 'lightCyan' if app.EMA12Check == True else None
    drawRect(5, 380, 90, 55,border = 'black', fill = fill)
    drawLabel('EMA12',50, 407.5)

    fill = 'paleTurquoise' if app.EMA26Check == True else None
    drawRect(5, 435, 90, 55,border = 'black', fill = fill)
    drawLabel('EMA26',50, 462.5)
        
    for i in range(len(app.lowerIndicators)):
        indicatorName = app.lowerIndicatorNames[i]
        drawLabel(f'{indicatorName}', 65, 537.5 + i*75)
        drawRect(40, 510 + i*75, 50,55, fill = None, dashes = True, border = 'grey')
        if i == 0:
            if app.RSICheck == True: 
                fill = 'green'
            else: fill = None
        if i == 1:
            if app.MACDCheck == True: 
                fill = 'green'
            else: fill = None
        drawRect(5, 525+i*75, 25, 25, fill = fill, border = 'black')

def drawRightSide(app):
    drawRect(800,80, 200, 570, fill = 'darkBlue')
    drawLine(800,0,800,app.height)
    drawImage('pictures/Logo.png', 900, 40, align = 'center', width = 60, height = 60)
    drawLabel(f'Your Current Holds: {app.account.shares}', 900, 200, bold = True, fill = 'white', size = 16)
    drawLabel(f'Floating Profit: {pythonRound(app.account.getProfit(app.tupleData[app.todayIndex][1]),2)}', 
            900, 230, bold = True, fill = 'white', size = 16)
    drawLabel(f"Today's Price: {app.tupleData[app.todayIndex][1]}", 900, 245, fill = 'white', size = 16)
    drawLabel(f"Today's Date: {str(app.tupleData[app.todayIndex][0])[:10]}", 900, 260, fill = 'white', size = 16)
    drawLabel(f"Cash: {pythonRound(app.account.account)}", 900, 215, fill = 'white', size = 16)
    drawLabel('Buy', 850, 300, bold = True, fill = 'white')
    drawLabel('Sell', 950, 300, bold = True, fill = 'white')
    drawRect(850, 300, 75, 50, align = 'center', fill = None, border = 'white')
    drawRect(950, 300, 75, 50, align = 'center', fill = None, border = 'white')
    drawLabel(f'AI Current Holds: {app.AITrader.shares}', 900, 375, bold = True, fill = 'white', size = 16)
    drawLabel(f'Floating Profit: {pythonRound(app.AITrader.getProfit(app.tupleData[app.todayIndex][1]),2)}', 
            900, 400, bold = True, fill = 'white', size = 16)
    drawLabel(f"Cash: {pythonRound(app.AITrader.account)}", 900, 415, fill = 'white', size = 16)

def drawMouse(app):
    if app.mousex != None and app.mousey != None:
        drawLabel('+', app.mousex, app.mousey, size = 36)
        drawLine(app.mousex,80,app.mousex,app.height,dashes = True)
        drawLine(100,app.mousey,800,app.mousey, dashes = True)

def toolchosen(app):
    if app.diagonal == True or app.dashedSquare== True or app.arrow == True:
        return True
    return False

def game_onMousePress(app, mouseX, mouseY):
    # If annotating, and have chosen a tool, press to record starting point (app.)
    if app.annotating==True and toolchosen(app):
        app.startpoint = mouseX, mouseY

    if 5 <= mouseX <= 95 and 150 <= mouseY <205: # SMA check box
        app.MA5Check = not app.MA5Check
    elif 5 <= mouseX <= 95 and 90 <= mouseY <=145: # SMA instruction
        app.SMAinstruction = True
        app.EMAinstruction = app.MACDinstruction = app.RSIinstruction = False
        app.gamePaused = True
        setActiveScreen('instruction')
    elif 5<= mouseX <= 95 and 205 <= mouseY < 260: #MA10
        app.MA10Check = not app.MA10Check
    elif 5 <= mouseX<=95 and 260 <= mouseY <= 315: #MA25
        app.MA25Check = not app.MA25Check
    elif 5 <= mouseX<= 95 and 320 <= mouseY <= 375: # EMA icon
        app.EMAinstruction = True
        app.SMAinstruction = app.MACDinstruction = app.RSIinstruction = False
        app.gamePaused = True
        setActiveScreen('instruction')
    elif 5 <= mouseX <= 95 and 380 <= mouseY < 435: # EMA12
        app.EMA12Check = not app.EMA12Check
    elif 5 <= mouseX <= 95 and 435 <= mouseY <=490: # EMA 26
        app.EMA26Check = not app.EMA26Check
    elif clickOnMACDCheckBox(mouseX, mouseY): #MACD
        if app.RSICheck == True and app.MACDCheck == False:
            app.RSICheck = False
        app.MACDCheck = not app.MACDCheck
    elif clickOnMACDIcon(mouseX, mouseY):# MACD instructinon
        app.MACDinstruction = True
        app.EMAinstruction = app.SMAinstruction = app.RSIinstruction = False
        app.gamePaused = True
        setActiveScreen('instruction')
    elif clickOnRSICheckBox(mouseX, mouseY):
        if app.RSICheck == False and app.MACDCheck == True:
            app.MACDCheck = False
        app.RSICheck = not app.RSICheck
    elif clickOnRSIIcon(mouseX, mouseY):
        app.RSIinstruction = True
        app.EMAinstruction = app.MACDinstruction = app.SMAinstruction = False
        app.gamePaused = True
        setActiveScreen('instruction')
    elif 15 <= mouseY <= 65 and 300 <= mouseX <= 350: # make annotation
        app.gamePaused = app.annotating = not app.gamePaused
        if app.annotating == False:
            app.diagonals = []
            app.dashedRects = []
            app.arrows = []
    elif 15 <= mouseY <= 65 and 355 <= mouseX <= 405 and app.annotating == True: # draw line
        app.diagonal = not app.diagonal
        app.dashedSquare= app.arrow =app.clearAll = False
    elif  15 <= mouseY <= 65 and 410 <= mouseX <= 460 and app.annotating == True: # draw dashed rect
        app.dashedSquare = not app.dashedSquare
        app.diagonal= app.arrow =app.clearAll = False
    elif 15 <= mouseY <= 65 and 465 <= mouseX <= 515 and app.annotating == True: # draw arrow
        app.arrow = not app.arrow
        app.diagonal= app.dashedSquare =app.clearAll = False
    elif 15 <= mouseY <= 65 and 520 <= mouseX <= 570 and app.annotating == True: # erase (by dragging)
        app.diagonal= app.dashedSquare =app.arrow = False
        app.diagonals = []
        app.dashedRects = []
        app.arrows = []
    elif 5 <= mouseY <= 25 and 150 <= mouseX <= 205: # zoom in
        if len(app.presentingData) > 3:
            app.presentingData = app.presentingData[3:]
            app.zoomingin = True
        elif len(app.presentingData) == 30: app.zoomingout = False
        else: pass
    elif 210 <=mouseX <= 265 and 5 <= mouseY <= 25: # zoom out
        if len(app.presentingData) == app.todayIndex:
            return
        if len(app.presentingData) <= app.todayIndex and len(app.presentingData) < 60: #2 months/ maximum all dates happened
            startIndex = app.todayIndex - len(app.presentingData)
            if startIndex >= 3:
                app.presentingData = app.tupleData[startIndex - 3: startIndex] + app.presentingData
                app.zoomingout = True
        elif len(app.presentingData) == 30: app.zoomingin = False
    elif 55 <= mouseY <= 75 and 150 <= mouseX <= 205: # speed up
        if app.stepsPerSecond <=10:
            app.stepsPerSecond += 0.2
    elif 55 <= mouseY <= 75 and 210 <= mouseX <= 265: # slow down
        if app.stepsPerSecond >0.2:
            app.stepsPerSecond -= 0.2
    elif 0<= mouseX <= 75 and 0 <= mouseY <= 75: #clickOnPauseGame
        app.gamePaused = True
        setActiveScreen('pause')

    elif 812 <= mouseX <= 888 and 275 <=mouseY <= 325: #click on buy
        app.gamePaused = True
        hold = app.getTextInput('Buy in (type in an integer):')
        if hold == '':
            app.gamePaused = False
            return
        else: hold = int(hold)
        if OOPLogics.validBuy(app,hold):
            order = OOPLogics.Order(+1, hold, app.tupleData[app.todayIndex][1])
            app.account.buyShare(order)
        app.gamePaused = False
    elif 912<= mouseX <= 988 and 275 <= mouseY <= 325:
        app.gamePaused = True
        hold = app.getTextInput('Sell out (type in an integer):')
        if hold == '':
            app.gamePaused = False
            return
        else: hold = int(hold)
        if OOPLogics.validSell(app,hold):
            order = OOPLogics.Order(-1, abs(hold), app.tupleData[app.todayIndex][1])
            app.account.sellShare(order)
        app.gamePaused = False

def clickOnRSICheckBox(mouseX, mouseY):
    return 5 <= mouseX <= 35 and 525 <= mouseY <= 550
def clickOnRSIIcon(mouseX, mouseY):
    return 40 <= mouseX <= 90 and 510 <= mouseY <= 565
def clickOnMACDCheckBox(mouseX, mouseY):
    return 5<= mouseX <= 30 and 600 <= mouseY <= 625
def clickOnMACDIcon(mouseX, mouseY):
    return 40 <= mouseX <= 90 and 585 <= mouseY <= 640

def game_onMouseRelease(app,mouseX,mouseY):
    app.dragging = False
    if app.annotating and 100 <= mouseX <= 800 and 85<= mouseY <= 500:
        app.endPoint = mouseX, mouseY
        if app.diagonal == True:
            startx, starty = app.startpoint
            newline = DrawAnnotation.makeLine(startx, starty, mouseX, mouseY)
            if newline != None:
                app.diagonals.append(newline)
        elif app.dashedSquare is True:
            startx, starty = app.startpoint
            newrect = DrawAnnotation.makeDashedRect(startx, starty,mouseX, mouseY)
            if newrect != None:
                app.dashedRects.append(newrect)
        elif app.arrow is True:
            startx, starty = app.startpoint
            newarrow = DrawAnnotation.makeArrow(startx, starty, mouseX, mouseY)
            if newarrow != None:
                app.arrows.append(newarrow)

def game_onMouseMove(app, mouseX, mouseY):
    if 100 <= mouseX<= 800 and 80 <= mouseY <= 500: # show this nomatter what
        app.mousex = mouseX
        app.mousey = mouseY

def game_onKeyPress(app,key):
    if key == 'p':
        app.gamePaused = not app.gamePaused
    elif key == 's':
        if app.stepsPerSecond >= 0.2: app.stepsPerSecond -= 0.2
    elif key == 'f':
        if app.stepsPerSecond < 5: app.stepsPerSecond += 0.2

def game_onStep(app):
    # if on game page
    if app.todayIndex == len(app.tupleData)-1: 
        app.gameOver = True
        if app.account.shares != 0:
            order = OOPLogics.Order(-1,app.account.shares,app.tupleData[app.todayIndex][1])
            app.account.sellShare(order) # app.account sell all the shares and realize profit
        if app.AITrader.shares != 0:
            orderAI = OOPLogics.Order(-1, app.AITrader.shares, app.tupleData[app.todayIndex][1])
            app.AITrader.sellShare(orderAI)
        setActiveScreen('gameOver')
    if app.gameStart == True and app.gamePaused == False:
        if app.todayIndex < len(app.tupleData):
            if len(app.presentingData) < 30:
                app.presentingData.append(app.tupleData[app.todayIndex])
            else:
                app.presentingData = app.presentingData[1:] + [app.tupleData[app.todayIndex]]
            OOPLogics.AImakeDecision(app)
            OOPLogics.fixDecision(app)
            app.todayIndex += 1

#############################################################################################
##### Pause, Game Over, instruction controllers and drawers #################################
#############################################################################################

def drawPauseBoard(app):
    url = 'https://www.shutterstock.com/shutterstock/videos/14307913/thumb/3.jpg?ip=x480'
    imageWidth, imageHeight = 480,270
    drawRect(0,0,app.width,app.height) # bg color
    drawLabel('Gold Spot', app.width/2, 50, fill = 'gold', size = 40, bold = True, align = 'top') #stock Name
    drawImage(url ,app.width/2, app.height/2-100, align='center')
    buttonY = app.height / 2 + imageHeight / 2
    drawRect(app.width / 3 , buttonY+20, 100, 80, border='white',align = 'center')  # Continue
    drawLabel('Continue', app.width / 3 , buttonY+20, fill='white', size = 16)
    drawRect(app.width *2 / 3 , buttonY+20, 100, 80, border='white',align = 'center')  # Restart
    drawLabel('Restart', app.width *2 / 3 , buttonY+20, fill='white', size = 16)

def pause_onMousePress(app,mouseX,mouseY):
    imageWidth, imageHeight = 480,270
    buttonY = app.height / 2 + imageHeight / 2
    if app.width / 3 - 50 <= mouseX <= app.width / 3 + 50 and 440 <= mouseY <= 520:
        app.gamePaused = False
        setActiveScreen('game')  # Continue
    elif 617 <= mouseX <= 717 and 440 <= mouseY <= 520:
        startEndLogics.restart(app)  # Restart
        setActiveScreen('game')

def drawGameOverBoard(app):
    drawRect(0,0, app.width, app.height, fill = 'darkSlateGray')
    drawLabel('Game Over!', app.width/2, app.height/4, fill = 'gold', bold = True, size = 30)
    verb = 'earned' if app.account.realizedProfit >=0 else 'loss'
    drawLabel(f'You {verb}: {rounded(app.account.realizedProfit)} dollars!', app.width/2, app.height/3,size = 20, fill = 'white')

    drawRect(app.width/2, app.height/3+30, 300, 30, align = 'center', fill = 'indigo')
    drawLabel(f"Auto trader {verb}: {rounded(app.AITrader.realizedProfit)} dollars", app.width/2, app.height/3 + 30, size = 20, fill = 'white')
    drawLabel("Click here to see your decisions and AI's", app.width/2, 500, size = 16, fill = 'white')
    drawRect(app.width/2, 500, 300, 50, fill = None, border = 'white', align = 'center')
    drawLabel('Try to earn more next time ^v^', app.width/2, 545, size = 20, fill = 'white')
    drawLabel('Press r to return game setting page', app.width/2, 580, size = 16, bold = True, fill = 'white')
    
def gameOver_onKeyPress(app,key):
    if key == 'r':
        startEndLogics.reset(app)
        setActiveScreen('start')
def gameOver_onMousePress(app, mouseX, mouseY):
    if clickOnAIsolution(mouseX,mouseY):
        app.AIsolution = True
        setActiveScreen('instruction')
def clickOnAIsolution(mouseX,mouseY):
    return 475 <= mouseY <= 525 and 350 <= mouseX <= 650

def instruction_redrawAll(app):
    # cite: https://www.investopedia.com/ask/answers/121114/what-difference-between-golden-cross-and-death-cross-pattern.asp
    # cite: https://capital.com/exponential-moving-average#:~:text=An%20EMA%20crossover%20strategy%20involves,signal%2C%20indicating%20a%20potential%20uptrend.
    # cite: https://stockstotrade.com/rsi-oversold-overbought/
    # cite: https://www.investopedia.com/terms/m/macd.asp
    if app.gameOver == False:
        drawRect(0,0,app.width, app.height, fill = 'aliceBlue')
        drawLabel('What is this for?', app.width/2, 30, size = 40, bold = True)
        if app.EMAinstruction == True: 
            drawLabel('EMA', app.width/2, 80, bold = True, size = 30)
            drawLabel('This indicator stands for Exponential Moving Average.', 100, 120, align = 'left', size = 20)
            drawLabel('It applies more weight to data that is more current, instead of simply taking average.',
                    100, 150, align = 'left', size = 20)
            drawLabel("You can see there're EMA12, EMA26 in the game, that means the index is calculated", 
                    100, 180, align = 'left', size = 20)
            drawLabel('by EMA = (K x (C - P)) + P',100, 210, align = 'left', size = 20)
            drawLabel("C = Current Price, P = Previous periods EMA (for the first calculation, use SMA)", 
                    100, 240, size = 20, align = 'left')
            drawLabel("K = Exponential smoothing constant, applying appropriate weight to the most recent price. ", 
                    100, 270, align = 'left', size = 20)
            drawLabel('EMA crossovers:', 100, 300, align = 'left', size = 20)
            drawLabel('·Golden Cross: when a shorter-period EMA crosses above a longer-period EMA', 
                    120, 330, align = 'left', size = 20)
            drawLabel('it indicates a potential uptrend. ',
                    120, 360, align = 'left', size = 20, fill = 'darkViolet', bold = True)
            drawLabel("·Death Cross: when a shorter-period EMA crosses below a longer-period EMA",
                    120, 390, align = 'left', size = 20)
            drawLabel('it suggests a potential downtrend.',
                    120, 420, align = 'left', size = 20, fill = 'darkViolet', bold = True)
            drawLabel('However, note that this indicator never works alone, please also check other indicators.', 
                    app.width/2, 510, fill = 'red', size = 20)
            
        elif app.SMAinstruction == True:
            drawLabel('SMA', app.width/2, 80, bold = True, size = 30)
            drawLabel('This indicator stands for Simple Moving Average.',
                    100, 120, align = 'left', size = 20)
            drawLabel('It is simply the average price over the specified period.',
                    100, 150, align = 'left', size = 20)
            drawLabel("You can see there're MA5, MA10, and MA25 in the game, that means the index is calculated",
                    100, 180, align = 'left', size = 20)
            drawLabel('by taking average over past 5, 10, or 25 days.',100, 210, align = 'left', size = 20)
            drawLabel("SMAs are often used to determine trend direction.", 100, 240, size = 20, align = 'left')
            drawLabel("We call MA5 as 'short-term MA'; MA25 here as 'mid-long-term MA'.",
                    100, 270, align = 'left', size = 20)
            drawLabel('SMA indicates the trend of stock price with crosses:',
                    100, 300, align = 'left', size = 20)
            drawLabel('·A Golden Cross occurs when a short-term MA crosses over',
                    120, 330, align = 'left', size = 20)
            drawLabel('a major long-term moving average to the upside. ',
                    120, 360, align = 'left', size = 20)
            drawLabel("·A Death Cross refers to a crossover of a short-term MA moving",
                    120, 390, align = 'left', size = 20)
            drawLabel('in the opposite direction of the golden cross.', 
                    120, 420, align = 'left', size = 20)
            drawLabel('A golden cross is a visual signal of a long-term bull market (going up) going forward,', 
                    100, 450, align = 'left', size = 20, fill = 'darkViolet', bold = True)
            drawLabel('while a death cross suggests a long-term bear (going down) market.', 
                    100, 480, align = 'left', size = 20, fill = 'darkViolet', bold = True)
            drawLabel('However, note that this indicator never works alone, please also check other indicators.', 
                    app.width/2, 510, fill = 'red', size = 20)
                    
        elif app.RSIinstruction == True:
            drawLabel('RSI', app.width/2, 80, bold = True, size = 30)
            drawLabel('This indicator stands for Relative Strength Index.',
                    100, 120, align = 'left', size = 20)
            drawLabel('It measures the speed and change of price movements',
                    100, 150, align = 'left', size = 20)
            drawLabel("and signals potential reversals in market trends.", 
                    100, 180, align = 'left', size = 20)
            drawLabel('RSI value varies from 0 to 100, the two dotted lines represents 70 and 30, accordingly.',
                    100, 210, align = 'left', size = 20)
            drawLabel("RSI helps traders identify overbought and oversold conditions in the stock market.", 
                    100, 240, size = 20, align = 'left')
            drawLabel("The upper dotted line is the overbought line, which has value of 70", 
                    100, 270, align = 'left', size = 20)
            drawLabel('The lower line is the oversold line, which has value of 30', 
                    100, 300, align = 'left', size = 20)
            drawLabel('·Overbought occurs when its recent price gains have been rapid and significant, ', 
                    120, 330, align = 'left', size = 20)
            drawLabel('potentially leading to an imminent price decline.', 
                    120, 360, align = 'left', size = 20)
            drawLabel("·Oversold occurs when its recent price declines have been rapid and significant,", 
                    120, 390, align = 'left', size = 20)
            drawLabel('suggesting that the stock may be undervalued', 
                    120, 420, align = 'left', size = 20)
            drawLabel('Overbought signals for a selling opportunity, while oversold suggests a buying opportunity.', 
                    100, 450, align = 'left', size = 20, fill = 'darkViolet', bold = True)
            drawLabel('However, note that this indicator never works alone, please also check other indicators.', 
                    app.width/2, 510, fill = 'red', size = 20)

        elif app.MACDinstruction == True:
            drawLabel('MACD', app.width/2, 80, bold = True, size = 30)
            drawLabel('This indicator stands for Moving average convergence/divergence.', 
                    100, 120, align = 'left', size = 20)
            drawLabel('It helps investors identify entry points for buying or selling.',
                    100, 150, align = 'left', size = 20)
            drawLabel("The MACD line is calculated by subtracting the 26-period exponential moving average (EMA) ", 
                    100, 180, align = 'left', size = 20)
            drawLabel('from the 12-period EMA; The signal line is a EMA9 of the MACD line.',
                    100, 210, align = 'left', size = 20)
            drawLabel("MACD helps traders identify overbought and oversold conditions in the stock market.", 
                    100, 240, size = 20, align = 'left')
            drawLabel("MACD is displayed with a histogram that graphs the distance between MACD and its signal line.", 
                    100, 270, align = 'left', size = 20)
            drawLabel('If MACD is above the signal line, the histogram will be above the baseline or zero line, vice versa', 
                    100, 300, align = 'left', size = 20)
            drawLabel('·Overbought is indicated when MACD crosses below its signal line  ', 
                    120, 330, align = 'left', size = 20)
            drawLabel('following a brief move higher within a longer-term downtrend', 
                    120, 360, align = 'left', size = 20)
            drawLabel("·Oversold is indicated MACD crosses above its signal line after a brief downside correction", 
                    120, 390, align = 'left', size = 20)
            drawLabel('within a longer-term uptren', 
                    120, 420, align = 'left', size = 20)
            drawLabel('Overbought signals for a selling opportunity, while oversold suggests a buying opportunity.', 
                    100, 450, align = 'left', size = 20, fill = 'darkViolet', bold = True)
            drawLabel('However, note that this indicator never works alone, please also check other indicators.', 
                    app.width/2, 510, fill = 'red', size = 20)
            
    else: # game is Over, show AI and player's decisions
        # title
        drawRect(0,0,app.width, app.height, fill = 'lightBlue')
        drawLabel('Decision History', app.width/2, 50, size = 30, bold = True)
        drawLine(300, 100, 700, 100, lineWidth = 5)
        # Player's
        verb = 'earned' if app.account.realizedProfit >=0 else 'loss'
        drawLabel(f'You {verb} {rounded(app.account.realizedProfit)} dollars', 
                app.width/4, app.height/3,size = 20, fill = 'white')
        for order in app.account.orders:
            drawLabel(f'{order}', app.width/4, app.height/3+30 + order.number*20, size = 15)
        # AI's
        verb = 'earned' if app.AITrader.realizedProfit >=0 else 'loss'
        drawLabel(f'Auto trader {verb} {rounded(app.AITrader.realizedProfit)} dollars', 
                app.width*3/4, app.height/3,size = 20, fill = 'black')
        count = 0
        for order in app.AITrader.orders:
            if order.number < 10 and count == order.number:
                drawLabel(f'{order}', app.width*3/4, app.height/3+30 + order.number*20, size = 15)
            count += 1
    drawRect(app.width/2, 580, 200, 50, align = 'center', borderWidth = 5, fill = 'white', border = 'black')
    drawLabel('Press to return',app.width/2, 580, align = 'center', size = 20, bold = True)

def instruction_onMousePress(app, mouseX, mouseY):
    if 400<= mouseX<=600 and 555 <= mouseY <= 605:
        app.gamePaused = False
        app.SMAinstruction = False
        app.EMAinsturction = False
        app.RSIinstruction = False
        app.MACDinstruction = False
        if not app.gameOver:
            setActiveScreen('game')
        else:
            setActiveScreen('gameOver')
#######################################
########## wrapping up ################
#######################################

def start_redrawAll(app):
    drawGameSettingPage(app)

def game_redrawAll(app):
    drawLeftSideButtons(app)
    drawRightSide(app)
    DrawAnnotation.drawUpsideButtons(app)
    drawMiddlePart(app)
    drawLowerIndicators(app)
    if not app.gamePaused:
        drawMouse(app)
    else:# game paused
        if app.annotating:
            if app.diagonals != []:
                DrawAnnotation.drawDiagonals(app)
            if app.dashedRects != []:
                DrawAnnotation.drawDashedRects(app)
            if app.arrows != []:
                DrawAnnotation.drawArrows(app)

def pause_redrawAll(app):
    drawPauseBoard(app)

def gameOver_redrawAll(app):
    drawGameOverBoard(app)

def main():
    runAppWithScreens(initialScreen='start', width=1000, height=650)

main()
