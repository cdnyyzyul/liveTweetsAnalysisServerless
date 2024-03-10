import boto3
from LOG8415.personal_project.twitterAPI_getTweets import *

# call get_Tweets (to get a defined number of tweets, write them to firehose.

os.chdir("C:\\Users\\nazho\\my_repo\\LOG8415\personal_project")

# aws eduction account: copy and paste your AWS education account keys into ̃/.aws/credentials, run”aws s3 ls”
with open('config.json') as secrets:
  settings = json.load(secrets)

# firehose = boto3.client('firehose',
#                         aws_access_key_id = settings["aws_access_key_id"],
#                         aws_secret_access_key = settings["aws_secret_access_key"] ,
#                         region_name = settings["region_name"])

# aws education account access key is set in ̃/.aws/credentials
firehose = boto3.client('firehose',
                        region_name = settings["region_name"])

#replace it with getTweets
# print("\n> Loading data from tweets_data.json")
# with open('results/tweets_data1.json') as f:
#   tweets = json.load(f)

num_tweets_to_get = 2

while num_tweets_to_get >= 0:
# get tweets live.
  tweets = get_tweets()
  num_tweets_to_get -= 1

  count = 0
  print("\n> sending data, check out S3 bucket.")
  for tweet in tweets["data"]:
    print("sending entry: ", str(count))
    print(tweet["text"])
    response = firehose.put_record(
      DeliveryStreamName=settings["stream_name"],
      Record={
        'Data': tweet["text"]
      }
    )
    print(response)
    count += 1
    time.sleep(0.5)