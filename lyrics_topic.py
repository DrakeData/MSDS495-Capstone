import pandas as pd
import numpy as np
import lyricsgenius as lg
import re
import nltk
import os
import wordcloud
import sklearn
import matplotlib.pyplot as plt
import gensim
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

from gensim.corpora import Dictionary
from gensim.corpora import MmCorpus
from gensim.models import LdaModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('omw-1.4', quiet=True)

# use LyricsGenius API to collect song lyrics
file = open("/Users/gracechen/Documents/GitHub/MSDS495-Capstone/generated_lyrics.txt", "w")

genius = lg.Genius('VBNlywB6f8BrbFPBFYdKG1FKwyT-qV49scmB8l7wh3oCwVMtBMZMmUxI5SZwDp0P', skip_non_songs=True,
                   excluded_terms=["(Remix)", "(Live)"],
                   remove_section_headers=True)


def get_lyrics_by_artist(arr, k):
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


def get_lyrics_by_song(song, arr):
    try:
        s = (genius.search_song(song, arr)).lyrics
        file.write(s)
        print(f"Songs grabbed.")
    except:
        print("exception")


# search by artist
# artists = ['Justin Bieber']
# get_lyrics_by_artist(artists, 1)

# search by song title and artist
get_lyrics_by_song("To You", "Andy Shauf")

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
raw2 = raw.replace('\n', ' ')
raw2 = raw2.split(' ')


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


print('#################')
lyric_corpus_tokenized = []
tokenizer = RegexpTokenizer(r'\w+')
for lyric in raw2:
    tokenized_lyric = tokenizer.tokenize(lyric.lower())  # tokenize and lower each lyric
    lyric_corpus_tokenized.append(lyric)

processed_text = []
for i in lyric_corpus_tokenized:
    text = normalize(i)
    processed_text.append(text)

final_corpus = []
for s, song in enumerate(processed_text):
    if len(song) > 2 and not song.isnumeric() and song != '':
        final_corpus.append(song)

# create word cloud image
wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(raw)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()

# token by frequency table in word cloud image
word_count = WordCloud().process_text(raw)
word_count_df = pd.DataFrame.from_dict(word_count, orient='index').reset_index()
word_count_df = word_count_df.rename(columns={"index": "Token", 0: "Frequency"})
word_count_df = word_count_df.sort_values(by=['Frequency'], ascending=False).reset_index(drop=True)
print(word_count_df)

# top 10 tokens with the highest mean tf-idf values
Tfidf = TfidfVectorizer(use_idf=True, ngram_range=(1, 1), norm=None)
TFIDF_matrix = Tfidf.fit_transform(final_corpus)
words = Tfidf.get_feature_names_out()
matrix = pd.DataFrame(TFIDF_matrix.toarray(), columns=words)
doc_term_matrix = TFIDF_matrix.todense()
doc_term_df = pd.DataFrame(doc_term_matrix, columns=Tfidf.get_feature_names_out())
top10_tfidf = pd.DataFrame(doc_term_df.mean().sort_values(ascending=False).head(10))
top10_tfidf.rename(columns={0: 'Mean TF-IDF'}, inplace=True)
print(top10_tfidf)

# topic modeling - LDA
dictionary = Dictionary([final_corpus])
gensim_corpus = [dictionary.doc2bow(song) for song in [final_corpus]]
temp = dictionary[0]
id2word = dictionary.id2token
num_topics = 3

lda_model = LdaModel(corpus=gensim_corpus, id2word=id2word, chunksize=2000, alpha='auto', eta='auto',
                     iterations=400,
                     num_topics=num_topics, passes=20
                     )

print(lda_model.print_topics(num_topics=num_topics, num_words=10))

vis_data = gensimvis.prepare(lda_model, gensim_corpus, dictionary)
pyLDAvis.display(vis_data)
pyLDAvis.save_html(vis_data, './Lyrics_LDA_k_' + str(num_topics) + '.html')
