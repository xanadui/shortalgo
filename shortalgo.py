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
    "apiKey": '633054c847df220001d99764',
    "secret": 'aaf9fd98-6ee1-489a-8461-cb8137ec2544',
    "password":'Krish005'
});

# file = open('jsonshort.json', 'w+')
# data = { "contract": "none", "amount": 0, "halfsies": 0}
# json.dump(data, file)

counter = 20
while counter == 20:
    file = open('jsonshort.json', 'r')
    filedump = json.load(file)
    if filedump["amount"] == 0:
        position = False
        print("False")
    else:
        position = True
        print("True")

    symbols = ["ETH/USDT:USDT", "BNB/USDT:USDT", "XRP/USDT:USDT",  "ETC/USDT:USDT", 'BTC/USDT:USDT', "SOL/USDT:USDT", 'RVN/USDT:USDT', "MATIC/USDT:USDT", "AVAX/USDT:USDT"]
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
    if position == False:
        for symbol in symbols:
                since2 = ku.milliseconds () - 450000000 
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
                thirdresult = secondresult
                fourthresult = thirdresult[:-1]
                smaresult = ta.trend.SMAIndicator(close=closer, window=40).sma_indicator()
                hundredsma = ta.trend.SMAIndicator(close=closer, window=100).sma_indicator()
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
                if (smaresult.iloc[-1] > lower.iloc[-1]):
                    xxx+=1
                if (smaresult.iloc[-1] < higher.iloc[-1]):
                    xxx+=1
                if smaresult.iloc[-2] < higher.iloc[-2] and smaresult.iloc[-2] > lower.iloc[-2] and smaresult.iloc[-3] > higher.iloc[-3] and smaresult.iloc[-3] < lower.iloc[-3] and smaresult.iloc[-4] < higher.iloc[-4] and smaresult.iloc[-4] > lower.iloc[-4]:
                    xxx-=1
                if ku.fetchBalance()['info']['data']['positionMargin'] < 2:
                    time.sleep(3)
                    xxx+=1
                if float(smaresult.iloc[-1]) > float(smaresult.iloc[-2]):
                    xxx+=1
                if float(hundredsma.iloc[-1]) > float(hundredsma.iloc[-2]):
                    xxx+=1
                if lower.iloc[-1]*1.015>=closer.iloc[-1] or lower.iloc[-1]*1.015>=opener.iloc[-1]:
                    xxx+=1
                if (higher.iloc[-1]/1.015)<=closer.iloc[-1] or (higher.iloc[-1]/1.015)<=opener.iloc[-1]:
                    xxx+=1
                if xxx==8:
                    print(f'SHORTSHORTSHORT {symbol}')
                    send(f'SHORT {symbol}!')
                    firstrestultbuy = secondresult.iloc[-1]
                    position = True
                    income = (ku.fetchBalance()['info']['data']["marginBalance"]*0.98)*5
                    time.sleep(5)
                    price = ku.fetchTicker(symbol)
                    #Figure the amount for each symbol - Fucking 8 if statements again
                    time.sleep(5)
                    m=0
                    while m<1:
                        try:
                            if symbol=='BTC/USDT:USDT':
                                time.sleep(10)
                                price = ku.fetchTicker(symbol)
                                time.sleep(30)
                                order = ku.createOrder('BTC/USDT:USDT', 'limit', 'sell', ((math.floor(income/float(price['info']['price'])*10000))/10000)*1000, float(price['info']['price'])*1.0003, {'leverage': 5})
                                amount = (math.floor(income/float(price['info']['price'])*10000)/10000)*1000
                                halfsies = (math.floor((0.5*income)/float(price['info']['price'])*10000)/10000)*1000
                                
                                # sl = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*10000)/10000)*1000, None, {'stopPrice': 0.98*price, 'leverage': 5})
                                # tp = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*10000)/10000)*1000, None, {'stopPrice': 1.02*price, 'leverage': 5})

                            elif symbol == "ETH/USDT:USDT":
                                time.sleep(10)
                                price = ku.fetchTicker(symbol)
                                time.sleep(30)
                                order = ku.createOrder(symbol, 'limit', 'sell', (math.floor((income/float(price['info']['price']))*1000)/1000)*100, float(price['info']['price'])*1.0003, {'leverage': 5})
                                amount = (math.floor((income/float(price['info']['price']))*1000)/1000)*100
                                halfsies = (math.floor((0.5*income)/float(price['info']['price'])*1000)/1000)*100
                                # sl = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*1000)/1000)*100, None, {'stopPrice': 0.98*price, 'leverage': 5})
                                # tp = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*1000)/1000)*100, None, {'stopPrice': 1.02*price, 'leverage': 5})
                            elif symbol == "SOL/USDT:USDT":    
                                time.sleep(10)
                                price = ku.fetchTicker(symbol)
                                time.sleep(30)
                                order = ku.createOrder(symbol, 'limit', 'sell', (math.floor(income/float(price['info']['price'])*100)/100)*10, float(price['info']['price'])*1.0003, {'leverage': 5})
                                amount = (math.floor(income/float(price['info']['price'])*100)/100)*10
                                halfsies = (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10
                                # sl = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10, None, {'stopPrice': 0.98*price,'leverage': 5})
                                # tp = ku.create_order(symbol, 'market', 'sell',  (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10, None, {'stopPrice': 1.02*price,'leverage': 5})
                            elif symbol == "XRP/USDT:USDT":
                                time.sleep(10)
                                price = ku.fetchTicker(symbol)
                                time.sleep(30)
                                order = ku.createOrder(symbol, 'limit', 'sell', (math.floor((income/float(price['info']['price']))))/10, float(price['info']['price'])*1.0003, {'leverage': 5})
                                amount = (math.floor((income/float(price['info']['price']))))/10
                                halfsies = (math.floor(((0.5*income)/float(price['info']['price']))))/10
                                # sl = ku.create_order(symbol, 'market', 'sell', (math.floor(((0.5*income)/price['info']['price'])))/10, None, {'stopPrice': 0.98*price,'leverage': 5})
                                # tp = ku.create_order(symbol, 'market', 'sell',  (math.floor(((0.5*income)/price['info']['price'])))/10, None, {'stopPrice': 1.02*price,'leverage': 5})
                            elif symbol == 'RVN/USDT:USDT':
                                time.sleep(10)
                                price = ku.fetchTicker(symbol)
                                time.sleep(30)
                                order = ku.createOrder(symbol, 'limit', 'sell', (math.floor((income/float(price['info']['price']))))/10, float(price['info']['price'])*1.0003, {'leverage': 5})
                                amount = (math.floor((income/float(price['info']['price']))))/10
                                halfsies = (math.floor(((0.5*income)/float(price['info']['price']))))/10
                                # sl = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10, None, {'stopPrice': 0.98*price,'leverage': 5})
                                # tp = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10, None, {'stopPrice': 1.02*price,'leverage': 5})
                            elif symbol == "MATIC/USDT:USDT":
                                time.sleep(10)
                                price = ku.fetchTicker(symbol)
                                time.sleep(30)
                                order = ku.createOrder(symbol, 'limit', 'sell', (math.floor((income/float(price['info']['price']))))/10, float(price['info']['price'])*1.0003, {'leverage': 5})
                                amount = (math.floor((income/float(price['info']['price']))))/10
                                halfsies = (math.floor(((0.5*income)/float(price['info']['price']))))/10
                                # sl = ku.create_order(symbol, 'market', 'sell', (math.floor(((0.5*income)/price['info']['price'])))/10, None, {'stopPrice': 0.98*price,'leverage': 5})
                                # tp = ku.create_order(symbol, 'market', 'sell',  (math.floor(((0.5*income)/price['info']['price'])))/10, None, {'stopPrice': 1.02*price,'leverage': 5})

                            elif symbol == "BNB/USDT:USDT":
                                time.sleep(10)
                                price = ku.fetchTicker(symbol)
                                time.sleep(30)
                                order = ku.createOrder(symbol, 'limit', 'sell', (math.floor(income/float(price['info']['price'])*1000)/1000)*100, float(price['info']['price'])*1.0003, {'leverage': 5})
                                amount = (math.floor(income/float(price['info']['price'])*1000)/1000)*100
                                halfsies = (math.floor((0.5*income)/float(price['info']['price'])*1000)/1000)*100
                                # sl = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*1000)/1000)*100, None, {'stopPrice': 0.98*price,'leverage': 5})
                                # tp = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*1000)/1000)*100, None, {'stopPrice': 1.02*price,'leverage': 5})
                            elif symbol == "ETC/USDT:USDT":
                                time.sleep(10)
                                price = ku.fetchTicker(symbol)
                                time.sleep(30)
                                order = ku.createOrder(symbol, 'limit', 'sell', (math.floor(income/float(price['info']['price'])*100)/100)*10, float(price['info']['price'])*1.0003, {'leverage': 5})
                                amount = (math.floor(income/float(price['info']['price'])*100)/100)*10
                                halfsies = (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10
                                # sl = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10, None, {'stopPrice': 0.98*price,'leverage': 5})
                                # tp = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10, None, {'stopPrice': 1.02*price,'leverage': 5})                        

                            elif symbol == "AVAX/USDT:USDT":
                                time.sleep(10)
                                price = ku.fetchTicker(symbol)
                                time.sleep(30)
                                order = ku.createOrder(symbol, 'limit', 'sell', (math.floor(income/float(price['info']['price'])*100)/100)*10, float(price['info']['price'])*1.0003, {'leverage': 5})
                                amount = (math.floor(income/float(price['info']['price'])*100)/100)*10
                                halfsies = (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10
                                # sl = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10, None, {'stopPrice': 0.98*price,'leverage': 5})
                                # tp = ku.create_order(symbol, 'market', 'sell', (math.floor((0.5*income)/float(price['info']['price'])*100)/100)*10, None, {'stopPrice': 1.02*price,'leverage': 5})                        
                            m+=1
                        except:
                            send("manual trade it")
                            time.sleep(25)
                    position = True
                    file = open('jsonshort.json', 'w+')
                    buydata = { "contract": symbol, "amount": amount, "halfsies": halfsies, "price": price, "time": datetime.now(), "higher": higher.iloc[-1]}
                    json.dump(buydata, file, default = str)
                    time.sleep(15)
                    parags = dict(reduceOnly=True)
                    firsttp = 0
                    secondtp = 0
                    while firsttp<1:
                        try:
                            takeprofitorder = ku.createOrder(symbol, "limit", "buy", halfsies, 1.018*float(price["info"]["price"]), {'leverage': 5})
                            firsttp+=1
                            time.sleep(20)
                            send("First tp Worked!!")
                        except:
                            time.sleep(20)
                            send("First tp didn't work but trying again")
                        

                elif secondresult.iloc[-1] == secondresult.iloc[-2]:
                    print(f'Holdup {symbol}')
                    time.sleep(100)
                    

                else:

                    now = datetime.now()

                    current_time = now.strftime("%H:%M:%S")
                    

                    print(f'Stay Away from {symbol}, {current_time} ')
                    print(thirdresult.iloc[-1])
                    print(fourthresult.iloc[-1])
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
            entryprice = filedump["price"]
            buyinhigh = filedump["higher"]

            timer = filedump["time"]

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
            thirdresult = secondresult
            fourthresult = thirdresult[:-1]
            smaresult = sma.iloc[-1]
            price = ku.fetchTicker(contract)
            
            
            if float(price['info']['price'])/1.00875 > entryprice:
                stopordersellvariable = 0
                while stopordersellvariable < 1:
                    try:
                        send("Closing Short Stop order")
                        canceled = ku.cancel_order(takeprofitorder['id'], takeprofitorder['symbol'])
                        time.sleep(20)
                        stopsellorder = ku.createOrder(contract, 'limit', 'buy', amount-halfsies, float(price['info']['price'])*.9997, {'leverage': 5})
                        stopordersellvariable +=1
                        time.sleep(20)
                        file = open('jsonshort.json', 'w+')
                        data = { "contract": "none", "amount": 0, "halfsies": 0}
                        json.dump(data, file)
                        time.sleep(15)
                        file = open('jsonshort.json', 'w+')
                        data = { "contract": "none", "amount": 0, "halfsies": 0}
                        json.dump(data, file)
                        break
                    except:
                        pass
                        time.sleep(10)
                if ku.fetchBalance()["info"]["data"]["positionMargin"] > 1:
                    stoptptwo = 0
                    price = ku.fetchTicker(contract)      
                    while stoptptwo <1:
                        time.sleep(10)                      
                        try:
                            stopsellordertoo = ku.createOrder(contract, 'limit', 'buy', halfsies, float(price['info']['price'])*0.9997, {'leverage': 5})
                            sellsecond+=1
                        except:
                            time.sleep(30)
                            price = ku.fetchTicker(contract)                            
                else:
                    pass
                

            # elif ((datetime.now() - timer).total_seconds())/3600 >= 3:
            #     price = ku.fetchTicker(contract)
            #     if price['info']['price'] < entryprice:
            #         send("Selling price is down after 3 hours")
            #         try:
            #             sellorder = ku.createOrder(contract, 'limit', 'sell', amount-halfsies, float(price['info']['price'])*.9997, {'leverage': 5})
            #             guacamole=1
            #             time.sleep(10)
            #         except:
            #             time.sleep(25)
            #             price = ku.fetchTicker(contract)
            #             time.sleep(10)
            #     price = ku.fetchTicker(contract)                    
            #     time.sleep(10)
            #     if ku.fetchBalance()["info"]["data"]["positionMargin"] > 1:
            #         sellorder = ku.createOrder(contract, 'limit', 'sell', halfsies, float(price['info']['price'])*.9997, {'leverage': 5})

            elif (opener.iloc[-1] > closer.iloc[-1] and opener.iloc[-2] > closer.iloc[-2] and buyinhigh != higher.iloc[-1] and buyinhigh != higher.iloc[-2]):
                send("Closing Short 2 ups")
                price = ku.fetchTicker(contract)
                time.sleep(10)
                notmovementstop = 0
                while nomovementstop < 1:
                    try:
                        sellorder = ku.createOrder(contract, 'limit', 'buy', amount-halfsies, float(price['info']['price'])*.9997, {'leverage': 5})
                        guacamole=1
                        nomovementstop +=1
                    except:
                        time.sleep(25)
                        price = ku.fetchTicker(contract)
                        time.sleep(10)
                    time.sleep(10)
                if ku.fetchBalance()["info"]["data"]["positionMargin"] > 1:
                    nomovementstophalfsies = 0
                    while nomovementstophalfsies<1:
                        try:
                            price = ku.fetchTicker(contract)
                            time.sleep(10)
                            sellorder = ku.createOrder(contract, 'limit', 'buy', halfsies, float(price['info']['price'])*.9997, {'leverage': 5})
                            nomovementstophalfsies+=1
                        except:
                            time.sleep(25)
                            price = ku.fetchTicker(contract)
                            time.sleep(10)




            elif thirdresult.iloc[-1] > fourthresult.iloc[-1]:
                price = ku.fetchTicker(contract)
                time.sleep(25)
                send(f'Exiting Short on {contract} cuz of MACD!')
                caca = 0
                caca2 = 0
                while caca<1:
                    try:
                        canceled = ku.cancel_order(takeprofitorder['id'], takeprofitorder['symbol'])
                        caca = 1
                    except:
                        time.sleep(20)
                time.sleep(10)
                price = ku.fetchTicker(contract)
                guacamole = 0
                while guacamole<1:
                    try:
                        sellorder = ku.createOrder(contract, 'limit', 'buy', amount-halfsies, float(price['info']['price'])*.9997, {'leverage': 5})
                        guacamole=1
                    except:
                        time.sleep(25)
                        price = ku.fetchTicker(contract)
                        time.sleep(10)


                time.sleep(15)
                if ku.fetchBalance()["info"]["data"]["positionMargin"] > 1:
                    send(f'Trying to exit halfsies on {contract}')
                    sellsecond = 0
                    price = ku.fetchTicker(contract)
                    while sellsecond<1:
                        try:
                            sellordertoo = ku.createOrder(contract, 'limit', 'buy', halfsies, float(price['info']['price'])*0.9997, {'leverage': 5})
                            sellsecond+=1
                        except:
                            time.sleep(30)
                            price = ku.fetchTicker(contract)                            
                else:
                    pass
                time.sleep(15)
                file = open('jsonshort.json', 'w+')
                data = { "contract": "none", "amount": 0, "halfsies": 0}
                json.dump(data, file)
                break
            else:
                print("Uh oh not yet buddy")
                print(thirdresult.iloc[-1])
                print(fourthresult.iloc[-1])
                time.sleep(120)
