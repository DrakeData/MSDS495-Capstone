import streamlit as st
import pandas as pd
import numpy as np
import requests
import spotipy
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import base64
from PIL import Image
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_KEY, SPOTIFY_SECRET_KEY
import urllib.parse
import re
from datetime import datetime

# ---- MAIN TAB SECTION ----
# emoji cheatsheet: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
    page_title="MSDS 498: Capstone Project", 
    page_icon=":musical_note:", 
    layout="wide"
    )

# Spotify API Authentication
CLIENT_ID = SPOTIFY_CLIENT_KEY
CLIENT_SECRET = SPOTIFY_SECRET_KEY
REDIRECT_URI = 'http://localhost:7777/callback'


# Define the scope for the required permissions
SCOPE = 'user-library-read user-top-read'  # Add any other scopes your app requires

# Create the SpotifyOAuth object
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=SCOPE)


 # Functions
 # Define a regex pattern to identify genres
pop_pattern = re.compile(r'pop', re.IGNORECASE)
rock_pattern = re.compile(r'rock', re.IGNORECASE)
hip_hop_pattern = re.compile(r'hip-?hop|rap', re.IGNORECASE)
electronic_pattern = re.compile(r'electronic|dance', re.IGNORECASE)
rnb_soul_pattern = re.compile(r'r&b|soul', re.IGNORECASE)
country_pattern = re.compile(r'country', re.IGNORECASE)
jazz_pattern = re.compile(r'jazz', re.IGNORECASE)
classical_pattern = re.compile(r'classical', re.IGNORECASE)
blues_pattern = re.compile(r'blues', re.IGNORECASE)
reggae_pattern = re.compile(r'reggae', re.IGNORECASE)
folk_pattern = re.compile(r'folk', re.IGNORECASE)
indie_alternative_pattern = re.compile(r'indie|alternative', re.IGNORECASE)
metal_pattern = re.compile(r'metal', re.IGNORECASE)
punk_pattern = re.compile(r'punk', re.IGNORECASE)
funk_pattern = re.compile(r'funk', re.IGNORECASE)
gospel_pattern = re.compile(r'gospel', re.IGNORECASE)
latin_pattern = re.compile(r'latin', re.IGNORECASE)
world_ethnic_pattern = re.compile(r'world|ethnic', re.IGNORECASE)
instrumental_pattern = re.compile(r'instrumental', re.IGNORECASE)
soundtrack_ost_pattern = re.compile(r'soundtrack|ost', re.IGNORECASE)

def simplify_genre(genre):
    if pop_pattern.search(genre):
        return 'Pop'
    elif rock_pattern.search(genre):
        return 'Rock'
    elif hip_hop_pattern.search(genre):
        return 'Hip-Hop / Rap'
    elif electronic_pattern.search(genre):
        return 'Electronic / Dance'
    elif rnb_soul_pattern.search(genre):
        return 'R&B / Soul'
    elif country_pattern.search(genre):
        return 'Country'
    elif jazz_pattern.search(genre):
        return 'Jazz'
    elif classical_pattern.search(genre):
        return 'Classical'
    elif blues_pattern.search(genre):
        return 'Blues'
    elif reggae_pattern.search(genre):
        return 'Reggae'
    elif folk_pattern.search(genre):
        return 'Folk'
    elif indie_alternative_pattern.search(genre):
        return 'Indie / Alternative'
    elif metal_pattern.search(genre):
        return 'Metal'
    elif punk_pattern.search(genre):
        return 'Punk'
    elif funk_pattern.search(genre):
        return 'Funk'
    elif gospel_pattern.search(genre):
        return 'Gospel'
    elif latin_pattern.search(genre):
        return 'Latin'
    elif world_ethnic_pattern.search(genre):
        return 'World / Ethnic'
    elif instrumental_pattern.search(genre):
        return 'Instrumental'
    elif soundtrack_ost_pattern.search(genre):
        return 'Soundtrack / OST'
    else:
        return genre

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8') 


