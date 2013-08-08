
import feedparser
import re
from random import randint

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
	puns = {}
	feed = feedparser.parse('http://www.reddit.com/r/punny/.rss?limit=50')
	feedlen = len(feed["items"])
	for item in range(feedlen):
		desc = exp.findall(feed["items"][item]["description"])
		if len(desc) >= 1:
			phenny.say(feed["items"][item]["title"])
			phenny.say(desc[0])
			break
pun.commands = ['pun']
pun.priority = 'low'
