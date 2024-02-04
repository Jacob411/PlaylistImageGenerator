from spotify_utils import *
from flask import Flask
from main import get_image_and_desciption
<<<<<<< HEAD

=======
from main import get_image_and_desciption 
>>>>>>> parent of 537968b (added the other functions)
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from Flask API!'

@app.route('/get_playlist_image/<token>/<playlist_href>')
def get_playlist_image(token, playlist_href):
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
    image_url, description = get_image_and_desciption(top_5_genres)

    print(f"Image URL: {image_url}")
    print(f"Description: {description}")
