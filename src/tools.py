from langchain_core.tools import tool
import requests


@tool
def get_albums():
    """Use this to get all albums of Taylor Swift (Taylor Version)

    output format :

    [
        {
            album_id : int,//id of the album. usefull to find songs associate with a specific album
            title : str,
            artist_id : int, // to be ignored
            release_date : <date>
                }
    ...
    ]

    """
    albums = requests.get("https://taylor-swift-api.sarbo.workers.dev/albums").json()
    return albums


@tool
def get_songs(id_album: int):
    """Retrieve list of all songs within a specific album.
    output format :
      {
          "song_id": 10,
          "song_title": "Wonderland",
          "album_id": 1
      }
    """
    songs = requests.get(
        f"https://taylor-swift-api.sarbo.workers.dev/albums/{id_album}"
    ).json()
    return songs


@tool
def get_lyrics(id_song: int):
    """Get Lyrics for a given song id"""
    lyrics = requests.get(
        f"https://taylor-swift-api.sarbo.workers.dev/lyrics/{id_song}"
    ).json()
    return lyrics
    # return "So casually cruel in the name of being honest"
