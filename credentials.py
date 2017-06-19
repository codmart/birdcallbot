# Credentials for your Twitter bot account

# 1. Sign into Twitter or create new account
# 2. Make sure your mobile number is listed at twitter.com/settings/devices
# 3. Head to apps.twitter.com and select Keys and Access Tokens
import os

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

# Create a new Access Token
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN') 
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
