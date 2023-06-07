from dotenv import load_dotenv
from main import SpotifyAPI
import os

load_dotenv()

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

app = SpotifyAPI(

    client_id = client_id,
    client_secret = client_secret
    
    )

app.auth()

artists_list = ['kendrick lamar', 'kanye west', 'tyler the creator', 'kali uchis', 'frank ocean']

for artist in artists_list:

    artist_id = app.get_artist_id(artist)
    albums_ids = app.get_albums(artist_id = artist_id, prefix = artist.split(' ')[0], include_groups = ["album"])

    for id_album in albums_ids:
        app.get_album_tacks(album_id = id_album[0], album_name = id_album[1], prefix = artist.split(' ')[0])