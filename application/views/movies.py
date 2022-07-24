from flask import request
from flask_restx import Namespace, Resource

from application import schema
from application.setup_db import db
from application.models import Movie

movie_ns = Namespace('movie')

movie_schema = schema.Movie()
movies_schema = schema.Movie(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    # получение всех экземпляров фильмов из бд
    def get(self):
        movies_all = db.session.query(Movie)

        args = request.args

        # возвращает фильмы по director_id
        director_id = args.get('director_id')
        if director_id is not None:
            movies_all = movies_all.filter(Movie.director_id == director_id)

        # возвращает фильмы по genre_id
        genre_id = args.get('genre_id')
        if genre_id is not None:
            movies_all = movies_all.filter(Movie.genre_id == genre_id)

        # возвращает фильмы за определённый год
        year = args.get('year')
        if year is not None:
            movies_all = movies_all.filter(Movie.year == year)

        movies = movies_all.all()

        return movies_schema.dump(movies), 200

    def post(self):

        # добавление нового фильма в базу данных
        movie = movie_schema.load(request.json)
        db.session.add(Movie(**movie))
        db.session.commit()

        return None, 201


@movie_ns.route('/<int:movie_id>')
class MovieView(Resource):
    def get_one(self, movie_id: int):
        # получение одного экземпляра фильма по movie_id из бд

        movie = db.session.query(Movie).filter(Movie.id == movie_id).one()

        if movie is None:
            return None, 404

        return movie_schema.dump(movie), 200

    def put(self, movie_id: int):
        # обновляет кино по movie_id
        db.session.query(Movie).filter(Movie.id == movie_id).update(request.json)
        db.session.commit()

        return None, 204

    def delete(self, movie_id: int):
        # удаляет фильм по movie_id
        db.session.query(Movie).filter(Movie.id == movie_id).delete()

        db.session.commit()
        return None, 200
