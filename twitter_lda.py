# -*- coding: utf-8 -*-
"""Twitter LDA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OcRx2R5bYCbN6c9Zvd1-2ybYMtCQyapI
"""

!curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -
!sudo apt-get install -y nodejs

!npm info tweet-harvest

data = "111.csv"
search_keyword = "pendidikan since:2024-07-01 until:2024-12-28"
limit = 1000
!npx --yes tweet-harvest@2.6.1 -o "{data}" -s "{search_keyword}" -l {limit} --token ""

from google.colab import files
files.download('/content/tweets-data/111.csv')

data = "222.csv"
search_keyword = "pendidikan since:2024-07-01 until:2024-12-29"
limit = 1000
!npx --yes tweet-harvest@2.6.1 -o "{data}" -s "{search_keyword}" -l {limit} --token ""

from google.colab import files
files.download('/content/tweets-data/222.csv')

data = "ghi.csv"
search_keyword = "pendidikan since:2024-01-01 until:2024-12-30"
limit = 1000
!npx --yes tweet-harvest@2.6.1 -o "{data}" -s "{search_keyword}" -l {limit} --token ""

from google.colab import files
files.download('/content/tweets-data/ghi.csv')

data = "jkl.csv"
search_keyword = "pendidikan since:2024-07-01 until:2024-12-31"
limit = 1000
!npx --yes tweet-harvest@2.6.1 -o "{data}" -s "{search_keyword}" -l {limit} --token ""

from google.colab import files
files.download('/content/tweets-data/jkl.csv')

data = "m.csv"
search_keyword = "pendidikan since:2024-07-01 until:2024-09-30"
limit = 1000
!npx --yes tweet-harvest@2.6.1 -o "{data}" -s "{search_keyword}" -l {limit} --token ""

from google.colab import files
files.download('/content/tweets-data/m.csv')

data = "n.csv"
search_keyword = "pendidikan since:2024-07-01 until:2024-11-02"
limit = 1000
!npx --yes tweet-harvest@2.6.1 -o "{data}" -s "{search_keyword}" -l {limit} --token ""

from google.colab import files
files.download('/content/tweets-data/n.csv')

data = "o.csv"
search_keyword = "pendidikan since:2024-07-01 until:2024-11-03"
limit = 1000
!npx --yes tweet-harvest@2.6.1 -o "{data}" -s "{search_keyword}" -l {limit} --token ""

from google.colab import files
files.download('/content/tweets-data/o.csv')

data = "p.csv"
search_keyword = "pendidikan since:2024-07-01 until:2024-11-04"
limit = 1000
!npx --yes tweet-harvest@2.6.1 -o "{data}" -s "{search_keyword}" -l {limit} --token ""

from google.colab import files
files.download('/content/tweets-data/p.csv')

data = "q.csv"
search_keyword = "pendidikan since:2024-07-01 until:2024-11-05"
limit = 1000
!npx --yes tweet-harvest@2.6.1 -o "{data}" -s "{search_keyword}" -l {limit} --token ""

import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
import gensim
from gensim import corpora
from gensim.models import LdaModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = stopwords.words('indonesian')
custom_stop_words = ['yang', 'ga', 'https', 'co', 'yg','t', 'ya', 'nya', 'gue','gw', 'gua', 'aja', 'kalo', 'ga', 'pemerintahnaikkangajiguru', 'amp','sih']  # Tambahkan stop words tambahan
stop_words.extend(custom_stop_words)

wtk = nltk.tokenize.RegexpTokenizer(r'\w+')
wnl = WordNetLemmatizer()

from google.colab import files

uploaded = files.upload()

file_name = list(uploaded.keys())[0]
app_reviews_df = pd.read_csv(file_name)

print(app_reviews_df.head())

reviews = app_reviews_df['description']

reviews.dropna(inplace=True)

reviews.reset_index(drop=True, inplace=True)

def preprocess_text(text):
    tokens = wtk.tokenize(text.lower())
    filtered_tokens = [word for word in tokens if word not in stop_words]
    lemmatized_tokens = [wnl.lemmatize(word) for word in filtered_tokens]
    return " ".join(lemmatized_tokens)

processed_reviews = reviews.apply(preprocess_text)

print(processed_reviews.head())

from gensim import corpora
from gensim.models import LdaModel

processed_reviews_list = processed_reviews.tolist()
dictionary = corpora.Dictionary([review.split() for review in processed_reviews_list])
corpus = [dictionary.doc2bow(review.split()) for review in processed_reviews_list]

num_topics = 5

lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=10, random_state=42)

topics = lda_model.show_topics(num_topics=num_topics, num_words=7, formatted=False)
topics = sorted(topics, key=lambda x: x[0])

for i, (_, word_list) in enumerate(topics):
    topic_words = ', '.join([word for word, _ in word_list])
    print(f"Topic {i}: {topic_words}")