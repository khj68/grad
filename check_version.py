from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import pickle
import os
from time import time
import pandas as pd
from mylib.tokenizer import tokenizer
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

stime = time()


client = MongoClient('mongodb+srv://khj68:1234@cluster0-jaaex.mongodb.net/test?retryWrites=true')
db = client.graddb
collection = db.batch_aws
cur_data = collection.find_one()
data_size = cur_data['batch']['data']
cur_num = cur_data['batch']['num']
n_version = cur_data['batch']['n_version']
c_version = cur_data['batch']['c_version']
updated = cur_data['batch']['updated']
print('current version : ', c_version)
print('new version : ', n_version)

if n_version > c_version :
  new_data = { "$set" : { "batch" : {"data" : data_size, "num" : cur_num , "n_version" : n_version, "c_version":n_version, "updated":1}}}
  collection.update_one(cur_data, new_data)
  os.rename("./data/pklObject/n_classifier.pkl","./data/pklObject/classifier.pkl")
  print('Current version is old. Update implemented.')
  print('version checked. model updated. your version is now newest.')    
else :
  print("Current version is new. Don't need to update.")
  print('version checked. your version is already newest.')

print(time()-stime)
