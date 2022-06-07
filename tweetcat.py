# https://www.reddit.com/r/Catswithjobs/
# https://www.reddit.com/r/CatsInBusinessAttire/
# https://twitter.com/CatWorkers
# I was able to download images using something like
# req = requests.get(lnk) if not req.ok: raise Exception("Bad image Link") filePath = './images/{0}.png'.format(uuid.uuid4()) with open(filePath, 'wb') as handler: handler.write(req.content) data["imageLink"] = filePath return data
#https://www.reddit.com/dev/api/
#https://www/reddit.com/pres/apps

from os import environ
from datetime import datetime, timedelta

import tweepy
import gspread

from dotenv import load_dotenv
load_dotenv()

import requests
import requests.auth

#Authenticate Reddit App
client_auth = requests.auth.HTTPBasicAuth(environ['REDDIT_API_SECRET'], environ['REDDIT_PERSONAL_USE_SCRIPT'])

post_data = {
    'grant_type': 'password',
    'username' : environ['REDDIT_USERNAME'],
    'password' : environ['REDDIT_PW'],
    'duration': 'permanent',
    'scope': '*'
}
headers = {'User-Agent': 'TwitterCatAPI/0.0.1 by Bargonzo'}
#Getting Token Access ID
TOKEN_ACCESS_ENDPOINT = 'https://www.reddit.com/api/v1/access_token'
response = requests.post(TOKEN_ACCESS_ENDPOINT, data=post_data, headers=headers, auth=client_auth)
print(response.json())

if response.status_code == 200:
    token_id = response.json()['access_token']
    OAUTH_ENDPOINT = 'https://oauth.reddit.com'
    params_get = {
        'limit': 100
    }
    headers_get = {
        'User-Agent': 'TwitterCatAPI/0.0.1 by Bargonzo',
        'Authorization' :'Bearer ' + token_id
    }
    response2 = requests.get(OAUTH_ENDPOINT + '/r/catsatwork/new/', headers = headers_get, params=params_get)
    data = response2.json()
    posts = data['data']['children']
    after_key = data['data']['after']
    before_key = data['data']['before']

# TOKEN = res.json()['access_token']
# print(TOKEN)

# # SAVE THE json FROM GOOGLE DEVELOPER CONSOLER FIRST
# gc = gspread.service_account(filename='googledrive_credentials.json')
# sh = gc.open_by_key("your_sheet_key")
# worksheet = sh.sheet1

# CONSUMER_KEY = environ['CONSUMER_KEY']
# CONSUMER_SECRET = environ['CONSUMER_SECRET']
# ACCESS_TOKEN = environ['ACCESS_TOKEN']
# ACCESS_SECRET = environ['ACCESS_SECRET']

# auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# tweet_api = tweepy.API(auth)

# def get_now_time_normalized():
#     return datetime.now()
#     # modify if needed, e.g.:
#     # return datetime.utcnow() + timedelta(hours=1)

# def check_and_update_tweets():
#     tweets = worksheet.get_all_records()
#     for row_idx, tweet in enumerate(tweets, start=2):
#         msg = tweet['message']
#         time_str = tweet['time']
#         done = tweet['done']
                
#         post_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
#         if not done:
#             now_time = get_now_time_normalized()
#             if post_time < now_time:
#                 try:
#                     tweet_api.update_status(msg)
#                     worksheet.update_cell(row_idx, 3, 1)  # row, col, value
#                 except Exception as e:
#                     print(f'exception during tweet! {e}')


# if __name__ == '__main__':
#     check_and_update_tweets()