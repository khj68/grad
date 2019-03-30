import re
import pandas as pd
from time import time

def preprocessor(text):
  # remove special characters and html tag except emoticons
  text = re.sub('<[^>]*>', '', text)
  emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)|\^.?\^', text)
  text = re.sub('[\W]+', ' ', text.lower()) + ' '.join(emoticons).replace('-', '')

  return text

df = pd.read_csv('./data/movie_review.csv')

stime = time()
print('start preprocessor')
df['review'] = df['review'].apply(preprocessor)
print('complete preprocessor : time [%d]s' %(time()-stime))

df.to_csv('./data/refined_movie_review.csv', index=False)