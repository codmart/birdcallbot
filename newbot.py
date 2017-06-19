# twitter bot starter kit

#import xl
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import smart_open
from dl import main
import tweepy, time
import os
#from credentials import *
auth = tweepy.OAuthHandler(os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))
auth.set_access_token(os.environ.get('ACCESS_TOKEN'), os.environ.get('ACCESS_SECRET'))
api = tweepy.API(auth)
client = boto.client('s3')

# import s3 database for line.txt
s3 = S3Connection(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])
bucket = s3.get_bucket('birdcallbot-assets')
k = Key(bucket)
k.key = 'line.txt'
line = int(k.get_contents_as_string())
k.set_contents_from_string(str(line+1))

# make a new bird
# with smart_open.smart_open('s3://birdcallbot-assets/line.txt', 'r+') as f:

'''
with open('line.txt', 'r+') as myfile:
    line=int(myfile.read())
    myfile.seek(0)
    myfile.write((str(line+1)))
'''
# What the bot will tweet

# populate folder with new media
main(line)

with open('tweet.txt', 'r') as text:
    tweet=text.read()

# update status
media = api.upload_chunked('video.mp4')		# using fitnr fork of tweepy: video_upload2 branch
api.update_status(status=tweet, media_ids=[media.media_id])

#sleep_time = 86400/4 #this will go 4 times a day
#time.sleep(sleep_time)


print("done")

