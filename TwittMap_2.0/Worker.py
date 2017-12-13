from SQSservice import SQS
from SNSservice import SNS
import json
import watson_developer_cloud
import watson_developer_cloud.natural_language_understanding.features.v1 as features

sqs = SQS()
sns = SNS()

# the api Key
#alchemy_language = AlchemyLanguageV1(api_key='')

nlu = watson_developer_cloud.NaturalLanguageUnderstandingV1(version='2017-02-27', username='', password='')

queue_name = 'twitterSQS'
topic_name = 'twitterSNS'

topic = sns.createTopic(topic_name)
queue = sqs.getQueue(queue_name)


for message in queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20):
    try:
        tweet = json.loads(message.body)
        text = tweet['text']
        # print "text:", text
        # sentiment = alchemy_language.sentiment(text=text)
        sentiment = nlu.analyze(text=text, features=[features.Sentiment()])
        # tweet['sentiment'] = sentiment['docSentiment']['type']
        tweet['sentiment'] = sentiment['sentiment']['document']['label']
        tweet = json.dumps(tweet)
        t = topic.publish(TopicArn='arn:aws:sns:us-west-2:368700261499:twitterSNS', Message=tweet)
        print "%% PUBLISH INTO SNS %% = ", t

    except Exception as e:
        print "error =", e
    message.delete()
