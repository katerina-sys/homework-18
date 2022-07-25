# основной файл приложения. здесь конфигурируется фласк, сервисы, SQLAlchemy и все остальное что требуется для приложения.
# этот файл часто является точкой входа в приложение

# Пример

from flask import Flask
from flask_restx import Api
import constants
import views.directors
import views.movies
import views.genres

from models import Movie, Director, Genre
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from config import Config

from setup_db import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    #app.config.app_context(config).push()
    register_extensions(app)
    app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 2}
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(movie_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(director_ns)
    create_data(app, db)


# функция
def create_data(app, db):
    with app.app_context():
        m1 = Movie(id=1, title="Гарри Поттер и философский камень", description='text', trailer='text', year=2001,
                   rating=8.2)
        m2 = Movie(id=1, title="Гарри Поттер и тайная комната", description='text', trailer='text', year=2002,
                   rating=8.1)
        d1 = Director(id=1, name="Крис Коламбус")
        d2 = Director(id=2, name="Крис Коламбус")

        g1 = Genre(id=1, name="фэнтези")
        g2 = Genre(id=2, name="фэнтези")
        db.drop_all()
        db.create_all()
        with db.session.begin():
            db.session.add_all([m1, m2])
            db.session.add_all([d1, d2])
            db.session.add_all([g1, g2])


if __name__ == '__main__':
    app_config = Config()
    app = create_app()
    app.debug = True
    app.run(host="localhost", port=10001, debug=True)
