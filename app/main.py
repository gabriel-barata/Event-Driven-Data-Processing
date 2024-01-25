from packages.spotify import SpotifyAPI
from packages.config import render_config

config = render_config()


if __name__ == '__main__':

    app = SpotifyAPI(
        client_id=config.SPOTIFY_CLIENT_ID,
        client_secret=config.SPOTIFY_CLIENT_SECRET,
        bucket_name=config.BUCKET_NAME
        )

    for artist in config.ARTIST_LIST:

        artist_id = app.retrieve_artist_id(artist)

        albums_ids = app.retrieve_artist_albums(
            artist_id=artist_id,
            prefix=artist.split(' ')[0],
            include_groups=["album"],
            bucket_name=config.BUCKET_NAME
        )

        for id_album in albums_ids:
            app.get_album_tacks(
                album_id=id_album[0],
                album_name=id_album[1],
                prefix=artist.split(' ')[0],
                bucket_name=config.BUCKET_NAME
                )
