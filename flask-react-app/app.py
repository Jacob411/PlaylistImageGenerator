from spotify_utils import *
from flask import Flask, request
from mongo import *
from download import download_image 
from main import get_image_and_description 
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from Flask API!'

# BQCeKbNc4oGiu9cdXAk_89Dbq64wWlM_N-MIAuLgWinv44i971JsnHp09DKvg8ntSQzQvxMqOtlginK4b33R4w6mqd9tpRitPL9oCBECC5cGyivSiktDCO4MA1iQ0lfo9ODDX8bqUMTbAZUu2EpqA8tobbZ6WeSDNDEeAyyj8avgnY5qk8EYw7zsmCnc11Oz4OlB8p7RsrxXNqkhf0d4GAt0gMYtoExv_GDnSx10n6e97J5HDH-7-Se3NSgCKpgaw80ps4cUQw
# href
# https://api.spotify.com/v1/playlists/3cEYpjA9oz9GiPac4AsH4n
@app.route('/get_playlist_image', methods=['POST'])
def get_playlist_image():

    json_data = request.get_json(force=True, silent=True)
    token = json_data.get('access_token')
    playlist_href = json_data.get('playlist')

    print(f"Token: {token}")
    print(f"Playlist href: {playlist_href}")
    prompt_info = get_prompt_info_from_playlist(playlist_href, token)
    print(prompt_info)
    genre_map = {}
    for prompt in prompt_info:
        for genre in prompt['genres']:
            if genre in genre_map:
                genre_map[genre] += 1
            else:
                genre_map[genre] = 1
    #print sorted genre map
    print(sorted(genre_map.items(), key=lambda x: x[1], reverse=True))
    top_5_genres = sorted(genre_map.items(), key=lambda x: x[1], reverse=True)[:5]
    print(top_5_genres)
    # strip out the count and leave only the genre
    top_5_genres = [genre[0] for genre in top_5_genres]
    print(top_5_genres)
    image_url, description = get_image_and_description(top_5_genres)

    print(f"Image URL: {image_url}")
    print(f"Description: {description}")
    
    return { image_url: image_url, description: description }
