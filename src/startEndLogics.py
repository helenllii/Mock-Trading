from datetime import datetime
import OOPLogics
#  use python date time lib https://www.digitalocean.com/community/tutorials/python-string-to-datetime-strptime
def validstart(date):
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
        earliest = datetime(2005, 1, 3)
        latest = datetime(2024, 3, 13)
        if earliest <= date <= latest:
            return True
        else:
            return False
    except ValueError:
        return False
def validend(app, date):
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
        earliest = datetime.strptime(app.startDate, "%Y-%m-%d")
        latest = datetime(2024, 3, 13)
        if earliest <= date <= latest and (date - earliest).days >= 60: # at least 2 months, will show in instruction
            return True
        else:
            return False
    except ValueError:
        return False

def restart(app):
    app.todayIndex = 0
    app.stepsPerSecond = 2
    app.gamePaused = False

    app.mousex = None # for the middle +
    app.mousey = None

    app.presentingData = [] # data that need to be drawn on the game board

    app.MA5Check = False # check box
    app.MA10Check = False
    app.MA25Check = False
    app.SMAinstruction = False
    app.EMA12Check = app.EMA26Check = False
    app.EMAinstruction = False
    app.MACDCheck = False
    app.MACDinstruction = False
    app.RSICheck = False
    app.RSIinstruction = False
    app.hint = ''

    app.annotating = False
    app.diagonal = app.dashedSquare = app.arrow  = app.clearAll = False
    app.annotation = [app.diagonal, app.dashedSquare, app.arrow, app.clearAll]
    app.dashedRects = []
    app.diagonals = []
    app.arrows = [] # store simple namespace
    app.dragging = False
    app.startpoint = None, None # for annotation
    app.endpoint = None, None # for annotation
    app.zoomingin = app.zoomingout = False

    app.AITrader = OOPLogics.Account(0,1000000)

def reset(app):
    app.gameSettingPage = True
    app.account = OOPLogics.Account(0,1000000)
    app.stockfile = None
    app.goldChosen = False
    app.existingData = [] # the data excerpt according to User Input
    app.startDate = None
    app.endDate = None
    app.todayIndex = 0
    app.gameStart = False
    app.gamePaused = False
    app.gameOver = False
    app.showGameInfo = False # inside game board
    app.stepsPerSecond = 2

    app.mousex = None # for the middle +
    app.mousey = None
    app.presentingData = [] # data that need to be drawn on the game board
    app.dataForGame = None # all data will be presented (from start to end)
    app.filteredData = app.highPrices = app.lowPrices = app.openPrices = app.closePrices = app.tupleData = None
    app.MA5=app.MA10=app.MA25 = app.EMA12 = app.EMA26 =app.RSI = app.MACD= app.signal = None
    
    app.MA5Check = False # check box
    app.MA10Check = False
    app.MA25Check = False
    app.SMAinstruction = False
    app.EMA12Check = app.EMA26Check = False
    app.EMAinstruction = False
    app.MACDCheck = False
    app.MACDinstruction = False
    app.RSICheck = False
    app.RSIinstruction = False
    app.checkbox = [app.MA5Check, app.MA10Check, app.MA25Check, app.EMA12Check, app.EMA26Check, app.RSICheck, app.MACDCheck]
    app.upperIndicators = [app.MA5Check, app.MA10Check, app.MA25Check, app.EMA12Check, app.EMA26Check]
    app.lowerIndicators = [app.RSICheck, app.MACDCheck]
    app.upperIndicatorNames = ['MA5', 'MA10','MA25','EMA12','EMA26']
    app.lowerIndicatorNames = ['RSI', 'MACD']
    app.hint = ''

    app.annotating = False
    app.diagonal = app.dashedSquare = app.arrow  = app.clearAll = False
    app.annotation = [app.diagonal, app.dashedSquare, app.arrow, app.clearAll]
    app.dashedRects = []
    app.diagonals = []
    app.arrows = [] # store simple namespace
    app.dragging = False
    app.startpoint = None, None # for annotation
    app.endpoint = None, None # for annotation
    app.zoomingin = app.zoomingout = False

    app.AITrader = OOPLogics.Account(0,1000000)