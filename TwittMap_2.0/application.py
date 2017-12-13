from flask import Flask, render_template, jsonify, request

from tweetStreaming import *
from dataProcess import dataProcessing

import thread
import boto3

def getTweetStream():
    startStreaming()

application = Flask(__name__)


client = boto3.client('sns', region_name='us-west-2', aws_access_key_id='',
                          aws_secret_access_key='')
msg_list = []

@application.route('/')
def root():
    msg_list = [] # clear msp_list after reload
    return render_template('twitter.html')
    '''
    if request.method == 'GET':
        response = client.subscribe(
            TopicArn='arn:aws:sns:us-west-2:368700261499:twitterSNS',
            Protocol='http',
            Endpoint='http://54.244.205.143:8080/sns'
        )
        print "%% Send Subscription info to Server %% = ", response
'''
    



@application.route('/search/<keyword>', methods=['GET', 'POST'])
def searchKeyword(keyword):
    if request.method == 'POST':
        print "The keyword is" + keyword
        dataProcess = dataProcessing()
        result = dataProcess.getTweet(keyword)
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



@application.route('/search/<keyword>/<distance>/<lat>/<lng>', methods=['GET', 'POST'])
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


@application.route('/sns', methods=['GET', 'POST'])
def sns():
    print "++++++SNS SECTION+++++"
    if request.method == 'POST':
        type = request.headers.get('X-Amz-Sns-Message-Type')
        builder = json.loads(request.data)
        # print "%% GET DATA %% = ", builder

        if type == 'SubscriptionConfirmation':
            print '%%%%%% CONFIRMATION !!! %%%%%%'
            token = builder['Token']
            response = client.confirm_subscription(
                TopicArn='arn:aws:sns:us-west-2:368700261499:twitterSNS',
                Token=token,
                AuthenticateOnUnsubscribe='True'
        )
        elif type == 'Notification':
            print '%%%%%% INSERT TO ES !!! %%%%%%'
            tweets = json.loads(builder['Message'])
            print "%%%%%%% TWEETS %%%%%%", tweets
            dataProcess = dataProcessing()
            msg_list.append({'text':tweets['text'], 'author':tweets['author'], 'sentiment':tweets['sentiment'], 'location':tweets['location']})
            result = dataProcess.addtoES(builder['Message'])
        return jsonify(msg_list)
    elif request.method=='GET':
        # print "%%%% list msg %%%%%", msg_list
        return jsonify(msg_list)



if __name__ == '__main__':
    thread.start_new_thread(getTweetStream, ())
    application.debug = True
    application.run(host='0.0.0.0', port=8081)
