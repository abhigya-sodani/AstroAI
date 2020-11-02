
from flask import Flask
from annoy import AnnoyIndex
from flask_cors import CORS
import requests
from io import BytesIO

from PIL import Image
import numpy as np
from operator import add
import numpy as np
from numpy.linalg import norm
import pickle
from tqdm import tqdm, tqdm_notebook
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
import random
import time
import math
from flask import request
from werkzeug.routing import BaseConverter
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.applications.mobilenet import MobileNet
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import Input, Flatten, Dense, Dropout, GlobalAveragePooling2D
import wget
import cv2
import pickle
from sklearn.neighbors import NearestNeighbors

def extract_model_till_layer(model, layerNo):
  outputs = model.layers[layerNo].output
  model = Model(inputs=model.inputs, outputs=outputs)
  return model

    
model1 = ResNet50(weights='imagenet',
                         include_top=False,
                         input_shape=(512, 512, 3),
                        pooling='max')

model2 = tf.keras.models.load_model('best_worldview_10_classes_full_aug.h5')

def eF(url, model):
    response = wget.download(url)
    input_shape = (224, 224, 3)
    img = image.load_img(response,
                         target_size=(input_shape[0], input_shape[1]))
    img_array = image.img_to_array(img)
    a = np.expand_dims(img_array, axis=0)
    #a = cv2.imread(response,cv2.IMREAD_COLOR)
    os.remove(response)
    #a=np.resize(a,(1,224,224,3))
    a=a/255.0
    features=model.predict(a)
    flattened_features=features.flatten()
    normalized_features=flattened_features / norm(flattened_features)
    return normalized_features

app = Flask(__name__)

CORS(app)

def findNearestSmall(url, count):
    """
    u=AnnoyIndex(128)
    u.load('fullDatabaseSmallNew.ann')
    indexes = u.get_nns_by_vector(eF(url,extract_model_till_layer(model2,10)),
                             count,
                              include_distances=True)
    """
    feature_list = pickle.load(open('features-worldview-custom-model-level-8.pickle','rb'))
    filename_list = pickle.load(open('filenames-worldview-level-8.pickle','rb'))
    neighbors = NearestNeighbors(n_neighbors=count,
                             algorithm='brute',
                             metric='euclidean').fit(feature_list)
    temp=eF(url,extract_model_till_layer(model2,10))
    distances, indices = neighbors.kneighbors([temp])
    
    j=""
    for a in indices[0]:
        a=filename_list[a].split("/")[4]
        a=int((a.split("."))[0])
        p=a//320
        o=a%320
        j+=("https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2005-08-29/250m/8/"+str(p)+"/"+str(o)+".jpg###")
    return j

def findNearestBig(url, count):
    """
    u1=AnnoyIndex(128)
    u1.load('hurricanes1.ann')
    indexes = u1.get_nns_by_vector(eF(url,extract_model_till_layer(model2,10)),
                             count,
                              include_distances=True)
    """
    feature_list = pickle.load(open('features-worldview-custom-model-level-4.pickle','rb'))
    filename_list = pickle.load(open('filenames-worldview-level-4.pickle','rb'))
    neighbors = NearestNeighbors(n_neighbors=count,
                             algorithm='brute',
                             metric='euclidean').fit(feature_list)
    temp=eF(url,extract_model_till_layer(model2,10))
    distances, indices = neighbors.kneighbors([temp])
    
    j=""
    for a in indices[0]:
        a=int(filename_list[a].split(".")[0])
        p=a//20
        o=a%20
        j+=("https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2005-08-29/250m/4/"+str(p)+"/"+str(o)+".jpg###")
    return j
    

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route("/resnet/")
def resnet():
    a=request.args.get('url')+"?REQUEST="+request.args.get('REQUEST')+"&TIME="+request.args.get('TIME')+"&BBOX="+request.args.get('BBOX')+"&CRS="+request.args.get('CRS')+"&LAYERS="+request.args.get("LAYERS")+"&WRAP="+request.args.get("WRAP")+"&FORMAT="+request.args.get('FORMAT')+"&WIDTH="+request.args.get('WIDTH')+"&HEIGHT="+request.args.get('HEIGHT')+"&ts="+request.args.get('ts')
    
    bbox=request.args.get('BBOX')
    arr=bbox.split(",")
    arr=[float(a) for a in arr]
    size=abs(arr[0]-arr[2])*abs(arr[1]-arr[3])
    j=""
    if(size>50):
        j=findNearestBig(a,int(request.args.get('count')))
    if(size<=50):
        j=findNearestSmall(a,int(request.args.get('count')))
        
    
    
    return j
    
@app.route("/multi/")
def multi():
    """
    uA=AnnoyIndex(128)
    uA.load('fullDatabaseSmallNew.ann')
    """
    feature_list = pickle.load(open('features-worldview-custom-model-level-8.pickle','rb'))
    filename_list = pickle.load(open('filenames-worldview-level-8.pickle','rb'))
    neighbors = NearestNeighbors(n_neighbors=30,
                             algorithm='brute',
                             metric='euclidean').fit(feature_list)
    

    url=request.args.get('url')
    urlSplit=url.split("|||")
    urlParts=[]
    for i in urlSplit:
        urlParts.append(i.split("***"))

    feats=[]

    for u in urlParts:
        a=int(u[0])
        b=int(u[1])
        feats.append(feature_list[filename_list.index("/dataset/level8images/level8images/"+str((a)*320+b)+".jpg")])

    final=feats[0]
    d={}
    for u in range(0,len(feats)):
      distances, indices=neighbors.kneighbors([feats[u]])
      
      for t in range(0,len(distances[0])):
        d.update({distances[0][t]:indices[0][t]})
    sorted_list=sorted(d)

    indices=[]
    for y in range(0,30):
        indices.append(d[sorted_list[y]])
    
    
    j=""
    for a in indices:
        a=filename_list[a].split("/")[4]
        a=int((a.split("."))[0])
        p=a//320
        o=a%320
        j+=("https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2005-08-29/250m/8/"+str(p)+"/"+str(o)+".jpg###")

    return j



@app.route("/multiBig/")
def multiBig():
    feature_list = pickle.load(open('features-worldview-custom-model-level-4.pickle','rb'))
    filename_list = pickle.load(open('filenames-worldview-level-4.pickle','rb'))
    neighbors = NearestNeighbors(n_neighbors=30,
                             algorithm='brute',
                             metric='euclidean').fit(feature_list)
    url=request.args.get('url')
    urlSplit=url.split("|||")
    urlParts=[]
    for i in urlSplit:
        urlParts.append(i.split("***"))

    feats=[]

    for u in urlParts:
        a=int(u[0])
        b=int(u[1])
        feats.append(feature_list[filename_list.index(str((a)*20+b)+".jpg")])

    final=feats[0]

    d={}
    for u in range(0,len(feats)):
      distances, indices=neighbors.kneighbors([feats[u]])
      
      for t in range(0,len(distances[0])):
        d.update({distances[0][t]:indices[0][t]})
    sorted_list=sorted(d)

    indices=[]
    for y in range(0,30):
        indices.append(d[sorted_list[y]])
    
    j=""
    for a in indices:
        p=a//20
        o=a%20
        j+=("https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2005-08-29/250m/4/"+str(p)+"/"+str(o)+".jpg###")

    return j



    

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)
