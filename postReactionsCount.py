import request as request
import const as const
import json
from datetime import datetime
import pymongo

url = "https://graph.facebook.com/v9.0/" + \
    const.grpId+"/feed?fields=reactions.summary(true)&access_token="+const.token

fp = open(const.postReactionsLog, 'a')
fp.write("=========================>\n")

myclient = pymongo.MongoClient(const.mongoClient)
db = myclient[const.grpId]
collection = db[const.PostCollection]


def handleData(data):
    for post in data:
        if 'id' in post and 'reactions' in post and 'summary' in post['reactions'] and 'total_count' in post['reactions']['summary'] :
            d2 = {'_id': post['id']}

            if collection.find({'_id': post['id']}).limit(1).count() ==0:
                collection.insert_one(d2)

            collection.update({'_id':post['id']},{
                "$set":{"reactions":post['reactions']['summary']['total_count']}
            })

while len(url):
    r = request.apiCall(url)
    if 'data' in r:
        handleData(r['data'])

    if 'paging' in r and 'next' in r['paging']:
        url = r['paging']['next']
    else:
        url = ''

fp.close()
