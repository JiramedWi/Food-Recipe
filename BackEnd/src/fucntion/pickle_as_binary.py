import pickle

from clean_data import clean_text, clean_text_ingre
from bm25 import BM25
from pre_process import pre_process
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

df = pickle.load(open('../../resource/food_cleaned.pkl', 'rb'))
title = df['Title']
ingredient = df['Ingredients']
bm25title = BM25()
bm25ingre = BM25()
bm25_title_fit = bm25title.fit(title)
bm25_ingre_fit = bm25ingre.fit(ingredient)
pickle.dump((bm25_title_fit, bm25_ingre_fit), open('../../resource/bm25.pkl', 'wb'))

