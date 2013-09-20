#!/usr/local/bin/python3.3
from flask import Flask
from flask import g
from model import *
import math
from datetime import datetime, timedelta
app = Flask(__name__)



@app.route('/')
def home():
   response = '''<head><title>IdleRPG2 Player Stats</title></head><body>
                 IdleRPG2<hr />Level - Player<br />'''
   for player in Player.select().order_by(Player.level.desc()):
      response += "%s - <a href='/p/%s'>%s</a><br />" % (player.level, player.name, player.name)

   response += '''<hr />Last 50 Battles (Most recent on top):<br /><br />'''
   for battle in Fight.select().order_by(Fight.fight_time.desc()).limit(50):
      attackerWon = battle.attack >= battle.defense
      critText = ""
      if battle.critical:
         critText = "%s's attack was a critical hit so %s was penalized for time!" % (battle.attacker.name, battle.defender.name)
      response += '''[%s] %s [%s] attacked %s [%s] and %s. %s<br />''' % (getFormattedDate(battle.fight_time), battle.attacker.name, battle.attack, battle.defender.name, battle.defense, "won" if attackerWon else "lost", critText)

   response += '''<hr />Last 50 Penalties (Most recent on top):<br /><br />'''
   for penalty in Penalty.select().order_by(Penalty.date.desc()):
      sway = "lost" if penalty.seconds < 0 else "gained"
      penaltyTime = getFormattedTime(penalty.seconds)

      reason = ""
      if penalty.reason == "Leave":
         reason = "leaving the channel."
      elif penalty.reason == "Nick":
         reason = "changing their nick."
      elif penalty.reason == "Battle Won":
         reason = "winning a battle."
      elif penalty.reason == "Battle Lost":
         reason = "losing a battle."
      elif penalty.reason == "Critical":
         reason = "getting hit with a crit."

      response += '''[%s] %s %s %s for %s<br />''' % (getFormattedDate(penalty.date), penalty.player_id.name, sway, penaltyTime, reason)


   return response

@app.route('/p/<name>')
def player(name=None):
   try:
      player = Player.get(Player.name == name)
   except:
      return "No such player"

   response = '''<head><title>IdleRPG2 Player Stats for %s</title></head><body>
                 <a href="/">Back</a><hr />''' % player.name

   #Time to level is (countdown_start + seconds_to_level) - now
   if player.logged_in:
      timeToLevel = (player.countdown_start + timedelta(seconds=player.seconds_to_level)) - datetime.now()
      timeToLevel = timeToLevel.seconds
   else:
      timeToLevel = player.seconds_to_level

   response += '''Name: %s<br />
                  Level: %s<br />
                  Time to level: %s<br />
                  Logged in: %s<br />
                  <hr />Inventory:<br />
                  ''' % (player.name, player.level, getFormattedTime(timeToLevel), "Yes" if player.logged_in else "No")
   totalAttack = player.level
   for item in player.items.order_by(Inventory.item_type):
      itemStat = item.origin.stat + item.item_type.stat + item.item_adj.stat
      totalAttack += itemStat
      response += '''%s %s of %s [%s]<br />''' % (item.origin.name, item.item_type.name, item.item_adj.name, itemStat)

   response += '''<br />Total Attack/Defense: %s<br />
                  (Sum of item stats + player level)''' % (totalAttack)

   response += '''<hr />Battles:<br >'''
   for battle in Fight.select().where((Fight.attacker == player.id) | (Fight.defender == player.id)).order_by(Fight.fight_time.desc()):
      attackerWon = battle.attack >= battle.defense
      critText = ""
      if battle.critical:
         critText = "%s's attack was a critical hit so %s was penalized for time!" % (battle.attacker.name, battle.defender.name)
      response += '''[%s] %s [%s] attacked %s [%s] and %s. %s<br />''' % (getFormattedDate(battle.fight_time), battle.attacker.name, battle.attack, battle.defender.name, battle.defense, "won" if attackerWon else "lost", critText)

   response += '''<hr />Penalties:<br >'''
   for penalty in player.penalties.order_by(Penalty.date.desc()).limit(50):

      sway = "lost" if penalty.seconds < 0 else "gained"

      penaltyTime = getFormattedTime(penalty.seconds)

      reason = ""
      if penalty.reason == "Leave":
         reason = "leaving the channel."
      elif penalty.reason == "Nick":
         reason = "changing their nick."
      elif penalty.reason == "Battle Won":
         reason = "winning a battle."
      elif penalty.reason == "Battle Lost":
         reason = "losing a battle."
      elif penalty.reason == "Critical":
         reason = "getting hit with a crit."

      response += '''[%s] %s %s %s for %s<br />''' % (getFormattedDate(penalty.date), penalty.player_id.name, sway, penaltyTime, reason)
      #player <gained/lost> <time> for <reason>



   return response

def getFormattedDate(dtime):
   return dtime.strftime("%m/%d/%y %I:%M:%S")

def getFormattedTime(seconds):
   d = datetime(1,1,1) + timedelta(seconds=math.fabs(seconds))
   return "%d days %d hours %d minutes %d seconds" % (d.day-1, d.hour, d.minute, d.second)

@app.before_request
def before_request():
    g.db = db
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080, debug=True)
