from __future__ import print_function

import base64
import json
import boto3

print('Loading function')


def lambda_handler(event, context):
    output = []

    for record in event['records']:
        payload = base64.b64decode(record['data']).decode('utf-8').strip()
        print(payload)

        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
        sentiment_all = comprehend.detect_sentiment(Text=payload, LanguageCode='en')
        sentiment = sentiment_all['Sentiment']
        print(sentiment)
        positive = sentiment_all['SentimentScore']['Positive']
        negative = sentiment_all['SentimentScore']['Negative']
        mixed = sentiment_all['SentimentScore']['Mixed']
        neutral = sentiment_all['SentimentScore']['Neutral']
        total = positive - negative
        print(total)

        data_record = {
            'message': payload,
            'sentiment': sentiment,
            'total': total
        }
        print(data_record)

        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(json.dumps(data_record).encode('utf-8')).decode('utf-8')
        }
        print(output_record)

        output.append(output_record)

    print(output)
    return {'records': output}