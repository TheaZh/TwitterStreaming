import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
from elasticsearch import Elasticsearch
from SQSservice import SQS

# The twitterAPI keys

# SQS name

name = 'twitterSQS'

sqs = SQS()
#sqs.createQueue(name)
queue = sqs.getQueue(name)
print queue.url

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

# Set keywords
Keywords = ['Oscar', 'health', 'clothes', 'amazon', 'cloud', 'restaurant', 'Trump', 'love', 'food', 'movie']


tweetCollection = {
    "mappings": {
        "tweets": {
            "properties": {
                "author": {
                    "type": "string"
                },
                "text": {
                    "type": "string"
                },
                "location": {
                    "type": "geo_point"
                }
            }
        }
    }
}

END_POINT = "search-twittermap2-xs4d2zl7f57z4mtnmjscygewty.us-west-2.es.amazonaws.com"
PORT = 80


# Create ES
try:
    es = Elasticsearch(host=END_POINT, port=PORT, use_ssl=False)
    es.indices.create(index="twitters", body=tweetCollection)
except Exception as e:
    print e


class tweetListener(StreamListener):

    def on_data(self, data):
        json_data = json.loads(data)

        try:
            if json_data['coordinates'] is not None:
                longitude = json_data['coordinates']['coordinates'][0]
                latitude = json_data['coordinates']['coordinates'][1]
            elif json_data['place'] is not None:
                longitude = json_data['place']['bounding_box']['coordinates'][0][0][0]
                latitude = json_data['place']['bounding_box']['coordinates'][0][0][1]
            location_data = [longitude, latitude]
            author = json_data['user']['name']
            text = json_data['text']

            body = {
                "author": author,
                "text": text,
                "location": location_data
            }

            # queue tweets into SQS
            tweet = json.dumps(body)
            #print tweet
            queue.send_message(MessageBody=tweet)

            # put tweets into ES
            #result = es.index(index='twitters', doc_type='tweets', body=body, ignore=400)
            #print result

            #print "updated"

            for message in queue.receive_messages(WaitTimeSeconds=5):
                try:
                    tweet_result = json.loads(message.body)
                    text_result = tweet_result['text']
                    # print text_result
                except Exception as e:
                    print e


        except:
            errorMessage = "Error - Status code " + str(data)
            #print(errorMessage)

    def on_error(self, status):
        print (status)

def startStreaming():

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    stream = Stream(auth=api.auth, listener=tweetListener())
    stream.filter(track=Keywords, languages=['en'])


# Test

if __name__ == '__main__':

    startStreaming()



