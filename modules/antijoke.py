
import feedparser
import re
from random import randint, choice

punCount = 0
exp = re.compile('<p>(.*?)<\/p>')

def antijoke(phenny, input):
   feed = feedparser.parse('http://www.reddit.com/r/antijokes/.rss?limit=50')
   rNum = randint(0,len(feed["items"]))
   title = feed["items"][rNum]["title"]
   desc = exp.findall(feed["items"][rNum]["description"])
   phenny.say(title)
   if len(desc) >= 1:
      phenny.say(desc[0])

antijoke.commands = ['antijoke']
antijoke.priority = 'low'	

def pun(phenny,input):
   feed = feedparser.parse('http://www.reddit.com/r/punny/.rss?limit=50')
   feedlen = len(feed["items"])
   all_puns = []
   for item in range(feedlen):
      desc = exp.findall(feed["items"][item]["description"])
      desclen = len(desc)
      if desclen >= 1:
         title = feed["items"][item]["title"] 
         txt = ""
         for ptag in range(desclen):
            txt = txt + " " + desc[ptag]
         
         all_puns.append([title, txt])
            		
   pun_choice = choice(all_puns)
   phenny.say(pun_choice[0])
   phenny.say(pun_choice[1])

pun.commands = ['pun']
pun.priority = 'low'
