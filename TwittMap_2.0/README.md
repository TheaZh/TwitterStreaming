## Columbia COMS 6998 Cloud Computing Assignment2 using SQS           
HW Group 32       
Yimeng Zhou (yz2993)           
Qianwen Zheng (qz2271)         
         
Based on TwittMap_1.0, we made following improvements.        
1. Use [Amazon SQS service](https://aws.amazon.com/sqs/) to create a processing queue for the Tweets that are delivered by the Twitter Streaming API.      
2. Use [Amazon SNS service](https://aws.amazon.com/sns/) to update the status processing on each tweet so the UI can refresh.             
3. Integrate a third party cloud service API into the Tweet processing flow.      
### tweetStreaming.py
Reads a stream of tweets from the Twitter Streaming API, which follows a set of specific keywords that we find interesting.        
After fetching a new tweet, check to see if it has geolocation info and is in English.             
Once the tweet validates these filters, send a message to SQS for asynchronous processing on the text of the tweet         
### dataProcessing.py        
Get tweets with certain rules from Elasticesearch
Index tweets into Elasticsearch

### Worker.py
Define a worker pool that will pick up messages from the queue to process.                 
Make a call to the sentiment API off your preference. This can return a positive, negative or neutral sentiment evaluation for the text of the submitted Tweet.                     
As soon as the tweet is processed send a notification -using SNS- to an HTTP endpoint that contains the information about the tweet.             
### Backend           
On receiving the notification, index this tweet in Elasticsearch.       
Provide the functionality to the user to search for tweets that match a particular keyword.          
### Frontend         
When a new tweet is indexed, provide some visual indication on the frontend.               
Give the user the ability to search your index via a free text input or a dropdown.                 
Plot the tweets that match the query on a map with custom markers to indicate the sentiment.
                   
![alt tag](https://github.com/TheaZh/TwittMap_demo/blob/master/TwittMap_2.0/img/TwittMap-diagram.png)

### Usage
Run Elastic BeanStalk URL

http://lowcost-env.qb5mcxvtsh.us-west-2.elasticbeanstalk.com

Run worker.py
```
python worker.py
```

### Sentiment Visualization

![alt tag](https://github.com/TheaZh/TwittMap_demo/blob/master/TwittMap_2.0/img/map-image.png)

In TwittMap, markers in different color represents different sentiments. Red marker means the sentiment of this tweet is negative. Green marker means the sentiment is positive. And yellow marker means the sentiment is neutral.

