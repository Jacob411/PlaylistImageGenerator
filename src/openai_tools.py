from openai import OpenAI
from dotenv import load_dotenv
import os

# TODO: get genres from Spotify API
genres = ['trap', 'hip hop', 'house']
#('classic soundtrack', 6), ('vintage italian soundtrack', 6), ('classical', 5), ('hollywood', 2), ('movie tunes', 2)
new_genres = ['classic soundtrack', 'vintage italian soundtrack', 'classical', 'hollywood', 'movie tunes']

def get_image_and_description(genres):
  
  # Load OpenAI API key from .env file
  load_dotenv()
  api_key = os.getenv('OPENAI_API_KEY')

  client = OpenAI(api_key=api_key)

  genre_length = len(genres)
  genre_prompt_insert = '' 

  if genre_length >= 3:
    for i in range(genre_length):
      if i != genre_length - 1:
        genre_prompt_insert += genres[i] + ", "
      else:
        genre_prompt_insert += "and " + genres[i]
  elif genre_length == 2:
    genre_prompt_insert += "and " + genres[1]

  # Get description of playlist based on given genres
  description_response = client.chat.completions.create(
    model='gpt-4',
    messages=[
      {
        'role': 'user',
        'content': f'Create a description of a playlist containing artists in the following genres: {genre_prompt_insert}.'
      }
    ]
  )
  playlist_description = description_response.choices[0].message.content

  art_styles_map = {
    'pixel' : 'use a pixel art style',
    'abstract' : 'use an abstract art style',
    'minimalist' : 'use a minimalist art style',
    'realistic' : 'use a realistic art style',
    'surreal' : 'use a surreal art style',
    'cartoon' : 'use a cartoon art style',
    'anime' : 'use an anime art style',
    'watercolor' : 'use a watercolor art style',
    'oil painting' : 'use an oil painting art style',
    'pop art' : 'use a pop art style',
    'impressionist' : 'use an impressionist art style',
    'expressionist' : 'use an expressionist art style',
    'cubist' : 'use a cubist art style',
    'futurist' : 'use a futurist art style',
    'none' : ''
    
  }
  # prompt user to select an art style
  style_num = input('Select an art style from the following list: \n1. Pixel\n2. Abstract\n3. Minimalist\n4. Realistic\n5. Surreal\n6. Cartoon\n7. Anime\n8. Watercolor\n9. Oil Painting\n10. Pop Art\n11. Impressionist\n12. Expressionist\n13. Cubist\n14. Futurist\nNone\n')
  style_arr = ['pixel', 'abstract', 'minimalist', 'realistic', 'surreal', 'cartoon', 'anime', 'watercolor', 'oil painting', 'pop art', 'impressionist', 'expressionist', 'cubist', 'futurist', 'none']
  selected_item = int(style_num) - 1



  print(f'description: {playlist_description}')
  # Get DALL-E prompt to construct texture for planet based on given genres
  prompt_response = client.chat.completions.create(
    model='gpt-4',
    messages=[
      {
        'role': 'user',
        'content': f'in one sentence, briefly describe cover art based on a playlist containing artists in the following genres: {genre_prompt_insert} try to not use the genre names' + art_styles_map[style_arr[selected_item]]
      }
    ]
  )

  print(f'\nprompt: {prompt_response.choices[0].message.content}')

  # Get planet texture image
  texture_response = client.images.generate(
    model='dall-e-3',
    prompt=prompt_response.choices[0].message.content,
    size='1792x1024',
    n=1
  )
  image_url = texture_response.data[0].url

  return playlist_description, image_url


def main():
  description, image_url = get_image_and_description(new_genres)
  print(description)
  print(image_url)


if __name__ == '__main__':
  main()
