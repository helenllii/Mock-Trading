import csv
from datetime import datetime
import OOPLogics
    # cite: https://docs.python.org/3/library/csv.html dict reader, 
    # cite: chatGPT debug(encoding utf-8-sig, I change this with the help of chatGPT)
    # cite: "entry", asked ChatGPT how to get access to a certain row using csv lib
    # cite: https://www.programiz.com/python-programming/datetime/strftime change date time and comparing and calculate
    # cite: https://groww.in/blog/relative-strength-index-rsi formula for RSI calculation
    # cite: EMA calculation https://www.strike.money/technical-analysis/ema#:~:text=The%20EMA%20is%20one%20of,or%20lower%20time%20frames%20also.&text=EMA%20%3D%20Closing%20price%20*%20multiplier%20%2B,number%20of%20observations%20%2B1).
def getData(app, stockfile):
    file_path = stockfile
    data = []
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['Date'] = datetime.strptime(row['Date'], '%m/%d/%Y')
            row['Price'] = float(row['Price'].replace(',', ''))
            row['Open'] = float(row['Open'].replace(',', ''))
            row['High'] = float(row['High'].replace(',', ''))
            row['Low'] = float(row['Low'].replace(',', ''))
            row['Change %'] = float(row['Change %'].replace('%', '')) / 100
            data.append(row)

    startDate, enddate = datetime.strptime(app.startDate, '%Y-%m-%d'), datetime.strptime(app.endDate, '%Y-%m-%d')
    filteredData = [row for row in data if startDate <= row['Date'] <= enddate]
    filteredData.reverse()
    highest = [row['High'] for row in filteredData]
    price = [row['Price'] for row in filteredData]
    lowest = [row['Low'] for row in filteredData]
    openPrice = [row['Open'] for row in filteredData]
    tuples = [
        (row['Date'], row['Price'], row['Open'], row['High'], row['Low'], row['Change %'])
        for row in filteredData
    ]
    return filteredData, highest, lowest, openPrice, price, tuples

def getIndicators(app):
    ma5 = calculateMA(app,5)
    ma10 = calculateMA(app,10)
    ma25 = calculateMA(app,25)
    rsi = calculateRSI(app)
    ema12 = calculateEMA(app,12)
    ema26 = calculateEMA(app,26)
    macd, signalLine = calculateMACD(app, ema12, ema26)
    return ma5, ma10, ma25, rsi, ema12, ema26, macd, signalLine

def calculateMA(app, timelength):
    sma = []
    for i in range(len(app.filteredData)):
        if i < timelength - 1:
            sma.append(None)
        else:
            prices = [entry['Price'] for entry in app.filteredData[i-timelength+1:i+1]]
            sma.append(sum(prices) / timelength)
    return sma

def calculateEMA(app, timelength):
    ema = []
    multiplier = 2 / (timelength + 1)
    prices = [entry['Price'] for entry in app.filteredData] 
    ema.append(None)
    for i in range(1, len(prices)):
        if i < timelength:
            ema.append(None)
        else:
            if ema[i-1] == None:
                Initialprices = prices[i-timelength+1:i+1]
                lastEma = sum(Initialprices) / timelength
                ema.append(lastEma)
            else:
                lastEma = ema[i-1]
            newValue = (prices[i] - lastEma) * multiplier + lastEma
            ema.append(newValue)
    return ema

def calculateRSI(app, period=14):
    prices = [entry['Price'] for entry in app.filteredData]
    gains = [0] * len(prices)
    losses = [0] * len(prices)
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        if change > 0:
            gains[i] = change
            losses[i] = 0
        elif change < 0:
            gains[i] = 0
            losses[i] = abs(change)
        else:
            gains[i] = 0
            losses[i] = 0

    avgGain = sum(gains[1:period + 1]) / period
    avgLoss = sum(losses[1:period + 1]) / period
    rsi = [None] * period
    for i in range(period, len(prices)):
        avgGain = (avgGain * (period - 1) + gains[i]) / period
        avgLoss = (avgLoss * (period - 1) + losses[i]) / period
        if avgLoss == 0:
            rsiValue = 100
        else:
            rs = avgGain / avgLoss #relative strength
            rsiValue = 100 - (100 / (1 + rs))
        rsi.append(rsiValue)
    return rsi

# MACD need two kinds of EMA data
def calculateMACD(app, ema12, ema26, signalPeriod= 9):
    macd = [] #dif between two EMAs
    for i in range(len(ema12)):
        if ema26[i] == None:
            macd.append(None)
            continue
        macd.append(ema12[i] - ema26[i])
    # Signal line
    signal = []
    multiplier = 2 / (signalPeriod + 1)
    signal.append(None)
    for i in range(1, len(macd)):
        if i < signalPeriod or macd[i] is None:
            signal.append(None)
        else:
            if signal[i - 1] is None:
                initial = [x for x in macd[i-signalPeriod+1:i+1] if x is not None]
                avg = sum(initial) / len(initial)
                signal.append(avg)
            else:
                signal.append((macd[i] - signal[i - 1]) * multiplier + signal[i - 1])

    return macd, signal
