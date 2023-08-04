import streamlit as st
import pandas as pd
import numpy as np
import requests
import spotipy
import os
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import textwrap
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

# ---- REMOVE SIDEBAR EXTRA SPACING UPTOP ----
st.markdown("""
  <style>
    div.css-1pd56a0.e1tzin5v0 {
      margin-top: -75px;
    }
  </style>
""", unsafe_allow_html=True)


# ---- REMOVE MAIN PAGE EXTRA SPACING UPTOP ----
st.markdown("""
        <style>
               .sidebar-content {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                }
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)

# Functions
def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)

# SVG Logo
logo_svg = """
        <svg width="400px" height="150px" viewBox="0 0 757.15 289" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	  style="enable-background:new 0 0 757.15 289;" xml:space="preserve">
<g>
	<path d="M736.79,198.01c-5.63-12.99-11.14-26.04-17.02-38.93c-2.11-4.63-2.64-7.55,1.97-11.66c4.05-3.6,7.17-9.5,8.25-14.88
		c1.45-7.17,1.49-14.97,0.42-22.24c-2.01-13.68-10.62-21.69-24.45-23.01c-10.58-1.01-21.29-0.5-31.92-1.06
		c-4.62-0.24-5.93,1.22-5.9,5.84c0.21,32.99,0.16,65.99,0.19,98.98c0.01,12.42,0.01,12.46,12.23,12.39
		c10.73-0.06,9.19,1.04,9.25-9.38c0.07-11.96,0.02-23.92,0.02-35.75c7.13-1.79,7.74-1.5,10.18,4.56
		c4.92,12.21,9.75,24.45,14.87,36.58c0.68,1.62,2.74,3.64,4.29,3.75c6.11,0.43,12.28,0.18,19.61,0.18
		C737.92,201.03,737.43,199.48,736.79,198.01z M689.77,138.47c0-10.35-0.05-20.47,0.09-30.58c0.01-0.97,1.08-2.52,1.95-2.78
		c8.88-2.61,16.92,2.94,17.9,12.2c0.17,1.65,0.25,3.32,0.23,4.98C709.77,135.44,703.83,140.43,689.77,138.47z"/>
	<path d="M565.4,140.06c-4.86-3.47-9.81-6.98-13.99-11.19c-5.36-5.4-5.83-14.87-1.85-20.35c3.31-4.56,9.64-5.48,17.41-2.48
		c1.55,0.6,3.02,1.4,4.55,2.04c1.15,0.48,2.35,0.86,3.75,1.37c1.97-4.69,3.65-9.02,5.6-13.23c1.16-2.52,0.58-3.94-1.86-5.14
		c-7.6-3.75-15.58-6.03-24.06-5.61c-11.92,0.6-21.11,5.88-26.04,17.12c-6.74,15.37-2.34,34.09,10.45,44.99
		c2.91,2.48,6.29,4.41,9.12,6.96c3.8,3.43,7.86,6.82,10.75,10.96c3.43,4.91,3.57,10.81,0.46,16.1c-3.16,5.38-8.7,6.09-14.11,4.96
		c-5.15-1.08-10.09-3.18-15.08-4.94c-1.65-0.58-3.18-1.53-5.6-2.72c0,6.14,0.18,11.42-0.06,16.68c-0.15,3.22,1.22,4.9,4.04,5.98
		c8.7,3.34,17.66,4.78,26.94,3.71c15.28-1.77,23.56-9.7,26.29-24.87C585.16,163.34,579.4,150.06,565.4,140.06z"/>
	<path d="M651.98,86.47c-19.82-0.17-39.64-0.14-59.46,0.04c-1.05,0.01-2.93,1.75-2.99,2.77c-0.31,5.1-0.14,10.23-0.14,15.97
		c5.94,0,11.24,0.28,16.51-0.08c4.59-0.32,5.93,1.22,5.91,5.85c-0.18,28.65-0.05,57.3-0.02,85.94c0,1.96,0,3.92,0,6.17
		c7.34,0,14.07,0,21.39,0c0-2.37,0-4.33,0-6.3c-0.03-27.65-0.08-55.3-0.08-82.95c0-9.79-1-8.61,8.4-8.65
		c15.6-0.06,15.67-0.04,13.68-15.69C655.03,88.36,653.1,86.48,651.98,86.47z"/>
	<path d="M462.19,184.86c-6.32,0.24-12.65,0.08-18.98,0.08c-6.66,0-6.66,0-6.67-6.76c-0.03-28.64-0.15-57.27-0.02-85.91
		c0.02-4.29-1.1-6.14-5.6-5.7c-3.46,0.34-7.01,0.34-10.48,0.02c-4.41-0.41-5.64,1.2-5.61,5.6c0.2,35.3,0.14,70.59,0.16,105.89
		c0,1.62,0,3.24,0,5.31c2.32,0.12,4.1,0.28,5.89,0.28c10.66,0.02,21.31,0,31.97-0.01c14.29,0,14.2,0,13.9-14.15
		C466.68,186.16,465.78,184.72,462.19,184.86z"/>
	<path d="M490.42,86.41c-4.63-0.39-5.9,1.26-5.87,5.85c0.21,35.33,0.15,70.66,0.2,105.99c0,1.62,0.17,3.23,0.26,4.9
		c6.78,0,13.14,0,19.47,0c0-38.94,0-77.4,0-116.66C499.36,86.49,494.86,86.79,490.42,86.41z"/>
</g>
<path d="M315.04,145.44c0,43.65,0.02,87.31-0.07,130.96c0,1.81-1.09,3.61-1.68,5.42c-0.62-1.78-1.77-3.56-1.77-5.34
	c-0.09-87.48-0.08-174.95-0.08-262.43c0-0.17-0.05-0.35,0.01-0.5c0.59-1.67,1.19-3.34,1.79-5c0.6,1.64,1.72,3.28,1.72,4.92
	C315.06,57.46,315.04,101.45,315.04,145.44z"/>
<g>
	<path d="M155.85,121.19c-20.49-0.03-40.99-0.01-61.48-0.01c-20.66,0-41.33,0.4-61.98-0.16c-11.36-0.3-19.57,9.65-19.43,19.44
		c0.4,27.15,0.49,54.32-0.03,81.47c-0.22,11.63,8.76,20.43,20.14,20.32c40.82-0.4,81.64-0.13,122.47-0.17
		c12.94-0.01,19.45-6.45,19.48-19.33c0.07-27.49,0.07-54.99-0.01-82.48C174.98,127.64,168.45,121.22,155.85,121.19z M161.94,222.47
		c-0.01,5.86-0.74,6.57-6.69,6.57c-20.32,0.03-40.64,0.01-60.96,0.01c-19.99,0-39.97,0.01-59.96,0c-7.02,0-7.52-0.47-7.52-7.27
		c-0.02-26.81-0.02-53.63,0-80.44c0-6.36,0.84-7.21,7.2-7.22c40.3-0.02,80.61-0.02,120.91,0c6.09,0,7.01,0.91,7.01,6.91
		C161.96,168.17,161.96,195.32,161.94,222.47z"/>
	<path d="M228.79,178.48c0.02-30.65,0.04-61.3,0-91.94c-0.01-12.82-6.62-19.42-19.32-19.43c-22.82-0.02-45.64,0-68.46,0
		c-23.15,0-46.3,0-69.46,0c-1.5,0-3.04-0.15-4.49,0.13c-3.71,0.72-6.03,2.95-5.89,6.87c0.13,3.68,2.28,5.8,5.98,6.12
		c1.99,0.17,3.99,0.17,5.99,0.17c44.97,0.01,89.94,0,134.92,0.01c7.24,0,7.63,0.4,7.64,7.61c0.01,29.82-0.01,59.63,0.03,89.45
		c0,2.14-0.27,4.77,0.81,6.3c1.34,1.89,4,3.99,6.02,3.92c1.99-0.07,4.25-2.46,5.72-4.34C229.13,182.25,228.79,180.13,228.79,178.48z
		"/>
	<path d="M182.39,94.19c-22.82-0.02-45.64-0.01-68.46-0.01c-23.15,0-46.3-0.01-69.46,0.01c-1.82,0-4.21-0.47-5.34,0.47
		c-2.06,1.72-4.33,4.17-4.76,6.62c-0.57,3.24,1.95,5.5,5.43,5.89c1.98,0.22,3.99,0.22,5.98,0.22c45.14,0.01,90.28,0,135.42,0.02
		c7.19,0,7.74,0.56,7.75,7.61c0.01,29.65,0,59.3,0.01,88.94c0,1.66-0.09,3.35,0.16,4.99c0.52,3.49,2.33,5.89,6.15,6.03
		c3.86,0.14,5.72-2.25,6.5-5.66c0.29-1.28,0.27-2.64,0.27-3.97c0.01-30.48,0.04-60.96-0.01-91.44
		C202.01,100.66,195.52,94.2,182.39,94.19z"/>
	<path d="M116.63,174.88c-10.49-6.11-21.04-12.12-31.64-18.06c-6.75-3.78-11.36-1.04-11.52,6.82c-0.12,5.99-0.02,11.98-0.02,17.97
		c0,6.16-0.14,12.32,0.04,18.47c0.22,7.19,4.89,9.96,11.09,6.55c10.78-5.94,21.51-11.98,32.17-18.13
		C123.68,184.5,123.62,178.96,116.63,174.88z"/>
</g>
</svg>
    """

# Spotify API Authentication
auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_KEY, client_secret=SPOTIFY_SECRET_KEY)
sp = spotipy.Spotify(auth_manager=auth_manager)

# ---- HEADER SECTION ----
with st.container():
    render_svg(logo_svg)

# Create Sidebar
search_options = ["Track", "Artist", "Album"]
search_selected = st.sidebar.selectbox("Search Options: ", search_options)

if search_selected == "Track":
    # User interactive search
    left_col, right_col = st.columns(2)
    with left_col:
        search_keyword = st.text_input(f"{search_selected} (Type in {search_selected} name)")
    with right_col:
        artist_name_search = st.text_input(f"Type in Artist name (optional)")
    button_clicked = st.button("Search")
else:
    # user interactive search minus artist search option
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
        artist_query = f" artist:{artist_name_search}" if artist_name_search else ""
        tracks = sp.search(q=f"track:{search_keyword}{artist_query}", type='track', limit=20)
        tracks_list = tracks['tracks']['items']
        if len(tracks_list) > 0:
            for track in tracks_list:
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
        #### ARTIST DATA ####
    elif search_selected == 'Artist':
        st.write("Start artist search")
        artists = sp.search(q='artist:'+ search_keyword,type='artist', limit=20)
        artists_list = artists['artists']['items']
        if len(artists_list) > 0:
            for artist in artists_list:
                # st.write(artist['name'])
                search_results.append(artist['name'])
        if selected_artist is not None and len(artists) > 0:
            artists_list = artists['artists']['items']
            artist_id = None
            artist_uri = None
            selected_artist_choice = None
            if len(artists_list) > 0:
                for artist in artists_list:
                    if selected_artist == artist['name']:
                        artist_id = artist['id']
                        artist_uri = artist['uri']
            
            if artist_id is not None:
                artist_choice = ['Albums', 'Top Songs']
                selected_artist_choice = st.selectbox('Select artist choice', artist_choice)
                        
            if selected_artist_choice is not None:
                if selected_artist_choice == 'Albums':
                    artist_uri = 'spotify:artist:' + artist_id
                    album_result = sp.artist_albums(artist_uri, album_type='album') 
                    all_albums = album_result['items']
                    col1, col2, col3 = st.columns((6,4,2))
                    for album in all_albums:
                        col1.write(album['name'])
                        col2.write(album['release_date'])
                        col3.write(album['total_tracks'])
                elif selected_artist_choice == 'Top Songs':
                    artist_uri = 'spotify:artist:' + artist_id
                    top_songs_result = sp.artist_top_tracks(artist_uri)
                    for track in top_songs_result['tracks']:
                        st.write(track['id'])
                        with st.container():
                            col1, col2, col3, col4 = st.columns((4,4,2,2))
                            col11, col12 = st.columns((10,2))
                            col21, col22 = st.columns((11,1))
                            col31, col32 = st.columns((11,1))
                            col1.write(track['id'])
                            col2.write(track['name'])
                            if track['preview_url'] is not None:
                                col11.write(track['preview_url'])  
                                with col12:   
                                    st.audio(track['preview_url'], format="audio/mp3")  
                            with col3:
                                def feature_requested():
                                    track_features  = sp.audio_features(track['id']) 
                                    df = pd.DataFrame(track_features, index=[0])
                                    df_features = df.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
                                    with col21:
                                        st.dataframe(df_features)
                                    with col31:
                                        labels= list(df_features)[:]
                                        stats= df_features.mean().tolist()
                                        
                                        angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)
                                        
                                        # close the plot
                                        stats=np.concatenate((stats,[stats[0]]))
                                        angles=np.concatenate((angles,[angles[0]]))
                                        
                                        # Size of the figure
                                        fig=plt.figure(figsize = (18,18))
                                        ax = fig.add_subplot(221, polar=True)
                                        ax.plot(angles, stats, 'o-', linewidth=2, label = "Features", color= 'gray')
                                        ax.fill(angles, stats, alpha=0.25, facecolor='gray')
                                        ax.set_thetagrids(angles[0:7] * 180/np.pi, labels , fontsize = 13)
                                        ax.set_rlabel_position(250)

                                        plt.yticks([0.2 , 0.4 , 0.6 , 0.8  ], ["0.2",'0.4', "0.6", "0.8"], color="grey", size=12)
                                        plt.ylim(0,1)
                                        plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))
                                        
                                        st.pyplot(plt)
                                    
                                feature_button_state = st.button('Track Audio Features', key=track['id'], on_click=feature_requested)
                            with col4:
                                st.write("WIP")
                                # def similar_songs_requested():
                                #     token = songrecommendations.get_token(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
                                #     similar_songs_json = songrecommendations.get_track_recommendations(track['id'], token)
                                #     recommendation_list = similar_songs_json['tracks']
                                #     recommendation_list_df = pd.DataFrame(recommendation_list)
                                #     recommendation_df = recommendation_list_df[['name', 'explicit', 'duration_ms', 'popularity']]
                                #     with col21:
                                #         st.dataframe(recommendation_df)
                                #     with col31:
                                #         songrecommendations.song_recommendation_vis(recommendation_df)

                                # similar_songs_state = st.button('Similar Songs', key=track['id'], on_click=similar_songs_requested)
                            # st.write('----')