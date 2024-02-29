import os
import spotipy
import re
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# spotify cred
SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"

def authenticate():
	client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
	return sp

def fetch_tracks_from_playlist(url, sp):
	playlist_id = re.search(r'/playlist/(\w+)', url).group(1)
	results = sp.playlist_tracks(playlist_id)
	return results['items'] if 'items' in results else []

def fetch_tracks_from_album(album_url, sp):
	album_id = album_url.split('/')[-1].split('?')[0]
	results = sp.album_tracks(album_id)
	return results['items'] if 'items' in results else []

def get_tracks(url, sp):
	if re.match(r'.*spotify.com/playlist/.*', url):
		return fetch_tracks_from_playlist(url, sp)
	elif re.match(r'.*spotify.com/album/.*', url):
		return fetch_tracks_from_album(url, sp)
	else:
		raise ValueError("Invalid URL. Please enter a valid Spotify playlist or album URL.")

def spotify_query(url):
	sp = authenticate()
	queries = []
	try:
		tracks = get_tracks(url, sp)
	except ValueError as e:
		print(e)
		return
		
	for track in tracks:
		track_name = track['name']
		artist_name = track['artists'][0]['name']
		query = f"{track_name} {artist_name} official song"
		queries.append(query)

	return queries


