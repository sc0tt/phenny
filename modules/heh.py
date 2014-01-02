#!/usr/bin/python3
from random import choice
import datetime
import requests

alotImages = ["http://i.imgur.com/7GJ5XoB.png",
              "http://i.imgur.com/xncEQ8B.png",
              "http://i.imgur.com/3t5QHBu.png",
              "http://i.imgur.com/Bz2ei9E.png",
              "http://i.imgur.com/lqBkdnP.png",
              "http://i.imgur.com/7gdB5fU.png",
              "http://i.imgur.com/B0jd549.png",
              "http://i.imgur.com/4Jpt8k6.png",
              "http://i.imgur.com/BlEay4o.png",
              "http://i.imgur.com/5X5a4ZQ.png",
              "http://i.imgur.com/iLLLhnP.png",
              "http://i.imgur.com/nMgttwX.png"]

def alot(phenny, input):
   phenny.say("%s LEARN TO SPELL: %s" % (input.nick, choice(alotImages)))

alot.rule = r'(^|.+ )alot( .+|$)'
alot.commands = ['alot']
alot.priority = 'low'

def heh(phenny, input):
   phenny.say("http://i.imgur.com/wjANVCD.jpg")

heh.commands = ['heh']
heh.priority = 'low'

def hue(phenny, input):
   phenny.say("http://i.imgur.com/0IYzpNm.jpg")

hue.commands = ['hue']

def dance(phenny, input):
   phenny.do("dances")

dance.commands = ['dance']
dance.priority = 'low'

def ohyou(phenny, input):
   phenny.say("http://i.imgur.com/CPjuz7E.jpg")

ohyou.commands = ['ohyou']
ohyou.priority = 'low'

def ohme(phenny, input):
   phenny.say("http://i.imgur.com/H5GdFcD.jpg")

ohme.commands = ['ohme']
ohme.priority = 'low'

def lod(phenny, input):
   phenny.say("ಠ_ಠ")
lod.commands = ['lod']
lod.priority = 'low'

def leet(phenny, input):
   replacements = ( ('hacker','haxor'), ('elite','eleet'), ('a','4'), ('e','3'),
                          ('l','1'), ('o','0'), ('t','+') )
   my_string = input.group(2) 
   if not my_string:
      pass
   else:
      new_string = my_string
      for old, new in replacements:
         new_string = new_string.replace(old, new)
      phenny.say(new_string)

leet.commands = ['leet']
leet.priority = 'low'

def srsly(phenny, input):
   phenny.say("http://i.imgur.com/4Zf2bzo.png")

srsly.commands = ['srsly']
srsly.priority = 'low'

def interesting(phenny, input):
   phenny.say("http://i.imgur.com/RAEek5T.jpg")

interesting.commands = ['interesting']
interesting.priority = 'low'

def brotato(phenny, input):
   phenny.say("http://i.imgur.com/1J2sRdk.jpg")

brotato.commands = ['brotato']
brotato.priority = 'low'

def party(phenny, input):
   phenny.say("http://i.imgur.com/34t9KcA.jpg")

party.commands = ['party']
party.priority = 'low'

def zen(phenny, input):
   uri = "https://api.github.com/zen"
   bytesData = requests.get(uri)
   phenny.say(bytesData.text)

zen.commands = ['zen']
zen.priority = 'low'

def pax(phenny, input):
   paxDate = datetime.datetime(2014, 4, 11)
   now = datetime.datetime.now()
   daysToPax = (paxDate - now).days
   phenny.say("%s days until PAX East!" % (daysToPax,))

pax.commands = ['pax']
pax.priority = 'low'

def troll(phenny, input):
   phenny.say("http://i.imgur.com/hKCXuZz.jpg")

troll.commands = ['trolled']

def hey(phenny, input):
   phenny.say("http://heeeeeeeey.com/")
hey.commands = ['hey']

def ho(phenny, input):
   phenny.say("http://hooooooooo.com/")
ho.commands = ['ho']

def nfact(phenny, input):
   phenny.say(requests.get("http://numbersapi.com/random").text)

nfact.commands = ['nfact']

def fourtytwo(phenny, input):
   phenny.say(requests.get("http://numbersapi.com/42").text)
fourtytwo.commands = ['42']

def today(phenny, input):
   month = datetime.datetime.now().month
   day = datetime.datetime.now().day
   phenny.say(requests.get("http://numbersapi.com/%s/%s/date" % (month, day)).text)
today.commands = ['tfact']

def fuckyou(phenny, input):
   replies = ["Sorry :(", 
              "I didn't mean to do anything wrong D:",
              ":/ okay."]
   phenny.say(choice(replies))
fuckyou.rule = 'fuck you, boredbot'

def ask(phenny, input):
  phenny.say(choice(requests.get("http://www.reddit.com/r/askreddit.json?limit=100").json()["data"]["children"])["data"]["title"])

ask.commands = ['ask']

def shower(phenny, input):
  phenny.say(choice(requests.get("http://www.reddit.com/r/showerthoughts.json?limit=100").json()["data"]["children"])["data"]["title"])

shower.commands = ['shower']

def rando(phenny, input):
  r = requests.get("http://reddit.com/r/random")
  a = choice(requests.get("http://reddit.com%s.json?limit=100" % (r.url[r.url.index("/r/"):])).json()["data"]["children"])
  phenny.say("%s - %s" % (a["data"]["title"], a["data"]["url"]))
rando.commands = ['rando']

#def reddit(phenny, input):
#   reddit = input.group(1)
#   phenny.say("http://reddit.com/r/%s" % reddit)

#reddit.rule = '.*r/([A-z0-9_-]+)'

