import urllib.request, urllib.parse, urllib.error
import web
import json
import decimal
import requests
import sqlite3

lastPrice = 0
initial_cash = 50

g_conn = sqlite3.connect("addresses.db", check_same_thread = False)
g_cur = g_conn.cursor()
g_cur.execute("""CREATE TABLE IF NOT EXISTS btc_addr (id INTEGER PRIMARY KEY, nick text, wallet text)""")
g_cur.execute("""CREATE TABLE IF NOT EXISTS btc_users (id INTEGER PRIMARY KEY, nick text, usd real, btc real)""")


def user_exists(nick):
   g_cur.execute("""SELECT * FROM btc_users WHERE nick=?""", [nick.lower(),])
   result = g_cur.fetchone()
   return bool(result)

def xbtc_init(phenny, input):
   if not user_exists(input.nick):
      g_cur.execute("""INSERT INTO btc_users (nick, usd, btc) VALUES (?, ?, ?)""", [input.nick.lower(), initial_cash, 0])
      g_conn.commit()
      phenny.say("%s: You have been credited $50 USD. You currently have ฿0" % (input.nick,))
   else:
      phenny.say("%s: You are already registered." % (input.nick,))

def xbtc_sell(phenny, input):
   if user_exists(input.nick):
      btc_to_sell = float(input.group(2))
      if btc_to_sell:
         g_cur.execute("""SELECT * FROM btc_users WHERE nick=? AND btc >= ?""", [input.nick.lower(), btc_to_sell])
         result = g_cur.fetchone()
         if result:
            usd_to_add = float(calcbtc2usd(btc_to_sell))
            g_cur.execute("""UPDATE btc_users SET usd = usd + ?, btc = btc - ? WHERE nick = ?""", [usd_to_add, btc_to_sell, input.nick.lower()])
            g_conn.commit()
            phenny.say("%s: You sold ฿%s. for %s" % (input.nick, btc_to_sell, usd_to_add))
         else:
            phenny.say("%s: You don't seen to have enough bitcoin." % (input.nick,))
      else:
         phenny.say("%s: You need to enter an amount to sell." % (input.nick,))
   else:
      phenny.say("%s: You need to register first. .xbtc-init" % (input.nick,))

xbtc_sell.commands = ['xbtc-sell']
xbtc_sell.priority = 'low'


def xbtc_buy(phenny, input):
   if user_exists(input.nick):
      btc_to_buy = float(input.group(2))
      if btc_to_buy:
         cost_in_usd = float(calcbtc2usd(btc_to_buy))
         g_cur.execute("""SELECT * FROM btc_users WHERE nick=? AND usd >= ?""", [input.nick.lower(), cost_in_usd])
         result = g_cur.fetchone()
         if result:
            g_cur.execute("""UPDATE btc_users SET usd = usd - ?, btc = btc + ? WHERE nick = ?""", [cost_in_usd, btc_to_buy, input.nick.lower()])
            g_conn.commit()
            phenny.say("%s: You bought ฿%s for $%s." % (input.nick, btc_to_buy, cost_in_usd))
         else:
            phenny.say("%s: You don't seen to have enough bitcoin." % (input.nick,))
      else:
         phenny.say("%s: You need to enter an amount to sell." % (input.nick,))
   else:
      phenny.say("%s: You need to register first. .xbtc-init" % (input.nick,))

xbtc_buy.commands = ['xbtc-buy']
xbtc_buy.priority = 'low'

def xbtc_status(phenny, input):
   possible_user = input.group(2)
   if possible_user:
      nick_to_use = possible_user
   else:
      nick_to_use = input.nick

   if user_exists(nick_to_use):
      g_cur.execute("""SELECT usd, btc FROM btc_users WHERE nick=?""", [input.nick.lower(),])
      result = g_cur.fetchone()
      phenny.say("%s has $%s and ฿%s" % (nick_to_use, result[0], result[1]))
   else:
      phenny.say("User does not exist.")

xbtc_status.commands = ['xbtc-status']
xbtc_status.priority = 'low'

def calcbtc2usd(num):
   uri = "https://coinbase.com/api/v1/currencies/exchange_rates"
   bytesData = requests.get(uri)
   data = json.loads(bytesData.text)
   return decimal.Decimal(num) * decimal.Decimal(data["btc_to_usd"])

def calcusd2btc(num):
   uri = "https://coinbase.com/api/v1/currencies/exchange_rates"
   bytesData = requests.get(uri)
   data = json.loads(bytesData.text)
   return decimal.Decimal(num) * decimal.Decimal(data["usd_to_btc"])


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
