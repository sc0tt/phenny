import urllib.request, urllib.parse, urllib.error
import web
import json
import decimal
import requests
import sqlite3

lastPrice = 0
g_conn = sqlite3.connect("addresses.db", check_same_thread = False)
g_cur = g_conn.cursor()
g_cur.execute("""CREATE TABLE IF NOT EXISTS btc_addr (id INTEGER PRIMARY KEY, nick text, wallet text)""")

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

def addr_set(phenny, input):
   wallet = input.group(2)
   if wallet:
      g_cur.execute("""DELETE FROM btc_addr WHERE nick=?""", [input.nick.lower(),])
      g_cur.execute("""INSERT INTO btc_addr (nick, wallet) VALUES (?, ?)""", [input.nick.lower(), wallet])
      phenny.say("%s, your wallet address has been updated!" % input.nick)
      g_conn.commit()
   else:
      phenny.say("Please provide your wallet address.")

addr_set.commands = ['addr-set']
addr_set.priority = 'low'

def addr(phenny, input):
   nick = input.group(2)
   g_cur.execute("""SELECT nick, wallet FROM btc_addr WHERE nick=?""", [nick,])
   result = g_cur.fetchone()
   if result:
      phenny.say("BTC Wallet Address for %s: %s" % (result[0], result[1]))
   else:
      phenny.say("I don't have a BTC Wallet Address for that user.")

addr.commands = ['btc-addr']
addr.priority = 'low'
