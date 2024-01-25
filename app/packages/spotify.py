import requests
import boto3

import json
import os
import re


class SpotifyAPI:

    def __init__(self, client_id, client_secret, bucket_name):

        self.client_id = client_id
        self.client_secret = client_secret
        self.bucket_name = bucket_name

        self.__create_dirs()

        self._auth()

    @staticmethod
    def __create_dirs():

        folders = ['albums', 'tracks']
        for folder in folders:
            path = os.path.join('data', folder)

            if not os.path.exists(path):
                os.makedirs(path)

    def _auth(self):

        """
        This function returns the access_token that will
        be used on further requests
        """

        endpoint = 'https://accounts.spotify.com/api/token'

        headers = {

            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {

            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        response = requests.post(endpoint, headers=headers, params=data)

        if response.status_code == 200:
            access_token = json.loads(response.content)["access_token"]
            token_type = json.loads(response.content)["token_type"]

            self.base_header = {
                'Authorization': f'{token_type} {access_token}'
                }

        else:
            print(f"-error during auth on spotify : {response.status_code}")

    def retrieve_artist_id(
        self,
        query: str,
        endpoint: str
    ) -> int:

        """
        This method returns an artist id given its name
        """

        params = {
            "q": query.capitalize(),
            "type": "artist",
            "limit": 1
            }

        response = requests.get(
            url=endpoint,
            headers=self.base_header,
            params=params)

        data = json.loads(response.content)
        artist_id = data["artists"]["items"][0]["id"]

        return artist_id

    def retrieve_artist_albums(
        self,
        artist_id: str,
        prefix: str,
        limit: int = 30,
        include_groups: list() = ['album', 'single']
    ) -> list[str]:

        """
        This function returns the artists album given its id
        """

        s3 = boto3.resource('s3')

        include_groups = ','.join(include_groups)

        endpoint = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
        params = {

            'include_groups': include_groups,
            'limit': limit

        }

        response = requests.get(
            endpoint,
            headers=self.base_header,
            params=params)

        json_data = json.loads(response.content)["items"]
        albums_ids = [(album["id"], album["name"]) for album in json_data]

        file_name = os.path.join(
            'data', 'albums', f'{prefix}-albums.json'
            )

        with open(file_name, 'w') as file:
            json.dump(json_data, file, indent=4)

        s3.Bucket(self.bucket_name).upload_file(
            file_name,
            prefix + '-albums.json'
            )

        return albums_ids

    def get_album_tacks(
        self,
        album_id: str,
        album_name: str,
        prefix: str,
        limit: int = 30,
        market: str = "BR"
    ) -> bool:

        """
        This function returns all tracks in a given album
        """

        s3 = boto3.resource('s3')

        album_name = '-'.join(re.sub(
            r'[^\w\s]', '', album_name).lower().split(' '))

        if not os.path.exists('data/tracks/' + album_name):
            os.makedirs('data/tracks/' + album_name)

        endpoint = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
        params = {
            'limit': limit,
            'market': market
        }

        response = requests.get(
            endpoint,
            headers=self.base_header,
            params=params)
        json_data = json.loads(response.content)["items"]

        for track in json_data:

            track_name = '-'.join(re.sub(
                r'[^\w\s]', '', track["name"]).lower().split(' '))

            file_name = os.path.join(
                'data', 'tracks', prefix, album_name, f'{track_name}.json'
                )

            with open(file_name, 'w') as file:
                json.dump(track, file, indent=4)

            s3.Bucket(self.bucket_name).upload_file(
                file_name, os.path.join(album_name, f'{track_name}.json')
            )

        return 0
