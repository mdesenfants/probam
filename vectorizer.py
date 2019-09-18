import json
from nltk.tokenize import RegexpTokenizer, sent_tokenize

from nltk.stem import PorterStemmer
from nltk import ngrams

stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')

with open('./products/8007.json') as document:
    product = json.load(document)
    overview = product['overview']
    sentences = sent_tokenize(overview)
    tokens = [tokenizer.tokenize(s) for s in sentences]
    stemmed = [[stemmer.stem(w) for w in t] for t in tokens]
    gram1 = [[ng for ng in ngrams(s, 1)] for s in stemmed]
    gram2 = [[ng for ng in ngrams(s, 2)] for s in stemmed]
    gram3 = [[ng for ng in ngrams(s, 3)] for s in stemmed]
    print(gram1, gram2, gram3)