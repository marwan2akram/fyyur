# from flask import Flask
# from flask_moment import Moment
# from flask_sqlalchemy import SQLAlchemy
# from forms import *
# from flask_migrate import Migrate
# #----------------------------------------------------------------------------#
# # App Config.
# #----------------------------------------------------------------------------#
#
# app = Flask(__name__)
# moment = Moment(app)
# app.config.from_object('config')
# db = SQLAlchemy(app)
#
# # TODO: connect to a local postgresql database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbuser:123321@localhost:5432/mydb'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# migrate = Migrate(app, db)
# #-----------------------------------
#
# class Venue(db.Model):
#     __tablename__ = 'venues'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     address = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     genres = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))
#     website = db.Column(db.String(500))
#     seeking_talent = db.Column(db.Boolean)
#     seeking_description = db.Column(db.String(500))
#     # shows = db.relationship('Show', backref='venue', lazy=True)
#     # TODO: implement any missing fields, as a database migration using Flask-Migrate
#
#
# class Artist(db.Model):
#     __tablename__ = 'artists'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     genres = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))
#     website = db.Column(db.String(500))
#     seek_venue = db.Column(db.String(500))
#     # Venue = db.relationship('Venue', secondary='artist_shows', backref=db.backref('artists', lazy=True))
#     # shows = db.relationship('Show', backref='Artist', lazy=True)
#
#     # TODO: implement any missing fields, as a database migration using Flask-Migrate
#
# # TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
# # Artist_Shows = db.Table('artist_shows',
# #     db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True),
# #     db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'), primary_key=True),
# #     db.Column('show_date', db.DateTime(timezone=False),default=datetime.utcnow,  primary_key=True))
#
# class Show(db.Model):
#     __tablename__ = 'shows'
#     id = db.Column(db.Integer, primary_key=True)
#     artists_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
#     venues_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
#     start_time=db.Column(db.DateTime(timezone=False))
# #----------------------------------------------------------------------------#