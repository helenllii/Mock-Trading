from cmu_graphics import*
def drawSMA(app, timeperiod):  # draw MA5, MA10, MA25
    lastMA5 = None
    drawingList = None
    linecolor = None
    if timeperiod == 5:
        drawingList = app.MA5
        linecolor = 'red'
    elif timeperiod == 10:
        drawingList = app.MA10
        linecolor = 'fireBrick'
    elif timeperiod == 25:
        drawingList = app.MA25
        linecolor = 'salmon'
    presentingDays = len(app.presentingData)
    endIndex = app.todayIndex
    startIndex = app.todayIndex - presentingDays
    startIndex = max(0, startIndex)  # used chat gpt to help debug # prevent exceeding index
    endIndex = min(len(drawingList) - 1, endIndex)

    presentingHigh = app.highPrices[startIndex:endIndex + 1]
    presentingLow = app.lowPrices[startIndex:endIndex + 1]

    if len(presentingHigh) >= 1:
        highestY = max(presentingHigh)
        lowestY = min(presentingLow)
        if highestY == lowestY:
            pxperdollar = 1
        else:
            pxperdollar = 420 / (highestY - lowestY)
        boxWidth = max((750 / 25) / 1.5, 5)
        if app.zoomingin or app.zoomingout:
            boxWidth = 750 / presentingDays / 1.5
        gap = 5
        totalBoxWidth = boxWidth + gap
    for i in range(startIndex, endIndex):
        if i >= len(drawingList) or drawingList[i] == None:
            continue  # skip nan value
        if lastMA5 is None:
            lastMA5 = drawingList[i]
            continue
        else:
            xPos = 100 + (i - startIndex-1) * totalBoxWidth + boxWidth / 2
            lastXPos = 100 + (i - 1 - startIndex-1) * totalBoxWidth + boxWidth / 2 
            if xPos > 800:
                break
            yPos = 500 - pxperdollar * (drawingList[i] - lowestY)
            lastYPos = 500 - pxperdollar * (lastMA5 - lowestY)
            if lastYPos > 500 or lastYPos< 80: # over the height of middle part
                lastMA5 = drawingList[i]
                continue
            if lastXPos < 100:
                lastMA5 = drawingList[i]
                continue
            drawLine(lastXPos, lastYPos, xPos, yPos, fill=linecolor)

            lastMA5 = drawingList[i]

def drawEMA(app, timeperiod):
    lastEMA = None
    drawingList = None
    linecolor = None
    if timeperiod == 12:
        drawingList = app.EMA12
        linecolor = 'steelBlue'
    elif timeperiod == 26:
        drawingList = app.EMA26
        linecolor = 'mediumBlue'
    presentingDays = len(app.presentingData)
    endIndex = app.todayIndex
    startIndex = app.todayIndex - presentingDays
    startIndex = max(0, startIndex)
    endIndex = min(len(drawingList) - 1, endIndex)

    presentingHigh = app.highPrices[startIndex:endIndex + 1]
    presentingLow = app.lowPrices[startIndex:endIndex + 1]

    if len(presentingHigh) >= 1:
        highestX = max(presentingHigh)
        lowestX = min(presentingLow)
        if highestX == lowestX:
            pxperdollar = 1
        else:
            pxperdollar = 420 / (highestX - lowestX)
        boxWidth = max((750 / 25) / 1.5, 5)
        if app.zoomingin or app.zoomingout:
            boxWidth = 750 / presentingDays / 1.5
        gap = 5
        totalBoxWidth = boxWidth + gap
    for i in range(startIndex, endIndex):
        if drawingList[i]==0:
            continue  # skip nan value
        if lastEMA is None:
            lastEMA = drawingList[i]
            continue
        else:
            xPos = 100 + (i - startIndex-1) * totalBoxWidth + boxWidth / 2
            lastXPos = 100 + (i - 1 - startIndex-1) * totalBoxWidth + boxWidth / 2
            if lastXPos < 100: 
                lastEMA = drawingList[i]
                continue
            if xPos > 800:
                break
            yPos = 500 - pxperdollar * (drawingList[i] - lowestX)
            lastYPos = 500 - pxperdollar * (lastEMA - lowestX)
            if lastYPos > 500 or lastYPos< 80: # over the height of middle part 
                lastEMA = drawingList[i]
                continue
            drawLine(lastXPos, lastYPos, xPos, yPos, fill = linecolor)
            lastEMA = drawingList[i]
            

