import boto3

class SNS:

    def __init__(self):
        self.sns = boto3.resource('sns', region_name='us-west-2', aws_access_key_id='',
                          aws_secret_access_key='')

    def createTopic(self, topic):
        result = self.sns.create_topic(Name=topic)
        return result
