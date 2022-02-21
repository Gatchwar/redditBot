import praw  
import re
import os
import json
import requests
from difflib import get_close_matches
from dotenv import load_dotenv  # import dotenv to get environment variables from .env file
load_dotenv()

REGEX = '{([^\[\]]*?)}'
ABOUT_BOT = '^^{CARDNAME} ^^to ^^invoke ^^a ^^card'
BASE_URL = 'http://yugiohprices.com/'
WIKI_URL = 'https://yugioh.fandom.com/wiki/'
MASTER_DUEL_URL = 'https://www.masterduelmeta.com/cards/'

username = os.environ.get("REDDIT_USERNAME")

reddit = praw.Reddit(client_id=os.environ.get("REDDIT_CLIENT_ID"),  
                        client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),  
                        username=username,  
                        password=os.environ.get("REDDIT_PASSWORD"), 
                        user_agent=os.environ.get("REDDIT_USER_AGENT")) 

subreddit = reddit.subreddit(os.environ.get("REDDIT_SUBREDDITS")) # Fetch subreddit instances from .env

req = requests.get(BASE_URL + 'api/card_names')
card_names_list = json.loads(json.dumps(req.json())) # get every card name and put into a list

def reply_builder(cards):
    reply = ''
    for i in cards:  # cast cards to set to remove duplicates
        print(i)
        card_input = ' '.join([word.capitalize() for word in i.split()]) # capitalize first letter of each word to make matching easier
        closest = get_close_matches(card_input, card_names_list, 1, 0.7) # finds card with name closest to input name if exists
        if closest:
            card_name = closest[0].split()
            reply += "[" + ' '.join(card_name) + "](" + BASE_URL + "api/card_image/" + '+'.join(card_name) + ")"
            reply += ' - '
            reply += "[(wiki)](" + WIKI_URL + '_'.join(card_name) + ") "
            reply += "[($)](" + BASE_URL + "card_price?name=" + '+'.join(card_name).replace('&', '%26') + ") "
            reply += "[(MD)](" + MASTER_DUEL_URL + closest[0] + ")"
            reply += '\n\n'
    return reply

def main():
    # subreddit.stream yields new comments/submissions as they are created
    # skip_existing=True ignores all comments/submissions created prior to the stream's creation
    # pause_after=-1 stream yields None after each request (allows monitoring 2 streams without blocking each other) 
    new_comments = subreddit.stream.comments(skip_existing=True, pause_after=-1)
    new_submissions = subreddit.stream.submissions(skip_existing=True, pause_after=-1)
    while True:
        for comment in new_comments:
            #If the post has been deleted, getting the author will return an error, use a try/except to avoid crashing
            try:
                author = comment.author.name
            except Exception:
                break
            if comment is None or author == username:  # do not self-reply
                break
            cards = re.findall(REGEX, comment.body)  # Regex to find all instances of {CARDNAME}
            reply = reply_builder(set(cards))
            if reply:  # only reply when any card names are found
                try:
                    reply += ABOUT_BOT
                    comment.reply(reply)
                except Exception as err: 
                    print(str(err))
    
        for submission in new_submissions:
            if submission is None:
                break
            cards = re.findall(REGEX, submission.selftext)
            reply = reply_builder(set(cards))
            if reply:
                try:
                    reply += ABOUT_BOT
                    submission.reply(reply)
                except Exception as err: 
                    print(str(err))


if __name__ == "__main__":
    main()

