"""
waffle-bot.py - waffle-bot Module
Copyright 2013, Scott Adie
Lalla
"""

import json
import psycopg2

with open("wafflebot.txt") as fp:
   db_user, db_pass = fp.read().split()

db = psycopg2.connect("dbname=wafflebot user=%s password=%s" % (db_user, db_pass))
cursor = db.cursor()

def wafflebot(phenny, input):
   print(input.group(0))
   for pair in rip_sentence(input.group(0)):
      key = pair[0].replace("'","\'")
      val = pair[1].replace("'","\'")
      cursor.execute("INSERT INTO pairs (key, val) VALUES (%s, %s)", (key, val))
      db.commit()


def rip_sentence(line):
   key_len = 3
   word_list = []
   line = line.lower()
   line = line.split()
   if len(line) > 5:
      for str_index in range(0, len(line)-(key_len*2) + 1):
         key = " ".join(line[str_index:key_len+str_index])
         val_start = str_index + key_len
         val_end = val_start + key_len
         val = " ".join(line[val_start:val_end])
         word_list.append([key, val])
   return word_list

wafflebot.rule = r'.*'
wafflebot.priority = 'high'
wafflebot.thread = False

def sentence(phenny, input):
   cursor.execute("SELECT key FROM pairs ORDER BY random() limit 1")
   sentence = ""
   seed = cursor.fetchone()[0]
   sentence += seed
   for i in range(0, 10):
      new_seed = getNextLink(seed)
      if not new_seed or new_seed[0].endswith("."):
         break
      sentence += " %s" % (new_seed[0],)
      seed = new_seed[0]
   phenny.say(sentence)


def getNextLink(input_line):
   cursor.execute("SELECT val FROM pairs WHERE key = %s", (input_line,))
   x = cursor.fetchone()
   return x
   
sentence.commands = ['talk']
sentence.priority = 'low'
sentence.thread = True
