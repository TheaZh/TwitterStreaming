from flask import Flask, render_template, jsonify,request

from tweetStreaming import *
from dataProcess import dataProcessing

import thread

def getTweetStream():
    startStreaming()

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('twitter.html')


@app.route('/search/<keyword>',methods=['GET','POST'])
def searchKeyword(keyword):
    if request.method == 'POST':
        print "The keyword is" + keyword
        dataProcess = dataProcessing()
        result = dataProcess.getTweet(keyword)
        #location = result['hits']['hits']
        #location_list = []
        #for hit in location:
        #    geo = hit['_source']['location']
        #    print geo
        #    location_list.append(geo)
        #print location
        #return jsonify(location_list)
        return jsonify(result)
    else:
        print "Error"
    '''
    if request.method == 'POST':
        print keyword
    else:
        print "error"
    return render_template('twitter.html')
    '''



@app.route('/search/<keyword>/<distance>/<lat>/<lng>',methods = ['GET','POST'])
def getCertainDistanceTweet(keyword, distance, lat, lng):
    if request.method == 'POST':
        searchTweets = dataProcessing()
        print lat + ", " + lng
        print keyword
        print distance
        result = searchTweets.getCertainDistanceTweet(keyword,distance,lat,lng)
        print result
        return jsonify(result)
    else:
        print "Error"

if __name__ == '__main__':
    thread.start_new_thread(getTweetStream, ())
    app.debug = True
    app.run()
