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
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIFY_CLIENT_KEY, SPOTIFY_SECRET_KEY

# ---- MAIN TAB SECTION ----
# emoji cheatsheet: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
    page_title="MSDS 498: Capstone Project", 
    page_icon=":musical_note:", 
    layout="wide"
    )

# Spotify API Authentication
auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_KEY, client_secret=SPOTIFY_SECRET_KEY)
sp = spotipy.Spotify(auth_manager=auth_manager)

# ---- HEADER SECTION ----
with st.container():
    st.title("LISTR")

# Create Sidebar
search_options = ["Track", "Artist", "Album"]
search_selected = st.sidebar.selectbox("Search Choise: ", search_options)

# user interactive search
search_keyword = st.text_input(f"{search_selected} (Type in {search_selected} name)")
button_clicked = st.button("Search")

# Pull Spotify Data
search_results = []
tracks = []
artists = []
albums = []
if search_keyword is not None and len(str(search_keyword)) > 0:
    # Track search
    if search_selected == 'Track':
        st.write("Searching track...")
        tracks = sp.search(q=f"track:{search_keyword}", type='track', limit=20)
        tracks_list = tracks['tracks']['items']
        if len(tracks_list) > 0:
            for track in tracks_list:
                # st.write(f"{track['name']} By {track['artists'][0]['name']}")
                search_results.append(f"{track['name']} By {track['artists'][0]['name']}")
    # Artist search
    elif search_selected == 'Artist':
        st.write("Searching artist...")
        artists = sp.search(q=f"artist:{search_keyword}", type='artist', limit=20)
        artists_list = artists['artists']['items']
        if len(artists_list) > 0:
            for artist in artists_list:
                # st.write(artist['name'])
                search_results.append(artist['name'])

    # Album search
    elif search_selected == 'Album':
        st.write("Searching album...")
        albums = sp.search(q=f"album:{search_keyword}", type='album', limit=20)
        albums_list = albums['albums']['items']
        if len(albums_list) > 0:
            for album in albums_list:
                # st.write(f"{album['name']} By {album['artists'][0]['name']}")
                search_results.append(f"{album['name']} By {album['artists'][0]['name']}")

# Create clean search result list
search_results_clean = list(dict.fromkeys(search_results))

selected_album = None
selected_artist = None
selected_track = None
if search_selected == 'Track':
    selected_track = st.selectbox(f"Select your track: ", search_results_clean)
elif search_selected == 'Artist':
    selected_artist = st.selectbox("Select your artist: ", search_results_clean)
elif search_selected == 'Album':
    selected_album = st.selectbox("Select your album: ", search_results_clean)


