from flask_sqlalchemy import SQLAlchemy
from flask_serialize import FlaskSerializeMixin

db = SQLAlchemy()

FlaskSerializeMixin.db = db


class Survey(FlaskSerializeMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    observations = db.relationship('Observation', backref='survey', lazy=True, cascade="all, delete-orphan")

    create_fields = update_fields = ['name']

    def __repr__(self):
        return '<Survey %r %r>' % (self.id, self.name)


class Observation(FlaskSerializeMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)

    create_fields = update_fields = ['frequency', 'value']

    def __repr__(self):
        return '<Observation %r %r %r %r>' % (self.id, self.survey_id, self.value, self.frequency)
