#!/usr/bin/python3
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
