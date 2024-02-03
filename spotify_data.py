code = authorize_spotify()
token = get_access_token(code)
playlist_hrefs = fetch_user_playlist_ids(token)
print(playlist_hrefs)
playlist_href = playlist_hrefs[6]
playlist_href = 'https://api.spotify.com/v1/playlists/49jW4Nm4xKaPbDqAHPSySY'
track_id = '4hm33jVolpa22nzhlY72jD'
prompt_info = get_prompt_info_from_playlist(playlist_href, token)
artist = get_track(track_id, token)['artists'][0]['id']
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
#