#### TRACK DATA ####
with st.container():
    # clear album images from directory
    dir = 'images/album_img'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    # Visualize track data
    if selected_track is not None and len(tracks) > 0:
        tracks_list = tracks['tracks']['items']
        track_id = None
        if len(tracks_list) > 0:
            for track in tracks_list:
                str_temp = f"{track['name']} By {track['artists'][0]['name']}"
                if str_temp == selected_track:
                    track_id = track['id']
                    track_album = track['album']['name']
                    album_img_url = track['album']['images'][1]['url']

                    # Save album image
                    r = requests.get(album_img_url)
                    open(f"images/album_img/{track_id}.jpg", "wb").write(r.content)

        selected_track_choice = None            
        if track_id is not None:
            image = Image.open(f"images/album_img/{track_id}.jpg")
            st.image(image)
            track_choices = ['Song Features', 'Similar Songs Recommendation']
            selected_track_choice = st.selectbox('Please select track option: ', track_choices)        
            if selected_track_choice == 'Song Features':
                track_features  = sp.audio_features(track_id) 
                df = pd.DataFrame(track_features, index=[0])
                df_features = df.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
                st.dataframe(df_features)

                labels = list(df_features)[:]
                stats = df_features.mean().tolist()

                angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)

                # close the plot
                stats = np.concatenate((stats,[stats[0]]))
                angles = np.concatenate((angles,[angles[0]]))

                #Size of the figure
                fig = plt.figure(figsize = (18,18))

                ax = fig.add_subplot(221, polar=True)
                ax.plot(angles, stats, 'o-', linewidth=2, label = "Features", color= 'gray')
                ax.fill(angles, stats, alpha=0.25, facecolor='gray')
                ax.set_thetagrids(angles[0:7] * 180/np.pi, labels , fontsize = 13)


                ax.set_rlabel_position(250)
                plt.yticks([0.2 , 0.4 , 0.6 , 0.8  ], ["0.2",'0.4', "0.6", "0.8"], color="grey", size=12)
                plt.ylim(0,1)

                plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))
                
                st.pyplot(plt)

            elif selected_track_choice == 'Similar Songs Recommendation':
                # Get Spotify token
                url = "https://accounts.spotify.com/api/token"
                headers = {}
                data = {}
                message = f"{SPOTIFY_CLIENT_KEY}:{SPOTIFY_SECRET_KEY}"
                messageBytes = message.encode('ascii')
                base64Bytes = base64.b64encode(messageBytes)
                base64Message = base64Bytes.decode('ascii')
                headers['Authorization'] = "Basic " + base64Message
                data['grant_type'] = "client_credentials"
                r = requests.post(url, headers=headers, data=data)
                token = r.json()['access_token']

                # Get track recomendation
                limit = 10
                recUrl = f"https://api.spotify.com/v1/recommendations?limit={limit}&seed_tracks={track_id}"

                headers = {
                    "Authorization": "Bearer " + token
                }

                res = requests.get(url=recUrl, headers=headers)
                similar_songs_json = res.json()

                recommendation_list = similar_songs_json['tracks']
                recommendation_list_df = pd.DataFrame(recommendation_list)
                # st.dataframe(recommendation_list_df)

                # Get recommended artist
                rec_artist_ls = []

                for i in range(len(similar_songs_json['tracks'])):
                    rec_artist_ls.append(similar_songs_json['tracks'][i]['artists'][0]['name'])

                recommendation_list_df['artist'] = rec_artist_ls
                
                recommendation_df = recommendation_list_df[['name', 'artist', 'explicit', 'duration_ms', 'popularity']]
                st.dataframe(recommendation_df)
        else:
            st.write("Please select a track from the list")

    #### ALBUM DATA ####
    elif selected_album is not None and len(albums) > 0:
        albums_list = albums['albums']['items']
        album_id = None
        album_uri = None    
        album_name = None
        if len(albums_list) > 0:
            for album in albums_list:
                str_temp = f"{album['name']} By {album['artists'][0]['name']}"
                if selected_album == str_temp:
                    album_id = album['id']
                    album_uri = album['uri']
                    album_name = album['name']
        if album_id is not None and album_uri is not None:
            st.write(f"Collecting all the tracks for the album: {album_name}")
            album_tracks = sp.album_tracks(album_id)
            df_album_tracks = pd.DataFrame(album_tracks['items'])
            # st.dataframe(df_album_tracks)
            df_tracks_min = df_album_tracks.loc[:,
                            ['id', 'name', 'duration_ms', 'explicit', 'preview_url']]
            # st.dataframe(df_tracks_min)
            for idx in df_tracks_min.index:
                with st.container():
                    col1, col2, col3, col4 = st.columns((4,4,1,1))
                    col11, col12 = st.columns((8,2))
                    col1.write(df_tracks_min['id'][idx])
                    col2.write(df_tracks_min['name'][idx])
                    col3.write(df_tracks_min['duration_ms'][idx])
                    col4.write(df_tracks_min['explicit'][idx])   
                    if df_tracks_min['preview_url'][idx] is not None:
                        col11.write(df_tracks_min['preview_url'][idx])  
                        with col12:   
                            st.audio(df_tracks_min['preview_url'][idx], format="audio/mp3")