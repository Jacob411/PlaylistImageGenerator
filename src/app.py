from spotify_utils import *
import requests
from urllib.request import urlopen
from flask import Flask, request
from flask_cors import CORS
from imageAPI import upload_image 
from download import download_image 
from main import get_image_and_description 
app = Flask(__name__)

CORS(app)

@app.route('/')
def hello():
    return 'Hello from Flask API!'

# href
# https://api.spotify.com/v1/playlists/3cEYpjA9oz9GiPac4AsH4n
@app.route('/get_playlist_image', methods=['POST'])
def get_playlist_image():
    print("OUT")
    code = authorize_spotify()
    token = get_access_token(code)

    user_info = get_user_info(token)
    print(user_info)

    json_data = request.get_json(force=True, silent=True)
    # token = json_data.get('access_token') # User when the token is passed in the request
    playlist_href = json_data.get('playlist')
    #
    print(f"Token: {token}")
    print(f"Playlist href: {playlist_href}")

    name, prompt_info = get_prompt_info_from_playlist(playlist_href, token)
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

    description, image_url = get_image_and_description(top_5_genres)

    print(f"Image URL: {image_url}")
    print(f"Description: {description}")
        
     
    # Open the image file from the URL in binary mode
    with urlopen(image_url) as response:
        image_data = response.read()

    # write the image data to a temporary file
    image_path = 'Files/image.jpg'
    with open(image_path, 'wb') as f:
        f.write(image_data)

    text_path = 'Files/textDisc.txt'
    with open(text_path, 'wb') as f:
        f.write(description.encode('utf-8'))



    data = { image_url: image_url, description: description }
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response
