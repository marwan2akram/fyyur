#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
# from models import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbuser:123321@localhost:5432/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
class Venue(db.Model):
  __tablename__ = 'venues'
  # implemnt the missing fields
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website = db.Column(db.String(500))
  seeking_talent = db.Column(db.Boolean)
  seeking_description = db.Column(db.String(500))
  shows = db.relationship('Show', backref='Venue', lazy=True)

  # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
  __tablename__ = 'artists'
  # implemnt the missing fields
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website = db.Column(db.String(500))
  seek_venue = db.Column(db.String(500))
  seeking_description = db.Column(db.String(500))
  shows = db.relationship('Show', backref='Artist', lazy=True)

  # TODO: implement any missing fields, as a database migration using Flask-Migrate


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
# implemnt the show model Which has a relationship that connects Artists and Venues
class Show(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer, primary_key=True)
  artists_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
  venues_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
  start_time = db.Column(db.DateTime(timezone=False))
  upcoming_shows = db.Column(db.Boolean, default=True)
#----------------------------------------------------------------------------#

# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
#A user can view a Venue Page with venue information from the database.
@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  city_state = Venue.query.with_entities(Venue.city, Venue.state).distinct().all()
  for one_city_state in city_state:
    venues = Venue.query.filter_by(city=one_city_state.city, state=one_city_state.state).all()
    values = []
    for venue in venues:
      values.append({'id': venue.id, 'name': venue.name})
    # build final returned data using venues,
    data.append({'city': one_city_state.city, 'state': one_city_state.state, "venues": values})
  return render_template('pages/venues.html', areas=data);

