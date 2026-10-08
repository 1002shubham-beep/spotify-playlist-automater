# Spotify Playlist Maker

A Python script that builds a Spotify playlist from a list of songs in a text file. Add your songs to `songs.txt`, run the script, and the playlist appears in your Spotify account.

## How it works

1. Put one song per line in `songs.txt`, written as the song name with the artist (e.g. `Song Name Artist Name`).
2. Run the script and log in to Spotify in the browser window that opens.
3. Enter a playlist name, or press Enter to auto-generate one (`Untitled Mix 001`, `Untitled Mix 002`, ...).
4. The script searches Spotify for each song, adds the matches to a new private playlist, and prints the playlist link.

Songs that can't be found are skipped and reported in the terminal.

## Built with AI assistance

I built this project with help from AI, mainly for the Spotify API integration and the login flow. I tested it and can explain how it works. This note is here for transparency.

## Tech used

- Python
- [Spotipy](https://spotipy.readthedocs.io/) (Spotify Web API wrapper)
- PKCE authentication, so no client secret is needed
- python-dotenv (keeps the client ID out of the code)

## Setup

1. Create an app in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Add this Redirect URI in the app settings: `http://127.0.0.1:8888/callback`
3. Copy `.env.example` to a new file named `.env` and paste in your own client ID:

```
   SPOTIFY_CLIENT_ID=your_client_id_here
```

4. Install the dependencies:

```bash
   pip install -r requirements.txt
```

5. Add your songs to `songs.txt`, then run:

```bash
   python main.py
```

## Notes

- Playlists are created as private by default.
- Search takes the top result for each line, so including the artist name improves accuracy.
- Your login tokens are stored locally in a `.cache` file, which is excluded from the repo by `.gitignore`.
