import re

import pandas as pd
import numpy as np
import pint
import string
from nltk.stem import PorterStemmer, porter
from nltk.tokenize import word_tokenize
import pickle
import csv

ureg = list(pint.UnitRegistry())
# df = pd.read_csv('D:/Git/Repositories/Food-Recipe/BackEnd/resource/food_recipe_and_ingredients_with_img.csv')
df = pd.read_csv('../../resource/food_recipe_and_ingredients_with_img.csv')

df_not_null = df.copy().dropna().reset_index(drop=True)
print(df_not_null.shape)

def clean_text(text):
    text = ' '.join([c.lower() for c in str(text).split() if len(c) > 2])
    numbers_patterns = re.compile('[0-9]+[\w]*')
    text = re.sub(numbers_patterns, '', text)
    punctiation_pattern = re.compile(r"[^\w\s\()]")
    text = re.sub(punctiation_pattern, '', text)
    return text


def clean_text_ingre(text):
    text = ' '.join([c.lower() for c in str(text).split() if len(c) > 2])
    numbers_patterns = re.compile('[0-9]+[\w]*')
    text = re.sub(numbers_patterns, '', text)
    punctiation_pattern = re.compile(r"[^a-zA-Z\s]+")
    text = re.sub(punctiation_pattern, '', text)
    text = text.split()
    text = ' '.join([w for w in text if PorterStemmer().stem(w) not in ureg])
    return text


df_not_null['Title'] = df_not_null['Title'].apply(clean_text)
# print(df_not_null.head(10).to_markdown())
#
df_not_null['Ingredients'] = df_not_null['Ingredients'].apply(clean_text_ingre)
# print(df_not_null.head(25).to_markdown())
#
# df_not_null.to_csv('../../resource/food_cleaned.csv')

pickle.dump(df_not_null, open('../../resource/food_cleaned.pkl', 'wb'))
