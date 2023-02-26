from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv
import os


load_dotenv()
# access the variables
client_id = os.getenv('spotipy.client_id')
client_secret = os.getenv('spotipy.client_secret')
redirect_uri = os.getenv('spotipy.redirect_uri')


class SpotifyAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global redirect_url
        redirect_url = self.path
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Authentication successful! You may now close this tab.')


def set_up_spotify_API_credentials():
    # Set up Spotify API credentials
    scope = "user-read-private user-read-email user-read-playback-state user-modify-playback-state streaming"

    # Create an instance of the SpotifyOAuth class
    sp_oauth = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_uri,
                            scope=scope)

    # Get the authorization URL
    auth_url = sp_oauth.get_authorize_url()

    # Open the authorization URL in a web browser
    webbrowser.open(auth_url)

    # Start a local web server to capture the redirect URL
    # npx kill - port 8888
    server_address = ('localhost', 8888)
    httpd = HTTPServer(server_address, SpotifyAuthHandler)
    httpd.handle_request()

    # Exchange the authorization code for an access token
    code = sp_oauth.parse_response_code(redirect_url)
    access_token = sp_oauth.get_access_token(code)

    # Create a new instance of the Spotify class with the access token
    sp = spotipy.Spotify(auth=access_token)

    return sp


class MusicPlayer():
    def __init__(self):
        self.sp = None
        self.is_playing = False
        self.device_id = "63f8783f779d3fe9bd9c0d4c7ef5740801b13263"

    def login(self):
        client_id = "7310455274a04f019b6548300ae048ab"
        client_secret = "1126cdca36e54ef48c1ad18688fae77b"
        client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        sp.trace = False
        return sp

    def get_device_id(self):
        devices = self.sp.devices()
        device_id = None
        for d in devices["devices"]:
            if d["is_active"]:
                device_id = d["id"]
                break
        if device_id:
            print("device_id", device_id)
            return device_id
        else:
            print("No active devices found.")

    def get_sp(self):
        try:
            sp = self.login()
            self.get_device_id()
        except:
            sp = set_up_spotify_API_credentials()
            sp = self.login()
        self.sp = sp
        return sp

    def run(self, song_name):
        self.get_sp()
        print()
        print("try to play: ", song_name)
        song_uri = self.search_song(self.sp, song_name)
        print("song_uri: ", song_uri)
        self.play_album(self.sp, song_uri, self.device_id)
        self.is_playing = True

    def stop(self):
        self.get_sp()
        self.sp.pause_playback(device_id=self.device_id)

        self.is_playing = False

    def next_track(self):
        self.get_sp()
        self.sp.next_track(device_id=self.device_id)

    def play_song(self, sp, song_uri, device_id):
        sp.transfer_playback(device_id)
        sp.pause_playback(device_id=device_id)

        track = sp.track(song_uri)
        track_uri = track['uri']
        sp.start_playback(uris=[track_uri], device_id=device_id)

    def play_album(self, sp, song_uri, device_id):
        track = sp.track(song_uri)
        album_uri = track['album']['uri']
        sp.transfer_playback(device_id)
        sp.pause_playback(device_id=device_id)
        sp.start_playback(device_id=device_id, context_uri=album_uri)

    def search_song(self, sp, song_name):
        results = sp.search(q=song_name, type='track')
        items = results['tracks']['items']

        # Check if any songs were found
        if len(items) == 0:
            print("No songs found.")
            # exit()

        # Play the first song in the search results
        song = items[0]
        song_uri = song['uri']
        return song_uri

