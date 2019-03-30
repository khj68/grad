from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

porter = PorterStemmer()
stop = stopwords.words('english')

# torkenize by whitespace
def tokenizer(text):
  return text.split()

# torkenize by Porter Stemming Algorithm
def tokenizer_porter(text):
  return [porter.stem(word) for word in text.split()]