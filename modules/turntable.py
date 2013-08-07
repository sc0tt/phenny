import ttapi
import threading

class TTBot(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.bot = None
        self.currentSong = "Nothing is currently playing. This will be updated when the next song starts."

    def run(self):
        with open("ttkeys.txt") as fp:
           arg1, arg2, arg3 = fp.read().split()
        self.bot = ttapi.Bot(arg1, arg2, arg3)
        self.bot.on('newsong', self.updateSong)
        self.bot.start()
        self.currentSong = None

    def updateSong(self, data):
        self.bot.bop()
        artist = data['room']['metadata']["current_song"]['metadata']["artist"]
        song = data['room']['metadata']["current_song"]['metadata']["song"]
        dj = data['room']['metadata']["current_song"]["djname"]
        self.currentSong = "%s is currently DJing: %s by %s" % (dj, song, artist)

myBot = TTBot()
myBot.start()

def tt(phenny, input):
    phenny.say(myBot.currentSong)

tt.commands = ['tt']
tt.priority = 'low'
