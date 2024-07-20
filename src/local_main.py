from spotify_utils import *
import requests
from urllib.request import urlopen
from openai_tools import get_image_and_description 

def get_playlist_image():
    print("OUT")
    code = authorize_spotify()
    token = get_access_token(code)

    user_info = get_user_info(token)
    print(user_info)

    # get user input for playlist ID
    playlist_id = input("Enter the playlist ID: ")
    print("\n")
    playlist_href = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    playlist_info = get_endpoint(token, playlist_href)
    print(playlist_info['name'])
    name = playlist_info['name']
    print(f"Playlist selected: {name}\n")

    prompt_info = get_prompt_info_from_playlist(playlist_href, token)

    genre_map = {}
    for prompt in prompt_info:
        for genre in prompt['genres']:
            if genre in genre_map:
                genre_map[genre] += 1
            else:
                genre_map[genre] = 1
    #print sorted genre map
    print(sorted(genre_map.items(), key=lambda x: x[1], reverse=True))
    print('\n')
    top_5_genres = sorted(genre_map.items(), key=lambda x: x[1], reverse=True)[:5]
    print(top_5_genres)
    print('\n')
    # strip out the count and leave only the genre
    top_5_genres = [genre[0] for genre in top_5_genres]
    print(top_5_genres)

    description, image_url = get_image_and_description(top_5_genres)

    print(f"Image URL: {image_url}")
        
     
    # Open the image file from the URL in binary mode
    with urlopen(image_url) as response:
        image_data = response.read()

    # write the image data to a temporary file
    image_path = f'Files/{name}.jpg'
    with open(image_path, 'wb') as f:
        f.write(image_data)

    text_path = 'Files/textDisc.txt'
    with open(text_path, 'wb') as f:
        f.write(description.encode('utf-8'))






def main():
    get_playlist_image()

if __name__ == "__main__":
    main()
