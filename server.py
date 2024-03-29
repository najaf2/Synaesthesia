from flask import Flask, request, render_template
from flask_cors import CORS
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import openai
from dotenv import load_dotenv
import os
import random

app = Flask(__name__)
load_dotenv()

CORS(app)

openai.api_key = os.environ.get('OPENAI_KEY')
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
                                               client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET'),
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-top-read playlist-modify-public"))


""" interpret with openai

    Parameters:
        - prompt - the mood/vibe the user inputted
    Returns:
        - a string
"""


def gpt3_interpret(prompt):
    # Define the prompt and the OpenAI API parameters
    model = "text-davinci-003"
    # model = "text-curie-001"
    temperature = .7
    max_tokens = 250
    prompt = f"What are some words that describe the the mood: {prompt}\n"

    # Call the OpenAI API to generate text based on the prompt
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )

    # Return the string
    return str(response.choices[0].text)


""" get tracks with openai

    Parameters:
        - prompt - the words to descirbe a users mood,
        use gpt3_interpret() first
    Returns
        - a string
"""


def gpt3_tracks(prompt, genre):
    # Define the prompt and the OpenAI API parameters
    model = "text-davinci-003"
    # model = "text-curie-001"
    temperature = .4
    max_tokens = 500
    frequency_penalty = 0.69
    presence_penalty = 0.56
    prompt = f"Can you give me a mix of 10 {genre} tracks that fit the following mood: {prompt}\n"

    # Call the OpenAI API to generate text based on the prompt
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    # Return the string
    return str(response.choices[0].text)


""" get mood emoji with openai

    Parameters:
        - prompt - the mood/vibe the user inputted
    Returns:
        - a string with 1-3 emojis 
"""


def gpt3_emoji(prompt):
    # Define the prompt and the OpenAI API parameters
    model = "text-davinci-003"
    # model = "text-curie-001"
    temperature = .7
    max_tokens = 256
    frequency_penalty = 0
    presence_penalty = 0
    prompt = f"What are 1 to 3 emojis that describes the the mood: {prompt}\n"

    # Call the OpenAI API to generate text based on the prompt
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    # Return the string
    return str(response.choices[0].text)


""" get a response to the phrase

    Parameters:
        - prompt - the mood/vibe the user inputted
    Returns:
        - a string 
"""


def gpt3_phrase(prompt):
    # Define the prompt and the OpenAI API parameters
    model = "text-davinci-003"
    # model = "text-curie-001"
    temperature = .7
    max_tokens = 256
    frequency_penalty = 0
    presence_penalty = 0
    prompt = f"What is a funny edgy positive thing I can tell my friend if they said: {prompt}\n"

    # Call the OpenAI API to generate text based on the prompt
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    # Return the string
    return str(response.choices[0].text)



def spotify_search_songs(track_list):
    """ 
    use spotify to search for tracks and return a list of them. Returns a list of song URLs

    Parameters:
        - song_list - a string of songs
    """
    to_strip = "0123456789. "
    tracks_url = []
    track_list_split = track_list.split('\n')

    for track in track_list_split:
        track = track.lstrip(to_strip)
        track = track.strip("\"“”")
        track = track.replace('"', '')
        track = track.replace('”', '')

        if not track:
            continue
        print(f"Searching for {track}")
        try:
            results = sp.search(q=str(track), type='track')
        except requests.exceptions.RequestException as e:
            print(str(e))
            continue

        # Check if any results were found
        if len(results['tracks']['items']) > 0:
            # Get the URI of the first search result
            tracks_url.append(results['tracks']['items']
                              [0]['external_urls']['spotify'])

    return tracks_url


""" use to get html embed code for a list of songs

    Parameters:
        - tracks_uri - a list of track uri's
    Returns:
        - a string HTML
"""


def spotify_get_embed(tracks_uri):
    embed_list = []
    for url in tracks_uri:
        oembed_url = f'https://open.spotify.com/oembed?url={url}'
        response = requests.get(oembed_url)
        embed_list.append(response.json()['html'])

    return embed_list


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    # Input mood
    # input = "roadtrip"
    genre = request.args.get('genres')
    input = request.args.get('q')

    print(input)
    print(genre)

    # Call functions
    interpretation = gpt3_interpret(input)
    print(interpretation)
    reponse_phrase = gpt3_phrase(input)
    print(reponse_phrase)
    emojis = gpt3_emoji(input)
    print(emojis)
    tracks_string = gpt3_tracks(interpretation, genre)
    # tracks_string = gpt3_tracks("", genre)
    # print(tracks_string)
    tracks_url = spotify_search_songs(tracks_string)
    embed_list = spotify_get_embed(tracks_url)

    # Define the HTML content as a string format
    html = ""
    for embed in embed_list:
        html += embed

    # Return JSON response
    response = {
        "html": html,
        "URLS": tracks_url,
        "emojis": emojis,
        "interpretation": interpretation,
        "phrase": reponse_phrase, 
    }

    return html

@app.route('/expsearch')
def expsearch():
    # Input mood
    # input = "roadtrip"
    genre = request.args.get('genres')
    input = request.args.get('q')

    print(input)
    print(genre)

    # Call functions
    reponse_phrase = gpt3_phrase(input)
    print(reponse_phrase)
    emojis = gpt3_emoji(input)
    print(emojis)
    tracks_string = gpt3_tracks(input, genre)
    # tracks_string = gpt3_tracks("", genre)
    # print(tracks_string)
    tracks_url = spotify_search_songs(tracks_string)
    embed_list = spotify_get_embed(tracks_url)

    # Define the HTML content as a string format
    html = ""
    for embed in embed_list:
        html += embed

    # Return JSON response
    response = {
        "html": html,
        "URLS": tracks_url,
        "emojis": emojis,
        "interpretation": input,
        "phrase": reponse_phrase, 
    }

    return html


app.run(host="0.0.0.0", port=5000)
