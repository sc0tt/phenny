from peeewee import *

mapdb = SqliteDatabase('mappings.db')

class MapModel(Model):
    class Meta:
        database = mapdb

class Maps(MapModel):
    key = peewee.TextField()
    val = peewee.TextField()
    
Maps.create_table(True)


def m(phenny, input):
   word = input.group(2)
   if word:
      word = word.split()
      key = word[0]
      try:
         image = Maps.get(Maps.key==key)
      except:
         image = Maps()
         
      if len(word) == 1:
            phenny.say(image.val)
         except Exception:
            phenny.say("Not Found")
      else:
         word = " ".join(word[1:])
         Maps.create(key=key, val=word)
         phenny.say(key + " = " + word)
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

