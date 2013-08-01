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
   phenny.say(choice(alotImages))

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
