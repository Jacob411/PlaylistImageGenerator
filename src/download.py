

import requests

def download_image(url, save_path):
    try:
        # Make a GET request to the URL
        response = requests.get(url, stream=True)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open a local file with write-binary mode
            with open(save_path, 'wb') as file:
                # Iterate over the content in chunks and write to the file
                for chunk in response.iter_content(chunk_size=128):
                    file.write(chunk)
            print(f"Image downloaded successfully to {save_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

