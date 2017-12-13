from SNSservice import SNS
from kafka import KafkaConsumer
import json
import watson_developer_cloud
import watson_developer_cloud.natural_language_understanding.features.v1 as features

queue_name = 'twitterKafka'
topic_name = 'twitterSNS'

sns = SNS()
consumer = KafkaConsumer(queue_name, group_id='my-group', bootstrap_servers='localhost:9092')

# the api Key
#alchemy_language = AlchemyLanguageV1(api_key='')

nlu = watson_developer_cloud.NaturalLanguageUnderstandingV1(version='2017-02-27', username='', password='')

topic = sns.createTopic(topic_name)


for message in consumer:
    try:
        tweet = json.loads(message.value)
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

