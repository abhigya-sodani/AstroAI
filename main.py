
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
from tensorflow.keras.layers import Input, Flatten, Dense, Dropout, GlobalAveragePooling2D
import wget
import cv2

def extract_model_till_layer(model, layerNo):
  outputs = model.layers[layerNo].output
  model = Model(inputs=model.inputs, outputs=outputs)
  return model


class SimpleConverter(BaseConverter):

    def to_python(self, value):
        value=value.replace("?","*")
        return value.replace


    
model1 = ResNet50(weights='imagenet',
                         include_top=False,
                         input_shape=(512, 512, 3),
                        pooling='max')

model2 = tf.keras.models.load_model('best_worldview_2.h5')

def extract_features(url, model):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    a=np.asarray(img)
    a=np.resize(a,(1,512,512,3))
    preprocessed_img = preprocess_input(a)
    features = model.predict(preprocessed_img)
    flattened_features = features.flatten()
    normalized_features = flattened_features / norm(flattened_features)
    return normalized_features

def eF(url, model):
    response = wget.download(url)
    a = cv2.imread(response)
    os.remove(response)
    a=np.resize(a,(1,224,224,3))
    a=a/255
    features=model.predict(a)
    flattened_features=features.flatten()
    normalized_features=flattened_features / norm(flattened_features)
    return normalized_features

app = Flask(__name__)

CORS(app)

def findNearestSmall(url, count):
    u=AnnoyIndex(128)
    u.load('fullDatabase.ann')
    indexes = u.get_nns_by_vector(extract_features(url,extract_model_till_layer(model2,10)),
                             count,
                              include_distances=True)

    j=""
    for a in indexes[0]:
        p=a//320
        o=a%320
        j+=("https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2012-07-09/250m/8/"+str(p)+"/"+str(o)+".jpg###")
    return j

def findNearestBig(url, count):
    u1=AnnoyIndex(128)
    u1.load('hurricanes1.ann')
    indexes = u1.get_nns_by_vector(eF(url,extract_model_till_layer(model2,10)),
                             count,
                              include_distances=True)
    j=""
    for a in indexes[0]:
        p=a//20
        o=a%20
        j+=("https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2005-08-29/250m/4/"+str(p)+"/"+str(o)+".jpg###")
    return j
    

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route("/resnet/")
def thing():
    a=request.args.get('url')+"?REQUEST="+request.args.get('REQUEST')+"&TIME="+request.args.get('TIME')+"&BBOX="+request.args.get('BBOX')+"&CRS="+request.args.get('CRS')+"&LAYERS="+request.args.get("LAYERS")+"&WRAP="+request.args.get("WRAP")+"&FORMAT="+request.args.get('FORMAT')+"&WIDTH="+request.args.get('WIDTH')+"&HEIGHT="+request.args.get('HEIGHT')+"&ts="+request.args.get('ts')

    bbox=request.args.get('BBOX')
    arr=bbox.split(",")
    arr=[float(a) for a in arr]
    size=abs(arr[0]-arr[2])*abs(arr[1]-arr[3])
    j=""
    if(size>250):
        j=findNearestBig(a,int(request.args.get('count')))
    if(size<=250):
        j=findNearestSmall(a,int(request.args.get('count')))
        
    
    
    return j
    
@app.route("/multi/")
def other():
    uA=AnnoyIndex(128)
    uA.load('fullDatabase.ann')

    a=request.args.get('url')
    urlL=a.split("|||")
    urlLL=[]
    for i in urlL:
        urlLL.append(i.split("***"))

    feats=[]

    for u in urlLL:
        a=int(u[0])
        b=int(u[1])
        feats.append(uA.get_item_vector((a)*320+b))

    final=feats[0]

    for y in range(1,len(feats)):
        list( map(add, final, feats[y]) )

    final=[x / len(feats) for x in final]

    indexes = uA.get_nns_by_vector(final,
                              int(request.args.get('count')),
                              include_distances=True)
    
    j=""
    for a in indexes[0]:
        p=a//320
        o=a%320
        j+=("https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2012-07-09/250m/8/"+str(p)+"/"+str(o)+".jpg###")

    return j



@app.route("/multiBig/")
def otherOne():
    uA=AnnoyIndex(128)
    uA.load('hurricanes1.ann')

    a=request.args.get('url')
    urlL=a.split("|||")
    urlLL=[]
    for i in urlL:
        urlLL.append(i.split("***"))

    feats=[]

    for u in urlLL:
        a=int(u[0])
        b=int(u[1])
        feats.append(uA.get_item_vector((a)*20+b))

    final=feats[0]

    for y in range(1,len(feats)):
        list( map(add, final, feats[y]) )

    final=[x / len(feats) for x in final]

    indexes = uA.get_nns_by_vector(final,
                              int(request.args.get('count')),
                              include_distances=True)
    
    j=""
    for a in indexes[0]:
        p=a//20
        o=a%20
        j+=("https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2005-08-29/250m/4/"+str(p)+"/"+str(o)+".jpg###")

    return j


@app.route("/simclr/")
def thingR():
    a=request.args.get('url')+"?REQUEST="+request.args.get('REQUEST')+"&TIME="+request.args.get('TIME')+"&BBOX="+request.args.get('BBOX')+"&CRS="+request.args.get('CRS')+"&LAYERS="+request.args.get("LAYERS")+"&WRAP="+request.args.get("WRAP")+"&FORMAT="+request.args.get('FORMAT')+"&WIDTH="+request.args.get('WIDTH')+"&HEIGHT="+request.args.get('HEIGHT')+"&ts="+request.args.get('ts')

    
    
    u=AnnoyIndex(128)
    u.load('imageFeatSuhas.ann')
    indexes = u.get_nns_by_vector(eF(a,model2),
                              30,
                              include_distances=True)
    j=""
    for a in indexes[0]:
        p=a//320
        o=a%320
        j+=("https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2012-07-09/250m/8/"+str(p+100)+"/"+str(o)+".jpg###")
    return j
    
    

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)
