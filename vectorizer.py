import json

from nltk.tokenize import RegexpTokenizer, sent_tokenize
from nltk.stem import PorterStemmer
from nltk import WordNetLemmatizer
from nltk import ngrams
from nltk.corpus import stopwords

import matplotlib.pyplot as plt
import numpy as np 

import re
import string

stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')
lemma = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


with open('./products/8007.json') as document:
    product = json.load(document)

    # add spaces to CamelCase words
    overview = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', product['overview'])
    overview = ''.join([c for c in overview if c.isalnum() or c.isspace() or c in string.punctuation])
    sentences = sent_tokenize(overview)
    tokens = [tokenizer.tokenize(s) for s in sentences]
    stemmed = [[lemma.lemmatize(w.lower())
                for w in t if w not in stop_words] for t in tokens]
    gram1 = [[ng for ng in ngrams(s, 1)] for s in stemmed]
    gram2 = [[ng for ng in ngrams(s, 2)] for s in stemmed]
    # seems like overkill: gram3 = [[ng for ng in ngrams(s, 3)] for s in stemmed]
    gram1_strings = [[s[0] for s in g] for g in gram1]
    gram2_strings = [[" ".join(s) for s in g] for g in gram2]

    # seems like overkill: print([[" ".join(s) for s in g] for g in gram3])

    singles = [item for sublist in gram1_strings for item in sublist]
    doubles = [item for sublist in gram2_strings for item in sublist]

    combined = singles + doubles

    sum_size = 20
    hashes = [(hash(i) % sum_size, 1) for i in combined]

    sums = [0 for i in range(0, sum_size)]
    for h in hashes:
        sums[h[0]] = sums[h[0]] + h[1]
    
    print(sums)