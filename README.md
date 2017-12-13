# TwittMap        
Columbia COMS 6998 Cloud Computing Assignments         
Yimeng Zhou(yz2993)          
Qianwen Zheng(qz2271)           
## TwittMap_1.0 Assignment1             
Use Twitter Streaming API to fetch tweets from the twitter hose in real-time.             
Use ElasticSearch or AWS ElasticSearch to store the tweets on the backend.          
Create a web UI that allows users to search for a few keywords. The keywords (up to 10) can be of your choosing.        
Use Google Maps API(or any other mapping library) to render these filtered tweets in the map in whatever manner you want.     
    
## TwittMap_2.0 Assignment2 Using SQS     
Based on TwittMap_1.0             
Use the Amazon SQS service to create a processing queue for the Tweets that are delivered by the Twitter Streaming API              
Use Amazon SNS service to update the status processing on each tweet so the UI can refresh.              
Integrate a third party cloud service API into the Tweet processing flow (add sentiment evaluation for the text of the submitted Tweet)          
## TwittMap_2.1 Assignment2 Using Kafka          
Based on TwittMap_2.0, we now use Kafka instead of SQS as the EventQueue.
