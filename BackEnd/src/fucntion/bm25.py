""" Implementation of OKapi BM25 with sklearn's TfidfVectorizer
Distributed as CC-0 (https://creativecommons.org/publicdomain/zero/1.0/)
"""
import pandas as pd
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import sparse
from pre_process import pre_process


class BM25(object):
    def __init__(self, b=0.75, k1=1.6):
        self.vectorizer = TfidfVectorizer(
            norm=None, smooth_idf=False, ngram_range=(1, 3), preprocessor=pre_process)
        self.b = b
        self.k1 = k1

    def fit(self, X):
        """ Fit IDF to documents X """
        self.vectorizer.fit(X)
        y = super(TfidfVectorizer, self.vectorizer).transform(X)
        self.X = y
        self.avdl = y.sum(1).mean()

    def transform(self, q):
        """ Calculate BM25 between query q and documents X """
        b, k1, avdl = self.b, self.k1, self.avdl

        len_X = self.X.sum(1).A1

        q, = super(TfidfVectorizer, self.vectorizer).transform([q])

        assert sparse.isspmatrix_csr(q)
        # convert to csc for better column slicing
        X = self.X.tocsc()[:, q.indices]
        denom = X + (k1 * (1 - b + b * len_X / avdl))[:, None]
        # idf(t) = log [ n / df(t) ] + 1 in sklearn, so it need to be coneverted
        # to idf(t) = log [ n / df(t) ] with minus 1
        idf = self.vectorizer._tfidf.idf_[None, q.indices] - 1.
        numer = X.multiply(np.broadcast_to(idf, X.shape)) * (k1 + 1)
        return (numer / denom).sum(1).A1


# ------------ End of library impl. Followings are the example -----------------
if __name__ == '__main__':
    df = pickle.load(open('../../resource/food_cleaned.pkl', 'rb'))
    # title = df['Title']
    # ingredient = df['Ingredients']
    bm25title = BM25()
    bm25ingre = BM25()
    bm25title.fit(df['Title'])
    bm25ingre.fit(df['Ingredients'])
    pickle.dump((bm25title, bm25ingre), open('../../resource/bm25_title_fit.pkl', 'wb'))
