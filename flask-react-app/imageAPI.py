   
import requests

def upload_image(image_url):
    body = {
        "key" : "6d207e02198a847aa98d0a2a901485a5",
        "source": image_url,
        
    }
    response = requests.post(f"https://freeimage.host/api/1/upload", data=body)
    print(response.json())
    return response.json()['image']['url']


