
## download and store info from macalauy library from online and excel sheet
## find corresponding audio and photo to make a :35 sec video

import xl
import urllib3
import urllib
import shutil
import os
import random
from lxml import html
from urllib.parse import urlencode
from pydub import AudioSegment
from requests import get  # to make GET request

def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)

def download_photo(url, file_name):
	#open in binary mode
	r = get(url, stream=True)
	with open(file_name, 'wb') as f:
		#force it to not compress
		r.raw.decode_content = True
		shutil.copyfileobj(r.raw, f)
	return file_name

def shorten_audio(bird_id, file_name, seconds):
	# turn my audio into a nice output (audio shortened to :30 or :45 and fade out) 
	directory = file_name
	# open raw mp3
	raw_audio = AudioSegment.from_file(directory, format="mp3")
	length = seconds * 1000 # 35 seconds
	# truncate and fade
	short_audio = raw_audio[:length].fade_out(5*1000) # 5 second fade
	# export as wav
	short_audio.export(bird_id+".wav", format="wav")

def clean_result(string):
	# take the string and delete whitespace and nonreadable
	string = string.strip("- &#xA0; &#169;")
	string = string.replace("\n\t\t", "")
	string = string.replace("© ", "")
	return string

def cleanup_files(bird_id):
	os.remove(bird_id + ".jpg")
	os.remove(bird_id + ".wav")
	os.remove(bird_id + ".mp3")

def main(bird_number):

	#bird_number = bird_number # this could be random? and controlled by the bot

	# make a new bird based on catalog id
	NewBird = xl.Bird(bird_number)
	bird_id = NewBird.id 		
	file_name = bird_id + ".mp3"
	url = "http://animalrecordings.org/Audio/Audio1/{0}/{1}".format(NewBird.id[:2], file_name)
	# download the whole file to folder
	download(url, file_name)

	#shorten audio	
	shorten_audio(bird_id, file_name, 25) #30 seconds long or shorter bc AUTH issues with tweepy


	# get the HTML of the search page on macalauy 
	query_args = { 'mediaType':'Photo', 'sort':'rating_rank_desc', 'q':NewBird.common, 'species':NewBird.common} # this is with date args omitted
	encoded_args = urlencode(query_args)
	photo_url = "https://search.macaulaylibrary.org/catalog?" + encoded_args
	page = get(photo_url)
	tree = html.fromstring(page.content)
	# get a list of the image sources
	images = tree.xpath('//img[@alt="{}"]/@src'.format(NewBird.common))
	# pick the top one
	image_pick = random.randint(0, 1)
	image_source = images[image_pick]
	top_image = image_source.replace("640","large")
	# download it 
	download_photo(top_image, NewBird.id + ".jpg")
	# go to photographer data in HTML (this could be done way quicker in JSON library at the bottom)
	photographers = tree.xpath("//div[@class= 'caption']/strong/following-sibling::text()[1]")
	# clean up results
	photo_credit = clean_result(photographers[image_pick])


	# save the bird credentials to an overwritable text file (or maybe it should keep history?)
	with open('tweet.txt', "w+") as text: 		
		text.write("{0} ({1})\nrecordist: {2}\npic: {3}".format(NewBird.common, NewBird.scientific, NewBird.credit, photo_credit))


	# combine the audio and video
	try:
		os.remove("video.mp4")

	except:
		pass

	os.system("ffmpeg -loop 1 -i {0}.jpg -i {1}.wav -c:v libx264 -vf: scale='trunc(oh*a/2)*2:720' -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest video.mp4".format(bird_id, bird_id))
	# clean up old downloads
	cleanup_files(bird_id)


if __name__ == '__main__':
	main(1)
	print(xl.Bird.get_Bird_ID() + " done")