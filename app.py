#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_wtf import FlaskForm
from forms import *
import collections
collections.Callable = collections.abc.Callable
from flask_migrate import Migrate
import psycopg2
import sys
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime
import re
from operator import itemgetter
#from flask_wtf import CsrfProtect



#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

connection = psycopg2.connect('dbname=henry user=postgres password=0')
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venues', lazy=True)
    past_shows_count = db.Column(db.Integer)
    upcoming_shows_count = db.Column(db.Integer)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy=True)
    #seeking_venue = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def add(self):
      db.session.add(self)
      db.session.commit()

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=True)
    artist_name = db.Column(db.String(120), nullable=True)
    artist_image_link = db.Column(db.String(500))
def __repr__(self):
  return f'<Show {self.id}, Artist {self.artist_id}, Venue {self.venue.id}>'
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):

  #date = dateutil.parser.parse(value)
  if isinstance(value, str):
    date = dateutil.parser.parse(value)
  else:
      date = value
  #if format == 'full':
      #format="EEEE MMMM, d, y 'at' h:mma"
  #elif format == 'medium':
      #format="EE MM, dd, y h:mma"
  #return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  venues = Venue.query.all()
  for venue in venues:
    data.append({
      "city" : venue.city ,
      "state" : venue.state ,
      "venues" : [{
      "id" : venue.id,
      "name" : venue.name,
      "genres" : venue.genres,
      "website link" : venue.website_link,
      "website" : venue.website,
      "seeking_talent" : venue.seeking_talent,
      "seeking_description" : venue.seeking_description,
      "image_link" : venue.image_link
      #"past_shows_count" : venue.past_shows_count,
     #"upcoming_shows_count" : venue.upcoming_shows_count
      }]
    })
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  
  # seach for Hop should return "The Musical Hop".
  search_term = request.form.get('search_term', '')
  data = Venue.query.filter(Venue.name.ilike('%{}%'.format(search_term))).all()
  count = []
  for outcome in data:
    count.append({
      "id":outcome.id,
      "name": outcome.name,
      "num_upcoming_shows": len(db.session.query(Show).filter(Show.venue_id == outcome.id).filter(Show.start_time > datetime.now()).all())
    })
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response = {
    "count":len(data),
    "data": count
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  venue = Venue.query.get(venue_id)
  # TODO: replace with real venue data from the venues table, using venue_id

  data={
      "id": venue.id,
      "name": venue.name,
      "genres": venue.genres,
      "address": venue.address,
      "city": venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "website": venue.website,
      "facebook_link": venue.facebook_link,
      "seeking_talent": True if venue.seeking_talent in (True, 't', 'True') else False,
      "seeking_description": venue.seeking_description,
      "image_link": venue.image_link if venue.image_link else "",
      "past_shows_count": venue.past_shows_count,
      "upcoming_shows_count": venue.upcoming_shows_count,
  }
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  #setattr(object, name, value)
  # TODO: modify data to be the data object returned from db insertion
  venue = Venue()
  for field in request.form:
    if field == 'genres':
      setattr(venue, field, request.form.getlist(field))
    elif field == 'seeking_talent':
      setattr(venue, field, True if request.form.get(field) in ('y', True, 't', 'True') else False)
    else:
      setattr(venue, field, request.form.get(field))

  try:
    db.session.add(venue)
    db.session.commit()
  # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  venue = Venue.query.get(venue_id)
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    db.session.delete(venue)
    db.session.commit()
    print('Venue' + venue.name + 'was successfully deleted!')
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  #artists = db.session.query(Artist.id).all() 

  data = []
  artists = Artist.query.all()
  for artist in artists:
      data.append({
          "id": artist.id,
          "name": artist.name
      })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  search_term = request.form.get('search_term', '').strip()
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  data = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all() 
  count = []
  for outcome in data:
    count.append({
      "id":outcome.id,
      "name": outcome.name,
      "num_upcoming_shows": len(db.session.query(Show).filter(Show.venue_id == outcome.id).filter(Show.start_time > datetime.now()).all())
    })
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response = {
    "count":len(data),
    "data": count
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.get(artist_id)   # Returns object by primary key, or None
  
  data = {
      "id": artist.id,
      "name": artist.name,
      "genres": artist.genres.split(','),
      "city": artist.city,
      "state": artist.state,
      "phone": artist.phone,
      "facebook_link": artist.facebook_link,
      "seeking_description": artist.seeking_description,
      "image_link": artist.image_link,
      "upcoming_shows": '1',
      "past_shows": '2'
    }
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  if artist: 
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres
    form.facebook_link.data = artist.facebook_link
    form.image_link.data = artist.image_link
    form.seeking_description.data = artist.seeking_description
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form)
  if form.validate():
    try:
      artist = Artist.query.filter(Artist.id==artist_id).first()
      artist.name = request.form['name']
      artist.genres = request.form['genres']

      artist.city = request.form['city']
      artist.state = request.form['state']
      artist.phone = request.form['phone']
      artist.facebook_link = request.form['facebook_link']
      artist.image_link = request.form['image_link']
      db.session.commit()
      flash('Artist....')
    except:
      flash('sorry...')
      db.session.rollback()
    finally:
      db.session.close()
  else:
    flash('Artist ' + request.form['name'] + 'could not be updated')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm()
  if venue: 
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.address.data = venue.address
    form.genres.data = venue.genres
    form.facebook_link.data = venue.facebook_link
    form.image_link.data = venue.image_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  form = VenueForm(request.form)
  try:
      venue = Venue.query.filter_by(id=venue_id)
      venue.name = form.name.data,
      venue.genres = form.genres.data,
      venue.city = form.city.data,
      venue.state = form.state.data,
      venue.phone = form.phone.data,
      venue.facebook_link = form.facebook_link.data,
      venue.image_link = form.image_link.data,
      venue.seeking_description = form.seeking_description.data

      db.session.add(venue)
      db.session.commit()
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully updated!')
  except:
      error: True
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Venue ' +
        request.form['name'] + ' could not be updated.') 
  #venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
 # called upon submitting the new artist listing form
  artist_form = ArtistForm(request.form)
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
      new_artist = Artist(
          name=artist_form.name.data,
          genres=','.join(artist_form.genres.data),
          #address=artist_form.address.data,
          city=artist_form.city.data,
          state=artist_form.state.data,
          phone=artist_form.phone.data,
          facebook_link=artist_form.facebook_link.data,
          image_link=artist_form.image_link.data)

      new_artist.add()
        # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Artist ' +
            request.form['name'] + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
 
  data=[]
  shows = Show.query.all()
  for show in shows:
    
      data.append({
        "artist_id": Show.artist_id,
        "venue_id": Show.venue_id,
        "start_time": Show.start_time,
        "artist_image_link": Show.artist_image_link
    })
    
  #form = ShowForm()
  return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
 
  try:
    form = ShowForm()

    artist_id = int(form.artist_id.data)
    venue_id = int(form.venue_id.data)
    start_time = str(form.start_time.data)
    #date = format_datetime(start_time, 'full')

    nshow = Show(artist_id=artist_id, venue_id=venue_id) #date=date)
     
    db.session.add(nshow)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
      
            # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
  #else:
      #print(form.errors)
     # flash("An error occurred. the provided IDs don't exist, Show could not be listed.")

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
