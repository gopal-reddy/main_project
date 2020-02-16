import credentials
import tweepy
from tweepy import StreamListener
from tweepy import Stream
import json
import csv
import re
from  textblob import TextBlob

fieldnames=["warren", "trump"]
f = open("polarity.csv", "w")
writer = csv.DictWriter(f, fieldnames)
writer.writeheader()

class getdata(StreamListener):
    
    def on_data(self, data):
        twets = json.loads(data)
        
        try:
            tweets = twets['text']
            print()
            print("tweets")
            print(tweets)
            tweets = ' '.join(re.sub('RT',' ', tweets).split())
            tweets = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweets).split())
            blob = TextBlob(tweets.strip())
            trump_polarity=""
            warren_polarity=""
            print("blob sentence")
            print()
            print(blob.sentences)
            print()
            for sent in blob.sentences:
                
                if "warren" in sent and "trump" not in sent:
                    print(sent)
                    warren_polarity = sent.sentiment.polarity
                elif "warren" not in sent and "trump" in sent:
                    print(sent)
                    trump_polarity = sent.sentiment.polarity
            
            with open('polarity.csv', 'a') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                pol_dic = {
                    'trump': trump_polarity,
                    'warren': warren_polarity
                }
                writer.writerow(pol_dic)
            
            
        except Exception as e:
            print(e)
        
    def on_error(self, status):
        print('error code')


if __name__ == "__main__":

    auth = tweepy.OAuthHandler(credentials.api_key,credentials.api_secret_key)
    auth.set_access_token(credentials.access_token,credentials.access_token_secret)
    twitter_stream = Stream(auth, getdata())
    twitter_stream.filter(track = ['Warren','trump'])