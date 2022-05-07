import sqlite3
import json
import threading

import tweepy #version 3.10.0 / StreamListener is working on Tweepy version 3.10.0
import credentials


#DB connection is set
connection=sqlite3.connect('Twitter.db')
cursor=connection.cursor()

#Twitter Authentication Credentials are set
#consumer_key , consumer_secret , access_token, access_token_secret

auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
auth.set_access_token(credentials.access_token, credentials.access_token_secret)
api = tweepy.API(auth)
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        print(status_code)

    def on_data(self,data):
        # Twitter returns data in JSON format
        all_data        = json.loads(data)
        user_name       = all_data['user']['name']
        id              = all_data['id']
        text            = all_data['text']
        created_at      = all_data['created_at']
        user_location   = all_data['user']['location']

        try:
            cursor.execute(f"INSERT INTO tweets (user_name,id,text,date,location) VALUES ('{user_name}', '{id}', '{text}','{created_at}','{user_location}')")
            connection.commit()
        except sqlite3.Error: #sqlite3.IntegrityError UNIQUE constraint failed
            print("Bu tweet zaten veritabanında mevcut.")


if __name__ == '__main__':
    '''  
    Bounding boxes for geolocations 
    Online-Tool to create boxes (c+p as raw CSV): http://boundingbox.klokantech.com/   
    '''
    GEOBOX_WORLD = [-180, -90, 180, 90]
    GEOBOX_TURKEY = [25.62, 35.81, 44.82, 42.3]

    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener, threading=True)
    stream.filter(track=['dolar -filter:retweets'], languages=['tr'], locations=GEOBOX_TURKEY)






























