import pandas as pd
import numpy as np
import lyricsgenius as lg
import re
import nltk
import os
import wordcloud
import sklearn
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('omw-1.4', quiet=True)

# use LyricsGenius API to collect song lyrics
file = open("/Users/gracechen/Documents/GitHub/MSDS495-Capstone/generated_lyrics.txt", "w")

genius = lg.Genius('8HZOq8Guax-CGuW96EMZgR1t3-EuTXI3Yl2guQ7u0_CE8DXwCcUj6GXX70mi3Gr0', skip_non_songs=True,
                   excluded_terms=["(Remix)", "(Live)"],
                   remove_section_headers=True)


def get_lyrics(arr, k):
    c = 0
    for name in arr:
        try:
            songs = (genius.search_artist(name, max_songs=k, sort='popularity')).songs
            s = [song.lyrics for song in songs]
            file.write("\n \n   <|endoftext|>   \n \n".join(s))
            c += 1
            print(f"Songs grabbed:{len(s)}")
        except:
            print(f"some exception at {name}: {c}")


# TODO: add option to input songs instead of artists
artists = ['Justin Bieber']

get_lyrics(artists, 1)
file.close()

# bug in LyricsGenius API, get rid of first line
with open("/Users/gracechen/Documents/GitHub/MSDS495-Capstone/generated_lyrics.txt", "r") as input:
    with open("/Users/gracechen/Documents/GitHub/MSDS495-Capstone/new_generated_lyrics.txt", "w") as output:
        for line in input:
            if "Lyrics" not in line.strip("\n"):
                output.write(line)
output.close()

# final corpus
f = open("/Users/gracechen/Documents/GitHub/MSDS495-Capstone/new_generated_lyrics.txt", "r", errors='ignore')
raw = f.read()
raw2 = raw.split("\n\n")


def remove_stop_words(text):
    stop_words = set(stopwords.words('english'))
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


# TODO: fix raw and raw2 multiple versions
normalized_text = normalize(raw)
processed_text = []
for i in raw2:
    text = normalize(i)
    processed_text.append(text)

print('#################')
# print(normalized_text2)

# create word cloud image
wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(normalized_text)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()
# wordcloud.to_file("img/first_review.png")

# token by frequency table in word cloud image
word_count = WordCloud().process_text(normalized_text)
word_count_df = pd.DataFrame.from_dict(word_count, orient='index').reset_index()
word_count_df = word_count_df.rename(columns={"index": "Token", 0: "Frequency"})
word_count_df = word_count_df.sort_values(by=['Frequency'], ascending=False)
# print(word_count_df)

# top 10 tokens with the highest mean tf-idf values
Tfidf = TfidfVectorizer(ngram_range=(1, 1))
TFIDF_matrix = Tfidf.fit_transform(processed_text)
words = Tfidf.get_feature_names_out()
matrix = pd.DataFrame(TFIDF_matrix.toarray(), columns=words)
doc_term_matrix = TFIDF_matrix.todense()
doc_term_df = pd.DataFrame(doc_term_matrix, columns=Tfidf.get_feature_names_out())
top10_tfidf = pd.DataFrame(doc_term_df.mean().sort_values(ascending=False).head(10))
top10_tfidf.rename(columns={0: 'Mean TF-IDF'}, inplace=True)

# count vectorizer
vectorizer = CountVectorizer(ngram_range=(1, 1))
count_matrix = vectorizer.fit_transform(processed_text)
words_count = vectorizer.get_feature_names_out()
word_counts = pd.DataFrame(count_matrix.toarray(), columns=words_count)
word_term_matrix = count_matrix.todense()
word_term_df = pd.DataFrame(word_term_matrix, columns=vectorizer.get_feature_names_out())
top10_count = pd.DataFrame(word_term_df.mean().sort_values(ascending=False).head(10))
top10_count.rename(columns={0: 'Mean Count'}, inplace=True)

# defined tokens (song genres + common song genres) with their associated tf-idf values
candidate_terms = [
    'heartbreak',
    'breakups',
    'desire',
    'sex',
    'relationships',
    'love',
    'lust',
    'loss',
    'death',
    'inpiration',
    'motivation',
    'success',
    'pain',
    'jealousy',
    'sadness',
    'loss'
]

# topic modeling - LSA


# topic modeling - LDA
