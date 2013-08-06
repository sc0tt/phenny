import urllib.request, urllib.parse, urllib.error
import web
import json
import decimal
import requests

lastPrice = 0

def bitcoin(phenny, input):
   global lastPrice
   uri = "https://coinbase.com/api/v1/prices/spot_rate"
   bytesData = requests.get(uri)
   data = json.loads(bytesData.text)
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
      uri = "https://coinbase.com/api/v1/currencies/exchange_rates"
      bytesData = requests.get(uri)
      data = json.loads(bytesData.text)
      rate = decimal.Decimal(data["btc_to_usd"])
      usd = decimal.Decimal(arg)
      output = '฿%s will get you $%s' % (usd, rate*usd)
      phenny.say(output)


btc2usd.commands = ['btc2usd']
btc2usd.priority = 'low'

def usd2btc(phenny, input):
   arg = input.group(2)
   #If an argument is provided, convert the exchange rate
   if arg:
      uri = "https://coinbase.com/api/v1/currencies/exchange_rates"
      bytesData = requests.get(uri)
      data = json.loads(bytesData.text)
      rate = decimal.Decimal(data["usd_to_btc"])
      usd = decimal.Decimal(arg)
      output = '$%s will get you ฿%s' % (usd, rate*usd)
      phenny.say(output)


usd2btc.commands = ['usd2btc']
usd2btc.priority = 'low'
