from peewee import *

db = SqliteDatabase('idlerpg.db')

class BaseModel(Model):
   class Meta:
      database = db

class Player(BaseModel):
   id = PrimaryKeyField()
   name = CharField()
   level = IntegerField()
   seconds_to_level = BigIntegerField()
   logged_in = BooleanField()
   channel = CharField()

class Fight(BaseModel):
   id = PrimaryKeyField()
   attacker = ForeignKeyField(Player, related_name='attacks')
   attack = IntegerField()
   defender = ForeignKeyField(Player, related_name='defends')
   defense = IntegerField()
   fight_time = DateTimeField()

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