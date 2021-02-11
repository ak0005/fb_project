import request as request
import const as const
import json
from datetime import datetime
import pymongo

url = "https://graph.facebook.com/v9.0/" + \
    const.grpId+"/feed?fields=attachments&access_token="+const.token

fp = open(const.attachmentLog, 'a')
fp.write("=========================>\n")

myclient = pymongo.MongoClient(const.mongoClient)
db = myclient[const.grpId]
collection = db[const.PostCollection]


def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


def handleData(data):
    for post in data:
        if 'id' in post and 'attachments' in post:
            if collection.find({'_id': post['id']}).limit(1).count() == 0:
                collection.insert_one({'_id': post['id']})

            fp.write(post['id']+','+str(datetime.now())+'\n')

            d2 = json_extract(post['attachments'], 'src')

            collection.update_one({'_id': post['id']}, {
                                  '$unset': {'attachments': ""}})
            collection.update({'_id': post['id']}, {
                              '$set': {'attachments': d2}})


while len(url):
    r = request.apiCall(url)
    if 'data' in r:
        handleData(r['data'])

    if 'paging' in r and 'next' in r['paging']:
        url = r['paging']['next']
    else:
        url = ''

fp.close()
