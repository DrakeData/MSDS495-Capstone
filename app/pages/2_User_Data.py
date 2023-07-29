import streamlit as st
import pandas as pd
import numpy as np
import requests
import spotipy
import os
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from PIL import Image
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_KEY, SPOTIFY_SECRET_KEY
import urllib.parse

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


st.title("Your Spotify Song Data")
# Display the login button
if st.button("Login to Spotify"):
    # Get the access token using SpotifyOAuth
    access_token = sp_oauth.get_access_token(as_dict=False)

    # Check if the token was successfully obtained
    if access_token:
        # Use the access token to authenticate Spotipy
        sp = spotipy.Spotify(auth_manager=sp_oauth)

        # Fetch and display the user's saved tracks
        st.header("Your Saved Tracks")
        results = sp.current_user_saved_tracks()
        for item in results['items']:
            track = item['track']
            st.write(f"{track['name']} - {track['artists'][0]['name']}")

        # Fetch and display the user's top tracks
        st.header("Your Top Tracks")
        top_tracks = sp.current_user_top_tracks(time_range='medium_term', limit=10)
        for track in top_tracks['items']:
            st.write(f"{track['name']} - {track['artists'][0]['name']}")

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
