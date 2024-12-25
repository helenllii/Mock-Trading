class Order:
    number = 0
    def __init__(self, side, quantity, price):
        self.side = side # +1 or -1 (buy in or sell out)
        self.quantity = quantity # how much stock 1, 2, or more?
        self.price = price # the stock price at that moment (day, in our game)
        self.number = Order.number # self.number (the number of the order)
        Order.number += 1
    def __repr__(self):
        action = 'bought in' if self.side== 1 else 'sold out'
        plural = 'share' if self.quantity == 1 else 'shares'
        return str(f' {action} {self.quantity} {plural} at price {self.price}')

class AIOrder:
    number = 0
    def __init__(self, side, quantity, price):
        self.side = side # +1 or -1 (buy in or sell out)
        self.quantity = quantity # how much stock 1, 2, or more?
        self.price = price # the stock price at that moment (day, in our game)
        self.number = AIOrder.number # self.number (the number of the order)
        AIOrder.number += 1
    def __repr__(self):
        action = 'bought in' if self.side== 1 else 'sold out'
        plural = 'share' if self.quantity == 1 else 'shares'
        return str(f' {action} {self.quantity} {plural} at price {self.price}')
    
class Account:
    def __init__(self, shares, account):
        self.shares = shares # int, either pos or 0 (you can't have neg shares)
        self.account = account # how much money do you have in your account
        self.orders = []
        self.floatingProfit = 0
        self.totalCost = 0
        self.realizedProfit = 0
    def __repr__(self):
        pass
    def buyShare(self, order):
        self.shares += order.quantity * order.side
        self.orders.append(order)
        cost = order.quantity * order.price
        self.totalCost += cost
        self.account -= cost
    def sellShare(self, order):
        if order.quantity > (self.shares):
            return #cannot do this way
        # cite: https://investopedia.com/ask/answers/05/stockgainsandlosses.asp
        averageCost = self.totalCost / self.shares 
        sellCost = order.quantity * averageCost
        sellRevenue = order.quantity * order.price
        self.realizedProfit += (sellRevenue - sellCost)
        self.account += sellRevenue
        self.shares -= order.quantity
        self.totalCost -= sellCost
        self.orders.append(order)


    def getProfit(self, currentPrice):
        marketValue = self.shares * currentPrice
        return marketValue - self.totalCost

def validSell(app, hold):
    if app.account.shares == 0:
        return False
    if abs(hold) > app.account.shares: # you cannot sell more than you have
        return False
    return True
def validBuy(app,hold):
    if abs(hold) * app.tupleData[app.todayIndex][1] > app.account.account:
        # you cannot buy using money more than you have
        return False
    return True


def AImakeDecision(app):
    todayPrice = app.tupleData[app.todayIndex][1]
    prevMA5, prevMA25, prevMA10 = app.MA5[app.todayIndex-1], app.MA25[app.todayIndex-1], app.MA10[app.todayIndex-1]
    todayMA5, todayMA25, todayMA10 = app.MA5[app.todayIndex], app.MA25[app.todayIndex], app.MA10[app.todayIndex]
    prevEMA12, prevEMA26 = app.EMA12[app.todayIndex-1], app.EMA26[app.todayIndex-1]
    todayEMA12, todayEMA26 = app.EMA12[app.todayIndex], app.EMA26[app.todayIndex]

    if None in {prevMA5, prevMA25, prevMA10, todayMA5, todayMA25, 
                todayMA10, prevEMA12, prevEMA26, todayEMA12, todayEMA26}:
        return

    SMAGoldenCross = prevMA10 > prevMA5 and todayMA10 < todayMA5
    SMADeathCross = prevMA10 < prevMA5 and todayMA10 > todayMA5

    LongGoldenCross = prevMA25 > prevMA5 and todayMA25 < todayMA5
    LongDeathCross = prevMA25 < prevMA5 and todayMA25 > todayMA5

    EMAGoldenCross = prevEMA26 > prevEMA12 and todayEMA26 < todayEMA12
    EMADeathCross = prevEMA26 < prevEMA12 and todayEMA26 > todayEMA12

    if (SMADeathCross or EMADeathCross) and app.AITrader.shares > 0:
        orderSize = min(10, app.AITrader.shares)
        order = AIOrder(-1, orderSize, todayPrice)
        app.AITrader.sellShare(order)

    elif SMAGoldenCross or EMAGoldenCross:
        order = AIOrder(+1, 10, todayPrice)
        app.AITrader.buyShare(order)

    if LongDeathCross and app.AITrader.shares > 0:
        order = AIOrder(-1, app.AITrader.shares, todayPrice)
        app.AITrader.sellShare(order)

    elif LongGoldenCross:
        order = AIOrder(+1, 50, todayPrice)
        app.AITrader.buyShare(order)

def fixDecision(app):
    todayPrice = app.tupleData[app.todayIndex][1]
    averageCost = app.AITrader.totalCost / app.AITrader.shares if app.AITrader.shares > 0 else None

    if averageCost:
        if todayPrice < averageCost * 0.95:
            reverseOrder(app, todayPrice)

        elif todayPrice > averageCost * 1.10:
            reverseOrder(app, todayPrice)

def reverseOrder(app, todayPrice):
    hold = app.AITrader.shares
    if hold > 0:
        order = AIOrder(-1, hold, todayPrice)
        app.AITrader.sellShare(order)