import urllib.request, urllib.parse, urllib.error
import web
import json
import decimal

def bitcoin(phenny, input):
   uri = "https://coinbase.com/api/v1/prices/spot_rate"
   bytesData = urllib.request.urlopen(uri)
   data = json.loads(bytesData.read().decode('utf-8'))
   output = 'Current Price of ฿1: $%s' % (data["amount"])
   phenny.say(output)

bitcoin.commands = ['btc']
bitcoin.priority = 'low'

def btc2usd(phenny, input):
   arg = input.group(2)
   #If an argument is provided, convert the exchange rate
   if arg:
      uri = "https://coinbase.com/api/v1/currencies/exchange_rates"
      bytesData = urllib.request.urlopen(uri)
      data = json.loads(bytesData.read().decode('utf-8'))
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
      bytesData = urllib.request.urlopen(uri)
      data = json.loads(bytesData.read().decode('utf-8'))
      rate = decimal.Decimal(data["usd_to_btc"])
      usd = decimal.Decimal(arg)
      output = '$%s will get you ฿%s' % (usd, rate*usd)
      phenny.say(output)


usd2btc.commands = ['usd2btc']
usd2btc.priority = 'low'
