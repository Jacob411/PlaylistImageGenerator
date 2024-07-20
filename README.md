# Spotify Playlist Art Generator
## Overview
This project is a Spotify playlist art generator that creates visual representations based on the content of a Spotify playlist. It utilizes Spotify's API to retrieve information about the tracks in the playlist and then generates art based on various attributes such as song popularity, mood, genre, etc. The generated art can serve as a creative visualization of the playlist's characteristics.

## Features
Playlist Analysis: The application analyzes the tracks within a given Spotify playlist, extracting relevant information on genres and artists.
Art Generation: Based on the analyzed data, the application generates art in the form of visualizations, graphics, or other creative representations.
Customization: Users can customize the art generation process by specifying parameters such as color scheme, visual style, or thematic elements.
Export: Generated art can be exported in various formats for sharing or further editing.

## Installation
Clone this repository:
```bash
git clone https://github.com/your_username/spotify-playlist-art-generator.git
```
Install dependencies:
```bash
cd PlaylistImageGenerator
pip install -r requirements.txt
```
Obtain Spotify API credentials by registering your application on the Spotify Developer Dashboard. Make sure to set the redirect URI to http://localhost:3000 or a custom URI if applicable.
Create a .env file in the project root directory and add your Spotify API credentials, as well as your OpenAI key:
#.env
#spotify credentials
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
#OpenAI 
OPENAI_API_KEY=your_key

## Usage
Run the application:
```bash
cd src
python3 local_main.py
```
Follow the on-screen instructions to authenticate with your Spotify account and select a playlist for analysis (playlist ID is the last segment of the playlist URL from spotify).
Customize the art generation process if desired.
Once the art is generated, it will be written into the "Files" Directory and a link will be print on the screen.

## Contributing
Contributions are welcome! If you have any ideas for new features, improvements, or bug fixes, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
