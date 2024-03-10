
import requests
import os
import json

# search a defined number of tweets. Default number = 10


os.chdir("/LOG8415/personal_project")


def auth():
    with open("config.json") as cj:
        settings = json.load(cj)
    return settings['TOKEN']


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def create_url(keyword, start_date, end_date, max_results=10):
    search_url = "https://api.twitter.com/2/tweets/search/recent"

    query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return (search_url, query_params)


def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

#Inputs for the request
bearer_token = auth()
headers = create_headers(bearer_token)
keyword = "(happy OR happiness) lang:en"
start_time = "2021-11-29T00:00:00.000Z"
end_time = "2021-12-02T00:00:00.000Z"
max_results = 10

def get_tweets():
    url = create_url(keyword, start_time,end_time, max_results)
    print(url[0])
    json_response = connect_to_endpoint(url[0], headers, url[1])
    return json_response

if __name__ == "__main__":
    caught_tweets = get_tweets()
    print(json.dumps(caught_tweets, indent=4, sort_keys=True))

    with open('results/tweets_data.json', 'w') as f:
        json.dump(caught_tweets, f)