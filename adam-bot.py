import tweepy
import requests
import random
import time

consumer_key = '*****'
consumer_secret = '*****'
access_token = '*****'
access_token_secret = '*****'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

FILE_NAME = 'last_seen.txt'

def generate_joke():
    url = 'https://official-joke-api.appspot.com/random_joke'
    response = requests.get(url)    
    resp_json = response.json()
    quest = resp_json['setup']
    answer = resp_json['punchline']
    formated_joke = quest + "\n\n" + answer
    return formated_joke

def select_image_path():
    nmr = random.randint(1, 32)
    image_path = 'images/' + str(nmr) + '.jpg'
    return image_path

def read_last_seen(FILE_NAME):
    file_read = open(FILE_NAME, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id

def store_last_seen(FILE_NAME, last_seen_id):
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return

def reply_tweet(tweet, joke, img):
    message = "@" + tweet.user.screen_name
    message = message + " there goes a funny joke \n\n"
    message = message + joke
    api.update_with_media(img, message, tweet.id)
    store_last_seen(FILE_NAME, tweet.id)

def main():
    tweets = api.mentions_timeline(read_last_seen(FILE_NAME), tweet_mode='extended')
    for tweet in reversed(tweets):
        joke = generate_joke()
        img = select_image_path()
        reply_tweet(tweet, joke, img)

while True:
    time.sleep(3.0)
    main()
