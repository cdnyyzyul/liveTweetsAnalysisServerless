import boto3

# download the trained model and then initialize the model.
def get_model():
    bucket= boto3.resource('s3').Bucket('deploy-ml-tst')
    bucket.download_file('model/saved_model.txt','/tmp/test_model.txt')
    model= lightgbm.Booster(model_file='/tmp/test_model.txt')
    # bucket.download_file('model/saved_model.txt','test_model.txt')
    # model= lightgbm.Booster(model_file='test_model.txt')
    return model

# get the model, a data sample, do a prediction
def predict(event):
    print("+" * 30)
    print(event, type(event))
    sample =event['body']
    print(sample)
    model = get_model()
    result = model.predict(sample)
    return result

def lambda_handler(event,context):
    result = predict(event)
    return {'StatusCode':200,
    'body':result[0]}
    