from flask import request
from flask_restx import Api, Namespace, Resource

import schema
from setup_db import db
from models import Genre

genre_ns = Namespace('genre')

genre_schema = schema.Genre()
genres_schema = schema.Genre(many=True)


@genre_ns.route('/')
class GenresView(Resource):
    def get_all(self):
        # получение всех жанров

        genres = db.session.query(Genre).all()

        return genres_schema.dump(genres), 200


@genre_ns.route('/<int:genre_id>')
class GenreView(Resource):
    def get_one(self, genre_id: int):
        genre = db.session.query(Genre).filter(Genre.id == genre_id).one()

        if genre is None:
            return None, 404

        return genre_schema.dump(genre), 200

