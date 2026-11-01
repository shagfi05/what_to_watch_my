import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 1. СОЗДАЁМ ОБЪЕКТ db СРАЗУ. 
# Он пока пустой, но он уже существует в памяти пакета.
db = SQLAlchemy()

# 2. ТЕПЕРЬ МОЖНО ИМПОРТИРОВАТЬ МОДЕЛИ И VIEWS.
# Они увидят этот db, потому что мы его уже создали выше.
from .views import bp
from .models import Opinion  # <-- Теперь эта строка сработает!
# Если у тебя есть forms.py, раскомментируй следующую строку, если нет - оставь как есть
# from .forms import OpinionForm 

def create_app(config_name=None):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_folder = os.path.join(base_dir, 'templates')
    
    app = Flask(__name__, template_folder=template_folder)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'MY SECRET KEY'
    
    # 3. ПРИВЯЗЫВАЕМ db К КОНКРЕТНОМУ ЭКЗЕМПЛЯРУ ПРИЛОЖЕНИЯ
    db.init_app(app)
    @app.cli.command('create_db')
    def create_db_command():
        """Создаёт таблицы в базе данных."""
        db.create_all()
        print('База данных успешно создана!')
    # 4. РЕГИСТРИРУЕМ МАРШРУТЫ
    app.register_blueprint(bp)
    
    return app