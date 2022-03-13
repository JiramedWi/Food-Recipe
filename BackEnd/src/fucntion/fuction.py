import pickle

import pandas as pd

from fucntion.bm25 import BM25
from fucntion.pre_process import pre_process

food_df = pickle.load(open('../../resource/food_cleaned.pkl', 'rb'))
title = pickle.load(open('../../resource/bm25_title.pkl', 'rb'))
ingre = pickle.load(open('../../resource/bm25_ingre.pkl', 'rb'))


def title_ranking(query):
    score = title.transform(query)
    tf = pd.DataFrame({'bm25': list(score),
                       'Title': list(food_df['Title']),
                       'Ingredient': list(food_df['Cleaned_Ingredients']),
                       'Instructions': list(food_df['Instructions']),
                       'Image': list(food_df['Image_Name'].apply(lambda s: s + '.jpg')),
                       'id': list(food_df.index)
                       }).nlargest(columns='bm25', n=10)
    tf['rank'] = tf['bm25'].rank(ascending=False)
    tf = tf.drop(columns='bm25', axis=1)
    tf = tf.to_dict('record')
    return tf


def ingredient_ranking(query):
    score_ingre = ingre.transform(query)
    tf = pd.DataFrame({'bm25': list(score_ingre),
                       'Title': list(food_df['Title']),
                       'Ingredient': list(food_df['Cleaned_Ingredients']),
                       'Instructions': list(food_df['Instructions']),
                       'Image': list(food_df['Image_Name'].apply(lambda s: s + '.jpg')),
                       'id': list(food_df.index)
                       }).nlargest(columns='bm25', n=10)
    tf['rank'] = tf['bm25'].rank(ascending=False)
    tf = tf.drop(columns='bm25', axis=1)
    tf = tf.to_dict('record')
    return tf
