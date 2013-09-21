from model import *
from peewee import *
from threading import Timer
import time
import random
import math
import datetime

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
         player.logged_in = True
      except:
         print("Player %s does not exist..." % (input.nick))
         player = Player.create(name=input.nick, level=1, seconds_to_level=getSecondsForLevel(1), logged_in=1, countdown_start=datetime.datetime.now())

      player.countdown_start = datetime.datetime.now()
      updateTime(player, penalty=0)
      player.timer.start()
      currentPlayers[input.nick] = player

def onLeave(phenny, input):
   if input.nick == phenny.nick:
      pass
   elif input.nick in currentPlayers:
      currentPlayers[input.nick].logged_in = 0
      penalty_time = 50.0*(math.pow(1.14, currentPlayers[input.nick].level))
      Penalty.create(player_id=currentPlayers[input.nick].id, seconds=penalty_time, reason='Leave', date=datetime.datetime.now())

      updateTime(currentPlayers[input.nick], penalty=penalty_time)
      #Do other mumbo jumbo to calculate penalty
      del currentPlayers[input.nick]

def onQuit(phenny, input):
   onLeave(phenny, input)

def onNick(phenny, input):
   oldNick = input.nick
   newNick = input.bytes

   penalty_time = 30.0*(math.pow(1.14, currentPlayers[oldNick].level))
   Penalty.create(player_id=currentPlayers[input.nick].id, seconds=penalty_time, reason='Nick', date=datetime.datetime.now())

   updateTime(currentPlayers[oldNick], penalty=penalty_time)
   currentPlayers[oldNick].timer.start()
   currentPlayers[newNick] = currentPlayers[oldNick]
   del currentPlayers[oldNick]

def updateUsers(phenny, input):
   input.nick = input.args[5]
   source = input.args[1]
   if source.startswith("#"):
      onJoin(phenny, input)

def levelUser(player):
   player.level += 1

   eventText = "%s leveled up to %s" % (player.name, player.level)
   Event.create(player_id=player.id, type="Level", text=eventText, date=datetime.datetime.now())
   print(eventText)

   updateTime(player)
   player.timer.start()

   if player.level >= 25 or random.random() < .3:
      print (player.name + " looks like he is gonna fight!")
      opponent = getRandomPlayer(ignore=player.name)
      if opponent is not None:
         initFight(player, opponent)

   #Find a new item!
   itemType = ItemType.select().where(ItemType.req_level <= player.level).order_by(fn.Random()).limit(1).get()
   itemOrigin = ItemOrigin.select().where((ItemOrigin.req_level <= player.level) & (ItemOrigin.fightable == False)).order_by(fn.Random()).limit(1).get()
   itemDesc = Descriptor.select().where(Descriptor.req_level <= player.level).order_by(fn.Random()).limit(1).get()
   itemStat = itemType.stat + itemOrigin.stat + itemDesc.stat

   currentItem = getItemOfUser(player, itemType.name)
   if currentItem is None:
      currentItem = Inventory.create(player_id=player.id, origin=itemOrigin.id, item_type=itemType.id, item_adj=itemDesc.id)

      eventText = "%s found a %s %s of %s" % (player.name, itemOrigin.name, itemType.name, itemDesc.name)
      Event.create(player_id=player.id, type="Item", text=eventText, date=datetime.datetime.now())
      print(eventText)

   elif getStatOfItem(currentItem) <= itemStat:

      eventText = "%s threw away his %s %s of %s [%s] and picked up a %s %s of %s [%s]" % (player.name,
                                                                                          currentItem.origin.name,
                                                                                          currentItem.item_type.name,
                                                                                          currentItem.item_adj.name,
                                                                                          getStatOfItem(currentItem),
                                                                                          itemOrigin.name,
                                                                                          itemType.name,
                                                                                          itemDesc.name,
                                                                                          itemStat)
      Event.create(player_id=player.id, type="Item", text=eventText, date=datetime.datetime.now())
      print(eventText)

      currentItem.origin = itemOrigin.id
      currentItem.item_type = itemType.id
      currentItem.item_adj = itemDesc.id
      currentItem.save()
   else:
      eventText = "%s found a %s %s of %s [%s] but their %s %s of %s [%s] was better!" % (player.name,
                                                                                          itemOrigin.name,
                                                                                          itemType.name,
                                                                                          itemDesc.name,
                                                                                          itemStat,
                                                                                          currentItem.origin.name,
                                                                                          currentItem.item_type.name,
                                                                                          currentItem.item_adj.name,
                                                                                          getStatOfItem(currentItem))
      Event.create(player_id=player.id, type="Item", text=eventText, date=datetime.datetime.now())
      print(eventText)

   #Tweet/update log with leveling information

def updateTime(player, penalty=None):
   #This exception will be thrown if this is a new user!
   try:
      player.timer.cancel()
   except AttributeError:
      pass


   if penalty is not None:
      remaining_time = getSecondsUntilNextLevel(player) + penalty
   else:
      remaining_time = getSecondsForLevel(player.level)

   player.countdown_start = datetime.datetime.now()
   player.seconds_to_level = remaining_time
   player.save()
   player.timer = Timer(player.seconds_to_level, lambda: levelUser(player))


def getSecondsForLevel(level):
   return int( 600 * math.pow( 1.16, level ) )

def getSecondsUntilNextLevel(player):
   current_time = datetime.datetime.now()
   elapsed_time = current_time - player.countdown_start
   return player.seconds_to_level - elapsed_time.seconds

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
      penalty_time = ( max(defender.level/4.0, 7) / 100.0 ) * getSecondsUntilNextLevel(attacker)
      Penalty.create(player_id=attacker.id, seconds=-penalty_time, reason='Battle Won', date=datetime.datetime.now())

      updateTime(attacker, penalty=-penalty_time)
      attacker.timer.start()
      print(attacker.name + " beat " + defender.name)

      #Critical!
      if random.random() < .03:
         print("It was a critical hit")
         critical = True
         penalty_time = (random.randrange(5, 25+1) / 100.0) * getSecondsUntilNextLevel(defender)
         Penalty.create(player_id=defender.id, seconds=penalty_time, reason='Critical', date=datetime.datetime.now())

         updateTime(defender, penalty=penalty_time)
         defender.timer.start()
   else:
      print(attacker.name + " lost to " + defender.name)
      penalty_time = ( max(defender.level/7.0, 7) / 100.0 ) * getSecondsUntilNextLevel(attacker)
      Penalty.create(player_id=attacker.id, seconds=penalty_time, reason='Battle Lost', date=datetime.datetime.now())

      updateTime(attacker, penalty=penalty_time)
      attacker.timer.start()


   Fight.create(attacker=attacker.id, attack=attack, defender=defender.id, defense=defense, critical=critical, fight_time=datetime.datetime.now())
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

   phenny.say("IdleRPG2 Stopped: Disabling all timers and updating all players information")
   for player in currentPlayers.values():
      player.logged_in = False
      updateTime(player, penalty=0)
   currentPlayers = {}

def forceUpdate(phenny, input):
   if not input.admin: return

   phenny.say("IdleRPG2 Start: Resuming all active players progress.")
   phenny.write(("WHO", input.sender))

saveAndStop.commands = ['irpg-stop']
forceUpdate.commands = ['irpg-start']

def cheat(phenny, input):
   if not input.admin: return
   levelUser(currentPlayers[input.nick])
cheat.commands = ['cheat']


def getList(phenny, input):
   phenny.msg(input.nick, str(currentPlayers))
getList.commands = ['listusers']

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
