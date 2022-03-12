import pickle

from clean_data import clean_text, clean_text_ingre
from bm25 import BM25
from pre_process import pre_process
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

df = pickle.load(open('../../resource/food_cleaned.pkl', 'rb'))
# title = df['Title']
# ingredient = df['Ingredients']
bm25title = BM25()
bm25ingre = BM25()
bm25title.fit(df['Title'])
bm25ingre.fit(df['Ingredients'])
pickle.dump(bm25title, open('../../resource/bm25_title.pkl', 'wb'))
pickle.dump(bm25ingre, open('../../resource/bm25_ingre.pkl', 'wb'))

