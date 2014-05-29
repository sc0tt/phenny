import requests


def define(phenny, input):
  word = input.group(2)
  if not word:
    phenny.say("-- .define <word>")
  else:
    payload = {'api_key': phenny.config.wordnik_api_key, 'limit': 1}
    response = requests.get("http://api.wordnik.com:80/v4/word.json/%s/definitions" % word.lower(), params=payload).json()
    phenny.say("%s: %s" % (word, response[0]['text']))
define.commands = ['define']


def wotd(phenny, input):
  payload = {'api_key': phenny.config.wordnik_api_key}
  response = requests.get("http://api.wordnik.com:80/v4/words.json/wordOfTheDay", params=payload).json()
  phenny.say("Word of the day: %s" % (response['word']))

  
wotd.commands = ['wotd']

def rword(phenny, input):
  pass
rword.commands = ['rword']
