channels = {}

def onJoin(phenny, input):
   if input.sender not in channels:
      channels[input.sender] = []
   #It was the bot who joined!
   if input.nick == phenny.nick:
      #Update the list of users in the channel by sending a WHO command
      phenny.write(("WHO", input.sender))
   #Attempt to add that user to the list
   elif input.nick not in channels[input.sender]:
      channels[input.sender].append(input.nick)

def onLeave(phenny, input):
   if input.sender not in channels:
      channels[input.sender] = []

   if input.nick == phenny.nick:
      pass
   elif input.nick in channels[input.sender]:
      channels[input.sender].remove(input.nick)

def onQuit(phenny, input):
   for channel in channels:
      if input.nick in channels[channel]:
         channels[channel].remove(input.nick)

def updateUsers(phenny, input):
   nick = input.args[5]
   channel = input.args[1]

   if channel not in channels:
      channels[channel] = []

   if nick not in channels[channel]:
      channels[channel].append(nick)

def getList(phenny, input):
   phenny.msg(input.nick, str(channels))

getList.commands = ['listusers']

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
