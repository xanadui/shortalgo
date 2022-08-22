import ccxt
import pandas as pd
import ta
import time
import sys
from datetime import datetime
import pickle
import math
import json
import requests
import requests


def send(text):
    token = '5782828239:AAE1H6hkzIJOjSvNCsnZ6bGYPTQX8yawQ3g'
    your_id = '5315858757'
    params = {'chat_id': your_id, 'text': text, 'parse_mode': 'HTML'}
    resp = requests.post('https://api.telegram.org/bot{}/sendMessage'.format(token), params)
    resp.raise_for_status()


# import http.client, urllib.request, urllib.parse, urllib.error
# conn = http.client.HTTPSConnection("api.pushover.net:443")

ku = ccxt.kucoinfutures({
    'adjustForTimeDifference': True,
    "apiKey": '62ec3e0b6a55680001b9c7c1',
    "secret": 'f8a6306e-05be-4f63-bc90-4981ed43a5bc',
    "password":'Krish005'
});

# file = open('jsonshort.json', 'w+')
# data = { "contract": "none", "amount": 0, "halfsies": 0}
# json.dump(data, file)



file = open('jsonshort.json', 'r')
filedump = json.load(file)
if filedump["amount"] == 0:
    position = False
    print("False")
else:
    position = True
    print("True")



symbols = ["BCH/USDT:USDT", "XRP/USDT:USDT", "ETH/USDT:USDT", "ETC/USDT:USDT", 'BTC/USDT:USDT', "SOL/USDT:USDT", 'APE/USDT:USDT', "MATIC/USDT:USDT", "BNB/USDT:USDT", "AVAX/USDT:USDT"]
counter = 20
firstresultbuyBTC = 1000000
firstresultbuyETH = 1000000
firstresultbuySOL = 1000000
firstresultbuyXRP = 1000000
firstresultbuyAPE = 1000000
firstresultbuyMATIC = 1000000
firstresultbuyBNB = 1000000
firstresultbuyETC = 1000000
firstresultbuyAVAX = 1000000
firstresultsell = -1000000
firstsmabuy = 1000000000
firstsmasell = -10000000000
amount = 0
halfsies = 0

