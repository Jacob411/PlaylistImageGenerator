import requests


def get_data():
    api_key = "WO7uubCnre2mr25S30AwC5p0W9TKFd1Q4TPk2afi"

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",  # Adjust content type as needed
    }
    response = requests.get('https://ud4r2e196g.execute-api.us-east-2.amazonaws.com/')
    return response.json()


def main():
    data = get_data()
    print(data)
