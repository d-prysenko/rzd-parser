import datetime
from peewee import *
from services.Settings import Settings

db = SqliteDatabase(Settings().cwd + '/storage/notifications.db')

def create_tables():
    db.create_tables([Notification])

class BaseModel(Model):
    class Meta:
        database = db

class Notification(BaseModel):
    id = AutoField(column_name='id')
    chat_id = TextField(column_name='chat_id', null=False)
    query_id = IntegerField(column_name='query_id', null=False)
    train_number = TextField(column_name='train_number', null=False)
    departure_datetime = TextField(column_name='departure_datetime', null=False)
    car_type_name = TextField(column_name='car_type_name', null=False)
    min_price = FloatField(column_name='min_price', null=False)
    place_quantity = IntegerField(column_name='place_quantity', null=False)
    lower_place_quantity = IntegerField(column_name='lower_place_quantity', null=False)
    sent_at = DateTimeField(column_name='sent_at', default=datetime.datetime.now)


    class Meta:
        table_name = 'notifications'

def create_notification(chat_id, query_id, train_number, departure_datetime, car_type_name, min_price, place_quantity, lower_place_quantity):
    return Notification.create(
        chat_id=chat_id,
        query_id=query_id,
        train_number=train_number,
        departure_datetime=departure_datetime,
        car_type_name=car_type_name,
        min_price=min_price,
        place_quantity=place_quantity,
        lower_place_quantity=lower_place_quantity
    )

def find_notification(chat_id, query_id, train_number, departure_datetime, car_type_name):
    return Notification.get_or_none(
        (Notification.chat_id == chat_id) &
        (Notification.query_id == query_id) &
        (Notification.train_number == train_number) &
        (Notification.departure_datetime == departure_datetime) &
        (Notification.car_type_name == car_type_name))

def select_notifications_by_query_id(query_id):
    return Notification.select().where(Notification.query_id == query_id)

def notification_exists(chat_id, query_id, train_number, departure_datetime, car_type_name, min_price, place_quantity, lower_place_quantity):
    return Notification.get_or_none(
        (Notification.chat_id == chat_id) &
        (Notification.query_id == query_id) &
        (Notification.train_number == train_number) &
        (Notification.departure_datetime == departure_datetime) &
        (Notification.car_type_name == car_type_name)& 
        (Notification.min_price == min_price) &
        (Notification.place_quantity == place_quantity) &
        (Notification.lower_place_quantity == lower_place_quantity)) != None

def update_notification(notification: Notification, min_price, place_quantity, lower_place_quantity):
    notification.min_price = min_price
    notification.place_quantity = place_quantity
    notification.lower_place_quantity = lower_place_quantity
    notification.save()
