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



# def install_and_import(package) :
#   import importlib
#   try :
#     importlib.import_module(package)
#   except ImportError:
#     from pip._internal import main as pipmain
#     pipmain(['install', package])
#   # finally:
#   #   globals()[package] = importlib.import_module(package)


def lambda_handler(event, context) :
  start = time()
  
  # s3 = boto3.resource('s3')
  # for bucket in s3.buckets.all() :
    # print(bucket.name)
  # bucket = s3.Bucket('mlbucket12156')
  # print(bucket)
  # for obj in bucket.objects.all() :
  #   print(obj)

  s3_client = boto3.client('s3', aws_access_key_id='AKIA55B2JG5FI5LA5NGZ', aws_secret_access_key='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')
  result = s3_client.get_bucket_acl(Bucket='mlbucket12156')
  print(result)
  s3_client.download_file('mlbucket12156','classifier.pkl', '/tmp/classifier.pkl')
  s3_client.download_file('mlbucket12156','refined_movie_review.csv', '/tmp/refined_movie_review.csv')


  client = MongoClient('mongodb+srv://khj68:1234@cluster0-jaaex.mongodb.net/test?retryWrites=true')
  db = client.graddb
  collection = db.batch
  cur_data = collection.find_one()
  data_size = cur_data['batch']['data']
  cur_num = cur_data['batch']['num']
  c_version = cur_data['batch']['c_version']
  updated = cur_data['batch']['updated']

  df = pd.read_csv('/tmp/refined_movie_review.csv')

  print('current data size : ', data_size)
  print('current index : ', cur_num)
  print('current version : ', c_version)

  X_train = df.loc[cur_num - 5000 :cur_num, 'review'].values
  y_train = df.loc[cur_num - 5000 :cur_num, 'sentiment'].values
  X_test = df.loc[45000:, 'review'].values
  y_test = df.loc[45000:, 'sentiment'].values

  tfidf = TfidfVectorizer(lowercase=False, tokenizer=tokenizer)
  lr_tfidf = Pipeline([('vect', tfidf), ('clf', LogisticRegression(C=10.0, penalty='l2', random_state=0))])

  stime = time()
  print('start machine learning')
  lr_tfidf.fit(X_train, y_train)
  print('finish machine learning')

  y_pred = lr_tfidf.predict(X_test)
  print('finish test : time [%d]s' %(time()-stime))
  print('precision: %.3f' %accuracy_score(y_test, y_pred))

  curDir = os.getcwd()
  # dest = os.path.join(curDir, 'tmp', 'pklObject')
  dest = os.path.join('/tmp/', 'pklObject')
  if not os.path.exists(dest):
    os.makedirs(dest)

  # pickle.dump(lr_tfidf, open(os.path.join(dest, 'tmp.pkl'), 'wb'), protocol=4)
  pickle.dump(lr_tfidf, open(os.path.join(dest, 'classifier.pkl'), 'wb'), protocol=4)
  print('finish saving machine learning data')


  if(cur_num + 5000 > data_size) :
    new_data = { "$set" : { "batch" : {"data" : 50000, "num" : 5000 , "n_version" : c_version+1, "c_version":c_version, "updated":updated}}}
    collection.update_one(cur_data, new_data)
  else:
    new_data = { "$set" : { "batch" : {"data" : 50000, "num" : cur_num+5000 , "n_version" : c_version+1, "c_version":c_version, "updated":updated}}}
    collection.update_one(cur_data, new_data)

  s3_client.upload_file('/tmp/classifier.pkl', 'mlbucket12156', 'new_classifier.pkl')
  print('uploaded to S3')

  end = time() - start
  print('time:', end)

  return {
    'statusCode': 200,
    'body': json.dumps('model updated')
  }
