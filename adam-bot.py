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
api = tweepy.API(auth, wait_on_rate_limit=True, 
wait_on_rate_limit_notify=True)

FILE_NAME = 'last_seen.txt'


def select_language(text):    
    if(text.count('@adamsandlerbot en') > 0):
        return 'en'
    if(text.count('@adamsandlerbot pt') > 0):
        return 'pt'
    return 'en'

def generate_joke_by_lang(url, quest_field, answer_field):
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers = headers)
    resp_json = response.json()
    quest = resp_json[quest_field]
    answer = resp_json[answer_field]
    formated_joke = quest + "\n\n" + answer
    return formated_joke

def generate_joke(lang):
    if(lang == 'pt'):
        url = 'https://api-charada.herokuapp.com/puzzle'
        return 'lá vai uma piada engraçada\n\n' + generate_joke_by_lang(url, 'question', 'answer')
    elif(lang == 'en'):
        url = 'https://official-joke-api.appspot.com/random_joke'
        return 'there goes a funny joke \n\n' + generate_joke_by_lang(url, 'setup', 'punchline')

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

def is_not_reply(tweet):
    count = tweet.full_text.count('@')
    return count < 3

def reply_tweet(tweet, joke, img):
    status = '@' + tweet.user.screen_name + ' ' + joke
    api.create_favorite(tweet.id)
    api.update_with_media(img, status, in_reply_to_status_id = tweet.id)
    store_last_seen(FILE_NAME, tweet.id)
    print("Replied!")

def bot_run():
    tweets = api.mentions_timeline(read_last_seen(FILE_NAME), tweet_mode='extended')    
    for tweet in reversed(tweets):
        if is_not_reply(tweet):
            lang = select_language(tweet.full_text)
            joke = generate_joke(lang)
            img = select_image_path()
            reply_tweet(tweet, joke, img)

def main():
    while True:
        try:
            bot_run()
            time.sleep(10)
        except tweepy.TweepError:
            time.sleep(60)
        except StopIteration:
            break
        
main()
