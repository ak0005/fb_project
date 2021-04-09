import utils.const as const
import utils.request as request
import pymongo
from datetime import datetime

url = "https://graph.facebook.com/v9.0/"+const.grpId + \
    "/feed?fields=comments%7Blike_count%7D&access_token="+const.tokenCommentLikeCount


fp = open(const.commentLikeCountLog, 'a')
fp.write("=========================>\n")

myclient = pymongo.MongoClient(const.mongoClient)
db = myclient[const.grpId]
collection = db[const.PostCollection]


def handleCommentData(postId, data):
    for comment in data:
        if 'id' in comment and "like_count" in comment:
            if collection.count_documents({'_id': postId, 'comments': {'$elemMatch': {'_id': comment['id']}}}, limit=1) == 0:
                collection.update_one({'_id': postId}, {
                    '$push': {'comments': {'_id': comment['id']}}})

            fp.write(postId+','+comment['id']+','+str(datetime.now())+'\n')
            collection.update_one({'_id': postId, 'comments': {'$elemMatch': {'_id': comment['id']}}}, {
                '$set': {'comments.$.like_count': comment['like_count']}})


def handleData(data):
    for post in data:
        if 'id' in post and 'comments' in post and 'data' in post['comments']:
            if collection.count_documents({'_id': str(post['id'])}, limit=1) == 0:
                collection.insert_one({'_id': post['id']})
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
