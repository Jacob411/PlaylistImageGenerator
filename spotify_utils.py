import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import requests
import time
import json
import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
# Global variable to store the authorization code

# Create a simple HTTP request handler
class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global authorization_code

        # Parse the query parameters from the request URL
        query_components = parse_qs(urlparse(self.path).query)

        # Retrieve the authorization code
        if 'code' in query_components:
            authorization_code = query_components['code'][0]

        # Send a response back to the browser
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>Authorization Successful</h1></body></html>')

# Function to start the HTTP server for the callback
def start_http_server():
    server_address = ('localhost', 3000)
    httpd = HTTPServer(server_address, CallbackHandler)
    httpd.handle_request()

# Open the web browser and prompt the user to authorize access
def authorize_spotify():
    load_dotenv(find_dotenv())
    client_id = os.getenv('CLIENT_ID')
    # Specify the URL of the Spotify authorization page
    scopes = 'playlist-read-private%20user-read-email%20user-top-read%20user-library-read%20playlist-modify-public%20playlist-modify-private'
    redirect_uri = 'http://localhost:3000/callback'
    spotify_auth_url = f"https://accounts.spotify.com/en/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scopes}"

    # Open the Spotify authorization page in the default web browser
    webbrowser.open(spotify_auth_url)

    # Start the HTTP server to listen for the callback
    start_http_server()

    # Wait until the authorization code is received
    while authorization_code is None: 
        pass

    

    return authorization_code
    # # Print the authorization code
    # print("Authorization Code:", authorization_code)


def get_access_token(authorization_code):
    token_url = 'https://accounts.spotify.com/api/token'
  
    load_dotenv(find_dotenv())
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    print(client_id)
    print(client_secret)


    token_params = {
        'client_id': client_id,
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': 'http://localhost:3000/callback'
    }


    response = requests.post(token_url, data=token_params, auth=(client_id, client_secret))

  
    # Extract the access token from the response
    access_token = response.json()['access_token']

    # Write the access token to a json file in the current users directory
    current_user_name = get_endpoint(access_token, 'https://api.spotify.com/v1/me')['display_name']

    print(f'Current user name: {current_user_name}')

    directory = f'Files/{current_user_name}'

    # Create local directory if it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write the access token to a json file in the current users directory
    with open(f'{directory}/access_token.json', 'w') as outfile:
        json.dump(response.json(), outfile, indent=4)

 
    return access_token

def refresh_access_token(refresh_token):
    load_dotenv(find_dotenv())
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(url, {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret' : client_secret})
    
    auth_response_data = auth_response.json()
    try:
        access_token = auth_response_data['access_token']
        # Write the access token to a json file in the current users directory
        current_user_name = get_endpoint(access_token, 'https://api.spotify.com/v1/me')['display_name']

        directory = f'Files/{current_user_name}'

        # Create local directory if it does not exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Write the access token to a json file in the current users directory
        with open(f'{directory}/access_token.json', 'w') as outfile:
            json.dump(auth_response_data, outfile, indent=4)
    except KeyError:
        print('Error: KEY ERROR')
        access_token = auth_response_data

    return access_token


def get_app_access_token():
    # Returns token that has access to only public data/does not require user authentication
    # Set up authorization

    load_dotenv(find_dotenv())
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')



    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']
    
    return access_token


def get_endpoint(access_token, endpoint=''):
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
    except requests.exceptions.Timeout:
        print('The request timed out')
    except requests.RequestException as e:
        print(e)

    return response.json()

def get_user_info(access_token, endpoint=''):

    profile_url = f'https://api.spotify.com/v1/me/{endpoint}'
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    # Send a GET request to the profile URL, and set the authorization header
    response = requests.get(profile_url, headers=headers)

    return response.json()

def fetch_public_playlist_tracks(user_id):

    access_token = get_app_access_token()
    URL = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    playlist_hrefs = []
    offset = 0
    while True:
        time.sleep(0.5)
        user_profile = get_endpoint(access_token, f'{URL}?limit=50&offset={offset}')
        
        for playlist in user_profile['items']:
            playlist_hrefs.append(playlist['href'])

        #get size of items
        if len(user_profile['items']) < 50:
            break
        offset += 50
    
        # Get the track ids

    headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }
    all_tracks = []

    for href in playlist_hrefs:
        playlist1 = requests.get(href, headers=headers).json()

        for track in playlist1['tracks']['items']:
            try:
                print(track['track']['name'])
                all_tracks.append(track['track']['id'])
            except:
                pass
                print('no track')

    return all_tracks

# Get the user's profile information
# user_profile = get_user_info(authorization_code, 'tracks?limit=50')
# print(user_profile['items'][0]['track'].keys())

def fetch_user_saved_tracks(access_token):
    user_profile = get_user_info(access_token, 'tracks?limit=50')
    saved_track_ids = []

    for track in user_profile['items']:
        print(track['track']['name'])
        saved_track_ids.append(track['track']['id'])

    return saved_track_ids

def fetch_user_top_tracks(access_token):
    top_track_ids = []

    user_profile = get_user_info(access_token, f'top/tracks?limit=50')
    print(user_profile['next'])
    for track in user_profile['items']:
        print(track['name'])
        top_track_ids.append(track['id'])

    return top_track_ids

def fetch_user_playlist_ids(access_token):
    # need to keep calling api until there are no more playlists
    
    playlist_ids = []
    offset = 0

    while True:
        time.sleep(0.5)
        user_profile = get_user_info(access_token, f'playlists?limit=50&offset={offset}')
        
        for playlist in user_profile['items']:
            playlist_ids.append(playlist['href'])

        #get size of items
        if len(user_profile['items']) < 50:
            break
        offset += 50
    return playlist_ids

def fetch_user_playlists_tracks(access_token):
 
    playlist_hrefs = fetch_user_playlist_ids(access_token)

    headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }
    all_tracks = []
    for href in playlist_hrefs:
        playlist1 = requests.get(href, headers=headers).json()
            
        for track in playlist1['tracks']['items']:
            # 2019-10-10T16:50:03Z
            # convert to datetime
            
            # datetime_str = track['added_at']
            # datetime_str = "2019-10-10T16:50:03Z"
            # datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")

            # current_datetime = datetime.now()
            # two_years_ago = current_datetime - timedelta(days=365*2)
            # if datetime_obj > two_years_ago:
                try:
                    print(track['track']['name'])
                    all_tracks.append(track['track']['id'])
                except:
                    pass
                    
                    print('no track')

    return all_tracks


