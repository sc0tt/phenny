images = {}
def m(phenny, input):
   word = input.group(2).split()
   if len(word) > 0:
      key = word[0]
      if key in images:
         phenny.say(images[key])
      else:
         if len(word) > 1:
            word = " ".join(word[1:])
            images[key] = word
            phenny.say(key + " = " + word)
         else:
            phenny.say("No value for key " + key)   
   else:
      phenny.say("-- .m <key> <value>")

m.commands = ['m']
m.priority = 'low'

def catchAll(phenny, input):
   word = input.group(0)
   word = word.lstrip('.')
   word = word.split()[0]
   if word in images:
      phenny.say(images[word])

#catchAll.rule = r'\..+'
#catchAll.priority = 'low'

