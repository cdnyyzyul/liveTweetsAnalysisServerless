from __future__ import print_function

import base64
import json
import requests

# Send message to web service to get prediction

print('NZ LOG: Loading function')

ec2_host = "172.31.83.21"
url = "http://" + ec2_host + ":8000/predict"


def lambda_handler(event, context):
    output = []

    for record in event['records']:
        payload = base64.b64decode(record['data']).decode('utf-8').strip()
        # print("NZ LOG payload: ", payload)

        data = {"text": payload}

        print("NZ LOG: data: ", data)

        response = requests.post(url, json=data)
        response_json = response.json()
        print("NZ LOG: response.json()", response_json)

        sentiment = response_json.get("sentiment")
        score = response_json.get("score")

        data_record = {
            'message': payload,
            'sentiment': sentiment,
            'score': score
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
