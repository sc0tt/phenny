currentPlayers = {}

def onJoin(phenny, input):
   #It was the bot who joined!
   if input.nick == phenny.nick:
      #Update the list of users in the channel by sending a WHO command
      phenny.write(("WHO", input.sender))
   #Attempt to add that user to the list
   elif input.nick not in currentPlayers:
      currentPlayers[input.nick] = None  #Replace with ORM item later on...


def onLeave(phenny, input):
   if input.nick == phenny.nick:
      pass
   elif input.nick in currentPlayers:
      del currentPlayers[input.nick]


def onQuit(phenny, input):
   del currentPlayers[input.nick]


def onNick(phenny, input):
   oldNick = input.nick
   newNick = input.bytes

   #penalty for changing nick
   currentPlayers[newNick] = currentPlayers[oldNick]
   del currentPlayers[oldNick]

def updateUsers(phenny, input):
   nick = input.args[5]
   if nick not in currentPlayers:
      currentPlayers[nick] = None  #Simplify later, duplicated code

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
