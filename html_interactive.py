import pickle
import os
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
import cgi, cgitb

form = cgi.FieldStorage()

name = form.getvalue('name')
comment = form.getvalue('textcontent')

df = pd.read_csv('./data/refined_movie_review.csv')

X_train = df.loc[:35000, 'review'].values
y_train = df.loc[:35000, 'sentiment'].values
X_test = df.loc[15000:, 'review'].values
y_test = df.loc[15000:, 'sentiment'].values

curDir = os.getcwd()
clf = pickle.load(open(os.path.join(curDir, 'data', 'pklObject', 'classifier.pkl'), 'rb'))

y_pred = clf.predict(X_test)
# print('precission of test : %.3f' %accuracy_score(y_test, y_pred))

label = {0:'negative comment', 1:'positive comment'}

  
example = [comment]
print('Content-type:text/html\r\n\r\n')
print('<html>')
print('<head>')
print('<title>MACHINE LEARNING RESULT</title>')
print('</head>')
print('<body>')
print('prediction: %s\nprecision: %.3f%%' %(label[clf.predict(example)[0]], np.max(clf.predict_proba(example))*100))
print('</body>')
print('</html>')