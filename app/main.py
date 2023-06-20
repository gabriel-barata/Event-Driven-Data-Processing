from datetime import datetime
import requests
import boto3
import json
import os
import re

class SpotifyAPI:

    def __init__(self, client_id, client_secret):
        
        self.client_id = client_id
        self.client_secret = client_secret

    ## This function returns the access_token that will be used to our further requests
    def auth(self):
        
        endpoint  = 'https://accounts.spotify.com/api/token'

        headers = {

            'Content-Type' : 'application/x-www-form-urlencoded'
        }

        data = {

            'grant_type' : 'client_credentials',
            'client_id' : self.client_id,
            'client_secret' : self.client_secret
        }

        response = requests.post(endpoint, headers = headers, params = data)
        
        if response.status_code == 200:
            access_token = json.loads(response.content)["access_token"]
            token_type = json.loads(response.content)["token_type"]   
            self.base_header = {'Authorization' : f'{token_type} {access_token}'}

        else:
             print(f"-error during auth on spotify : {response.status_code}")

    ##Function to search for artists, it will return the 'artist_id' that will be used on further functions
    def get_artist_id(self, query):

        query = query.capitalize()
        endpoint = f"https://api.spotify.com/v1/search?q={query}&type=artist&limit=1" 
        response = requests.get(endpoint, headers = self.base_header)
        data = json.loads(response.content)
        artist_id = data["artists"]["items"][0]["id"]
        
        return artist_id

    ##This function gets the data from albums maden by the given 
    def get_albums(self, artist_id, prefix, bucket_name, include_groups : list() = ['album', 'single'], limit : int = 30):

        s3 = boto3.resource('s3')

        include_groups = ','.join(include_groups)

        endpoint = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
        params = {

            'include_groups' : include_groups,
            'limit' : limit

        }

        response = requests.get(endpoint, headers = self.base_header, params = params)
        json_data = json.loads(response.content)["items"]
        albums_ids = [(album["id"], album["name"]) for album in json_data]

        with open('data/albums/' + prefix + '-albums' + '.json', 'w') as file:
            json.dump(json_data, file, indent = 4)

        s3.Bucket(bucket_name)\
            .upload_file('data/albums/' + prefix + '-albums' + '.json', prefix + '-albums.json')

        return albums_ids
    
    ##This function gets all the tracks in a album
    def get_album_tacks(self, album_id, bucket_name, album_name, prefix, limit : int = 30, market : str = "BR"):

        s3 = boto3.resource('s3')

        album_name = '-'.join(re.sub(r'[^\w\s]', '', album_name).lower().split(' '))

        if not os.path.exists('data/tracks/' + album_name):
            os.makedirs('data/tracks/' + album_name)

        endpoint  = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
        params = {

            'limit' : limit,
            'market' : market

        }

        response = requests.get(endpoint, headers = self.base_header, params = params)
        json_data = json.loads(response.content)["items"]

        for track in json_data:

            track_name = track["name"]
            track_name  = '-'.join(re.sub(r'[^\w\s]', '', track_name).lower().split(' '))

            with open('data/tracks/' + prefix + '/' + album_name + '/' + track_name + '.json', 'w') as file:
                json.dump(track, file, indent = 4)
            
            s3.Bucket(bucket_name)\
                .upload_file('data/tracks/' + prefix + '/' + album_name + '/' + track_name + '.json', album_name + '/' + track_name + '.json')

        return 0