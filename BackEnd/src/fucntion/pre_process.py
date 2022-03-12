from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


def pre_process(s):
    ps = PorterStemmer()
    s = word_tokenize(s)
    stopwords_set = set(stopwords.words())
    stop_dict = {s: 1 for s in stopwords_set}
    s = [ps.stem(w) for w in s]
    s = ' '.join(s)
    s = [w for w in s if w not in stop_dict]
    return s
