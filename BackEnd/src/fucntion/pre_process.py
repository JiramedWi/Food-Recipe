import re
import string

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


def pre_process(s):
    ps = PorterStemmer()
    s = re.sub('[^A-za-z]', ' ', s)
    s = word_tokenize(s)
    stopwords_set = set(stopwords.words())
    stop_dict = {s: 1 for s in stopwords_set}
    s = [w for w in s if w not in stop_dict]
    s = [ps.stem(w) for w in s]
    s = ' '.join(s)
    s = s.translate(str.maketrans('', '', string.punctuation + u'\xa0'))
    return s
