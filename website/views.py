from flask import Blueprint, render_template, request

# import mongo
from website import mongo


# import the database queries
import website.queries as dbq


views = Blueprint('views', __name__)

# Fan routes

@views.route('/')
def home():

    # load ten artists, ten tracks, and ten shows from the database
    db_artists = dbq.get_ten_artists()
    db_tracks = dbq.get_ten_tracks()
    db_shows = dbq.get_ten_shows()
    return render_template("index.html", artists = db_artists, tracks=db_tracks, shows=db_shows)

@views.route('/fans-signup')
def fan_signup():
    return render_template('signup.html')

@views.route('/fans-home')
def fan_home():
    # load ten artists, ten tracks, and ten shows from the database
    db_artists = dbq.get_ten_artists()
    db_tracks = dbq.get_ten_tracks()
    db_shows = dbq.get_ten_shows()
    return render_template("fans_home.html", artists = db_artists, tracks=db_tracks, shows=db_shows)

@views.route('/fan-dashboard')
def fan_dashboard():
    return render_template('fan_dashboard.html')

@views.route('/landing')
def landing_page():
    return render_template('landing_page.html')

@views.route('/artists')
def artists():
    db_artists = dbq.get_artists()
    return render_template('artists.html', artists= db_artists)

@views.route('/shows')
def shows():
    db_shows = dbq.get_shows()
    return render_template('shows.html', shows = db_shows)

# Artist routes

@views.route('/artist-home')
def artist_home():
    return render_template("artist_home.html")

@views.route('/add-tracks')
def add_tracks():
    return render_template("new_track.html")

@views.route('/edit-tracks')
def edit_tracks():

    # load some tracks to edit
    tracks_to_edit = dbq.get_ten_tracks()

    return render_template("edit_track.html", tracks=tracks_to_edit)

@views.route('/edit-tracks', methods = ['POST'])
def add_track_form():
    print(request.files)
    if 'track_artwork' in request.files:
        track_artwork = request.files['track_artwork']
        mongo.save_file(track_artwork.filename, track_artwork)
        artwork = track_artwork.filename
    else:
        artwork = ""

    artist = 'none'
    name = request.form['track-name']
    description = request.form['track-description']
    genre = request.form['track-genre']
    audio = True
    pricing = request.form['pricing']
    date = request.form['track-date']
    credit = request.form['track-credits']
    privacy = True

    new_track = dbq.add_track(artist, name, description, genre, audio, artwork, pricing, date, credit, privacy)
    tracks_to_edit = dbq.get_tracks()
    return render_template('edit_track.html', tracks=tracks_to_edit)


@views.route('/add-shows')
def add_shows():
    return render_template("new_show.html")

@views.route('/edit-shows')
def edit_shows():

    shows_to_edit = dbq.get_ten_shows()
    return render_template('edit_show.html', shows=shows_to_edit)

@views.route('/edit-shows', methods = ['POST'])
def add_show_form():
    artist = "none"
    name = request.form['show-name']
    description = request.form['show-description']
    genre = request.form['show-genre']
    link = request.form['show-link']
    date = request.form['show-date']
    time = request.form['show-time']
    pricing = request.form['pricing']

    new_show = dbq.add_show(date, time, name, artist, description, link)
    shows_to_edit = dbq.get_shows()
    
    return render_template('edit_show.html', shows=shows_to_edit)



@views.route('/view-tracks')
def view_tracks():
    return render_template("view_tracks.html")


# just a place for Asa to work on troubleshooting uploading to mongodb
@views.route('/upload-test')
def upload_audio():
    return render_template("upload_test.html")

# place for uploading an actual file
@views.route('/create', methods=['POST'])
def create():
    if 'album_cover' in request.files:
        album_cover = request.files['album_cover']
        album_name = request.form.get('album_name')
        dbq.save_to_db(file=album_cover, name=album_name)

    return render_template("upload_test.html")



