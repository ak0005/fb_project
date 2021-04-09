import utils.const as const
import utils.request as request
from datetime import datetime
import pymongo

url = "https://graph.facebook.com/v9.0/" + \
    const.grpId+"/feed?access_token="+const.tokenPost

fp = open(const.postLog, 'a')
fp.write("=========================>\n")

myclient = pymongo.MongoClient(const.mongoClient)
db = myclient[const.grpId]
collection = db[const.PostCollection]


def handleData(data):
    for post in data:
        if 'id' in post:
            d2 = {'_id': post['id']}

            if collection.count_documents({'_id': post['id']}, limit=1) == 0:
                collection.insert_one(d2)

            fp.write(post['id']+','+str(datetime.now())+'\n')

            if 'updated_time' in post:
                d2['updated_time'] = post['updated_time']
            if 'message' in post:
                d2['message'] = post['message']

            collection.update_one({'_id': post['id']}, {
                "$set": d2
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
