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

  print(f'description: {playlist_description}')
  # Get DALL-E prompt to construct texture for planet based on given genres
  prompt_response = client.chat.completions.create(
    model='gpt-4',
    messages=[
      {
        'role': 'user',
        'content': f'describe cover art based on a playlist containing artists in the following genres: {genre_prompt_insert} try to not use the genre names, but give a description of the cover art.'
      }
    ]
  )

  print(f'prompt: {prompt_response.choices[0].message.content}')

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
