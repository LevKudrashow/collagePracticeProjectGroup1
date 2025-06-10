from peewee import Model, CharField, ForeignKeyField, DateTimeField
from peewee import PostgresqlDatabase
from dotenv import load_dotenv
import datetime
import os

load_dotenv()

DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')

db = PostgresqlDatabase(DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    nickname = CharField(unique=True)
    password = CharField()

class RefreshToken(BaseModel):
    user = ForeignKeyField(User, backref='tokens')
    token = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    expires_at = DateTimeField()