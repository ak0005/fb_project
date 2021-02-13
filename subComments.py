import request as request
import const as const
from datetime import datetime
import pymongo

url = "https://graph.facebook.com/v9.0/"+const.grpId + \
    "/feed?fields=comments%7Bcomments%7D&access_token="+const.tokenSubComments

fp = open(const.subCommentLog, 'a')
fp.write("=========================>\n")

myclient = pymongo.MongoClient(const.mongoClient)
db = myclient[const.grpId]
collection = db[const.PostCollection]


def handleSubCommentData(postId, commentId, data):
    for subComment in data:
        if 'id' in subComment:

            if collection.find({'_id': postId, 'comments.subComments': {'$elemMatch': {'_id': commentId, "_id": subComment['id']}}}).limit(1).count() > 0:
                continue

            fp.write(postId+','+commentId+',' +
                     subComment['id']+','+str(datetime.now())+'\n')

            d2 = {'_id': subComment['id']}

            if 'created_time' in subComment:
                d2['created_time'] = subComment['created_time']
            if 'message' in subComment:
                d2['message'] = subComment['message']

            collection.update({'_id': postId, 'comments': {'$elemMatch': {'_id': commentId}}}, {
                              '$push': {'comments.$.subComments': d2}})


def handleCommentData(postId, data):
    for comment in data:
        if 'id' in comment and 'comments' in comment and 'data' in comment['comments']:
            if collection.find({'_id': postId, 'comments': {'$elemMatch': {'_id': comment['id']}}}).limit(1).count() == 0:
                collection.update({'_id': postId}, {
                                  '$push': {'comments': {'_id': comment['id']}}})
                                  
            handleSubCommentData(
                postId, comment['id'], comment['comments']['data'])


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
