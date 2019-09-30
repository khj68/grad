import boto3
import pickle
import os
import numpy as np
import pandas as pd
from mylib.tokenizer import tokenizer
from pymongo import MongoClient
from bson.objectid import ObjectId
from sklearn.metrics import accuracy_score
import cgi, cgitb
import sys
import json
from time import time



# s3 = boto3.resource('s3')
# for bucket in s3.buckets.all() :
#   print(bucket.name)
# bucket = s3.Bucket('mlbucket12156')
# print(bucket)
# for obj in bucket.objects.all() :
#   print(obj)
def lambda_handler(event, context) :
  start = time()
  # print(event)
  # print(event['name'][0])
  # print(event['comment'][0])
  # print(context)
  if not (os.path.exists('/tmp/classifier.pkl')) :
    s3_client = boto3.client('s3', aws_access_key_id='AKIA55B2JG5FH2ES7QJB', aws_secret_access_key='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')
    result = s3_client.get_bucket_acl(Bucket='mlbucket12156')
    s3_client.download_file('mlbucket12156','classifier.pkl', '/tmp/classifier.pkl')

  # curDir = os.getcwd()
#   clf = pickle.load(open(os.path.join(curDir, 'tmp', 'pklObject', 'classifier.pkl'), 'rb'))
  clf = pickle.load(open(os.path.join('/tmp/', 'classifier.pkl'), 'rb'))
#   clf = pickle.load(open('/tmp/classifier.pkl', 'rb'))

  label = {0:'negative comment', 1:'positive comment'}
    
  # example = [event['comment'][0]]
  example = ['I love this movie']

  # print('%s! Thank you for your comment!' %(event['name']))
  print('%s! Thank you for your comment!' %('Hyungjun'))
  print('comment : ', example[0], '\nprediction : ',label[clf.predict(example)[0]], '\nprecision : ', max(clf.predict_proba(example))[1]*100)

  end = time() - start
  print(end)
  return {
    'statusCode': 200,
    'body': json.dumps('your comment predicted')
  }
