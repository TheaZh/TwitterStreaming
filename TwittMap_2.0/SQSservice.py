import boto3

class SQS:

    def __init__(self):
        self.sqs = boto3.resource('sqs', region_name='us-west-2', aws_access_key_id='',
                          aws_secret_access_key='')

    def createQueue(self, name):
        return self.sqs.create_queue(QueueName=name)

    def getQueue(self, name):
        return self.sqs.get_queue_by_name(QueueName=name)
