import json
import decimal
import requests

lastPrice = 0
lastLTCPrice = 0
lastDogePrice = 0

def calcdoge2usd(num):
   uri = "http://www.cryptocoincharts.info/v2/api/tradingPair/doge_btc"
   data = requests.get(uri).json()
   return calcbtc2usd(decimal.Decimal(num) * decimal.Decimal(data["price"]))

def doge2usd(phenny, input):
   arg = input.group(2)
   #If an argument is provided, convert the exchange rate
   if arg:
      rate = calcdoge2usd(arg)
      usd = decimal.Decimal(arg)
      output = '%s DOGE will get you $%s' % (usd, rate)
      phenny.say(output)

doge2usd.commands = ['doge2usd']

def dogecoin(phenny, input):
   global lastDogePrice
   uri = "http://www.cryptocoincharts.info/v2/api/tradingPair/doge_btc"   
   data = requests.get(uri).json()
   data["price"] = calcbtc2usd(data["price"])
   diff = decimal.Decimal(data["price"]) - lastDogePrice
   diffStr = ""
   if diff != decimal.Decimal(0):
      sign = "+" if diff > 0 else ''
      diffStr = " (%s%s)" % (sign, diff)
   output = 'Current Price of 1 DOGE: $%s%s' % (data["price"], diffStr)
   lastDogePrice = decimal.Decimal(data["price"])
   phenny.say(output)
dogecoin.commands = ['doge']

def calcbtc2usd(num):
   uri = "https://coinbase.com/api/v1/currencies/exchange_rates"
   data = requests.get(uri).json()
   return decimal.Decimal(num) * decimal.Decimal(data["btc_to_usd"])

def calcusd2btc(num):
   uri = "https://coinbase.com/api/v1/currencies/exchange_rates"
   data = requests.get(uri).json()
   return decimal.Decimal(num) * decimal.Decimal(data["usd_to_btc"])

def bitcoin(phenny, input):
   global lastPrice
   uri = "https://coinbase.com/api/v1/prices/spot_rate"
   data = requests.get(uri).json()
   diff = decimal.Decimal(data["amount"]) - lastPrice
   diffStr = ""
   if diff != decimal.Decimal(0):
      sign = "+" if diff > 0 else ''
      diffStr = " (%s%s)" % (sign, diff)
   output = 'Current Price of ฿1: $%s%s' % (data["amount"], diffStr)
   lastPrice = decimal.Decimal(data["amount"])
   phenny.say(output)

bitcoin.commands = ['btc']
bitcoin.priority = 'low'

def btc2usd(phenny, input):
   arg = input.group(2)
   #If an argument is provided, convert the exchange rate
   if arg:
      rate = calcbtc2usd(arg)
      usd = decimal.Decimal(arg)
      output = '฿%s will get you $%s' % (usd, rate)
      phenny.say(output)


btc2usd.commands = ['btc2usd']
btc2usd.priority = 'low'

def usd2btc(phenny, input):
   arg = input.group(2)
   #If an argument is provided, convert the exchange rate
   if arg:
      rate = calcusd2btc(arg)
      usd = decimal.Decimal(arg)
      output = '$%s will get you ฿%s' % (usd, rate)
      phenny.say(output)


usd2btc.commands = ['usd2btc']
usd2btc.priority = 'low'

def calcltc2usd(num):
   uri = "https://btc-e.com/api/2/ltc_usd/ticker"
   data = requests.get(uri).json()
   return decimal.Decimal(num) * decimal.Decimal(data["ticker"]["last"])

def calcusd2ltc(num):
   uri = "https://btc-e.com/api/2/ltc_usd/ticker"
   data = requests.get(uri).json()
   usdPerLtc = decimal.Decimal("1.0") / decimal.Decimal(data["ticker"]["last"])
   return decimal.Decimal(num) * usdPerLtc

def litecoin(phenny, input):
   global lastLTCPrice
   uri = "https://btc-e.com/api/2/ltc_usd/ticker"
   data = requests.get(uri).json()
   diff = decimal.Decimal(data["ticker"]["last"]) - lastLTCPrice
   diffStr = ""
   if diff != decimal.Decimal(0):
      sign = "+" if diff > 0 else ''
      diffStr = " (%s%0.5f)" % (sign, diff)
   output = 'Current Price of Ł1: $%0.5f%s' % (data["ticker"]["last"], diffStr)
   lastLTCPrice = decimal.Decimal(data["ticker"]["last"])
   phenny.say(output)

litecoin.commands = ['ltc']
litecoin.priority = 'low'

def ltc2usd(phenny, input):
   arg = input.group(2)
   #If an argument is provided, convert the exchange rate
   if arg:
      rate = calcltc2usd(arg)
      usd = decimal.Decimal(arg)
      output = 'Ł%s will get you $%.05f' % (usd, rate)
      phenny.say(output)


ltc2usd.commands = ['ltc2usd']
ltc2usd.priority = 'low'

def usd2ltc(phenny, input):
   arg = input.group(2)
   #If an argument is provided, convert the exchange rate
   if arg:
      rate = calcusd2ltc(arg)
      usd = decimal.Decimal(arg)
      output = '$%s will get you Ł%.05f' % (usd, rate)
      phenny.say(output)


usd2ltc.commands = ['usd2ltc']
usd2ltc.priority = 'low'

def ticker(phenny, input):
   bitcoin(phenny, input)
   litecoin(phenny, input)
   dogecoin(phenny, input)

ticker.commands = ['tick']
