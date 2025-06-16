from peewee import *
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
    nickname = CharField(unique=True, max_length=255)
    password = CharField()
    role = CharField()

class Food(BaseModel):
    name = CharField(max_length=255) 
    category = CharField(max_length=255)
    calories = FloatField()
    protein = FloatField()
    fat = FloatField()
    carbs = FloatField()
    unit = CharField(max_length=50)

class MealPlans(BaseModel):
    user = ForeignKeyField(User, backref="mealplans")
    date = DateField()
    type = CharField(max_length=50) 
    notes = TextField()

class MealItems(BaseModel):
    quantity = FloatField()
    meal_plan = ForeignKeyField(MealPlans, backref="mealitems")  
    food = ForeignKeyField(Food, backref="mealitems")  

class UserData(BaseModel):
    user = ForeignKeyField(User, backref="personal_data")  
    weight = FloatField()
    year_of_birth = IntegerField()  
    gender = BooleanField()

class LabTest(BaseModel):
    user = ForeignKeyField(User, backref="labtests")
    date = DateField()
    value = FloatField()
    unit = CharField(max_length=50) 
    frequency = CharField(max_length=50)  

class Notification(BaseModel):
    user = ForeignKeyField(User, backref="notifications")
    title = CharField(max_length=255)  

class Reminders(BaseModel):
    user = ForeignKeyField(User, backref="reminders") 
    type = CharField(max_length=50)  
    target_date = DateField()  
    description = TextField()

class Pantry(BaseModel):
    user = ForeignKeyField(User, backref="pantries")
    food = ForeignKeyField(Food, backref="pantries") 
    quantity = FloatField()
    unit = CharField(max_length=50) 
    expiry_date = DateField()  

class DietUser(BaseModel):
    user_data = ForeignKeyField(UserData, backref="diets") 
    diet_name = CharField(max_length=255) 
    diet_description = TextField()  
    is_active = BooleanField() 
    author = CharField(max_length=255)  

class SupportMessages(BaseModel):
    user = ForeignKeyField(User, backref="support_messages")  
    recipient_type = CharField(max_length=50)  
    description = TextField()
    time_date = DateTimeField() 


class RefreshToken(BaseModel):
    user = ForeignKeyField(User, backref='tokens')
    token = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    expires_at = DateTimeField()