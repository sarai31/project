# Import the Twython class
import datetime

import maya
import mysql.connector
from twython import TwythonStreamer
import json
import twitter




mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="schema1"
)

# Load credentials from json file
with open("token.json", "r") as file:
    creds = json.load(file)

print(creds)

api = twitter.Api(consumer_key=creds['apiKey'],
                      consumer_secret=creds['apiSecretKey'],
                      access_token_key=creds['accessToken'],
                      access_token_secret=creds['accessTokenSecret'])
print(api.VerifyCredentials())
r = api.GetStreamSample(delimited=False, stall_warnings=True)

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

def process_tweet(tweet):
    if (tweet['entities']['hashtags']):
        d = {}
        d['id'] = tweet['id']
        d['hashtags'] = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
        d['text'] = tweet['text']
        d['user'] = tweet['user']['screen_name']
        d['user_loc'] = tweet['user']['location']
        d['created_at'] = tweet['created_at']
        d['lang'] = tweet['lang']

        try:
            datetime_parsed = maya.parse( d['created_at']).datetime()
            sql = "INSERT IGNORE INTO twitter_table (id,created_at,data) VALUES (%s, %s, %s)"
            val = (d['id'], datetime_parsed.strftime('%Y-%m-%d %H:%M:%S'), deEmojify(json.dumps(d)))

            mycursor = mydb.cursor()
            mycursor.execute(sql, val)

            mydb.commit()

            #print(d)
        except Exception as e:
            print("exception - ", datetime.datetime.now(), e)
        return d
    else:
        return True

class MyStreamer(TwythonStreamer):
    # Received data
    def on_success(self, data):

        # Only collect tweets in English
        if 'text' in data:
            tweet_data = process_tweet(data)
            #print(tweet_data, '\n', deEmojify(json.dumps(tweet_data)))

    # Problem with the API
    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()


# Instantiate from our streaming class
stream = MyStreamer(creds['apiKey'], creds['apiSecretKey'],
                    creds['accessToken'], creds['accessTokenSecret'])
# Start the stream
while(True):
    try:
        stream.statuses.sample(filter_level='none')
    except Exception as ex:
        print("Exception", datetime.datetime.now(), ex)


