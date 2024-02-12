import json
from pathlib import Path
import os
import pickle
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from nltk.corpus import stopwords
import BM_ranking
from nltk.stem import PorterStemmer

def preProcessor(s):
    ps = PorterStemmer()
    s = re.sub(r'[^A-Za-z]', ' ', s)
    s = re.sub(r'\s+', ' ' , s)
    s = [word for word in s.split(' ') if len(word) > 2]
    s = [ps.stem(w) for w in s]
    s = ' '.join(s)
    return s

class Indexer:
    def __init__(self):
        self.crawled_folder = Path(os.path.abspath('')).parent / 'crawled/'
        self.stored_file = 'resource/manual_indexer.pkl'
        if os.path.isfile(self.stored_file):
            with open(self.stored_file, 'rb') as f:
                cached_dict = pickle.load(f)
            self.__dict__.update(cached_dict)
        else:
            self.run_indexer()

    def run_indexer(self):
        documents = []
        for file in os.listdir(self.crawled_folder):
            if file.endswith(".txt"):
                try:
                    j = json.load(open(os.path.join(self.crawled_folder, file)))
                    documents.append(j)
                except:
                    continue
        self.documents = pd.DataFrame.from_dict(documents)

        # print(self.documents.apply(lambda s: ' '.join(s[['title', 'text']]), axis=1))
        tfidf_vecotorizor = TfidfVectorizer(preprocessor=preProcessor, stop_words=stopwords.words('english'), use_idf=True)
        self.bm25 = BM_ranking.BM25(tfidf_vecotorizor)
        self.bm25.fit(self.documents.apply(lambda s: ' '.join(s[['title', 'text']]), axis=1))
        with open(self.stored_file, 'wb') as f:
            pickle.dump(self.__dict__, f)

    def search(self, query):
        score = self.bm25.transform(query)
        score = pd.DataFrame(score , columns=["score"])
        df = self.documents.join(score)
        df = df.sort_values(by=["score"], ascending=False)
        return df
        # print(self.documents.iloc[rank[:5]].to_markdown())

