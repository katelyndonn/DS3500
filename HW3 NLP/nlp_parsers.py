"""
nlp_parsers.py: a reusable library for parsers
compatible with nlp_visualizer TextProcessor objects
"""

import json
import pandas as pd
import string
from collections import Counter
from nltk.corpus import stopwords
from nlp_visualizer import TextProcessor
from utils import title_from_url


def json_parser(filename):
    f = open(filename, 'r')
    raw = json.load(f)
    text = raw['text']
    words = text.split(" ")
    wc = Counter(words)
    num = len(words)
    f.close()
    return {'wordcount': wc, 'numwords': num}


def csv_parser(filename, idx, url_header=None):
    text = pd.read_csv(filename).iloc[idx, 0]
    words = text.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).lower().split(' ')
    stop_words = TextProcessor.load_stop_words(stopwords.words('english'), words)
    words = [w for w in words if w not in stop_words]
    words = [w for w in words if w != '' and w != '—']

    results = {'word_count': dict(Counter(words)),
               'num_words': len(words),
               'word_length': dict(zip([w for w in words], [len(w) for w in words]))}

    if url_header is not None:
        url = pd.read_csv(filename).iloc[idx, 1]
        label = title_from_url(url, url_header)

    else:
        label = filename

    return results, label
