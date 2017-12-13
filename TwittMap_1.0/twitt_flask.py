from flask import Flask, render_template, request
import googlemaps
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
app = Flask(__name__)

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''


class StdOutListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        if tweet['lang'] == 'en' and tweet['user'].get('location') is not None:
            place = tweet['user'].get('location')
            if place:
                tweet_id = str(tweet['id'])
                geocode_result = googlemaps.Client(key='').geocode(place)
                lat = geocode_result[0]['geometry']['location']['lat']
                lng = geocode_result[0]['geometry']['location']['lng']
                tweet_text = tweet['text'].lower().encode('ascii', 'ignore').decode('ascii')
                raw_tweet = {
                    'user': tweet['user']['screen_name'],
                    'text': tweet_text,
                    'place': place,
                    'coordinates': {'location': str(lat) + "," + str(lng)},
                    'time': tweet['created_at']
                }
                print raw_tweet['coordinates']['location']
        return True

    def on_error(self, status):
        print (status)


@app.route('/')
def hello_world():
    location = []
    return render_template('index.html',locations=location)


@app.route('/pin',methods=['GET'])
def mappin():
    keyword = request.args.get('keyWords')
    location = []
    if keyword == 'cs':
        location.append([41.508742,12.60])
        print keyword
    else:
        location.append([43,15])
    print location
    return render_template('index.html', locations = location)



if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = Stream(auth, StdOutListener())
    app.run()
