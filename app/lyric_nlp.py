import re
import streamlit as st
import nltk
import matplotlib.pyplot as plt
from lyricsgenius import Genius
import pyLDAvis.gensim_models as gensimvis
from transformers import AutoTokenizer, T5ForConditionalGeneration
# from config import LG_TOKEN

from gensim.corpora import Dictionary
from gensim.corpora import MmCorpus
from gensim.models import LdaModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Retrieving and Classifying Lyrics
tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion", use_fast=False)
model = T5ForConditionalGeneration.from_pretrained("mrm8488/t5-base-finetuned-emotion")

# token = LG_TOKEN
token = st.secrests['LG_TOKEN']
genius = Genius(token, timeout = 200, verbose = False, excluded_terms=["(Remix)", "(Live)"], remove_section_headers = True)

def get_emotion(text):
    input_ids = tokenizer.encode(text + '</s>', return_tensors='pt', max_length = 512, truncation = True)

    output = model.generate(input_ids=input_ids,
               max_length=2)
  
    dec = [tokenizer.decode(ids) for ids in output]
    label = dec[0]
    return label

def song_emotion(track_name, artist):
    songs = genius.search_songs(track_name + ' ' + artist) #Finding all searches
    try:
        lyrics = genius.lyrics(song_url = songs['hits'][0]['result']['url']) #Returning the first song's lyrics
        lyrics = lyrics.split('Lyrics\n', 1)[1] #Removing the title
        lyrics = lyrics.split('Embed')[0] #Removing the end
        lyrics = lyrics.replace('\n', ' ') #Removing line breaks from string
        track_emotion = get_emotion(lyrics).split(' ')[1]
        st.write(f'Track Emotion: {track_emotion}')
    except:
        st.write('Track Emotion: Not Detected')

def get_lyrics_by_song(song, arr):
    try:
        songs = (genius.search_song(song, arr)).lyrics
        print(f"Songs grabbed.")
    except:
        print("exception")
    return songs

def remove_stop_words(text):
    stop_words = stopwords.words('english')
    new_stop_words = ['ooh', 'yeah', 'hey', 'whoa', 'woah', 'ohh', 'was', 'mmm', 'oooh', 'yah', 'yeh', 'mmm', 'hmm',
                      'deh', 'doh', 'jah', 'wa']
    stop_words.extend(new_stop_words)
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return filtered_sentence


def apply_lemmatization(text):
    lem = WordNetLemmatizer()
    word_list = word_tokenize(text)
    output = ' '.join([lem.lemmatize(w) for w in word_list])
    return output


# text preprocessing
def normalize(text):
    text = re.sub('[^a-zA-Z]', ' ', str(text))
    text = text.lower()
    text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)
    text = re.sub("(\\d|\\W)+", " ", text)
    text = ' '.join(remove_stop_words(text))
    text = apply_lemmatization(text)
    return text

def show_lyrics(track_name, artist_name):
    # Search for the song using the Genius API
    songs = genius.search_songs(track_name + ' ' + artist_name) #Finding all searches
    try:
        lyrics = genius.lyrics(song_url = songs['hits'][0]['result']['url']) #Returning the first song's lyrics
        lyrics = lyrics.split('Lyrics\n', 1)[1] #Removing the title
        lyrics = lyrics.split('Embed')[0] #Removing the end

        st.subheader(f"Lyrics for '{track_name}' by {artist_name}")
        st.text_area("Lyrics", lyrics, height=400)
    except:
        print('')