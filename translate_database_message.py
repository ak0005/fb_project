import pymongo
import json
from googletrans import Translator

database = 'fb_grp'
collection = 'fb_grp_data'

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient[database]
collection = db[collection]

#Appending all necessary information of post in msg_list
msg_list = []

#Initiating translator object
translator = Translator()

#collecting all required informaiton
for message in collection.find({},
                              {
                                  '_id':1,
                                 'message':1,
                                 'comments._id':1,
                                 'comments.message':1,
                                 'comments.subComments._id':1,
                                 'comments.subComments.message':1  
                              }):
    msg_list.append(message)


for msg in msg_list: 

    #Translating post message
    if 'message' in msg: 
       message_text = msg['message']
       update_message = translator.translate(message_text,dest='en')

       #Updating message in collection
       collection.update({ 
		          '_id': msg['_id'] 
	 		 },
	  		 {
	   		  '$set':{
		                   'message' : update_message.text
		                 }
	    	         }) 

    #Translating comments
    if 'comments' in msg:
      
      #Checking for parent comment
      for parent_comment in msg['comments']:   	
          
          #If message exists in comment
          if 'message' in parent_comment:
            parent_comment_message = parent_comment['message']
            update_parent_comment_message = translator.translate( parent_comment_message,dest='en')
            
            #Updating parent comment message in collection
            collection.update({
                                '_id':msg['_id'],
                                'comments':{
                                             '$elemMatch': {
                                                             '_id': parent_comment['_id']
                                                           }
                                           }
                              },
                              {
                                '$set': {
                                          'comments.$.message': update_parent_comment_message.text
                                        }
                              })         
          
          #if subcomment exists in comment 
          if 'subComments' in parent_comment:

             #Removing all child comment message in collection before traversing subcomments
             collection.update_one({
                                     '_id': msg['_id'], 
                                     'comments':{
                                                  '$elemMatch': {
                                                                  '_id': parent_comment['_id']
                                                                }
                                                }
                                   }, 
                                   {
                                     '$unset': {
                                                'comments.$.subComments': ""
                                               }
                                   })

             for child_comment in parent_comment['subComments']:
                if 'message' in child_comment:
                  child_comment_message = child_comment['message']
                  update_child_comment_message = translator.translate( child_comment_message,dest='en')
                  
                  #Updating subcomment object
                  child_comment['message'] = update_child_comment_message.text                

                  collection.update_one({
	                                  '_id': msg['_id'], 
	                                  'comments':{
	                                               '$elemMatch': {
	                                                               '_id': parent_comment['_id']
	                                                             }
	                                             }
                                        }, 
                                        {
                                          '$push': {
                                                      'comments.$.subComments': child_comment 
                                                   }
                                       })
