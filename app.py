import streamlit as st
import pickle
import string
import joblib
from nltk.corpus import stopwords
import nltk 
nltk.download('stopwords')
nltk.download('punkt')

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
tfidf = joblib.load(open('Vectorizer.pkl','rb'))
model = joblib.load(open('model.pkl','rb'))

st.title("Email/SMS spam classifier")

input_sms = st.text_input("Enter the message")

def transform_text(text):
  text = text.lower()
  text = nltk.word_tokenize(text)
  
  y = []
  for i in text:
    if i.isalnum():
      y.append(i)
  
  text = y[:]
  y.clear()

  for i in text:
    if i not in stopwords.words('english') and i not in string.punctuation:
      y.append(i)
  
  text = y[:]
  y.clear()
  
  for i in text:
    y.append(ps.stem(i))

  return " ".join(y) 

if st.button('Predict'):
#1 preprocess
   transformed_sms = transform_text(input_sms)
#2 vectorize
   vector_input = tfidf.transform([transformed_sms])
#3 predict
   result = model.predict(vector_input)[0]
#4 display
   if result == 1:
      st.header("Spam")
   else:
      st.header("Not Spam")

