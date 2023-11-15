from bs4 import BeautifulSoup
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI')

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=SPOTIPY_REDIRECT_URI,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="26wnsohsescnlplep3vbwiojn",
    )
)

user_id = sp.current_user()["id"]
week = input(str('Which year do you want me to travel to? Type the date in this format. YYYY-MM-DD: '))

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{week}")
web_page = response.text

soup = BeautifulSoup(web_page, 'html.parser')
song_names_spans = soup.select("li ul li h3")


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
song_names = [i.getText().strip() for i in song_names_spans]

song_uris = []
year = week.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    #print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        pass

playlist = sp.user_playlist_create(user=user_id, name=f"{week} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
