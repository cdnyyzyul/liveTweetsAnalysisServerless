from __future__ import print_function

import base64
import json
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import re


def preProcess_data(text):
    text = text.lower()
    new_text = re.sub('[^a-zA-z0-9\s]', '', text)
    new_text = re.sub('rt', '', new_text)
    return new_text


data = pd.read_csv('Sentiment.csv')
tokenizer = Tokenizer(num_words=2000, split=' ')
tokenizer.fit_on_texts(data['text'].values)


def my_pipeline(text):
    text_new = preProcess_data(text)
    X = tokenizer.texts_to_sequences(pd.Series(text_new).values)
    X = pad_sequences(X, maxlen=28)
    return X


loaded_model = tf.keras.models.load_model('sentiment.h5')

print('NZ LOG: Loading function')

def handler(event, context):
    output = []

    for record in event['records']:
        payload = base64.b64decode(record['data']).decode('utf-8').strip()
        print("NZ LOG payload: ", payload)

        clean_text = my_pipeline(payload)
        predictions = loaded_model.predict(clean_text)
        sentiment = int(np.argmax(predictions))  # the index of the max value
        probability = max(predictions.tolist()[0])
        print(sentiment)
        if sentiment == 0:
            t_sentiment = 'Negative'
        elif sentiment == 1:
            t_sentiment = 'Neutral'
        elif sentiment == 2:
            t_sentiment = 'Positive'

        data_record = {
            'message': payload,
            'sentiment': t_sentiment,
            'score': probability
        }

        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(json.dumps(data_record).encode('utf-8')).decode('utf-8')
        }
        print("NZ LOG: output_record: ", output_record)

        output.append(output_record)

    print("NZ LOG: output: ", output)
    print("=" * 50)
    return {'records': output}
