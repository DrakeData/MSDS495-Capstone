import streamlit as st
import pandas as pd
import spotipy
import base64
from sklearn.cluster import KMeans
import plotly.express as px
from PIL import Image
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
# from config import SPOTIFY_CLIENT_KEY, SPOTIFY_SECRET_KEY


# ---- MAIN TAB SECTION ----
# emoji cheatsheet: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
    page_title="MSDS 498: Capstone Project", 
    page_icon=":musical_note:", 
    layout="centered",
    initial_sidebar_state="collapsed"
    )

# ---- Hide Sidebar ----
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

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

def GetPlaylistTrackDetails(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    track_id_ls = []
    track_name_ls = []
    artist_name_ls = []
    album_name_ls = []
    popularity_ls = []
    release_date_ls = []

    for i in range(len(results['items'])):
        track_id_ls.append(results['items'][i]['track']['id'])
        track_name_ls.append(results['items'][i]['track']['name'])
        artist_name_ls.append(results['items'][i]['track']['artists'][0]['name'])
        album_name_ls.append(results['items'][i]['track']['album']['name'])
        popularity_ls.append(results['items'][i]['track']['popularity'])
        release_date_ls.append(results['items'][i]['track']['album']['release_date'])

    zipped = list(zip(track_id_ls, track_name_ls, artist_name_ls, album_name_ls, popularity_ls, release_date_ls))

    df = pd.DataFrame(zipped, columns=['track_id', 'track_name', 'artist', 'album', 'popularity', 'release_date'])
    
    # get track details
    # function to divide a list of uris (or ids) into chuncks of 50.
    chunker = lambda y, x: [y[i : i + x] for i in range(0, len(y), x)]

    # using the function
    track_chunks = chunker(track_id_ls, 100)

    # Get track details
    track_features_ls = []

    for t_id in track_chunks:
        track_features  = sp.audio_features(t_id)
        track_features_ls.append(track_features)

    track_features_df = pd.DataFrame(track_features_ls[0])
    track_features_df = track_features_df.rename(columns={'id':'track_id'})

    df_main = df.merge(track_features_df, on='track_id', how='left')
    
    return df_main

# SVG Logo
logo_svg = """
        <svg width="250px" height="75px" fill="#ffffff" viewBox="0 0 757.15 289" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
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
# auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_KEY, client_secret=SPOTIFY_SECRET_KEY)

SPOTIFY_CLIENT_KEY = st.secrets["SPOTIFY_CLIENT_KEY"]
SPOTIFY_SECRET_KEY = st.secrets["SPOTIFY_SECRET_KEY"]

auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_KEY, client_secret=SPOTIFY_SECRET_KEY)
sp = spotipy.Spotify(auth_manager=auth_manager)

# ---- HEADER SECTION ----
with st.container():
    left_col, right_col = st.columns([1,2])
    with left_col:
        render_svg(logo_svg)
    with right_col:
        search_page = option_menu(
            menu_title=None,
            options=["Search", "User Data", "Playlist"],
            icons=["search", "person-circle", "vinyl"],
            menu_icon="cast",
            default_index=2,
            orientation="horizontal",
            styles={
        "container": {"padding": "0!important", "text-align": "center"},
        "icon": {"color": "orange", "font-size": "18px"}, 
        "nav-link": {"font-size": "15px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
        # "nav-link-selected": {"background-color": "green"},
    }
    )
        if search_page == "Search":
            switch_page("homepage")
        if search_page == 'User Data':
            switch_page("User Data")
        # if search_page == 'Playlist':
        #     switch_page("Playlist")

with st.container():
    st.title("Playlist Comparison")
    st.markdown('''
            Let's compare two Spotify playlist of your choosing. Please make sure that they are public playlist.
            
            In Spotify, go to the playlist and click the three '...' >> 'Share' >> 'Copy Link to Playlist'
            
            Copy and paste the URL link to the playlist in Listr.
                
            Sample URL: https://open.spotify.com/playlist/5Qnr7ct4jZ4ad1yDRuM1to?si=0bdc634e4b6c43f6

                ''')
   
with st.container():
    playlist1 = st.text_input(f"Enter Playlist 1 URL or Playlist ID")
    playlist2 = st.text_input(f"Enter Playlist 2 URL or Playlist ID")
    
    button_clicked = st.button("Analyze Playlist")

    if button_clicked and playlist1 is not None and playlist2 is not None:
        playlist1_id = playlist1.strip('https://open.spotify.com/playlist').split('?', 1)[0]
        playlist2_id = playlist2.strip('https://open.spotify.com/playlist').split('?', 1)[0]

        # st.write(f"Playlist1 ID: {playlist1_id}")
        # st.write(f"Playlist2 ID: {playlist2_id}")

        df1 = GetPlaylistTrackDetails(playlist1_id)
        df1['playlist_origin'] = 'playlist1'


        df2 = GetPlaylistTrackDetails(playlist2_id)
        df2['playlist_origin'] = 'playlist2'
    
        # Concatinating two playlists
        df = pd.concat([df1,df2], axis=0)

        # drop duplicates in playlist and reset's index
        df = df.drop_duplicates(subset='track_id').reset_index(drop=True)
        # st.dataframe(df)

        # MAKE MODEL
        df_model = df.drop(['track_id', 'track_name', 'album', 'artist', 
                            'release_date','type', 'uri', 'track_href', 'analysis_url', 
                            'duration_ms', 'time_signature', 'playlist_origin'], axis=1)
        # st.dataframe(dataset)

        # Create cluster
        model = KMeans(n_clusters=3)
        y_pred = model.fit_predict(df_model)

        # add cluster to new column
        df_model['cluster'] = y_pred

        # reindex
        df_model = df_model.reset_index(drop=True)

        grouped_df = df_model.groupby('cluster')
        # st.dataframe(grouped_df)

        mean_df = grouped_df.mean()
        mean_df = mean_df.reset_index()

        # Create filters
        pop_filter = mean_df[mean_df['cluster'] == 1]['popularity'].iloc[0]
        dance_filter = mean_df[mean_df['cluster'] == 1]['danceability'].iloc[0]
        valence_filter = mean_df[mean_df['cluster'] == 1]['valence'].iloc[0]
        energy_filter = mean_df[mean_df['cluster'] == 1]['energy'].iloc[0]
        # st.write(pop_filter, dance_filter, valence_filter, energy_filter)
        # Apply filters to each data frame and only return max 50 tracks from each playlist

        df1_update = df1[(df1['popularity']>= pop_filter) & (df1['danceability']>=dance_filter) & (df1['valence'].between(valence_filter-.20, valence_filter+.50)) & (df1['energy'].between(energy_filter-.20, energy_filter+.50))].reset_index(drop=True).sample(25, replace=True)
        df2_update = df2[(df2['popularity']>= pop_filter) & (df2['danceability']>=dance_filter) & (df2['valence'].between(valence_filter-.20, valence_filter+.50)) & (df2['energy'].between(energy_filter-.20, energy_filter+.50))].reset_index(drop=True).sample(25, replace=True)
        # st.write(f"playlist1: {len(df1_update['track_id'])}")
        # st.write(f"playlist2: {len(df2_update['track_id'])}")
        
        # Concatinating two playlists
        new_df = pd.concat([df1_update,df2_update], axis=0).sample(50)
        
        # Clean dataframe
        new_df = new_df.drop_duplicates()

        # Convert mill second to hours, minutes, seconds
        millis=new_df['duration_ms']
        new_df['track_duration'] = pd.to_datetime(millis, unit='ms').dt.strftime('%H:%M:%S')

        st.session_state.new_df = new_df
        st.dataframe(new_df, hide_index=True)

        # List of audio features for the box plot
        audio_features = ['danceability', 'energy', 'valence']

        # Create the Track Analysis Distribution using a Box Plot
        fig1 = px.box(new_df, y=audio_features, title='Track Analysis Distribution',
                    labels={'variable': 'Audio Features', 'value': 'Value'},
                    boxmode='group'  # 'group' for side-by-side boxes, 'overlay' for overlapping boxes
                    )
        st.plotly_chart(fig1)


    # Initialize st.session_state.new_df if not already initialized
    if 'new_df' not in st.session_state:
        st.session_state.new_df = None

    # Get track ID list
    if st.session_state.new_df is not None:
        track_ids_ls = st.session_state.new_df['track_id'].tolist()

        # Get the playlist name
        st.header("Like what you see?")
        st.write("If you have a spotify account, enter your playlist name and we'll add it to your playlist to share with others")
        st.write("This feature is currently in the process of being introduced.")

        playlist_name = st.text_input("Enter Playlist Name", key="playlist_name_input")

        # Create a playlist button
        button_clicked2 = st.button("Create Playlist")

        # Only create the playlist when the button is clicked
        if button_clicked2 and len(track_ids_ls) > 0 and playlist_name:

            # # Spotify API Authentication
            # CLIENT_ID = st.secrets["SPOTIFY_CLIENT_KEY"]
            # CLIENT_SECRET = st.secrets["SPOTIFY_SECRET_KEY"]
            # REDIRECT_URI = 'http://localhost:7777/callback'

            # # Define the scope for the required permissions
            # SCOPE = 'playlist-modify-public'

            # # Create the SpotifyOAuth object
            # sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
            #                         redirect_uri=REDIRECT_URI, scope=SCOPE)

            # # Get the access token using SpotifyOAuth
            # access_token = sp_oauth.get_access_token(as_dict=False)

            # # Use the access token to authenticate Spotipy
            # sp2 = spotipy.Spotify(auth_manager=sp_oauth)

            # # Create the playlist and add tracks
            # playlist = sp2.user_playlist_create(sp.me()["id"], f"{playlist_name}_listr", public=True)
            # sp2.playlist_add_items(playlist["id"], track_ids_ls)
            st.success(f"Playlist '{playlist_name}_listr' created with {len(track_ids_ls)} tracks!")
# Ad
st.image("https://raw.githubusercontent.com/DrakeData/MSDS498-Capstone/2367a792f89c807e2e2cb5f57c57e3f19c12dc7a/app/listr_premium_ad2.png")

left_col, center_col, right_col = st.columns([2, 1, 2])
with left_col:
    st.write("")
with center_col:
    st.write("© 2023 LISTR")
with right_col:
    st.write("")