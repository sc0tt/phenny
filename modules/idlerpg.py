from model import *
from threading import Timer
import time
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
         player = Player.create(name=input.nick, level=1, seconds_to_level=getSecondsToLevel(1), logged_in=1)

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
      currentPlayers[input.nick].logged_in.save()
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
   onJoin(phenny, input)


def levelUser(player):
   print(player.name + " leveled")
   player.level += 1
   updateTime(player)
   player.timer.start()


def updateTime(player, penalty=None):
   player.timer.cancel()
   current_time = int(time.time())
   elapsed_time = current_time - player.timer_start
   if penalty is not None:
      remaining_time = ( player.seconds_to_level - elapsed_time ) + time_to_add
   else:
      remaining_time = getSecondsToLevel(player.level)

   player.seconds_to_level = remaining_time
   player.timer_start = int(time.time())
   player.timer = Timer(player.seconds_to_level, lambda: levelUser(player))
   player.save()

def getSecondsToLevel(level):
   return int( 600 * math.pow( 1.16, level ) )

def getList(phenny, input):
   phenny.msg(input.nick, str(currentPlayers))

def saveAndStop():
   for player in currentPlayers.values():
      updateTime(player, penalty=0)

def forceUpdate(phenny, input):
   phenny.write(("WHO", input.sender))

#forceUpdate.commands = ["forceupdate"]


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
