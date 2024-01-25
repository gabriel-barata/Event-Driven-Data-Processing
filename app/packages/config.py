from pydantic import BaseModel
from dotenv import load_dotenv

from typing import List, Optional
import os

from packages import variables as v

load_dotenv(v.ENV_FILE)


class Config(BaseModel):

    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str

    SEARCH_ENDPOINT: str

    ARTIST_LIST: List[str]

    BUCKET_NAME: Optional[str] = None


def render_config():

    config_dict = {
        "SPOTIFY_CLIENT_ID": os.getenv("SPOTIFY_CLIENT_ID"),
        "SPOTIFY_CLIENT_SECRET": os.getenv("SPOTIFY_CLIENT_SECRET"),

        "SEARCH_ENDPOINT": v.SEARCH_ENDPOINT,

        "BUCKET_NAME": os.getenv("BUKET_NAME"),
        "ARTIST_LIST": v.ARTIST_LIST
    }

    config = Config(**config_dict)

    return config
