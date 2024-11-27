import sqlite3
import datetime
from peewee import *
from Settings import Settings

db = SqliteDatabase(Settings().cwd + '/trains.db')

def createTables():
    db.create_tables([Train])

class BaseModel(Model):
    class Meta:
        database = db

class Train(BaseModel):
    id = AutoField(column_name='id')
    train_number = TextField(column_name='train_number', null=False)
    departure_datetime = TextField(column_name='departure_datetime', null=False)
    sent_at = DateTimeField(column_name='sent_at', default=datetime.datetime.now)


    class Meta:
        table_name = 'trains'