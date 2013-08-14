
import feedparser
import re
from random import randint, choice
import html.parser

punCount = 0
exp = re.compile('<p>(.*?)<\/p>')
hrefExp = re.compile('<a href="(.*?)">[link]')
htmlParser = html.parser.HTMLParser()

def antijoke(phenny, input):
   feed = feedparser.parse('http://www.reddit.com/r/antijokes/.rss?limit=50')
   rNum = randint(0,len(feed["items"]))
   title = feed["items"][rNum]["title"]
   desc = exp.findall(feed["items"][rNum]["description"])
   phenny.say(htmlParser.unescape(title))
   if len(desc) >= 1:
      phenny.say(htmlParser.unescape(desc[0]))

antijoke.commands = ['antijoke']
antijoke.priority = 'low'	

def pun(phenny,input):
   feed = feedparser.parse('http://www.reddit.com/r/punny/.rss?limit=100')
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
   phenny.say(htmlParser.unescape(pun_choice[0]))
   phenny.say(htmlParser.unescape(pun_choice[1]))

pun.commands = ['pun']
pun.priority = 'low'

def subr(phenny,input):
   subreddit = input.group(2)
   feed = feedparser.parse('http://www.reddit.com/r/'+subreddit+'/.rss?limit=100')
   rNum = randint(0,len(feed["items"]))
   link = feed["items"][rNum]["link"]
   phenny.say(link)

subr.commands = ['subr']
subr.priority = 'low'