st.title("Your Spotify Song Data")
# Display the login button
if st.button("Login to Spotify"):
    # Get the access token using SpotifyOAuth
    access_token = sp_oauth.get_access_token(as_dict=False)

    # Check if the token was successfully obtained
    if access_token:
        st.write("Pulling your user data...")
        # Use the access token to authenticate Spotipy
        sp = spotipy.Spotify(auth_manager=sp_oauth)
        
        # Get user tracks
        top_tracks = sp.current_user_top_tracks(time_range='medium_term', limit=50)

        track_id_ls = []
        track_name_ls = []
        track_release_ls = []
        artist_name_ls = []
        pop_ls = []

        # Will use to get genre in artist call
        artist_url = []
        album_url = []


        for track in top_tracks['items']:
            track_id_ls.append(track['id'])
            track_name_ls.append(track['name'])
            track_release_ls.append(track['album']['release_date'])
            artist_name_ls.append(track['artists'][0]['name'])
            pop_ls.append(track['popularity'])
            artist_url.append(track['artists'][0]['external_urls']['spotify'])
            album_url.append(track['album']['external_urls']['spotify'])

        df = pd.DataFrame({'id':track_id_ls,
                  'track_name':track_name_ls,
                  'track_release':track_release_ls,
                  'artist_name':artist_name_ls,
                  'popularity':pop_ls})
        
        # Get track details
        track_features_ls = []

        for t_id in track_id_ls:
            track_features  = sp.audio_features(t_id)
            track_features_ls.append(track_features[0])

        track_features_df = pd.DataFrame(track_features_ls)

        df_main = df.merge(track_features_df, on='id', how='left')

        # Add a new column for track ranking
        df_main['track_rank'] = range(1, len(df_main) + 1)

        # Get genre
        artist_genre_ls = []
        for art_url in artist_url:
            artist = sp.artist(art_url)
            artist_genre_ls.append(artist['genres'])

        artist_genre_ls2 = []

        # Get the first genre of each list
        simplify_genre_ls = []

        for genre in artist_genre_ls:
            try:
                simplify_genre_ls.append(genre[0])
            except IndexError:
                simplify_genre_ls.append('No Genre Data')


        # Test the regex patterns on sample genres
        for genre in simplify_genre_ls:
            artist_genre_ls2.append(simplify_genre(genre))
        
        df_main['genre'] = artist_genre_ls2

        # show raw table
        st.dataframe(df_main)

        # Visualizations
        # Favorite Simplified Genres - Bar Chart
        favorite_genres = df_main['track_name'].groupby(df_main['genre']).count().reset_index()
        favorite_genres = favorite_genres.rename(columns={'track_name': 'count'})
        favorite_genres = favorite_genres.sort_values('count', ascending=False)

        fig1 = px.bar(favorite_genres, x='Genre', y='Count', title='Top Favorite Simplified Genres')
        st.plotly_chart(fig1)
        
        # Danceability vs. Energy - Scatter Plot
        fig2 = px.scatter(df_main, x='Danceability', y='Energy', hover_data=['track_name', 'artist_name'],
                  title='Danceability vs. Energy of Listened Tracks')
        st.plotly_chart(fig2)

        # List of audio features for the box plot
        audio_features = ['danceability', 'energy', 'valence']

        # Create the Track Analysis Distribution using a Box Plot
        fig3 = px.box(df_main, y=audio_features, title='Track Analysis Distribution',
                    labels={'variable': 'Audio Features', 'value': 'Value'},
                    boxmode='group'  # 'group' for side-by-side boxes, 'overlay' for overlapping boxes
                    )
        st.plotly_chart(fig3)

        # Download table to csv
        today = datetime.today().strftime('%Y%m%d')

        csv = convert_df(df_main)
        st.download_button(
        "Press to Download",
        csv,
        f"{today}_SpotifyUserData.csv",
        "text/csv",
        key='download-csv'
        )

        # Fetch and display the user's top tracks
    

    else:
        st.error("Authentication failed. Please check your credentials and scope.")
        st.warning("Make sure you set the correct CLIENT_ID and CLIENT_SECRET.")




# if "code" in st.session_state:
#         # User has returned with the authorization code
#         code = st.session_state.code
#         # Get access token using the code
#         access_token = sp.get_access_token(as_dict=False)
#         # Get user's display name and show it
#         user = sp.current_user()
#         st.write(f"Logged in as: {user['display_name']}")

# def get_access_token():
#     access_token = sp_oauth.get_access_token(as_dict=False)
#     return access_token


# Get the access token
# access_token = get_access_token()

# Check if the token was successfully obtained
# if access_token:
#     # Use the access token to authenticate Spotipy
#     sp = spotipy.Spotify(auth=access_token)

#     # Fetch and display the user's saved tracks
#     st.header("Your Saved Tracks")
#     results = sp.current_user_saved_tracks()
#     for item in results['items']:
#         track = item['track']
#         st.write(f"{track['name']} - {track['artists'][0]['name']}")

#     else:
#         st.error("Authentication failed. Please check your credentials and scope.")
#         st.warning("Make sure you set the correct CLIENT_ID and CLIENT_SECRET.")


# Authenticate with Spotify using Spotipy
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
#                                                client_secret=CLIENT_SECRET,
#                                                redirect_uri=REDIRECT_URI,
#                                                scope='user-read-recently-played'))


# # ---- HEADER SECTION ----
# with st.container():
#     st.title("LISTR")

# with st.container():
#     st.title("Your Spotify Song Data")
#     if st.button("Log in with Spotify"):
#         # Redirect user to Spotify login page
#         auth_url = sp.auth_manager.get_authorize_url()
#         st.markdown(f"[Click here to log in with Spotify]({auth_url}), {auth_url}")
#         st.write(st.session_state)
#         print("Callback URL:", st.session_state.url)
#     if "code" in st.session_state:
#         # User has returned with the authorization code
#         code = st.session_state.code
#         st.write(code)
#         # Get access token using the code
#         sp.auth_manager.get_access_token(code)
#         # Get user's display name and show it
#         user = sp.current_user()
#         st.write(f"Logged in as: {user['display_name']}")
