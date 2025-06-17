from flask import Flask
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
import os
from app.routes import register_blueprints
from init_db import db  #Singleton - одна точка входа для взаимодействия с базой данных
# задача разработчиков лишь в том, что бы обращаться к методам класса
#без pip install psycopg2-binary работать не будет
load_dotenv()
app = Flask(__name__)
CORS(app)

#ниже представлен пример как можно записывать данные из бек-энд части в базу данных
#Тестовая запись в базу данных(это всего лишь пример для разработчиков)
if __name__ == '__main__':
    #всё уже настроено, просто используй методы из init_db по этому принципу -
    user = db.create_user(nickname='testuser222', password='secret1233')
    food = db.add_food(
        name='гречка',
        category='крупы',
        calories=343,
        protein=13,
        fat=3,
        carbs=72,
        unit='г'
    )
    # Пример - создание плана питания (например, завтрак)
    plan = db.create_meal_plan(user=user, date=datetime.now().date(), type='завтрак')
    # Пример - добавление продукта в план питания с указанием количества
    db.add_meal_item(meal_plan=plan, food=food, quantity=100)


    print("Добавлено:")
    print(f"Пользователь: {user.nickname}")
    print(f"Еда: {food.name}")
    print(f"План питания: {plan.type}")

register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=False)
