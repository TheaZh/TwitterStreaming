### Columbia COMS 6998 Cloud Computing Assignment 1     
HW Group 32       
Name: Yimeng Zhou (yz2993)                  
Name: Qianwen Zheng (qz2271)     

This web application would collect Twitts and do some processing and represent the Twitts on GoogleMaps.     
     
Use Twitter Streaming API to fetch tweets from the twitter hose in real-time.       
Use AWS ElasticSearch to store the tweets on the backend.     
Create a web UI that allows users to search for a few keywords (via a dropdown). The keywords (up to 10) can be of your choosing.           
Use Google Maps API to render these filtered tweets in the map in whatever manner you want.         
Deploy your application on AWS Elastic Beanstalk in an auto-scaling environment.         


### tweetStreaming.py      
Fetch a stream of tweets from the Twitter Streaming API and index tweets in Elasticsearch.       
### dataProcess.py        
Get tweets with certain rules from Elasticesearch       
### tweetJS.js        
Provide some visual indication on the frontend. Give the user the ability to search via a dropdown. Plot tweets that match the query on the Google map.


