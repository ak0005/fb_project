#https://developers.facebook.com/tools/explorer/
#user_managed_groups, groups_show_list, groups_access_member_info, public_profile
#https://developers.facebook.com/tools/debug/accesstoken/

token='access token'

#token corresponding to all the files that u r willing to run should be unique
tokenPost=token
tokenComments=token
tokenSubComments=token
tokenAttachments=token
tokenCommentAttachments=token
tokenCommentLikeCount=token
tokenPostReactions=token

grpId='1991716644473195'

PostCollection='post'

tempFile='temp.txt'

postLog='postLog.csv'
commentLog='commentLog.csv'
subCommentLog='subCommentLog.csv'
attachmentLog='attachmentLog.csv'
commentAttachmentsLog='commentAttachmentsLog.csv'
commentLikeCountLog='subCommentLikeCount.csv'
postReactionsLog='postReactionsLog.csv'
requestLog='requestLog.txt'


dump='data_dump.json'

mongoClient="mongodb://localhost:27017/"

TIMEOUT=20
WAIT=1803
