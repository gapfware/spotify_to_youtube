import spotipy
import itertools
from tqdm import tqdm
from ytmusicapi import YTMusic
from dotenv import load_dotenv
from urllib.parse import urlparse
from spotipy.oauth2 import SpotifyClientCredentials


def get_playlist_id():
    playlist_url = input("Enter spotify playlist url: ")
    parsed_url = urlparse(playlist_url)
    path = parsed_url.path
    path_parts = path.split("/")
    playlist_key = path_parts[-1] if path_parts else ""
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


def get_youtube_videos_ids(spotify_playlist, ytmusic_client):
    yt_videos_ids = []
    for song in tqdm(spotify_playlist):
        title = song["track"]["name"]
        album = song["track"]["album"]["name"]
        artists = " ".join(
            [
                artist["name"]
                for artist in song["track"]["artists"]
                if artist["type"] == "artist"
            ]
        )
        query = f"{title} {artists} {album}"
        search_results = ytmusic_client.search(query=query)

        for result in search_results:
            if result["resultType"] == "song":
                if result["videoId"] not in yt_videos_ids:
                    yt_videos_ids.append(result["videoId"])
                    print(f"Added: {query}")
                    break
        else:
            print(f"Could Not find a match to {query}")
    return yt_videos_ids


def main():
    try:
        ytmusic_client = YTMusic("oauth.json")
        auth_manager = SpotifyClientCredentials()
        spotify_client = spotipy.Spotify(auth_manager=auth_manager)

        playlist_id = get_playlist_id()

        playlist_info = spotify_client.playlist(playlist_id=playlist_id)
        playlist_name = playlist_info["name"]
        playlist_description = playlist_info["description"]

        spotify_playlist = list(playlist_items(spotify_client, playlist_id))
        yt_playlist_id = ytmusic_client.create_playlist(
            title=playlist_name, description=playlist_description
        )

        videos_ids = get_youtube_videos_ids(spotify_playlist, ytmusic_client)

        added_tracks = ytmusic_client.add_playlist_items(
            playlistId=yt_playlist_id, videoIds=videos_ids,
        )

        if added_tracks["status"] == "STATUS_FAILED":
            print(f"Failed to migrate playlist '{playlist_name}'")
        else:
            print(f"Playlist '{playlist_name}' succesfully migrated")

    except Exception as err:
        print(f"An error has occurred.\nError message: {err}")


if __name__ == "__main__":
    load_dotenv()
    main()
