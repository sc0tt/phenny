#!/usr/local/bin/python3.3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from model import *
import math
from operator import itemgetter
from datetime import datetime, timedelta
app = Flask(__name__, template_folder="template")


@app.route('/')
def home():
   players = Player.select().order_by(Player.level.desc())

   playerList = []

   for player in players:
      if player.logged_in:
         secondsToLevel = (player.countdown_start + timedelta(seconds=player.seconds_to_level)) - datetime.now()
         secondsToLevel = secondsToLevel.seconds
      else:
         secondsToLevel = player.seconds_to_level
      timeToLevel = getFormattedTime(secondsToLevel, False)

      totalAttack = player.level
      for item in player.items.order_by(Inventory.item_type):
         totalAttack += item.origin.stat + item.item_type.stat + item.item_adj.stat

      playerList.append(dict(name=player.name, ttl=timeToLevel, level=player.level, atk=totalAttack, logged="Yes" if player.logged_in else "No", stl=secondsToLevel))

      playerList = sorted(playerList, key=lambda k: (-k['level'], k['stl']))



   #for player in Player.select().order_by(Player.level.desc()):
   #   players.append(dict(name=player.name, level=player.level))

   battles = []
   for battle in Fight.select().order_by(Fight.fight_time.desc()).limit(50):
      response = ""
      attackerWon = battle.attack >= battle.defense
      critText = ""
      if battle.critical:
         critText = "It was a critical hit!"
      response += '''%s [%s] attacked %s [%s] and %s. %s''' % (battle.attacker.name, battle.attack, battle.defender.name, battle.defense, "won" if attackerWon else "lost", critText)
      battles.append(dict(date=getFormattedDate(battle.fight_time), text=response, crit=battle.critical))

   penalties = []
   for penalty in Penalty.select().order_by(Penalty.date.desc()).limit(50):
      lostTime = penalty.seconds < 0
      penaltyTime = getFormattedTime(penalty.seconds)

      reason = ""
      if penalty.reason == "Leave":
         reason = "Leaving"
      elif penalty.reason == "Nick":
         reason = "Nick change."
      elif penalty.reason == "Battle Won":
         reason = "Battle won."
      elif penalty.reason == "Battle Lost":
         reason = "Battle lost."
      elif penalty.reason == "Critical":
         reason = "Critical hit."

      penalties.append(dict(lostTime=lostTime, player=penalty.player_id.name, time=penaltyTime, reason=reason))


   return render_template('index.html', players=playerList, battles=battles, penalties=penalties)

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

   totalAttack = player.level
   items = []
   for item in player.items.order_by(Inventory.item_type):
      itemStat = item.origin.stat + item.item_type.stat + item.item_adj.stat
      totalAttack += itemStat
      name = '%s %s of %s' % (item.origin.name, item.item_type.name, item.item_adj.name)
      items.append(dict(name=name, stat=itemStat))

   playerOut = dict(name=player.name, level=player.level, ttl=getFormattedTime(timeToLevel, False), logged="Yes" if player.logged_in else "No", attack=totalAttack)

   battles = []
   for battle in Fight.select().where((Fight.attacker == player.id) | (Fight.defender == player.id)).order_by(Fight.fight_time.desc()):
      response = ""
      attackerWon = battle.attack >= battle.defense
      critText = ""
      if battle.critical:
         critText = "It was a critical hit!"
      response += '''%s [%s] attacked %s [%s] and %s. %s''' % (battle.attacker.name, battle.attack, battle.defender.name, battle.defense, "won" if attackerWon else "lost", critText)
      battles.append(dict(date=getFormattedDate(battle.fight_time), text=response, crit=battle.critical))

   penalties = []
   for penalty in Penalty.select().where(Penalty.player_id == player.id).order_by(Penalty.date.desc()):
      lostTime = penalty.seconds < 0
      penaltyTime = getFormattedTime(penalty.seconds)

      reason = ""
      if penalty.reason == "Leave":
         reason = "Leaving"
      elif penalty.reason == "Nick":
         reason = "Nick change."
      elif penalty.reason == "Battle Won":
         reason = "Battle won."
      elif penalty.reason == "Battle Lost":
         reason = "Battle lost."
      elif penalty.reason == "Critical":
         reason = "Critical hit."

      penalties.append(dict(lostTime=lostTime, player=penalty.player_id.name, time=penaltyTime, reason=reason))

   return render_template('player.html', player=playerOut, items=items, battles=battles, penalties=penalties)

def getFormattedDate(dtime):
   return dtime.strftime("%m/%d/%y %I:%M:%S %p")

def getFormattedTime(seconds, compact=True):
   d = datetime(1,1,1) + timedelta(seconds=math.fabs(seconds))
   if compact:
      return "%s%02d:%02d:%02d:%02d" % ("-" if seconds < 0 else "", d.day-1, d.hour, d.minute, d.second)
   else:
      return "%dd %dh %dm %ds" % (d.day-1, d.hour, d.minute, d.second)

@app.before_request
def before_request():
    g.db = db
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080, debug=False)
