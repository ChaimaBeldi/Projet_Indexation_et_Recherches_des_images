from pathlib import Path
import numpy as np
from datetime import datetime
from sklearn.decomposition import PCA
from flask import Flask, request, render_template
#from scipy.spatial import distance as dist
from PIL import Image
#from feature_extractor import FeatureExtractor
import glob
import datetime
import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

#elasticsearch 
# es = Elasticsearch(["http://localhost:9200"],timeout=60)
# es.cluster.health(wait_for_status='yellow', request_timeout=1)
# index = 'search_engine_os_final'
# source_no_vecs = ['imageId', 'title', 'author', 'tags', 'labels', 'imgUrl']

# #feature_extraction & pca
# fe = FeatureExtractor()
# pca = PCA(n_components=785)

# #query : 
# def search_by_image_query(image_id=None, feature_vector=None,size=5):
#     if image_id==None and feature_vector==None:
#         raise ValueError("Please enter an Image ID or a Feature Vector")
    
#     if image_id:
#         query = {
#             "elastiknn_nearest_neighbors": {
#               "vec": {
#                 "index": index,
#                 "field": "featureVec",
#                 "id": image_id
#               },
#               "field": "featureVec",
#               "model": "lsh",
#               "similarity": "l2",
#               "candidates": 100
#             }
#           }
#     elif feature_vector:
#         query = {
#             "elastiknn_nearest_neighbors": {
#               "vec": {
#                 "values": feature_vector
#               },
#               "field": "featureVec",
#               "model": "lsh",
#               "similarity": "l2",
#               "candidates": 150
#             }
#           }
#     res = es.search(index=index, query=query, size=size, _source=source_no_vecs)
#     return res

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		file = request.files['query_img']
		img = Image.open(file.stream)
		#upload image from any folder folder
		#i = file.filename.split('.')[0]
		# i = int (i)
		# i=i//10000
		#print(i)
		uploaded_img_path='static/uploaded/'+ datetime.now().isoformat().replace(':','.') + "_" + file.filename
        img.save(uploaded_img_path)
        #print(uploaded_img_path)
        return render_template('index.html',query_path=uploaded_img_path)
        
       
        # img_features = fe.extract(img)
        # vector= pca.fit_transform(img_features.reshape(1,-1))[0].tolist()
    
    
        # res = search_by_image_query(feature_vector=vector,size=5)
	
		

        # answers =[] 
        # for hit in res['hits']['hits']:
        #     s = hit['_source']
        #     if 'tags' in s:
        #         desc = str(s.get('tags', None))
        #         print(f"Desc    {desc[:80] + ('...' if len(desc) > 80 else '')}")
        #     if 'price' in s:
        #         print(f"Labels   {s['labels']}")
        #         print(f"ID      {s.get('imageId', None)}")
        #         print(f"Score   {hit.get('_score', None)}")
        #     if 'imgUrl' in s:
        #         answers.append([s.get("imgUrl"),' '])

		
	else:
		return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)

