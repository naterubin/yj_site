from pathlib import Path

from flask import Flask, abort, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
admin = Admin(app, name='yj', template_mode='bootstrap3')
app.secret_key = 'testtesttest'

AUDIO_DIR = 'audio'
ART_DIR = 'art'


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    track_number = db.Column(db.Integer)
    art = db.Column(db.String(500))
    audio = db.Column(db.String(500), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    album = db.relationship('Album', backref=db.backref('songs', lazy=True))

    def __repr__(self):
        return '<Song: %s. %s>' % (self.track_number, self.title)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    art = db.Column(db.String(500))

    def __repr__(self):
        return '<Album: %s>' % self.title


admin.add_view(ModelView(Song, db.session))
admin.add_view(ModelView(Album, db.session))


@app.route('/')
def index():
    try:
        album = Album.query.all()[0]
    except KeyError:
        abort(404)

    return render_template('album.html', album=album)


@app.route('/album/<int:album_id>/art.jpg')
def album_art(album_id):
    album = Album.query.filter_by(id=album_id).first()
    return send_from_directory(ART_DIR, album.art)


@app.route('/audio/<int:song_id>.mp3')
def audio_file(song_id):
    song = Song.query.filter_by(id=song_id).first()
    return send_from_directory(AUDIO_DIR, song.audio, cache_timeout=0)


@app.route('/audio/<int:song_id>.jpg')
def song_art(song_id):
    song = Song.query.filter_by(id=song_id).first()
    return send_from_directory(ART_DIR, song.art)
