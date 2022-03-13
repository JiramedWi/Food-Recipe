import pickle
import random

import pandas as pd

from fucntion.bm25 import BM25
from fucntion.pre_process import pre_process

food_df = pickle.load(open('../../resource/food_cleaned.pkl', 'rb'))
title = pickle.load(open('../../resource/bm25_title.pkl', 'rb'))
ingre = pickle.load(open('../../resource/bm25_ingre.pkl', 'rb'))
words = open('../../resource/mergedict.txt', 'r').read().split(' ')


def get_word():
    index = random.randint(0, 295375)
    word = words[index]
    print(word)
    return word


def home_ranking(query):
    score = title.transform(query)
    score_ingre = ingre.transform(query)
    score = score + score_ingre
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


def bookmark_ranking(query, food_id):
    score = title.transform(query)
    score_ingre = ingre.transform(query)
    score = score + score_ingre
    tf = pd.DataFrame({'bm25': list(score),
                       'Title': list(food_df['Title']),
                       'Ingredient': list(food_df['Cleaned_Ingredients']),
                       'Instructions': list(food_df['Instructions']),
                       'Image': list(food_df['Image_Name'].apply(lambda s: s + '.jpg')),
                       })
    tf = tf.iloc[food_id].nlargest(columns='bm25', n=10)
    tf['rank'] = tf['bm25'].rank(ascending=False)
    tf = tf.drop(columns='bm25', axis=1)
    tf = tf.to_dict('record')
    return tf


def getdataframe():
    df = pd.DataFrame(
        {'id': list(food_df.index), 'Title': list(food_df['Title']),
         'Ingredient': list(food_df['Cleaned_Ingredients']),
         'Instructions': list(food_df['Instructions']),
         'Image': list(food_df['Image_Name'].apply(lambda s: s + '.jpg'))})
    return df
