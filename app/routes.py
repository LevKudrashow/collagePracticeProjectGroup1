from flask import request, jsonify
from passlib.hash import pbkdf2_sha256 as hash_handler
import jwt
from datetime import datetime, timedelta
from app.models import User, RefreshToken #from models import User, RefreshToken
import os

SECRET_KEY = os.getenv('SECRET_KEY')


def generate_tokens(user_id):
    access_token = jwt.encode(
        {'user_id': user_id, 'exp': datetime.utcnow() + timedelta(days=1)},
        SECRET_KEY,
        algorithm='HS256'
    )
    refresh_token = jwt.encode(
        {'user_id': user_id, 'exp': datetime.utcnow() + timedelta(days=7)},
        SECRET_KEY,
        algorithm='HS256'
    )
    return access_token, refresh_token


def register_blueprints(app):
    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        nickname = data.get('nickname')
        password = data.get('password')
        if User.get_or_none(User.nickname == nickname):
            return jsonify({"error": "Nickname already taken!"}), 400
        hashed_password = hash_handler.hash(password)
        user = User.create(nickname=nickname, password=hashed_password)

        access_token, refresh_token = generate_tokens(user.id)
        # Сохраняем refresh токен в БД
        RefreshToken.create(user=user, token=refresh_token, expires_at=datetime.now() + datetime.timedelta(days=7))
        return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        nickname = data.get('nickname')
        password = data.get('password')
        user = User.get_or_none(User.nickname == nickname)
        if user and hash_handler.verify(password, user.password):
            access_token, refresh_token = generate_tokens(user.id)
            # Сохраняем refresh токен в БД (или обновляем)
            RefreshToken.create(user=user, token=refresh_token, expires_at=datetime.now() + timedelta(days=7))
            return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200
        return jsonify({"error": "Invalid credentials!"}), 401

    @app.route('/token/refresh', methods=['POST'])
    def refresh_token():
        data = request.json
        refresh_token = data.get('refresh_token')
        try:
            # Декодируем refresh токен
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            # Проверяем наличие refresh токена в БД и его истечение
            token_entry = RefreshToken.get_or_none(RefreshToken.token == refresh_token)
            if token_entry and token_entry.expires_at > datetime.now():
                # Генерируем новые токены
                access_token, new_refresh_token = generate_tokens(user_id)
                # Обновляем refresh токен в БД
                token_entry.token = new_refresh_token
                token_entry.expires_at = datetime.now() + timedelta(days=7)
                token_entry.save()
                return jsonify({"access_token": access_token, "refresh_token": new_refresh_token}), 200
            return jsonify({"error": "Invalid or expired refresh token!"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Refresh token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401