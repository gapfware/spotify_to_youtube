import spotipy
import itertools
from tqdm import tqdm
from ytmusicapi import YTMusic
from dotenv import load_dotenv
from urllib.parse import urlparse
from spotipy.oauth2 import SpotifyClientCredentials


def get_playlist_id(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    partes_del_path = path.split("/")
    playlist_key = partes_del_path[-1] if partes_del_path else ""
    return playlist_key


def playlist_items(spotify_client, spotify_playlist_id):
    for offset in itertools.count(step=100):
        response = spotify_client.playlist_items(
            spotify_playlist_id, offset=offset, limit=100
        )
        for item in response["items"]:
            yield item
        if response["next"] is None:
            return


def main():
    try:
        videos_id = []
        ytmusic_client = YTMusic("oauth.json")
        auth_manager = SpotifyClientCredentials()
        spotify_client = spotipy.Spotify(auth_manager=auth_manager)

        playlist_url = input("Enter spotify playlist url: ")
        playlist_id = get_playlist_id(playlist_url)
        sp_playlist = list(playlist_items(spotify_client, playlist_id))
        new_playlist_title = spotify_client.playlist(playlist_id=playlist_id)
        new_playlist_desc = input("Ingrese la descripcion de la playlist a crear: ")
        yt_playlist_id = ytmusic_client.create_playlist(
            title=new_playlist_title['name'], description=new_playlist_desc
        )

        for item in tqdm(sp_playlist):
            title = item["track"]["name"]
            artists = " ".join(
                [
                    artist["name"]
                    for artist in item["track"]["artists"]
                    if artist["type"] == "artist"
                ]
            )
            query = f"{title} {artists}"
            search_results = ytmusic_client.search(query=query)
            for result in search_results:
                if result["resultType"] == "song":
                    if result["videoId"] not in videos_id:
                        videos_id.append(result["videoId"])
                        print(f"Added: {query}")
                        break
            else:
                print(f"Could Not find a match to {query}")

        added = ytmusic_client.add_playlist_items(
            playlistId=yt_playlist_id, videoIds=videos_id
        )
        if added["status"] == "STATUS_FAILED":
            print("No se agregaron al playlist")
        else:
            print("Migrado correctamente")
    except Exception as err:
        print(f"An error occurred.\nError message: {err}")


if __name__ == "__main__":
    load_dotenv()
    main()