def drawRSI(app):
    overbought = app.height - 150*0.7
    oversold = app.height - 150*0.3
    drawLine(100, overbought, 800, overbought, dashes = True) # 70% overbought line
    drawLine(100, oversold, 800, oversold, dashes = True) # 30% oversold line
    lastRSI = None
    drawingList = app.RSI
    presentingDays = len(app.presentingData)
    endIndex = app.todayIndex
    startIndex = app.todayIndex - presentingDays
    startIndex = max(0, startIndex)
    endIndex = min(len(drawingList) - 1, endIndex)

    if len(app.presentingData) >= 1:
        boxWidth = max((750 / 26) / 1.5, 5)
        if app.zoomingin or app.zoomingout:
            boxWidth = 750 / presentingDays / 1.5
        gap = 5
        totalBoxWidth = boxWidth + gap
    for i in range(startIndex, endIndex + 1):
        if i >= len(drawingList) or drawingList[i] == None:
            continue  # skip nan value
        if lastRSI is None:
            lastRSI = drawingList[i]
            continue
        else:
            xPos = 100 + (i - startIndex) * totalBoxWidth
            if xPos > 800:
                break
            yPos = app.height - drawingList[i]
            lastYPos = app.height - lastRSI
            drawLine(xPos - totalBoxWidth, lastYPos, xPos, yPos, fill="blue")
            lastRSI = drawingList[i]

def drawMACD(app):
    # draw MACD line
    baseLine = 575
    lastMACD = None
    drawingList = app.MACD
    highestVal = max(drawingList[27:])
    lowestVal = min(drawingList[27:])
    pxperunit = 75/(highestVal-lowestVal)
    presentingDays = len(app.presentingData)
    endIndex = app.todayIndex
    startIndex = app.todayIndex - presentingDays
    startIndex = max(0, startIndex)
    endIndex = min(len(drawingList) - 1, endIndex)

    if len(app.presentingData) >= 1:
        boxWidth = max((750 / 25) / 1.5, 5)
        if app.zoomingin or app.zoomingout:
            boxWidth = 750 / presentingDays / 1.5
        gap = 5
        totalBoxWidth = boxWidth + gap
    for i in range(startIndex, endIndex + 1):
        if i >= len(drawingList) or drawingList[i] == None:
            continue  # skip nan value
        if lastMACD is None:
            lastMACD = drawingList[i]
            continue
        else:
            xPos = 100 + (i - startIndex-1) * totalBoxWidth + boxWidth / 2
            lastXPos = 100 + (i - 1 - startIndex-1) * totalBoxWidth + boxWidth / 2
            if lastXPos < 100:
                lastMACD = drawingList[i]
                continue
            if xPos > 800:
                break
            yPos = baseLine - drawingList[i]*pxperunit
            lastYPos = baseLine - lastMACD*pxperunit
            drawLine(lastXPos, lastYPos, xPos, yPos, fill="blue")
            lastMACD = drawingList[i]


def drawSignal(app):
    lastSignal = None
    baseLine = 575
    drawingList = app.signal
    presentingDays = len(app.presentingData)
    endIndex = app.todayIndex
    startIndex = app.todayIndex - presentingDays
    startIndex = max(0, startIndex)
    endIndex = min(len(drawingList) - 1, endIndex)
    highestVal = max(drawingList[27:])
    lowestVal = min(drawingList[27:])
    pxperunit = 75/(highestVal-lowestVal)
    if len(app.presentingData) >= 1:
        boxWidth = max((750 / 25) / 1.5, 5)
        if app.zoomingin or app.zoomingout:
            boxWidth = 750 / presentingDays / 1.5
        gap = 5
        totalBoxWidth = boxWidth + gap
    for i in range(startIndex, endIndex + 1):
        if i >= len(drawingList) or drawingList[i] == None:
            continue  # skip nan value
        if lastSignal is None:
            lastSignal = drawingList[i]
            continue
        else:
            xPos = 100 + (i - startIndex-1) * totalBoxWidth + boxWidth / 2
            lastXPos = 100 + (i - 1 - startIndex-1) * totalBoxWidth + boxWidth / 2
            if lastXPos < 100:
                lastSignal = drawingList[i]
                continue
            if xPos > 800:
                break
            yPos = baseLine - drawingList[i]*pxperunit
            lastYPos = baseLine - lastSignal*pxperunit
            drawLine(lastXPos, lastYPos, xPos, yPos, fill='lightSkyBlue')
            lastSignal = drawingList[i]