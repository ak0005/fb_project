#https://developers.facebook.com/tools/explorer/
#user_managed_groups, groups_show_list, groups_access_member_info, public_profile
#https://developers.facebook.com/tools/debug/accesstoken/

token='EAAJKCn7sDoYBAHuPOXwNGyRUReCofs4bPVOcfyGrU7ayD6Mybx3uunVic1CJu47E7NCYmF7oTuGqcVwGgZC4jOhbUYvOa3L0cVP0ULoU2PmDNd0CEdf28UFxkoHu1Ftk61Ab2CIeSFr0ZAKpW8baMVQ0Bv8GZByZAjdpJNlqLoHwitcZBhtj0HX6styiDrQFLk49lxG6ZAl7eQmBDhBgQJIi87vLCU7CR5NoISg7zsSAZDZD'
grpId='161136235596016'

PostCollection='post'

tempFile='temp.txt'

postLog='postLog.csv'
commentLog='commentLog.csv'
subCommentLog='subCommentLog.csv'
attachmentLog='attachmentLog.csv'
commentAttachmentsLog='commentAttachmentsLog.csv'
requestLog='requestLog.txt'


dump='data_dump.json'

mongoClient="mongodb://localhost:27017/"

TIMEOUT=20
WAIT=1803