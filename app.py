import numpy as np
from fastapi import FastAPI
from fastapi import Request
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import re

# web service for prediction. (EC2)

def preProcess_data(text):
    
    text = text.lower()
    new_text = re.sub('[^a-zA-z0-9\s]','',text)
    new_text = re.sub('rt', '', new_text)
    return new_text

app = FastAPI()

data = pd.read_csv('Sentiment.csv')
tokenizer = Tokenizer(num_words=2000, split=' ')
tokenizer.fit_on_texts(data['text'].values)


def my_pipeline(text):
  text_new = preProcess_data(text)
  X = tokenizer.texts_to_sequences(pd.Series(text_new).values)
  X = pad_sequences(X, maxlen=28)
  return X


loaded_model = tf.keras.models.load_model('sentiment.h5')

@app.get('/')
def basic_view():
    return {"WELCOME": "GO TO /docs route, or send post request to /predict "}


@app.post('/predict')
async def predict(request: Request):
    #print(request)
    req_info = await request.json()
    #print(req_info)
    text = req_info.get("text")
    clean_text = my_pipeline(text)
    #loaded_model = tf.keras.models.load_model('sentiment.h5')
    predictions = loaded_model.predict(clean_text)
    sentiment = int(np.argmax(predictions))   # the index of the max value
    probability = max(predictions.tolist()[0])
    print(sentiment)
    if sentiment==0:
        t_sentiment = 'Negative'
    elif sentiment==1:
        t_sentiment = 'Neutral'
    elif sentiment==2:
        t_sentiment='Positive'
    
    return {
        "message": text,
        "sentiment": t_sentiment,
        "score": probability
    }

