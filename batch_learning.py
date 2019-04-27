from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import pickle
import os
from time import time
import pandas as pd
from mylib.tokenizer import tokenizer, tokenizer_porter
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb+srv://khj68:1234@cluster0-jaaex.mongodb.net/test?retryWrites=true')
db = client.graddb
collection = db.batch
cur_data = collection.find_one()
data_size = cur_data['batch']['data']
cur_num = cur_data['batch']['num']

df = pd.read_csv('./data/refined_movie_review.csv')

# X_train = df.loc[:35000, 'review'].values
# y_train = df.loc[:35000, 'sentiment'].values
# X_test = df.loc[15000:, 'review'].values
# y_test = df.loc[15000:, 'sentiment'].values
print('current data size is ', data_size)
print('current index is ', cur_num)

X_train = df.loc[:cur_num, 'review'].values
y_train = df.loc[:cur_num, 'sentiment'].values
X_test = df.loc[35000:, 'review'].values
y_test = df.loc[35000:, 'sentiment'].values

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
dest = os.path.join(curDir, 'data', 'pklObject')
if not os.path.exists(dest):
  os.makedirs(dest)

pickle.dump(lr_tfidf, open(os.path.join(dest, 'classifier.pkl'), 'wb'), protocol=4)
print('finish saving machine learning data')


if(cur_num + 5000 > data_size) :
  new_data = { "$set" : { "batch" : {"data" : 50000, "num" : 5000 }}}
  collection.update_one(cur_data, new_data)
else:
  new_data = { "$set" : { "batch" : {"data" : 50000, "num" : cur_num+5000 }}}
  collection.update_one(cur_data, new_data)