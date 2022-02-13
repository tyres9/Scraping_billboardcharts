from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                              redirect_uri="http://example.com",
                              client_id= CLIENT_ID,
                              client_secret= CLIENT_SECRET,
                              show_dialog=True,
                              cache_path="token.txt"
                              ))
user_id = sp.current_user()['id']
choice_date = input("Which year do you want to travel to? Type the date in this format.YYYY-MM-DD : ")
req = requests.get(f'https://www.billboard.com/charts/hot-100/{choice_date}/')
site_html = req.text
soup = BeautifulSoup(site_html, 'html.parser')
songs = soup.select(selector="li h3", id="title-of-a-story")
song_uris = []
year = choice_date.split("-")[0]
for song in songs[:100]:
    title = song.getText()
    result = sp.search(q=f'track:{title} year:{year}', type='track')
    try:
        uri = result['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"{title} doesn't exist in Spotify. Skipped")

#create a private playlist name the date
user_playlist = sp.user_playlist_create(user=user_id,
                                        name='{choice_date} Billboard 100',
                                        public=False,
                                        description='Top 100 Songs ')
#add items in the playlist
sp.playlist_add_items(playlist_id=user_playlist["id"], items=song_uris)