#A user can successfully execute a Search that queries the database.
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')

  results = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()

  response = {
    "count": len(results),
    "data": []
  }
  for venue in results:
    response["data"].append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": Show.query.filter_by(venues_id=venue.id, upcoming_shows=True).count()
    })
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.filter_by(id=venue_id).first()
  start_time=""
  start_show_time = Show.query.filter_by(venues_id=venue_id, upcoming_shows=False).all()
  for start_time in start_show_time:
    start_time=str(start_time.start_time)
  data1={
    "id": venue.id,
    "name": venue.name,
    "genres": [venue.genres],
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": [{
      "artist_id": [x.id for x in Show.query.filter_by(venues_id=venue_id, upcoming_shows=False).all()],
      "artist_name": [x.Artist.name for x in Show.query.filter_by(venues_id=venue_id, upcoming_shows=False).all()],
      "artist_image_link": [x.Artist.image_link for x in Show.query.filter_by(venues_id=venue_id, upcoming_shows=False).all()],
      "start_time": start_time,
    }],
    "upcoming_shows": [],
    "past_shows_count": Show.query.filter_by(venues_id=venue_id,upcoming_shows=False).count(),
    "upcoming_shows_count": Show.query.filter_by(venues_id=venue_id,upcoming_shows=True).count(),
  }

  data = list(filter(lambda d: d['id'] == venue_id, [data1]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

#A user can create new venue.
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  name= request.form.get("name", "")
  city= request.form.get("city","")
  state= request.form.get("state", "")
  address= request.form.get("address","")
  phone= request.form.get("phone","")
  genres= request.form.get("genres","")
  facebook_link= request.form.get("facebook_link","")
  error = False
  try:
    venue = Venue(
      name=name, city=city, state=state, address=address, phone=phone, genres=genres,
                  facebook_link=facebook_link
    )
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error :
  # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' didnot  listed!')
    abort(500)
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

#Implement a button to delete a Venue
@app.route('/venues/delete/<venue_id>')
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue_to_delete = Venue.query.get_or_404(venue_id)
    db.session.delete(venue_to_delete)
    db.session.commit()

  except:
    db.session.rollback()

  finally:
    db.session.close()
    return redirect('/venues')
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  # return redirect(url_for("venues"))

#  Artists
#  ----------------------------------------------------------------
#A user can view a artists Page with  artists information from the database.
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  data=Artist.query.all()
  return render_template('pages/artists.html', artists=data)


#A user can successfully execute a Search that queries the database.
@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')

  results = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()

  response = {
    "count": len(results),
    "data": []
  }
  for artist in results:
    response["data"].append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": Show.query.filter_by(artists_id=artist.id, upcoming_shows=True).count()
    })
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.filter_by(id=artist_id).first()
  start_time=""
  start_show_time = Show.query.filter_by(artists_id=artist_id, upcoming_shows=False).all()
  for start_time in start_show_time:
    start_time=str(start_time.start_time)
  data1={
    "id": artist.id,
    "name": artist.name,
    "genres": [artist.genres],
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seek_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": [{
      "venue_id": [x.Venue.id for x in Show.query.filter_by(artists_id=artist_id,upcoming_shows=False).all()],
      "venue_name": [x.Venue.name for x in Show.query.filter_by(artists_id=artist_id,upcoming_shows=False).all()],
      "venue_image_link":[x.Venue.image_link for x in Show.query.filter_by(artists_id=artist_id,upcoming_shows=False).all()],
      "start_time": start_time
    }],
    "upcoming_shows": [],
    "past_shows_count": Show.query.filter_by(artists_id=artist.id, upcoming_shows=False).count(),
    "upcoming_shows_count": Show.query.filter_by(artists_id=artist.id, upcoming_shows=True).count(),
  }
  data = list(filter(lambda d: d['id'] == artist_id, [data1]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = request.args.get(artist_id)
  the_artist = Artist.query.get(artist)

  artist = {
    "id": the_artist.id,
    "name": the_artist.name,
    "genres": the_artist.genres.split(','),
    "city": the_artist.city,
    "state": the_artist.state,
    "phone": the_artist.phone,
    "website": the_artist.website,
    "facebook_link": the_artist.facebook_link,
    "seeking_venue": the_artist.seeking_venue,
    "seeking_description": the_artist.seeking_description,
    "image_link": the_artist.image_link
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

#a user can successfully edit and update the artisit data and save it in the database.
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']
  facebook_link = request.form['facebook_link']
  genres = request.form['genres']
  image_link = request.form['image_link']
  website = request.form['website']

  try:
    db.session.commit()
    flash(" updated {}".format(name))
  except:
    db.session.rollback()
    flash("Faild to updated {}".format(name))
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = request.args.get(venue_id)
  the_venue = Artist.query.get(venue)
  venue={
    "id": the_venue.id,
    "name": the_venue.name,
    "genres": the_venue.genres.split(','),
    "city": the_venue.city,
    "state": the_venue.state,
    "phone": the_venue.phone,
    "website": the_venue.website,
    "facebook_link": the_venue.facebook_link,
    "seeking_talent": the_venue.seeking_talent,
    "seeking_description": the_venue.seeking_description,
    "image_link": the_venue.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

#a user can successfully edit and update the venues data and save it in the database.
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

#a user can successfully create artisit data.
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  name = request.form.get("name", "")
  city = request.form.get("city", "")
  state = request.form.get("state", "")
  address = request.form.get("address", "")
  phone = request.form.get("phone", "")
  genres = request.form.get("genres", "")
  facebook_link = request.form.get("facebook_link", "")
  error = False
  try:
    artist = Artist(
      name=name, city=city, state=state, phone=phone, genres=genres,
      facebook_link=facebook_link
    )
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    abort(500)
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------
  #change static fake data
  #to display shows instead reading from database.
@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  show=Show.query.all()
  for one_show in show:
    data1={
      "venue_id": one_show.Venue.id ,
      "venue_name":one_show.Venue.name,
      "artist_id": one_show.Artist.id,
      "artist_name": one_show.Artist.name,
      "artist_image_link":one_show.Artist.image_link,
      "start_time": str(one_show.start_time)
    }
    data.append(data1)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


#A user can create new show listing via the New show Page.
@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  #change static fake data
  #to display shows instead reading from a proper model that represents data stored in database.
  artist_id = request.form.get("artist_id", "")
  venue_id = request.form.get("venue_id", "")
  start_time = request.form.get("start_time", "")
  error =False
  try:
    show = Show(
      artists_id=artist_id,
      venues_id=venue_id,
      start_time=start_time
    )
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    # on successful db insert, flash success
    flash('Show was not successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
