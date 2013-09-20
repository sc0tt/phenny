#!/usr/local/bin/python3.3
from peewee import *

db = SqliteDatabase('idlerpg.db', threadlocals=True)

class BaseModel(Model):
   class Meta:
      database = db

class Player(BaseModel):
   id = PrimaryKeyField()
   name = CharField()
   level = IntegerField()
   countdown_start = DateTimeField()
   seconds_to_level = BigIntegerField()
   logged_in = BooleanField()

class Fight(BaseModel):
   id = PrimaryKeyField()
   attacker = ForeignKeyField(Player, related_name='attacks')
   attack = IntegerField()
   defender = ForeignKeyField(Player, related_name='defends')
   defense = IntegerField()
   critical = BooleanField()
   fight_time = DateTimeField()

class Penalty(BaseModel):
   id = PrimaryKeyField()
   player_id = ForeignKeyField(Player, related_name='penalties')
   seconds = IntegerField()
   reason = CharField()
   date = DateTimeField()

class ItemType(BaseModel):
   id = PrimaryKeyField()
   name = CharField()
   stat = IntegerField()
   req_level = IntegerField()

class ItemOrigin(BaseModel):
   id = PrimaryKeyField()
   name = CharField()
   stat = IntegerField()
   req_level = IntegerField()
   fightable = BooleanField()

class Descriptor(BaseModel):
   id = PrimaryKeyField()
   name = CharField()
   stat = IntegerField()
   req_level = IntegerField()

class Inventory(BaseModel):
   id = PrimaryKeyField()
   player_id = ForeignKeyField(Player, related_name='items')
   origin = ForeignKeyField(ItemOrigin)
   item_type = ForeignKeyField(ItemType)
   item_adj = ForeignKeyField(Descriptor)

class Event(BaseModel):
   id = PrimaryKeyField()
   player_id = ForeignKeyField(Player, related_name='events')
   type = CharField()
   text = CharField()
   date = DateTimeField()

