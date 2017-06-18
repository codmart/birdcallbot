# twitter bot starter kit

#import xl
from dl import main
import tweepy, time
from credentials import *
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)


# What the bot will tweet

# make a new bird
line = 0
# populate folder with new media
main(line)

with open('tweet.txt', 'r') as text:
    tweet=text.read()

# update status
media = api.upload_chunked('video.mp4')		# using fitnr fork of tweepy: video_upload2 branch
api.update_status(status=tweet, media_ids=[media.media_id])

sleep_time = 86400/4 #this will go 4 times a day
time.sleep(sleep_time)
line += 1

print("done")

