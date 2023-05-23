import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
username = "31qpcvf4dqxgrplnvdfitwdanrna"
Client_ID = "a5938e8f9773469cba0bd6e21017fac7"
Client_Secret = "cae8e5366c2b41aaa7e2471258abda38"

auth_manager = SpotifyOAuth(
    client_id=Client_ID,
    client_secret=Client_Secret,
    redirect_uri="http://localhost:8888/callback",
    scope="playlist-modify-private",
    show_dialog=True,
    cache_path="token.txt"
)
sp = spotipy.Spotify(auth_manager=auth_manager)
user_id = sp.current_user()["id"]

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:\n")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"
response = requests.get(URL)
billboard_web_page = response.text
soup = BeautifulSoup(billboard_web_page, "html.parser")
song_titles = [song.getText().strip() for song in soup.find_all(name="h3", class_="a-no-trucate", id="title-of-a-story")]

song_uris = []
year = date.split("-")[0]
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

play_list = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(play_list["id"], items=song_uris)

