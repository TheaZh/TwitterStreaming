from elasticsearch import Elasticsearch

END_POINT = "search-twittermap2-xs4d2zl7f57z4mtnmjscygewty.us-west-2.es.amazonaws.com"
PORT = 80

class dataProcessing():
    def __init__(self):
        self.index = "twitters"
        self.docType = "tweets"
        self.es = Elasticsearch(host=END_POINT, port=PORT, use_ssl=False)

    def getTweet(self, keyword):
        body = {
            "query": {
                "match": {
                    "_all": keyword
                }
            }
        }

        size = 1000
        result = self.es.search(index=self.index, doc_type=self.docType, body=body, size=size, ignore=400)
        return result

    def getCertainDistanceTweet(self, keyword, distance, lat,lng):
        distanceRange = str(distance) + "km"
        body = {
            "query": {
                "match": {
                    "_all": keyword
                }
            },
            "filter": {
                "geo_distance": {
                    "distance": distanceRange,
                    "distance_type": "sloppy_arc",
                    "location": {
                        "lon": lng,
                        "lat": lat
                    }
                }
            }
        }
        size = 1000
        result = self.es.search(index=self.index, doc_type=self.docType, body=body, size=size, ignore=400)
        return result

    # Add to ElasticSearch
    def addtoES(self, body):
        result = self.es.index(index=self.index, doc_type=self.docType, body=body, ignore=400)
        return result


    # Queue data, just for test
    def queueTweet(self, author, text, location):
        print author
        print text
        print location
        body = {
             "author": author,
             "text": text,
             "location": location
        }
        result = self.es.index(index=self.index, doc_type=self.docType, body=body, ignore=400)
        return result



# Test
if __name__ == '__main__':
    dataProcess = dataProcessing()
    longitude = -87
    latitude = 42
    author = "Rita"
    text = "I love U LOVE LOVE U"



    result2 = dataProcess.getCertainDistanceTweet("food", 100, latitude,longitude)
    for hit in result2['hits']['hits']:
        tweet = hit['_source']['location']
        print tweet
