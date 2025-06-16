import os
import sys
import locale
from dotenv import load_dotenv
from peewee import PostgresqlDatabase


print(f"Python encoding: {sys.getdefaultencoding()}")
print(f"Preferred encoding: {locale.getpreferredencoding()}")


try:
    from app.models import User, RefreshToken
except ImportError as e:
    print("Ошибка импорта моделей:", e)
    sys.exit(1)

load_dotenv()

DATABASE_NAME = os.getenv('DATABASE_NAME', '').strip()
DATABASE_USER = os.getenv('DATABASE_USER', '').strip()
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '').strip()
DATABASE_HOST = os.getenv('DATABASE_HOST', '').strip()
DATABASE_PORT_RAW = os.getenv('DATABASE_PORT', '5432').strip()

try:
    DATABASE_PORT = int(DATABASE_PORT_RAW)
except ValueError:
    print(f"Неверный порт: '{DATABASE_PORT_RAW}'")
    sys.exit(1)


DATABASE_PASSWORD = DATABASE_PASSWORD.encode('utf-8', errors='ignore').decode('utf-8')

db = PostgresqlDatabase(
    DATABASE_NAME,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    options=''
)

print(f"Попытка подключения к {DATABASE_HOST}:{DATABASE_PORT}")
print("DATABASE_PASSWORD bytes:", list(DATABASE_PASSWORD.encode('utf-8')))

def init():
    try:
        if db.is_closed():
            db.connect()
        else:
            print("Соединение с БД открыто, используем существующее")
        db.create_tables([User, RefreshToken], safe=True)
        print("Таблицы успешно созданы")
    except Exception as e:
        print("Ошибка подключения к БД:", e)
    finally:
        if not db.is_closed():
            db.close()

if __name__ == '__main__':
    init()
