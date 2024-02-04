

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

# Example usage:
image_url = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-kA2Y6zurcMnzpyky2Sycr4gd/user-E2DsGxkvntx0VwlqgjIY8vMp/img-LIJvWgtdNQomNWz6sAeCHSaz.png?st=2024-02-04T05%3A54%3A09Z&se=2024-02-04T07%3A54%3A09Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-02-04T02%3A29%3A30Z&ske=2024-02-05T02%3A29%3A30Z&sks=b&skv=2021-08-06&sig=n8sY9E2ygfP9kG7tA2Qy%2BoVdEogBMWLhegDv42eoQsQ%3D"
local_path = "downloaded_image.jpg"

download_image(image_url, local_path)
