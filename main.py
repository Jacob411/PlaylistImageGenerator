from openai import OpenAI


# TODO: get genres from Spotify API
genres = ['trap', 'hip hop', 'house']
#('classic soundtrack', 6), ('vintage italian soundtrack', 6), ('classical', 5), ('hollywood', 2), ('movie tunes', 2)
new_genres = ['classic soundtrack', 'vintage italian soundtrack', 'classical', 'hollywood', 'movie tunes']

def get_image_and_description(genres):
  client = OpenAI(api_key='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')

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
        'content': f'Create a description of a playlist containing artists in the following genres: {genre_prompt_insert}. Limit the description to one paragraph.'
      }
    ]
  )
  playlist_description = description_response.choices[0].message.content

  # Get DALL-E prompt to construct texture for planet based on given genres
  prompt_response = client.chat.completions.create(
    model='gpt-4',
    messages=[
      {
        'role': 'user',
        'content': f'Construct a prompt for DALL-E to create a texture for a planet based on a playlist containing artists in the following genres: {genre_prompt_insert} (fill the entire image with the texture).'
      }
    ]
  )

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