while counter == 20:
    if position == False:
        for symbol in symbols:
                since2 = ku.milliseconds () - 400000000
                ohlcv = ku.fetchOHLCV(symbol, timeframe='1h', since=since2) 
                x = pd.DataFrame(ohlcv)
                x.columns = ["Time", "Open", "High", "Low", "Close", "V"]
                higher = x.loc[:,"High"]
                lower = x.loc[:, "Low"]
                closer = x.loc[:,"Close"]
                opener = x.loc[:, "Open"]
                closer = closer[:-1]
                higher = higher[:-1]
                lower = lower[:-1]
                opener = opener[:-1]
                y = ta.trend.EMAIndicator(close=closer, window=12).ema_indicator()
                z = ta.trend.EMAIndicator(close=closer, window=26).ema_indicator()
                sma = ta.trend.SMAIndicator(close=closer, window=40).sma_indicator()
                secondresult = y-z
                thirdresult = secondresult[:-1]
                hundredsma = ta.trend.SMAIndicator(close=closer, window=100).sma_indicator()
                fourthresult = thirdresult[:-1]
                smaresult = sma.iloc[-1]
                characters = '/USDT:USDT'
                if symbol=='BTC/USDT:USDT':
                    newname = 'BTC'
                elif symbol == "ETH/USDT:USDT":
                    newname = 'ETH'
                elif symbol == "SOL/USDT:USDT":    
                    newname = 'SOL'
                elif symbol == "XRP/USDT:USDT":
                    newname = 'XRP'
                elif symbol == 'APE/USDT:USDT':
                    newname = 'APE'
                elif symbol == "MATIC/USDT:USDT":
                    newname = 'MATIC'
                elif symbol == "BNB/USDT:USDT":
                    newname = 'BNB'
                elif symbol == "ETC/USDT:USDT":
                    newname = 'ETC'
                elif symbol == "AVAX/USDT:USDT":
                    newname = 'AVAX'
                xxx=0
                if thirdresult.iloc[-1] < fourthresult.iloc[-1]:
                    xxx+=1
                if smaresult > lower.iloc[-1]:
                    xxx+=1
                if smaresult < higher.iloc[-1]:
                    xxx+=1
                if smaresult < sma.iloc[-2]:
                    xxx+=1
                if ku.fetchBalance()['info']['data']['positionMargin'] < 2:
                    time.sleep(3)
                    xxx+=1
                if hundredsma.iloc[-1] > smaresult:
                    xxx+=1
                if xxx==6:
                    print(f'SHORTSHORTSHORT {symbol}')
                    send(f'Short {symbol}!')
                    firstrestultbuy = secondresult.iloc[-1]
                    position = True
                    income = 780
                    time.sleep(10)
                    price = ku.fetchTicker(symbol)
                    print(price["info"]["price"])
                    #Figure the amount for each symbol - Fucking 8 if statements again
                    time.sleep(5)
                    amount = math.floor(((math.floor((income/float(price["info"]["price"]))*1000))/1000)*100)
                    print(amount)
                    if symbol=='BTC/USDT:USDT':
                        time.sleep(10)
                        amount = (math.floor(income/float(price['info']['price'])*10000)/10000)*1000
                        order = ku.createOrder('BTC/USDT:USDT', 'limit', 'sell', amount, price['info']['price'], 'leverage': 5)
                        halfsies = (math.floor((0.5*income)/float(price['info']['price'])*10000)/10000)*1000
                        # sl = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*10000)/10000)*1000, None, {'stopPrice': 0.98*price, 'leverage': 5})
                        # tp = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*10000)/10000)*1000, None, {'stopPrice': 1.02*price, 'leverage': 5})

                    elif symbol == "ETH/USDT:USDT":
                        time.sleep(10)
                        amount = (math.floor(income/float(price['info']['price'])*1000)/1000)*100
                        order = ku.createOrder(symbol, 'limit', 'sell', amount, price['info']['price'], 'leverage': 5)
                        halfsies = (math.floor((0.5*income)/float(price['info']['price'])*1000)/1000)*100
                        # sl = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*1000)/1000)*100, None, {'stopPrice': 0.98*price, 'leverage': 5})
                        # tp = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*1000)/1000)*100, None, {'stopPrice': 1.02*price, 'leverage': 5})
                    elif symbol == "SOL/USDT:USDT":    
                        time.sleep(10)
                        amount = (math.floor(income/float(price['info']['price'])*100)/100)*10
                        order = ku.createOrder(symbol, 'limit', 'sell', amount, price['info']['price'], 'leverage': 5)
                        halfsies = (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10
                        # sl = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10, None, {'stopPrice': 0.98*price,'leverage': 5})
                        # tp = ku.create_order(symbol, 'market', 'sell',  (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10, None, {'stopPrice': 1.02*price,'leverage': 5})
                    elif symbol == "XRP/USDT:USDT":
                        time.sleep(10)
                        amount = (math.floor((income/(float(price['info']['price'])))))/10
                        order = ku.createOrder(symbol, 'limit', 'sell', amount, price['info']['price'], 'leverage': 5)
                        halfsies = (math.floor(((0.5*income)/float(price['info']['price']))))/10
                        # sl = ku.create_order(symbol, 'market', 'sell', (math.floor(((0.5*income)/price['info']['price'])))/10, None, {'stopPrice': 0.98*price,'leverage': 5})
                        # tp = ku.create_order(symbol, 'market', 'sell',  (math.floor(((0.5*income)/price['info']['price'])))/10, None, {'stopPrice': 1.02*price,'leverage': 5})
                    elif symbol == 'APE/USDT:USDT':
                        time.sleep(10)
                        amount = (math.floor(income/float(price['info']['price'])*100)/100)*10
                        order = ku.createOrder(symbol, 'limit', 'sell', amount, price['info']['price'], 'leverage': 5)
                        halfsies = (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10
                        # sl = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10, None, {'stopPrice': 0.98*price,'leverage': 5})
                        # tp = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10, None, {'stopPrice': 1.02*price,'leverage': 5})
                    elif symbol == "MATIC/USDT:USDT":
                        time.sleep(10)
                        amount = (math.floor((income/price['info']['price'])))/10
                        order = ku.createOrder(symbol, 'limit', 'sell', amount, price['info']['price'], 'leverage': 5)
                        halfsies = (math.floor(((0.5*income)/price['info']['price'])))/10
                        # sl = ku.create_order(symbol, 'market', 'sell', (math.floor(((0.5*income)/price['info']['price'])))/10, None, {'stopPrice': 0.98*price,'leverage': 5})
                        # tp = ku.create_order(symbol, 'market', 'sell',  (math.floor(((0.5*income)/price['info']['price'])))/10, None, {'stopPrice': 1.02*price,'leverage': 5})

                    elif symbol == "BCH/USDT:USDT":
                        time.sleep(10)
                        amount = ((math.floor(income/float(price['info']['price'])*1000)/1000)*100)
                        order = ku.createOrder(symbol, 'limit', 'sell', amount, price['info']['price'], 'leverage': 5)
                        halfsies = (math.floor((0.5*income)/float(price['info']['price'])*1000)/1000)*100
                        # sl = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*1000)/1000)*100, None, {'stopPrice': 0.98*price,'leverage': 5})
                        # tp = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*1000)/1000)*100, None, {'stopPrice': 1.02*price,'leverage': 5})
                    elif symbol == "ETC/USDT:USDT":
                        time.sleep(10)
                        amount = (math.floor(income/float(price['info']['price'])*100)/100)*10
                        order = ku.createOrder(symbol, 'limit', 'sell', amount, price['info']['price'], 'leverage': 5)
                        halfsies = (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10
                        # sl = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10, None, {'stopPrice': 0.98*price,'leverage': 5})
                        # tp = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10, None, {'stopPrice': 1.02*price,'leverage': 5})                        

                    elif symbol == "AVAX/USDT:USDT":
                        time.sleep(10)
                        amount = (math.floor(income/float(price['info']['price'])*100)/100)*10
                        order = ku.createOrder(symbol, 'limit', 'sell', amount, price['info']['price'], 'leverage': 5)
                        halfsies = (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10
                        # sl = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10, None, {'stopPrice': 0.98*price,'leverage': 5})
                        # tp = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10, None, {'stopPrice': 1.02*price,'leverage': 5})                        
                    print(amount)
                    position = True
                    pos = symbol
                    file = open('jsonshort.json', 'w+')
                    buydata = { "contract": symbol, "amount": amount, "halfsies": halfsies }
                    json.dump(buydata, file)
                    ku.create_order(symbol, "limit", "buy", halfsies, 0.98*float(price["info"]["price"]), {'leverage': 5})


                elif secondresult.iloc[-1] == secondresult.iloc[-2]:
                    print(f'Holdup {symbol}')
                    time.sleep(100)
                    

                else:

                    now = datetime.now()

                    current_time = now.strftime("%H:%M:%S")
                    

                    print(f'Stay Away from {symbol}, {current_time} ')
                    time.sleep(100)

                if position == True:
                    break

    elif position == True:
        if position == True:
            file = open('jsonshort.json', 'r')
            filedump = json.load(file)
            contract = filedump["contract"]
            amount = filedump["amount"]
            halfsies = filedump["halfsies"]
            since2 = ku.milliseconds () - 720000000
            ohlcv = ku.fetchOHLCV(contract, timeframe='1h', since=since2) 
            x = pd.DataFrame(ohlcv)
            x.columns = ["Time", "Open", "High", "Low", "Close", "V"]
            higher = x.loc[:,"High"]
            lower = x.loc[:, "Low"]
            closer = x.loc[:,"Close"]
            opener = x.loc[:, "Open"]
            closer = closer[:-1]
            higher = higher[:-1]
            lower = lower[:-1]
            opener = opener[:-1]
            y = ta.trend.EMAIndicator(close=closer, window=12).ema_indicator()
            z = ta.trend.EMAIndicator(close=closer, window=26).ema_indicator()
            sma = ta.trend.SMAIndicator(close=closer, window=40).sma_indicator()
            secondresult = y-z
            thirdresult = secondresult[:-1]
            fourthresult = thirdresult[:-1]
            smaresult = sma.iloc[-1]
            price = ku.fetchTicker(contract)

            if thirdresult.iloc[-1] > fourthresult.iloc[-1]:
                sellorder = ku.createOrder(contract, 'limit', 'buy', amount-halfsies, price['info']['price'], {'leverage': 5})
                time.sleep(5)
                if ku.fetchBalance()["info"]["data"]["positionMargin"] > 1:
                    sellordertoo = ku.createOrder(contract, 'limit', 'buy', amount - (amount-halfsies), price['info']['price'], {'leverage': 5})
                else:
                    pass
                
                file = open('jsonshort.json', 'w+')
                data = { "contract": "none", "amount": 0, "halfsies": 0}
                
                json.dump(data, file)

                break
            else:
                print("Uh oh not yet buddy")
                time.sleep(100)


