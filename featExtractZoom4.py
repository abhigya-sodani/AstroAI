from annoy import AnnoyIndex
import requests
from io import BytesIO
import cv2
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

def extract_features(url, model):
        
       
  response = wget.download(url)
  a = cv2.imread(response)
  os.remove(response)
  a=np.resize(a,(1,224,224,3))
  a=a/255       
  #preprocessed_img = preprocess_input(a)
  features = model.predict(a)
  flattened_features = features.flatten()
  normalized_features = flattened_features / norm(flattened_features)
  return normalized_features

def extract_model_till_layer(model, layerNo):
  
  outputs = model.layers[layerNo].output
  model = Model(inputs=model.inputs, outputs=outputs)
  return model


model2 = ResNet50(weights='imagenet',
                         include_top=False,
                         input_shape=(512, 512, 3),
                        pooling='max')
model = tf.keras.models.load_model('best_worldview_2.h5') #replace with whichever model you wish to featurize with
model.summary()


model1=extract_model_till_layer(model,10) #change for what layer you want to featurize till
                      
features=[]
try:
    
   
   


    for i in range(0,10):
        for j in range(0,20):
            feats=extract_features("https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2005-08-29/250m/4/"+str(i)+"/"+str(j)+".jpg", model1)
            print("length",len(feats))
            features.append(feats)
            print(str(i)+" "+str(j))
            
        time.sleep(30)



     # Length of item vector that will be indexed
    t=AnnoyIndex(len(features[0]))
    for p in range(len(features)):
        feature = features[p]
        t.add_item(p, feature)

    t.build(40)  # 40 trees
    t.save('hurricanes1.ann')

except:
    print("Error occured, indexing the current features")
    t=AnnoyIndex(features[0])
    for p in range(len(features)):
        feature = features[p]
        t.add_item(p, feature)

    t.build(40)  # 40 trees
    t.save('hurricanes1.ann')
