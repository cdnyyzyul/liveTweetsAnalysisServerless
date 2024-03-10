import boto3
import json
import os
import tweepy

# stream tweets, write to Data Firehose

os.chdir("C:\\Users\\nazho\\my_repo\\LOG8415\personal_project")

# aws eduction account: copy and paste your AWS education account keys into ̃/.aws/credentials, run”aws s3 ls”
with open('config.json') as secrets:
  settings = json.load(secrets)

# aws education account access key is set in ̃/.aws/credentials
firehose = boto3.client('firehose',
                        region_name = settings["region_name"])


# auth = tweepy.OAuthHandler(settings["twitter_consumer_key"],
#                            settings["twitter_consumer_secret"])
# auth.set_access_token(settings["twitter_access_token"], settings["twitter_access_token_secret"])


stream = tweepy.Stream(
  settings["twitter_consumer_key"], settings["twitter_consumer_secret"],
  settings["twitter_access_token"], settings["twitter_access_token_secret"]
)

class IDPrinter(tweepy.Stream):

    def on_data(self, data):
        tmpdata = json.loads(data)
        if tmpdata.get('lang') == "en":
            print(tmpdata.get('text'))
         #   time.sleep(0.1)
            #print(tmpdata.get('lang'))
           # print(json.dumps(tmpdata, indent=4, sort_keys=True))
            response = firehose.put_record(DeliveryStreamName=settings["stream_name"],
                                           Record={'Data': tmpdata.get('text')}
                                           )
            print(response)

    def on_error(self, status):
        print(status)

# main starts
printer = IDPrinter(
  settings["twitter_consumer_key"], settings["twitter_consumer_secret"],
  settings["twitter_access_token"], settings["twitter_access_token_secret"]
)
printer.sample()









