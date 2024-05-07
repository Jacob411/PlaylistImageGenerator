# Description: This file contains the code to connect to the MongoDB database and retrieve the documents from the collection.

# Import the required libraries
import os
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from gridfs import GridFS
from bson.objectid import ObjectId 
from urllib.request import urlopen
def write_image(image_url):
    load_dotenv(find_dotenv())
    connection_string = os.getenv("CONNECTION_STR")

    # Create a MongoClient instance
    client = MongoClient(connection_string)

    # Access the desired database and collection
    db = client['DalleImages']

    fs = GridFS(db)
 
   # Open the image file from the URL in binary mode
    with urlopen(image_url) as response:
        image_data = response.read()

    file_id = fs.put(image_data, filename='my_image.jpg')

    print(f"Image stored in MongoDB with file ID: {file_id}")


    # Close the MongoDB connection
    client.close()

    return file_id


def retrieve_image(file_id, output_path):
    load_dotenv(find_dotenv())
    connection_string = os.getenv("CONNECTION_STR")

    # Create a MongoClient instance
    client = MongoClient(connection_string)

    # Access the desired database and collection
    db = client['DalleImages']

    fs = GridFS(db)

    # Retrieve the image file from GridFS using the file ID
    file = fs.get(ObjectId(file_id))

    # Save the file to the local system
    with open(output_path, 'wb') as output_file:
        output_file.write(file.read())

    print(f"Image retrieved from MongoDB and saved to {output_path}")







def main():
    # Get documents from the MongoDB collection
    retrieve_image("65bf616887699a07da92df2a", "my_image.jpg")
    
if __name__ == "__main__":
    main()
