from cmu_graphics import*
from types import SimpleNamespace
def drawUpsideButtons(app):
    drawLine(0,80,app.width,80)
    # zoom in out
    drawLabel('Zoom', 102, 15,bold = True, size = 16, align = 'left')
    drawRect(150,5,60,20,fill = None, border = 'black')
    drawLabel('+',172.5,15, size = 20, bold = True, fill = 'black', align = 'center')
    drawRect(205,5,60,20,fill = None, border = 'black')
    drawLabel('-',235,15,size = 40, bold = True, fill = 'black', align = 'top')

    # change steps per second
    drawLabel('Speed', 102, 65,bold = True, size = 16, align = 'left')
    drawRect(150,55,60,20,fill = None, border = 'black')
    drawLabel('+',172.5,65, size = 20, bold = True, fill = 'black', align = 'center')
    drawRect(205,55,60,20,fill = None, border = 'black')
    drawLabel('-',235,65,size = 40, bold = True, fill = 'black', align = 'top')
    
    # draw annotation buttons (image cite: https://em-content.zobj.net/source/skype/289/wastebasket_1f5d1-fe0f.png, https://cdn.creazilla.com/emojis/47161/pen-emoji-clipart-xl.png, https://cdn-icons-png.flaticon.com/512/815/815497.png, https://static.thenounproject.com/png/230519-200.png, https://cdn-icons-png.flaticon.com/512/2223/2223606.png, https://attic.sh/1wexb5fu3stjbl4cyl9g1773c1g6)
    penUrl='MockTrading/pictures/pen.png'
    drawImage(penUrl, 300, 15,width=50, height=50)
    urls = ['MockTrading/pictures/diagonalLine.png', 'MockTrading/pictures/dashedRect.png','MockTrading/pictures/arrow.png', 'MockTrading/pictures/trashcan.png'] 
    # diagonal, dashed square, arrow, clearAll(trash can emoji)
    for i in range(1,5):
        border = 'black' if app.annotating else 'grey'
        fill = None
        if app.annotation[i-1] == True: fill = 'green'
        imageurl = urls[i-1]
        drawRect(300 + i*55, 15, 50, 50, border = border, fill = fill)
        drawImage(imageurl, 302 + i*55, 17, width = 45, height = 45)
    
    # Stock Name
    stockName = None
    fill = None
    if app.goldChosen == True:
        stockName = 'Gold Spot'
        fill = 'gold'
    elif app.oilChosen == True:
        stockName = 'Oil'
        fill = 'darkSeaGreen'
    elif app.appleChosen == True:
        stockName = 'Apple'
        fill = 'lightPink'
    drawLabel(f'{stockName}', 700, 40, size = 30, fill = fill)

def makeLine(startX,startY,endX,endY):
    line = SimpleNamespace()
    line.startX = startX
    line.startY = startY
    line.endX = endX
    line.endY = endY
    if abs(line.startX - line.endX) > 0 or abs(line.startY - line.endY) > 0:
        return line
def makeDashedRect(startX,startY,endX,endY ):
    dashedrect = SimpleNamespace()
    dashedrect.startX = min(startX,endX)
    dashedrect.startY = min(startY,endY)
    dashedrect.width = abs(endX-startX)
    dashedrect.height = abs(endY-startY)
    if dashedrect.height > 0 and dashedrect.width > 0:
        return dashedrect
def makeArrow(startX,startY,endX,endY):
    arrow = SimpleNamespace()
    arrow.startX = startX
    arrow.startY = startY
    arrow.endX = endX
    arrow.endY = endY
    if abs(arrow.startX - arrow.endX) > 0 or abs(arrow.startY - arrow.endY) > 0:
        return arrow
            
def drawDiagonals(app):
    for line in app.diagonals:
        drawLine(line.startX,line.startY,line.endX,line.endY)
def drawDashedRects(app):
    for rect in app.dashedRects:
            drawRect(rect.startX, rect.startY, rect.width, rect.height, dashes = True, fill = None, border = 'grey')
def drawArrows(app):
    for arrow in app.arrows:
            fill = 'red' if arrow.startY <= arrow.endY else 'green'
            drawLine(arrow.startX, arrow.startY, arrow.endX, arrow.endY, arrowEnd=True,fill = fill)