
import requests
import os
import json


os.chdir("/LOG8415/personal_project")

def auth():
    with open("../config.json") as cj:
        settings = json.load(cj)
    return settings['TOKEN']


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    query_params = {
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,lang',
                    'user.fields': 'id,name,username,created_at,description'}
    return (headers, query_params)


# def create_url():
#     url = "https://api.twitter.com/2/tweets/sample/stream"
#     return (url)


def connect_to_endpoint(url, headers, query_params):
    response = requests.request("GET", url, headers = headers, params=query_params, stream=True)
    print(response.status_code)
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )


#Inputs for the request
bearer_token = auth()
headers, query_params = create_headers(bearer_token)

def get_tweets():
    url = "https://api.twitter.com/2/tweets/sample/stream"
    json_response = connect_to_endpoint(url, headers, query_params)
    return json_response

if __name__ == "__main__":
    caught_tweets = get_tweets()
    print(json.dumps(caught_tweets, indent=4, sort_keys=True))
