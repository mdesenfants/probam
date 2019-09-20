import json

from nltk.tokenize import RegexpTokenizer, sent_tokenize
from nltk.stem import PorterStemmer
from nltk import WordNetLemmatizer
from nltk import ngrams
from nltk.corpus import stopwords

import matplotlib.pyplot as plt
import numpy as np

import re
import os
import string
import glob
from math import pi
import ntpath

stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')
lemma = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

files = glob.glob('./products/*.json')

try:
    os.mkdir('./products')
except:
    pass

sum_size = 20
shapes = []
maxes = [0 for i in range(0, sum_size)]

for f in files:
    product_id = ntpath.basename(f).split('.')[0]

    with open(f) as document:
        product = json.load(document)

        # add spaces to CamelCase words
        overview = re.sub(
            r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', product['overview'])
        overview = ''.join([c for c in overview if c.isalnum()
                            or c.isspace() or c in string.punctuation])
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
        hashes = [(hash(i) % sum_size, 1) for i in combined]

        sums = [0 for i in range(0, sum_size)]
        for h in hashes:
            sums[h[0]] = sums[h[0]] + h[1]

        shapes.append([product_id] + sums)

        N = len(sums)
        maxes = [max(x[0], x[1]) for x in zip(sums, maxes)]

for values in shapes:
    print(values)
    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    product_id = values[0]
    values = [x[0] / x[1] for x in zip(values[1:], maxes)]
    values += values[:1]

    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    plt.figure(figsize=(1,1))
    ax = plt.subplot(111, polar=True)

    plt.xticks(angles[:-1], angles, color='grey', size=8)
    ax.set_rlabel_position(0)
    max_value = max(values)
    plt.yticks([0.5, 1],
               ['', ''], color="grey", size=7)
    plt.ylim(0, max(values))

    ax.plot(angles, values, linewidth=1, linestyle='solid')

    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)
    ax.set_thetagrids([a * 180/np.pi for a in angles],
                      ["" for n in range(0, len(sums))])

    fig = plt.gcf()
    fig.savefig('./products/images/'+product_id+'.svg', dpi=fig.dpi)
    plt.clf()
