#!/usr/bin/python3
from random import choice

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

def dance(phenny, input):
   phenny.do("dances")

dance.commands = ['dance']
dance.priority = 'low'

def ohyou(phenny, input):
   phenny.say("http://i.imgur.com/CPjuz7E.jpg")

ohyou.commands = ['ohyou']
ohyou.priority = 'low'

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
