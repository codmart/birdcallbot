# birdcallbot newbot

# twitter bot script to run on timed basis

import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from dl import main
import tweepy, time
import os

# set up api
auth = tweepy.OAuthHandler(os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))
auth.set_access_token(os.environ.get('ACCESS_TOKEN'), os.environ.get('ACCESS_SECRET'))
api = tweepy.API(auth)

# import s3 database for line.txt
s3 = S3Connection(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])
bucket = s3.get_bucket('birdcallbot-assets')
k = Key(bucket)
k.key = 'line.txt'
# read line and add one for later
line = int(k.get_contents_as_string())
k.set_contents_from_string(str(line+1))

# make a new bird
# populate folder with new media
main(line)

# what the bot will tweet
with open('tweet.txt', 'r') as text:
    tweet=text.read()

# update status
media = api.upload_chunked('video.mp4')		# using fitnr fork of tweepy: video_upload2 branch
api.update_status(status=tweet, media_ids=[media.media_id])

# now set timer


print(line + "done")

