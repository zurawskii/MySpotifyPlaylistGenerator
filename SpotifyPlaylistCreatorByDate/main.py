import os
import dotenv
import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

dotenv.load_dotenv()


date = input("What year do you want to travel to? Type the data in this format YYYY-MM-DD: ")

SPOTIPY_CLIENT_ID = "45d86fd2467d4aed98c6dec231877372"
SPOTIPY_CLIENT_SECRET = "7d17bfb5b82d49b19a6f8e179d35b624"
MY_ID = "21ipcw7qebkkhvnemmcidsqqi"

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/").text
soup = BeautifulSoup(response, 'html.parser')

divs = soup.find_all(name="div", class_="o-chart-results-list-row-container")
titles = []

for div in divs:
    div_text = div.find(name="h3", id="title-of-a-story").string
    title = div_text.replace('\t', '').replace('\n', '')
    titles.append(title)

print(titles)

# Creating Spotipy object

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope='playlist-modify-private',
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri='http://example.com',
        show_dialog=True,
        cache_path='token.txt',
        username=MY_ID,
    )
)

user = sp.current_user()
print(user)

# Creating playlist

year = date.split("-")[0]
song_uris = []

for title in titles:
    title_search = sp.search(q=f"track:{title} year:{year}", type="track")
    try:
        song_uri = title_search['tracks']['items'][0]['uri']
        song_uris.append(song_uri)
        print(song_uri)
    except IndexError:
        print(f"{title} doesn't exist in Spotify. Skipped.")

print(song_uris)

playlist = sp.user_playlist_create(user=MY_ID, name=f"{date} Billboard 100 2.2", public=False)

sp.playlist_add_items("0Tetlb8i0oSkLuhlKIMHgk", items=song_uris, position=None)
