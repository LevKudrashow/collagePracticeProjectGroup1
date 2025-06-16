from flask import Flask
from flask_cors import CORS
from peewee import PostgresqlDatabase
import os
from dotenv import load_dotenv
from app.models import User, RefreshToken
from app.routes import register_blueprints

load_dotenv()
app = Flask(__name__)
CORS(app)

DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_HOST = os.getenv('DATABASE_HOST')

db = PostgresqlDatabase(DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT)

register_blueprints(app)
if __name__ == '__main__':
    db.connect()
    db.create_tables([User, RefreshToken], safe=True)
    app.run(debug=True)


