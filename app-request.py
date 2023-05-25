from dotenv import load_dotenv
from main import SpotifyAPI
import os

load_dotenv()

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

app = SpotifyAPI(client_id = client_id,
                 client_secret = client_secret)
app.auth()
kendrick_id = app.get_artist_id('kendrick lamar')
kendrick_albums = app.get_albums(artist_id = kendrick_id)