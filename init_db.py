import os
from dotenv import load_dotenv
from peewee import PostgresqlDatabase
from app import models
# При первом импорте init_db создаст все нужные таблицы в PostgreSQL, если их ещё нет.
# Это работает автоматически через DatabaseManager, не требует ручной миграции.


load_dotenv()

DATABASE_NAME = os.getenv('DATABASE_NAME', '').strip()
DATABASE_USER = os.getenv('DATABASE_USER', '').strip()
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '').strip()
DATABASE_HOST = os.getenv('DATABASE_HOST', '').strip()
DATABASE_PORT = int(os.getenv('DATABASE_PORT', '5432').strip())

db_instance = models.db
db_instance.init(
    DATABASE_NAME,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
)

MODELS = [
    models.User,
    models.RefreshToken,
    models.Food,
    models.MealPlans,
    models.MealItems,
    models.UserData,
    models.LabTest,
    models.Notification,
    models.Reminders,
    models.Pantry,
    models.DietUser,
    models.SupportMessages,
]


class DatabaseManager:
    _instance = None

    def __init__(self):
        self.db = db_instance
        self._connect_and_initialize()

    def _connect_and_initialize(self):
        if self.db.is_closed():
            self.db.connect()
        self.db.create_tables(MODELS, safe=True)
        print("[DatabaseManager] База данных подключена и таблицы созданы.")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # User
    def create_user(self, nickname, password, role='user'):
        return models.User.create(nickname=nickname, password=password, role=role)

    def get_user_by_nickname(self, nickname):
        return models.User.get_or_none(models.User.nickname == nickname)

    def get_user_by_id(self, user_id):
        return models.User.get_or_none(models.User.id == user_id)

    #RefreshToken
    def save_refresh_token(self, user, token, expires_at):
        return models.RefreshToken.create(user=user, token=token, expires_at=expires_at)

    def get_refresh_token(self, token):
        return models.RefreshToken.get_or_none(models.RefreshToken.token == token)

    #Food
    def add_food(self, name, category, calories, protein, fat, carbs, unit):
        return models.Food.create(
            name=name,
            category=category,
            calories=calories,
            protein=protein,
            fat=fat,
            carbs=carbs,
            unit=unit
        )

    def get_food_by_name(self, name):
        return models.Food.get_or_none(models.Food.name == name)

    #MealPlans
    def create_meal_plan(self, user, date, type, notes=''):
        return models.MealPlans.create(user=user, date=date, type=type, notes=notes)

    def get_meal_plans_for_user(self, user):
        return list(models.MealPlans.select().where(models.MealPlans.user == user))

    #MealItems
    def add_meal_item(self, meal_plan, food, quantity):
        return models.MealItems.create(meal_plan=meal_plan, food=food, quantity=quantity)

    def get_meal_items_by_plan(self, plan):
        return list(models.MealItems.select().where(models.MealItems.plan == plan))

    #UserData
    def save_user_data(self, user, height, weight, age):
        return models.UserData.create(user=user, height=height, weight=weight, age=age)

    def get_user_data(self, user):
        return models.UserData.get_or_none(models.UserData.user == user)

    #LabTest
    def add_lab_test(self, user, test_type, result, date):
        return models.LabTest.create(user=user, test_type=test_type, result=result, date=date)

    def get_lab_tests(self, user):
        return list(models.LabTest.select().where(models.LabTest.user == user))

    #Notification
    def create_notification(self, user, message, seen=False):
        return models.Notification.create(user=user, message=message, seen=seen)

    def get_unseen_notifications(self, user):
        return list(models.Notification.select().where((models.Notification.user == user) & (~models.Notification.seen)))

    #Reminders
    def create_reminder(self, user, text, datetime):
        return models.Reminders.create(user=user, text=text, datetime=datetime)

    def get_reminders(self, user):
        return list(models.Reminders.select().where(models.Reminders.user == user))

    #Pantry
    def add_to_pantry(self, user, food, quantity):
        return models.Pantry.create(user=user, food=food, quantity=quantity)

    def get_pantry(self, user):
        return list(models.Pantry.select().where(models.Pantry.user == user))

    #DietUser
    def assign_diet_to_user(self, user, diet_name):
        return models.DietUser.create(user=user, diet_name=diet_name)

    def get_user_diet(self, user):
        return models.DietUser.get_or_none(models.DietUser.user == user)

    #SupportMessages
    def send_support_message(self, user, message):
        return models.SupportMessages.create(user=user, message=message)

    def get_support_messages(self, user):
        return list(models.SupportMessages.select().where(models.SupportMessages.user == user))

    #Update / Delete: User
    def update_user_password(self, user, new_password):
        user.password = new_password
        user.save()
        return user

    def delete_user(self, user):
        return user.delete_instance()

    #RefreshToken
    def delete_refresh_token(self, token_str):
        token = self.get_refresh_token(token_str)
        if token:
            token.delete_instance()
            return True
        return False

    #Food
    def update_food(self, food, **kwargs):
        for key, value in kwargs.items():
            setattr(food, key, value)
        food.save()
        return food

    def delete_food(self, food):
        return food.delete_instance()

    #MealPlans
    def delete_meal_plan(self, plan):
        return plan.delete_instance()

    #MealItems
    def update_meal_item_quantity(self, item, new_quantity):
        item.quantity = new_quantity
        item.save()
        return item

    def delete_meal_item(self, item):
        return item.delete_instance()

    #UserData
    def update_user_data(self, user_data, **kwargs):
        for key, value in kwargs.items():
            setattr(user_data, key, value)
        user_data.save()
        return user_data

    def delete_user_data(self, user_data):
        return user_data.delete_instance()

    #LabTest
    def delete_lab_test(self, test):
        return test.delete_instance()

    #Notification
    def mark_notification_as_seen(self, notification):
        notification.seen = True
        notification.save()
        return notification

    def delete_notification(self, notification):
        return notification.delete_instance()

    #Reminders
    def update_reminder_time(self, reminder, new_datetime):
        reminder.datetime = new_datetime
        reminder.save()
        return reminder

    def delete_reminder(self, reminder):
        return reminder.delete_instance()

    #Pantry
    def update_pantry_quantity(self, pantry_entry, new_quantity):
        pantry_entry.quantity = new_quantity
        pantry_entry.save()
        return pantry_entry

    def delete_pantry_item(self, pantry_entry):
        return pantry_entry.delete_instance()

    #DietUser
    def update_user_diet(self, diet_entry, new_diet_name):
        diet_entry.diet_name = new_diet_name
        diet_entry.save()
        return diet_entry

    def delete_user_diet(self, diet_entry):
        return diet_entry.delete_instance()

    #SupportMessages
    def delete_support_message(self, message_entry):
        return message_entry.delete_instance()


#Экспорт singleton-объекта
db = DatabaseManager.get_instance()
