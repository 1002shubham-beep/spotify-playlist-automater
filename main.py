import spotipy
from spotipy.oauth2 import SpotifyPKCE
from dotenv import load_dotenv

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
REDIRECT_URI = "http://127.0.0.1:8888/callback"

SCOPE = "playlist-modify-public playlist-modify-private playlist-read-private"


# ---------- AUTOMATIC PLAYLIST NAME ----------
def get_playlist_name(sp):
    name = input("\nEnter playlist name (press Enter for automatic): ").strip()

    if name:
        return name

    playlists = sp.current_user_playlists(limit=50)

    number = 1

    while True:
        automatic_name = f"Untitled Mix {number:03d}"

        exists = any(
            playlist["name"] == automatic_name
            for playlist in playlists["items"]
        )

        if not exists:
            return automatic_name

        number += 1


# ---------- CONNECT TO SPOTIFY ----------
auth_manager = SpotifyPKCE(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)

sp = spotipy.Spotify(auth_manager=auth_manager)

user = sp.current_user()

print(f"\nLogged in as: {user['display_name']}")
print("Spotify connection successful!\n")


# ---------- READ SONGS ----------
with open("songs.txt", "r", encoding="utf-8") as file:
    songs = [line.strip() for line in file if line.strip()]

print(f"Found {len(songs)} songs.\n")


# ---------- SEARCH SONGS ----------
track_uris = []

for song in songs:

    print(f"Searching: {song}")

    results = sp.search(
        q=song,
        type="track",
        limit=1
    )

    tracks = results["tracks"]["items"]

    if tracks:
        track = tracks[0]

        print(
            f"✓ Found: {track['name']} — "
            f"{track['artists'][0]['name']}"
        )

        track_uris.append(track["uri"])

    else:
        print(f"✗ Could not find: {song}")


# ---------- ASK FOR PLAYLIST NAME ----------
playlist_name = get_playlist_name(sp)

print(f"\nPlaylist name: {playlist_name}")


# ---------- CREATE PLAYLIST ----------
playlist = sp._post(
    "me/playlists",
    payload={
        "name": playlist_name,
        "public": False,
        "description": "Created automatically using Python 🎵"
    }
)

print("\nPlaylist created!")


# ---------- ADD SONGS ----------
if track_uris:

    sp._post(
        f"playlists/{playlist['id']}/items",
        payload={
            "uris": track_uris
        }
    )

print(f"✓ Added {len(track_uris)} songs.")

print("\n🎵 DONE!")
print(f"Playlist: {playlist['external_urls']['spotify']}")
