import time
from elasticsearch import Elasticsearch
from flask import Flask , request
import pandas as pd

from ManualIndexer import Indexer, preProcessor

app = Flask(__name__)
app.es_client  = Elasticsearch('https://localhost:9200', basic_auth=("elastic", "6E0GWL_MEddnKJWCnk*M"),
                    ca_certs="./http_ca.crt")
app.indexer = Indexer()
app.indexer.run_indexer()

@app.route('/manual_index', methods=["GET"])
def manual_index():
    
    start = time.time()
    res = {'status': 'success'}
    argList = request.args.to_dict(flat=False)
    query_term = argList['query'][0]
    results = app.indexer.search(query_term)
    end = time.time()
    total_hit = len(results)
    
    res['total_hit'] = total_hit
    res['results'] = results.sort_values("score", ascending=False).drop("url_lists", axis=1).head(100).to_dict('records')
    res['elapse'] = end-start

    return res

if __name__ == '__main__':
    app.run(debug=False)