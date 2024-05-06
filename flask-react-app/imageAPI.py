   
import requests

def upload_image(image_url):
    body = {
        "key" : "",
        "source": image_url,
        
    }
    response = requests.post(f"https://freeimage.host/api/1/upload", data=body)
    print(response.json())
    return response.json()['image']['url']


