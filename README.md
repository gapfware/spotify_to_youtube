# Spotify to YouTube Music Playlist Migration Script

## Description

This script allows you to migrate your playlists from Spotify to YouTube Music seamlessly. It utilizes the Spotipy and ytmusicapi Python libraries to access and transfer your playlists between the two platforms.

## Prerequisites

1. Python 3.6+
2. Create a virtual environment (optional but recommended)
   ```shell
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

## Installation

Clone this repository:

```shell
git clone https://github.com/gapfware/spotify_to_youtube
cd spotify_to_youtube/
```

Install the required Python packages:

```shell
pip install -r requirements.txt
```

Create a .env file in the root directory of the project and set the following variables:

```makefile
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=your_redirect_uri
```

## Configuration

Follow the instructions in the Spotipy documentation to create the necessary credentials for your Spotify account.

Refer to the ytmusicapi documentation to set up OAuth credentials for YouTube Music.

Also, follow the ytmusicapi documentation to configure the browser for accessing your YouTube Music account.

## Usage

Run the script:

```shell
python migrate_playlist.py
```

The script will ask you to enter the Spotify playlist url that you want to migrate.
Once selected, the script will transfer the selected Spotify playlist to your YouTube Music account.

## Important Notes

Please be aware that migrating playlists between platforms may result in some differences due to differences in song availability.

This script is for educational and personal use only. Respect the terms of use of both Spotify and YouTube Music.

It is recommended to review the code and understand how the script works before using it.

## Disclaimer

This project is not affiliated with Spotify or YouTube Music. Use this script responsibly and at your own risk.

License
This project is licensed under the MIT License.

```makefile
Make sure to replace placeholders like `your_spotify_client_id`, `your_spotify_client_secret`, `your_redirect_uri`, and update URLs and paths as necessary. Also, adapt the installation and usage instructions according to your project structure and preferences.
```
