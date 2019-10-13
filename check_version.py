import boto3
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


def lambda_handler(event, context) :

  # s3 = boto3.resource('s3')
  # for bucket in s3.buckets.all() :
  #   print(bucket.name)
  # bucket = s3.Bucket('mlbucket12156')
  # print(bucket)
  # for obj in bucket.objects.all() :
  #   print(obj)

  s3_client = boto3.client('s3', aws_access_key_id='AKIA55B2JG5FI5LA5NGZ', aws_secret_access_key='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')
  result = s3_client.get_bucket_acl(Bucket='mlbucket12156')
  # print(result)


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
    s3_client.download_file('mlbucket12156','new_classifier.pkl', '/tmp/new_classifier.pkl')
    s3_client.upload_file('/tmp/new_classifier.pkl', 'mlbucket12156', 'classifier.pkl')
    print('Current version is old. Update implemented.')
    pinrt('version checked. model updated. your version is now newest.')    
  else :
    print("Current version is new. Don't need to update.")
    print('version checked. your version is already newest.')