def get_features(access_token, track_ids):
    track_features = []
    count = 0
    for track_id in track_ids:
        track_feature = get_endpoint(access_token, f'https://api.spotify.com/v1/audio-features/{track_id}')
        if track_feature.get('error'):
            print('rate limit reached')
            time.sleep(5)
            track_feature = get_endpoint(access_token, f'https://api.spotify.com/v1/audio-features/{track_id}')
            break
        track_features.append(track_feature)
        print(f'{count} / {len(track_ids)}')
        count += 1

    return track_features
def get_track(track_id, access_token):
    track = get_endpoint(access_token, f'https://api.spotify.com/v1/tracks/{track_id}')
    return track
def get_artist(artist_id, access_token):
    artist = get_endpoint(access_token, f'https://api.spotify.com/v1/artists/{artist_id}')
    return artist

def get_prompt_info_from_playlist(playlist_href, access_token):
    playlist = get_endpoint(access_token, playlist_href)
    all_tracks = [] 
    for track in playlist['tracks']['items']:
        try:
            print(track['track']['name'])
            all_tracks.append(track['track']['id'])
        except:
            pass        
            print('no track')


    final = []
    for track in all_tracks:
        track_info = get_track(track, access_token)
        curr_obj = {}
        curr_obj['name'] = track_info['name']
        curr_obj['artist'] = track_info['artists'][0]['name']
        curr_obj['id'] = track
        curr_obj['genres'] = get_artist(track_info['artists'][0]['id'], access_token)['genres']
        final.append(curr_obj)
    return final


def get_all_features(access_token):
    count = 0
    # Get playlist track features and add weight property to them
    playlist_features = get_features(access_token, fetch_user_playlists_tracks(access_token))
    # add weight 1 to playlist tracks
    for feature in playlist_features:
        print(count)
        count += 1

        feature['weight'] = 1


    # Get saved track features and add weight property to them
    saved_features = get_features(access_token, fetch_user_saved_tracks(access_token))
    # add weight 1 to saved tracks
    for feature in saved_features:
        print(count)
        count += 1

        feature['weight'] = 1

    # Get top track features and add weight property to them
    top_features = get_features(access_token, fetch_user_top_tracks(access_token))
    # add weight 3 to top tracks
    for feature in top_features:
        print(count)
        count += 1

        feature['weight'] = 3

    # Combine all features into one list
    all_features = top_features + saved_features + playlist_features
    return all_features

# code = authorize_spotify()
# token = get_access_token(code)
# all_tracks = get_all_features(token)
# # Write all features to a JSON file

# output_file = " jakerstx_data1.json"
# # Write the data to the JSON file
# with open(output_file, "w") as file:
#     json.dump(all_tracks, file, indent=4)  # indent=4 for pretty formatting

# print("JSON data written to", output_file)
#print(track)
# TODO combine functions
# TODO make sure no duplicates
# TODO implement a public only option, that doesnt require auth
# TODO make sure it works for all users
# TODO change all keys so they are not visible on github
# TODO stop popup window from opening if user already authorized
# TODO have a progress bar for the user to see how much longer it will take
# TODO make a gui
# TODO allow user to input a whole playlist or album and get what percent of the songs they would like
