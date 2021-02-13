import request as request
import const as const
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
            if collection.find({'_id': postId, 'comments': {'$elemMatch': {'_id': comment['id']}}}).limit(1).count() == 0:
                collection.update({'_id': postId}, {
                                  '$push': {'comments': {'_id': comment['id']}}})

            fp.write(postId+','+comment['id']+','+str(datetime.now())+'\n')                 
            collection.update({'_id': postId, 'comments': {'$elemMatch': {'_id': comment['id']}}}, {
                              '$set': {'comments.$.like_count': comment['like_count']}})


def handleData(data):
    for post in data:
        if 'id' in post and 'comments' in post and 'data' in post['comments']:
            if collection.find({'_id': post['id']}).limit(1).count() == 0:
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
