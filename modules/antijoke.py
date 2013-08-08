
import feedparser
import re
from random import randint

def antijoke(phenny, input):
	feed = feedparser.parse('http://www.reddit.com/r/antijokes/.rss?limit=50')
	rNum = randint(0,len(feed["items"]))
	title = feed["items"][rNum]["title"]
	desc = feed["items"][rNum]["description"]
	exp = re.compile('<p>(.*?)<\/p>')
	joke = exp.findall(desc)
	phenny.say(title)
	phenny.say(joke[0])

antijoke.commands = ['antijoke']
antijoke.priority = 'low'	
