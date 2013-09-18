from model import *
from peewee import *
from threading import Timer
import time
import random
import math

currentPlayers = {}

def onJoin(phenny, input):
   #It was the bot who joined!
   if input.nick == phenny.nick:
      #Update the list of users in the channel by sending a WHO command
      phenny.write(("WHO", input.sender))
   #Attempt to add that user to the list
   elif input.nick not in currentPlayers:
      try:
         player = Player.get(Player.name == input.nick)
      except:
         player = Player.create(name=input.nick, level=1, seconds_to_level=getSecondsForLevel(1), logged_in=1)

      player.timer_start = int(time.time())
      player.timer = Timer(player.seconds_to_level, lambda: levelUser(player))
      player.save()
      player.timer.start()
      currentPlayers[input.nick] = player

def onLeave(phenny, input):
   if input.nick == phenny.nick:
      pass
   elif input.nick in currentPlayers:
      currentPlayers[input.nick].logged_in = 0
      currentPlayers[input.nick].save()
      updateTime(currentPlayers[input.nick], penalty=50.0*(math.pow(1.14, currentPlayers[input.nick].level)))
      #Do other mumbo jumbo to calculate penalty
      del currentPlayers[input.nick]

def onQuit(phenny, input):
   onLeave(phenny, input)

def onNick(phenny, input):
   oldNick = input.nick
   newNick = input.bytes

   updateTime(currentPlayers[oldNick], penalty=30.0*(math.pow(1.14, currentPlayers[oldNick].level)))
   currentPlayers[oldNick].timer.start()
   currentPlayers[newNick] = currentPlayers[oldNick]
   del currentPlayers[oldNick]

def updateUsers(phenny, input):
   input.nick = input.args[5]
   source = input.args[1]
   if source.startswith("#"):
      onJoin(phenny, input)

def levelUser(player):
   print(player.name + " leveled")
   player.level += 1
   updateTime(player)
   player.timer.start()
   if player.level >= 25 or random.random() < .25:
      opponent = getRandomPlayer(ignore=player.name)
      if opponent is not None:
         initFight(player, opponent)

   #Find a new item!
   itemType = ItemType.select().where(ItemType.req_level <= player.level).order_by(fn.Random()).limit(1).get()
   itemOrigin = ItemOrigin.select().where(ItemOrigin.req_level <= player.level, ItemOrigin.fightable == False).order_by(fn.Random()).limit(1).get()
   itemDesc = Descriptor.select().where(Descriptor.req_level <= player.level).order_by(fn.Random()).limit(1).get()

   currentItem = getItemOfUser(player, itemType.name)
   if currentItem is None:
      currentItem = Inventory.create(player_id=player.id, origin=itemOrigin.id, item_type=itemType.id, item_adj=itemDesc.id)
      print("%s found a %s %s of %s" % (player.name, itemOrigin.name, itemType.name, itemDesc.name))

   elif getStatOfItem(currentItem) <= (itemType.stat + itemOrigin.stat + itemDesc.stat):
      print("%s threw away his %s %s of %s and got a %s %s of %s" % (player.name, currentItem.origin.name, currentItem.item_type.name, currentItem.item_adj.name, itemOrigin.name, itemType.name, itemDesc.name))
      currentItem.origin = ItemOrigin.id
      currentItem.item_type = itemType.id
      currentItem.item_adj = itemDesc.id
      currentItem.save()

   #Tweet/update log with leveling information

def updateTime(player, penalty=None):
   player.timer.cancel()
   if penalty is not None:
      remaining_time = getSecondsUntilNextLevel(player) + penalty
   else:
      remaining_time = getSecondsForLevel(player.level)

   player.seconds_to_level = remaining_time
   player.timer_start = int(time.time())
   player.timer = Timer(player.seconds_to_level, lambda: levelUser(player))
   player.save()

def getSecondsForLevel(level):
   return int( 600 * math.pow( 1.16, level ) )

def getSecondsUntilNextLevel(player):
   current_time = int(time.time())
   elapsed_time = current_time - player.timer_start
   return player.seconds_to_level - elapsed_time

def getList(phenny, input):
   phenny.msg(input.nick, str(currentPlayers))

def getItemOfUser(player, itemType):
   retVal = None

   for item in player.items:
      if item.item_type.name == itemType:
         retVal = item
         break

   return retVal

def getRandomPlayer(ignore=""):
   retVal = None
   while len(currentPlayers) > 1:
      player = random.choice(list(currentPlayers.values()))
      if player.name != ignore:
         retVal = player
         break
   return retVal

def initFight(attacker, defender):
   attack = random.randrange(0, getStats(attacker)+1)
   defense = random.randrange(0, getStats(defender)+1)
   critical = False
   if attack >= defense:
      timeLost = ( max(defender.level/4.0, 7) / 100.0 ) * getSecondsUntilNextLevel(attacker)
      updateTime(attacker, penalty=-timeLost)
      attacker.timer.start()
      print(attacker.name + " beat " + defender.name)

      #Critical!
      if random.random() < .03:
         print("It was a critical hit")
         critical = True
         timeAdded = (random.randrange(5, 25+1) / 100.0) * getSecondsUntilNextLevel(defender)
         updateTime(defender, timeAdded)
         defender.timer.start()
   Fight.create(attacker=attacker.id, attack=attack, defender=defender.id, defense=defense, critical=critical, fight_time=time.time())
   #Tweet/update log with fight information

def getStats(player):
   retVal = player.level
   for item in player.items:
      retVal += getStatOfItem(item)
   return retVal

def getStatOfItem(item):
   retVal = 0
   retVal += item.origin.stat
   retVal += item.item_type.stat
   retVal += item.item_adj.stat
   return retVal

def saveAndStop(phenny, input):
   global currentPlayers
   if not input.admin: return
   for player in currentPlayers.values():
      updateTime(player, penalty=0)
   currentPlayers = {}

def forceUpdate(phenny, input):
   if not input.admin: return
   phenny.write(("WHO", input.sender))

saveAndStop.commands = ['irpg-stop']
forceUpdate.commands = ['irpg-start']

def cheat(phenny, input):
   if not input.admin: return
   levelUser(currentPlayers[input.nick])
cheat.commands = ['cheat']

#forceUpdate.commands = ["forceupdate"]


#getList.commands = ['listusers']

onNick.event = "NICK"
onNick.rule = r'.*'

updateUsers.event = "352"
updateUsers.rule = r'.*'

onLeave.event = "PART"
onLeave.rule = r'.*'

onQuit.event = "QUIT"
onQuit.rule = r'.*'

onJoin.event = "JOIN"
onJoin.rule = r'.*'
#If this bot joined, update the list of users on the channel.
#otherwise just add this user
