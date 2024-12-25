from cmu_graphics import *

def drawBoxPlot(app, data):
    maxBoxes = 25
    presentingDays = len(app.presentingData)
    endIndex = app.todayIndex
    startIndex = app.todayIndex - presentingDays
    presentingHigh = app.highPrices[startIndex:endIndex]
    presentingLow = app.lowPrices[startIndex:endIndex]
    if len(presentingHigh) < 1 or len(presentingLow) < 1:
        return
    if len(presentingHigh) >= 1:
        highestX = max(presentingHigh)
        lowestX = min(presentingLow)
        pxperdollar = 420 / (highestX - lowestX)
        boxWidth = max((700 / maxBoxes) / 1.5, 5)
        if app.zoomingin or app.zoomingout:
            boxWidth = 700/presentingDays/1.5
        gap = 5
        totalBoxWidth = boxWidth + gap
        for box in range(presentingDays):
            openPrice = app.presentingData[box][2]
            close = app.presentingData[box][1]
            high = presentingHigh[box]
            low = presentingLow[box]
            # boxHeight
            boxHeight = pxperdollar * abs(openPrice - close)
            if almostEqual(boxHeight,0): boxHeight = 0.1
            # High line and low line
            highLinelength = pxperdollar * (high - max(openPrice, close))
            lowLinelength = pxperdollar * (min(openPrice, close) - low)
            # Y coordinate
            lowlineendY = 500 - (low - lowestX) * pxperdollar
            highlinestartY = 80 + (highestX - high) * pxperdollar

            boxstartY = highlinestartY + highLinelength
            boxendY = boxstartY + boxHeight
            # If Open > Close (the price gets lower) then fill with red; otherwise green
            fill = 'red' if openPrice > close else None
            linefill = 'red' if openPrice > close else 'green'
            border = 'red' if fill=='red' else 'green'
            xPos = 100 + box * totalBoxWidth
            if xPos + totalBoxWidth > 800:  # stop drawing if exceed the boundary
                break
            drawLine(xPos+boxWidth/2, highlinestartY, xPos+boxWidth/2, boxstartY, fill=linefill)  # high
            drawRect(xPos, boxstartY, boxWidth, boxHeight, fill=fill, border=border)  # box
            drawLine(xPos+boxWidth/2, boxendY, xPos+boxWidth/2, lowlineendY, fill=linefill)  # low