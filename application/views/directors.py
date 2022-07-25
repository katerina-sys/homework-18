from flask import request
from flask_restx import Api, Namespace, Resource
from setup_db import db
from models import Director
import schema

director_ns = Namespace('director')

director_schema = schema.Director()
directors_schema = schema.Director(many=True)


@director_ns.route('/')
class DirectorsView(Resource):
    def get_all(self):
        directors = db.session.query(Director).all()

        return directors_schema.dump(directors), 200


@director_ns.route('/<int:director_id>')
class DirectorView(Resource):
    def get_one(self, director_id):
        # получение одного режиссера по director_id
        director = db.session.query(Director).filter(Director.id == director_id).one()

        if director is None:
            return None, 404

        return director_schema.dump(director), 200
