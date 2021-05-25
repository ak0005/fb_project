import pymongo
from datetime import datetime
import utils.const as const


myclient = pymongo.MongoClient(const.mongoClient)
db = myclient[const.grpId]
collection = db[const.PostCollection]

name='gui_data.csv'

with open(name,'w') as fp:
    fp.write('postId,created_time,updated_time,img_count,vid_count,reactions,comment_sentiment,comment_count\n')

    for post in collection.find({}):
        if '_id' in post:
            fp.write(str(post['_id']))
        
        fp.write(',')
        if 'created_time' in post:
            fp.write(str(datetime.fromtimestamp(int(float(post['created_time'])))))
        
        fp.write(',')
        if 'updated_time' in post:
            fp.write(str(datetime.fromtimestamp(int(float(post['updated_time'])))))
        
        fp.write(',')
        if 'attachments' in post and 'images' in post['attachments'] :
            fp.write(str(len(post['attachments']['images'])))
        else:
            fp.write('0')

        fp.write(',')
        if 'attachments' in post and 'videos' in post['attachments'] :
            fp.write(str(len(post['attachments']['videos'])))
        else:
            fp.write('0')

        fp.write(',')
        if 'reactions' in post:
            fp.write(str(post['reactions']))

        fp.write(',')
        if 'comment_sentiment' in post:
            fp.write(str(post['comment_sentiment']))
        
        fp.write(',')
        if 'comments' in post:
            fp.write(str(len(post['comments'])))
        else:
            fp.write('0')

        fp.write('\n')

        