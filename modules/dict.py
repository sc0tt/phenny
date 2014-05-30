import requests

def lookup(word, api_key):
  payload = {'api_key': api_key, 'limit': 1}
  try:
    response = requests.get("http://api.wordnik.com:80/v4/word.json/%s/definitions" % word.lower(), params=payload).json()
    return response[0]['text']
  except:
    return None

def define(phenny, input):
  word = input.group(2)
  if not word:
    phenny.say("-- .define <word>")
  else:
    definition = lookup(word, phenny.config.wordnik_api_key)
    if definition is None:
      phenny.say("Word not found!")
    else:
      phenny.say("%s: %s" % (word, definition))
define.commands = ['define']


def wotd(phenny, input):
  payload = {'api_key': phenny.config.wordnik_api_key}
  response = requests.get("http://api.wordnik.com:80/v4/words.json/wordOfTheDay", params=payload).json()
  definition = lookup(response['word'], phenny.config.wordnik_api_key)
  phenny.say("Word of the day: %s - %s" % (response['word'], definition))

  
wotd.commands = ['wotd']

def rword(phenny, input):
  payload = {'api_key': phenny.config.wordnik_api_key,
             'hasDictionaryDef': 'true' }
  response = requests.get("http://api.wordnik.com:80/v4/words.json/randomWord", params=payload).json()
  definition = lookup(response['word'], phenny.config.wordnik_api_key)
  phenny.say("Random word: %s - %s" % (response['word'], definition))
rword.commands = ['rword']
