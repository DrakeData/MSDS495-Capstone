# MSDS498-Capstone
This repository contains the code used for MSDS 498 Capstone Project.

**Lister App URL:** https://msds498-listr-tac4cnsusq-uc.a.run.app/

## Table of Contents
- [Introduction](#introduction)
- [About the Data](#about-the-data)
- [Requirements](#requirements)
- [Project Details](#project-details)
- [Project Limitations](#project-limitations)
- [Future Enhancements](#future-enhancements)
- [References](#references)
- [Project Owners](#project-owners)

## Introduction
![listr_logo](images/Listr_Logo.svg)

Streaming has become the primary listening format for music in the last decade. It has grown at an average rate of 43.9% since 2014 with an annual revenue of $13.7B in the United States alone in 2022 [[1]](#1). With any highly profitable business, there are bound to be many competitors vying for their own share. Spotify currently dominates the global music streaming market share at 32% in 2021, but that is on the decline as they were at 34% in 2019 [[2]](#2). The market is oversaturated-- Amazon Music and YouTube Music increased their subscriber count by 25% and 50% respectively in 2021.

Our current objective with our AI music streaming venture, Listr – The AI Music Streaming Add-On App, is to develop an accompanying application that seamlessly aligns with the preferences of Spotify users. Listr capitalizes on the capabilities of AI-based personalization to curate distinct playlists and enhance the social user interaction, all while operating within the confines of Spotify's established structure. This document serves as an introduction to our aims, achievements, data origins, challenges faced, and recommendations that lie ahead.

## About the Data

|<div style="width:100px">Data Set</div>|Description|
|:-------------------------------------:|:----------|
|<img align="left" src="images/spotify_api.png"> | [The Spotify Web API](https://developer.spotify.com/documentation/web-api) [[3]](#3) empowers the development of applications that seamlessly interact with Spotify's streaming service. It enables retrieving content metadata, accessing recommendations, managing playlists, and controlling playback functionalities. |
| <img align="left" src="images/genius_logo.png"> | [The Lyric Genius API](https://docs.genius.com/) [[4]](#4), which is associated with the Genius platform, provides developers with programmatic access to song lyrics, annotations, and related metadata. This includes features like retrieving lyrics, displaying annotations, searching for songs, and integrating these elements into applications or services. |


## Requirements
- Access to [Spotify's API](https://developer.spotify.com/documentation/web-api)
    - You will need to follow [these instructions](https://docs.google.com/document/d/1jyA7lVMDGPY58dkp6uqyZzQIvDeGvZ6be5VlswqpvPg/edit) to get your Client ID and Client Secret API Keys
- Access to [LyricsGenius API](https://lyricsgenius.readthedocs.io/en/master/index.html)
    - Sign up for a (free) account that authorizes access to [the Genius API](https://genius.com/signup_or_login).
    - Go to the API section on Genius and [create a new API client](https://genius.com/api-clients/new).
    - After creating your client, you can generate an access token to use with the library.
    
Create a config.py to contain all of your API Keys, it should include:
- SPOTIFY_CLIENT_KEY = "YOUR_SPOTIFY_CLIENT_KEY"
- SPOTIFY_SECRET_KEY = "YOUR_SPOTIFY_SECRET_KEY"
- LG_TOKEN = "YOUR_LYRICSGENIUS_USER_TOKEN"

Save config.py file in app directory

## Project Details
All details for this project can be found in the project_reports repository.

01. [Listr Project Goals](https://github.com/DrakeData/MSDS498-Capstone/blob/main/project_reports/01.%20Listr%20Project%20Goals.pdf)
    - This document outlines our project's objectives, methodology, and expected deliverables to provide a clear understanding of our approach and its potential impact on the organization. We aim to achieve specific goals by conducting a comprehensive analysis using data-driven techniques and advanced analytic tools.

02. [Lister Initial Findings](https://github.com/DrakeData/MSDS498-Capstone/blob/main/project_reports/02.%20Listr%20Initial%20Findings.pdf)
    - This document provides an update on the progress of our consulting project, detailing our initial findings, accomplishments, and addressing concerns regarding expenditure. We are committed to delivering meaningful results aligned with the organization's goals and ensuring efficient resource utilization.

03. Final Report (Coming Soon)
    - This will be the final report that is turned in with problem statement, analysis, graphs, recommendations, and everything else.

## Project Limitations
### Data Issues
In an earlier report, The Million Song Dataset [[5]](#5) was initially scoped out to be the primary choice due to its number of tracks and robust data features. While this dataset initially provided great promise, it ended up being shelved due to data integrity issues. Because of this, it was decided to promote the Spotify dataset to the primary source. 

MusixMatch [[6]](#6) was originally chosen to be used alongside the Million Song Dataset, but upon further investigation, the lyrics are not full texts but rather a bag-of-words which is not usable for our intended purpose. 

### API Limitations
When integrating the Spotify API with Streamlit, we observed a problem related to accessing the redirect URL for Spotify authentication. This issue arises when the authentication attempt triggers the opening of the redirect URL in a separate tab. Our current focus is on addressing this matter by developing a solution that enables the redirection URL to open within the confines of the List application itself.


## Future Enhancements
- Chatbot: Allows app users to ask a chatbot for recommendations based on similar songs, artists, moods, or activities.
- Song Recs: The current recommendation engine is solely based on Spotify's API. There are additional internal models in the works that will enhance those recommendations.
- Clusters: There will be clustering functionalities that will allow users to compare albums, artists, and more.
- User Data: Users will be able to seamlessly log into their Spotify account and extract their user data, generate user reports, and get recommendations based on their activity.

## References
<a id="1">[1]</a>
David Curry, “Music Streaming App Revenue and Usage Statistics (2023),” Business of Apps, May 2, 2023, https://www.businessofapps.com/data/music-streaming-market/.

<a id="2">[2]</a>
“Music Streaming Market Share and Revenue Statistics: Details on the Biggest Music Streaming Services,” SiriusXM Music for Business, January 27, 2023, https://sxmbusiness.com/music-streaming-market-share-and-revenue-statistic.

<a id="3">[3]</a>
“Spotify API,” Web API | Spotify for Developers, accessed July 8, 2023, https://developer.spotify.com/documentation/web-api.

<a id="4">[4]</a>
“Genius API Documentation.” Genius API. Accessed August 6, 2023. https://docs.genius.com/.

<a id="5">[5]</a>
Million Song Dataset, accessed July 8, 2023, http://millionsongdataset.com/.

<a id="6">[6]</a>
“Build with Lyrics.” Musixmatch Developer. Accessed July 8, 2023. https://developer.musixmatch.com/. 

## Project Owners
- [Grace Chen](https://github.com/grchen99)
- Patrick
- [Nicholas Drake](https://github.com/DrakeData)
- [Olushola Durojaiye](https://github.com/oluduroj)
- [Lena Lu](https://github.com/lenaxlu)

Repository created: 7/11/2023
