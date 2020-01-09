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
from math import pi, log10
import ntpath

stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')
lemma = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

files = glob.glob('./products/*.json')

try:
    os.mkdir('./products')
    os.mkdir('./images')
    os.mkdir('./shapes')
except:
    pass

sum_size = 20 # buckets available in my vector
term_frequencies = []
shapes = []
maxes = [0 for i in range(0, sum_size)]

df = {}
# tf = log(number of times term occurs in document)
# idf = log(number of documents / number of documents in which term occurs)
# want tf * idf

for f in files:
    product_id = ntpath.basename(f).split('.')[0]

    with open(f) as document:
        product = json.load(document)

        # add spaces to CamelCase words
        overview = re.sub(
            r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', product['title'] + ' ' + product['overview'])

        # clear punctuation
        overview = ''.join([c for c in overview if c.isalnum()
                            or c.isspace() or c in string.punctuation])

        # get sentences
        sentences = sent_tokenize(overview)

        # tokenize the sentences themselves
        tokens = [tokenizer.tokenize(s) for s in sentences]

        # stem or lemmatize the words in each sentence
        stemmed = [[lemma.lemmatize(w.lower())
                    for w in t if w not in stop_words] for t in tokens]

        # build lists of ngrams
        gram1 = [[ng for ng in ngrams(s, 1)] for s in stemmed]
        gram2 = [[ng for ng in ngrams(s, 2)] for s in stemmed]
        gram1_strings = [[s[0] for s in g] for g in gram1]
        gram2_strings = [["".join(s) for s in g] for g in gram2]

        # accumulate all ngrams into flat list
        singles = [item for sublist in gram1_strings for item in sublist]
        doubles = [item for sublist in gram2_strings for item in sublist]
        combined = singles + doubles # final array of all ngrams

        # get one-hot encoded flag for each present word in document
        local_df = {}
        for c in combined:
            if c not in local_df.keys():
                local_df[c] = 1
        
        # go through all unique words in document and add them to the document frequency
        for f in local_df:
            if f in df.keys():
                df[f] = df[f] + 1
            else:
                df[f] = 1

        # track tf here
        tf = {}
        for t in combined:
            if t not in tf.keys():
                tf[t] = 1
            else:
                tf[t] = tf[t] + 1
        
        term_frequencies.append([product_id, len(combined), tf])

# Build vector sumamries of each document
for docs in term_frequencies:
    # dimensionality reduction here
    total_doc_count = len(files)
    hashes = [(hash(i) % sum_size, (docs[2][i] / docs[1]) / log10(total_doc_count / df[i])) for i in docs[2].keys()]

    sums = [0 for i in range(0, sum_size)]
    for h in hashes:
        sums[h[0]] = sums[h[0]] + h[1]

    shapes.append([docs[0]] + sums)

    # save the vector (shape) file
    with open('./shapes/' + docs[0] + '.json', 'w') as shapefile:
        json.dump(sums, shapefile)

    N = len(sums)
    maxes = [max(x[0], x[1]) for x in zip(sums, maxes)]

# make a visual representation for everything for the wetware with Pyplot
for values in shapes:
    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    product_id = values[0]
    values = [x[0] / x[1] for x in zip(values[1:], maxes)]
    specific_max = max(values)
    if specific_max == 0:
        specific_max = 1
    values = [x / specific_max for x in values]
    values += values[:1]

    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    plt.figure(figsize=(5,5))
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
    fig.savefig('./images/'+product_id+'.svg', dpi=fig.dpi)
    plt.close('all')
