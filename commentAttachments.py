import request as request
import const as const
from datetime import datetime
import pymongo

url = "https://graph.facebook.com/v9.0/" + \
    const.grpId+"/feed?fields=comments%7Battachment%7D&access_token="+const.tokenCommentAttachments

fp = open(const.commentAttachmentsLog, 'a')
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


def handleCommentData(postId, data):
    for comment in data:
        if 'id' in comment and 'attachment' in comment:

            if collection.find({'_id': postId, 'comments': {'$elemMatch': {'_id': comment['id']}}}).limit(1).count() == 0:
                collection.update({'_id': postId}, {'$push': {'comments': {'_id':comment['id']}}})
                

            fp.write(postId+','+comment['id']+','+str(datetime.now())+'\n')

            dI = json_extract(comment['attachment'], 'src')
            dV = json_extract(comment['attachment'], 'source')

            collection.update_one({'_id': postId, 'comments': {'$elemMatch': {'_id': comment['id']}}}, {
                                  '$unset': {'comments.$.attachment': ""}})

            collection.update({'_id': postId, 'comments': {'$elemMatch': {'_id': comment['id']}}}, {
                              '$set': {'comments.$.attachment.images': dI}})
            collection.update({'_id': postId, 'comments': {'$elemMatch': {'_id': comment['id']}}}, {
                              '$set': {'comments.$.attachment.videos': dV}})               


def handleData(data):
    for post in data:
        if 'id' in post and 'comments' in post and 'data' in post['comments']:
            if collection.find({'_id': post['id']}).limit(1).count() == 0:
                collection.insert_one({'_id':post['id']})

            handleCommentData(post['id'], post['comments']['data'])


while len(url):
    r = request.apiCall(url)
    if 'data' in r:
        handleData(r['data'])

    if 'paging' in r and 'next' in r['paging']:
        url = r['paging']['next']
    else:
        url = ''

fp.close()
