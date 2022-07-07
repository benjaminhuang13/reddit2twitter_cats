# https://www.reddit.com/r/Catswithjobs/
# https://www.reddit.com/r/CatsInBusinessAttire/
# https://twitter.com/CatWorkers
# I was able to download images using something like
# req = requests.get(lnk) if not req.ok: raise Exception("Bad image Link") filePath = './images/{0}.png'.format(uuid.uuid4()) with open(filePath, 'wb') as handler: handler.write(req.content) data["imageLink"] = filePath return data
#https://www.reddit.com/dev/api/
#https://www/reddit.com/pres/apps
import os
from os import environ
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
# import tweepy
# import gspread

import requests 
import requests.auth
import urllib
import tweepy

#Authenticate Reddit App
client_auth = requests.auth.HTTPBasicAuth(os.environ['REDDIT_PERSONAL_USE_SCRIPT'], os.environ['REDDIT_API_SECRET'])

post_data = {
    'grant_type': 'password',
    'username' : os.environ['REDDIT_USERNAME'],
    'password' : os.environ['REDDIT_PW'],
    'duration': 'permanent',
    'scope': '*'
}
headers = {'User-Agent': 'TwitterCatAPI/0.0.1 by Bargonzo'}
#Getting Token Access ID
TOKEN_ACCESS_ENDPOINT = 'https://www.reddit.com/api/v1/access_token'
response = requests.post(TOKEN_ACCESS_ENDPOINT, data=post_data, headers=headers, auth=client_auth)

try:
    if response.status_code == 200:
        token_id = response.json()['access_token']
        OAUTH_ENDPOINT = 'https://oauth.reddit.com'
        params_get = {
            'limit': 100,
        }
        headers_get = {
            'User-Agent': 'TwitterCatAPI/0.0.1 by Bargonzo',
            'Authorization' :'Bearer ' + token_id
        }
        response2 = requests.get(OAUTH_ENDPOINT + '/r/catswithjobs/hot/', headers = headers_get, params=params_get)
        data = response2.json()
        posts = data['data']['children']
        after_key = data['data']['after']
        before_key = data['data']['before']
        to_extract = ['title','url']

        title = posts[1]['data']['title']
        imageURL = posts[1]['data']['url']
        if(posts[1]['data']['is_video']):
            urllib.request.urlretrieve(imageURL, "redditvid.mp4")
        else:
            urllib.request.urlretrieve(imageURL, "redditimg.jpg")
        #assess twitter
        CONSUMER_KEY = os.environ['CONSUMER_KEY']
        CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
        ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
        ACCESS_SECRET = os.environ['ACCESS_SECRET']

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

        tweet_api = tweepy.API(auth)

        client = tweepy.Client(consumer_key=CONSUMER_KEY,
                    consumer_secret=CONSUMER_SECRET,
                    access_token=ACCESS_TOKEN,
                    access_token_secret=ACCESS_SECRET)
        # try:
        #     twitterresponse = client.create_tweet(text=title)
        
        #     print(twitterresponse)
        # except:
        #     print('Failed to post')

        
        tweet_api.verify_credentials()
        print('Successful Authentication')
        # tweet_api.update_status(title)
        # tweet_api.media_upload('redditimg.jpg', title)
        tweet_api.update_status_with_media(title, 'redditimg.jpg')
        # for e in to_extract:
        #     titleAndLink = posts[1]['data'][e]
        #     print(f"{e}: {posts[1]['data'][e]}")
        #     print(titleAndLink)

        # printing reddit post keys
        # for post in posts[0]['data'].keys():
        #     print(post)

        # print("before key: " + str(before_key))
        # print("after key: " + str(after_key))

except Exception as ex:
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print(message)
