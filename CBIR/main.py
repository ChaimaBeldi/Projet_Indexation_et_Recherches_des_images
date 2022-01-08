import numpy as np
import pickle as pkl
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from flask import Flask, request, render_template
from pathlib import Path
from sklearn.decomposition import PCA
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

app = Flask(__name__)
##partie elasticsearch 
es = Elasticsearch('127.0.0.1',port=9200,timeout=600,)
es.cluster.health(wait_for_status='yellow', request_timeout=600)
index = 'search_engine_os_final'
source_no_vecs = ['imageId', 'title', 'author', 'tags', 'labels', 'imgUrl']
# #feature_extraction & pca
fe = FeatureExtractor()
pca = pca = pkl.load(open("C:\\Users\ASUS\\Desktop\\extract_from_img\\pca.pkl",'rb'))

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/result.html', methods=['GET', 'POST'])
def search_by_word():
    search_term = request.form["input"] 
    res =es.search(
        index="search_engine_os_final", 
        size=16, 
        body={
             "query": {
                "fuzzy" : {
                    "tags": search_term, 
                    
                }
            }
            # "query": {

            #     "multi_match" : { "query": search_term, "fields" :["title", "tags"] }
               
            # }
        }
    )
    answers =[] 
    for hit in res['hits']['hits']:
        s = hit['_source']
        if 'tags' in s:
                 desc = str(s.get('tags', None))
                 print(f"Desc    {desc[:80] + ('...' if len(desc) > 80 else '')}")
        if 'price' in s:
                 print(f"Labels   {s['labels']}")
                 print(f"ID      {s.get('imageId', None)}")
                 print(f"Score   {hit.get('_score', None)}")
        if 'imgUrl' in s:
                 answers.append([s.get("imgUrl"),' '])
        print(answers)
    return render_template('result.html', answers=answers,search_term=search_term )
#  Search by img
@app.route('/result1.html', methods=['GET', 'POST']) 
def search_by_img():
    if request.method == 'POST' :

        file = request.files['query_img']

            # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

            # #Run search
        img_features = fe.extract(img)
        vector= pca.transform(img_features.reshape(1,-1))[0].tolist()
        res =es.search(
            index="search_engine_os_final", 
            size=12, 
            body={
                    "query" : { 
                "elastiknn_nearest_neighbors": {
                "vec": {
                    "values": vector
                },
                "field": "featureVec",
                "model": "lsh",
                "similarity": "l2",
                "candidates": 150
                }
                }
            }
        )
        answers =[] 
        for hit in res['hits']['hits']:
            s = hit['_source']
            if 'tags' in s:
                    desc = str(s.get('tags', None))
                    print(f"Desc    {desc[:80] + ('...' if len(desc) > 80 else '')}")
            if 'price' in s:
                    print(f"Labels   {s['labels']}")
                    print(f"ID      {s.get('imageId', None)}")
                    print(f"Score   {hit.get('_score', None)}")
            if 'imgUrl' in s:
                    answers.append([s.get("imgUrl"),' '])
            
        return render_template('result1.html',
                                query_path=uploaded_img_path,answers=answers)
    else :
        return render_template('result1.html')



if __name__=="__main__":
    app.run("0.0.0.0")