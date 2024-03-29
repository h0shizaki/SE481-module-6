from elasticsearch import Elasticsearch
import os
from pathlib import Path
import pickle
import json


class ElasticIndexer:
    def __init__(self):
        self.crawled_folder = Path(os.path.abspath('')).parent / 'crawled/'
        with open(self.crawled_folder / 'url_list.pickle', 'rb') as f:
            self.file_mapper = pickle.load(f) 
        self.es_client = Elasticsearch('http://localhost:9200', basic_auth=("elastic", "6E0GWL_MEddnKJWCnk*M"),
                    ca_certs="./http_ca.crt")

    def run_indexer(self):
        self.es_client.options(ignore_status=400).indices.create(index='simple')
        self.es_client.options(ignore_status=[400,404]).indices.delete(index='simple')

        for file in os.listdir(self.crawled_folder):
            if file.endswith(".txt"):
                j = json.load(open(os.path.join(self.crawled_folder, file)))
                j['id'] = j['url']
                print(j)
                self.es_client.index(index='simple', document=j)

if __name__ == '__main__':
    s = ElasticIndexer()
    s.run_indexer()
    query = {'bool': {'must': [{'match': {'text': 'camt'}}]}}
    results = s.es_client.search(index='simple', query=query)
    print("Got %d Hits :" % results['hits']['value'])
    for hit in results['hits']['hits']:
        print("The title is {0} ({1})".format(hit['source']['title'], hit['_source']['url']))