from annoy import AnnoyIndex
import requests
from io import BytesIO
import cv2
import PIL
from PIL import Image
import numpy as np
import time
import numpy as np
from numpy.linalg import norm
import pickle
from tqdm import tqdm, tqdm_notebook
import os
import random
import time
import math
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

model2 = ResNet50(weights='imagenet',
                         include_top=False,
                         input_shape=(512, 512, 3),
                        pooling='max')
model = tf.keras.models.load_model('best_worldview_2.h5')
model.summary()

def extract_model_till_layer(model, layerNo):
  outputs = model.layers[layerNo].output
  model = Model(inputs=model.inputs, outputs=outputs)
  return model
model1=extract_model_till_layer(model,10)
                      
features=[]
try:
    
    baseUrl="https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2012-07-09/250m/8/29/0.jpg"
    def extract_features(url, model):
        
       
        
        a = np.asarray(PIL.Image.open('C://Users//abhig//level8images//'+url))
       
        a=np.resize(a,(1,224,224,3))
        a=a/255       
        #preprocessed_img = preprocess_input(a)
        features = model.predict(a)
        flattened_features = features.flatten()
        normalized_features = flattened_features / norm(flattened_features)
        return normalized_features

    counter=1
    for filename in os.listdir("C://Users//abhig//level8images"):
            a=extract_features(filename, model1)
            print("length",len(a))
            features.append(a)
            print(counter)
            counter+=1
       
    print(len(features[0]))
    print(features[0])


     # Length of item vector that will be indexed
    t=AnnoyIndex(len(features[0]))
    for p in range(len(features)):
        feature = features[p]
        t.add_item(p, feature)

    t.build(40)  # 50 trees
    t.save('fullDatabase.ann')

except:
    print("aaaa")
    t=AnnoyIndex(features[0])
    for p in range(len(features)):
        feature = features[p]
        t.add_item(p, feature)

    t.build(40)  # 50 trees
    t.save('fullDatabase.ann')
