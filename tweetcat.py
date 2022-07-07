import sys
import os
from os.path import exists
from os import environ
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

import requests 
import requests.auth
import urllib
import tweepy

import pickle
from keep_alive import keep_alive

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
#Getting Reddit Token Access ID
TOKEN_ACCESS_ENDPOINT = 'https://www.reddit.com/api/v1/access_token'
response = requests.post(TOKEN_ACCESS_ENDPOINT, data=post_data, headers=headers, auth=client_auth)
#Twitter Access Data and Authentication
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
tweet_api.verify_credentials()
print('Successful Authentication')

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
        response2 = requests.get(OAUTH_ENDPOINT + '/r/catswithjobs/new/', headers = headers_get, params=params_get)
        data = response2.json()
        posts = data['data']['children']
        # after_key = data['data']['after']
        # before_key = data['data']['before']
        with open('postIDs.pkl', 'rb') as f:
            listOfPostId = pickle.load(f)
        count = 0
        # Will check if posts IDs are already in pickle file, if they arent they will be posted on twitter
        while(count<3):
            to_extract = ['title','url','id']
            
            if not(posts[count]['data']['is_video']) and posts[count]['data']['id'] not in listOfPostId and 'jpg' in posts[count]['data']['url']:
                for e in to_extract:
                    print(f"{e}: {posts[count]['data'][e]}")
                title = posts[count]['data']['title']
                imageURL = posts[count]['data']['url']
                urllib.request.urlretrieve(imageURL, "redditimg.jpg")
                listOfPostId.append(posts[count]['data']['id'])
                tweet_api.update_status_with_media(title, 'redditimg.jpg')
                print('image posted on twitter')
            else:
                print("Reddit post already posted on twitter")
            count+=1
        with open('postIDs.pkl', 'wb') as f:
            pickle.dump(listOfPostId, f)
        if(exists('redditimg.jpg')):
            os.remove('redditimg.jpg')
            print('Image removed')
        print(listOfPostId)

        # printing reddit post keys
        # for post in posts[0]['data'].keys():
        #     print(post)

        # print("before key: " + str(before_key))
        # print("after key: " + str(after_key))
  
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(e).__name__, e.args)
    print(message)
    print(exc_type, fname, exc_tb.tb_lineno)

keep_alive()
