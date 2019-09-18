import json
from nltk.tokenize import RegexpTokenizer, sent_tokenize

from nltk.stem import PorterStemmer
from nltk import WordNetLemmatizer
from nltk import ngrams
from nltk.corpus import stopwords

stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')
lemma = WordNetLemmatizer()
stop_words = set(stopwords.words('english')) 


with open('./products/8007.json') as document:
    product = json.load(document)
    overview = ''.join([c for c in product['overview'] if c.isalnum() or c.isspace()])
    print(overview)
    sentences = sent_tokenize(overview)
    tokens = [tokenizer.tokenize(s) for s in sentences]
    stemmed = [[lemma.lemmatize(w.lower()) for w in t if w not in stop_words] for t in tokens]
    gram1 = [[ng for ng in ngrams(s, 1)] for s in stemmed]
    gram2 = [[ng for ng in ngrams(s, 2)] for s in stemmed]
    gram3 = [[ng for ng in ngrams(s, 3)] for s in stemmed]
    print([[s[0] for s in g] for g in gram1])
    print([[" ".join(s) for s in g] for g in gram2])
    print([[" ".join(s) for s in g] for g in gram3])