import praw  
import re
import os
from time import sleep
from dotenv import load_dotenv  # import dotenv to get environment variables from .env file
load_dotenv()

if os.path.isfile('./praw.ini'): 
    # Create reddit instance using the credentials in the praw.ini
    reddit = praw.Reddit('bot1') 
else:
    reddit = praw.Reddit(client_id=os.environ.get("REDDIT_CLIENT_ID"),  
                            client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),  
                            username=os.environ.get("REDDIT_USERNAME"),  
                            password=os.environ.get("REDDIT_PASSWORD"), 
                            user_agent=os.environ.get("REDDIT_USER_AGENT")) 

subreddit = reddit.subreddit('TCGBotTest937') 

def reply():
    sub_comments = subreddit.stream.comments(skip_existing=True)
    for comment in sub_comments:
        cards = re.findall("{([^\[\]]*?)}", comment.body)
        reply = ""
        for i in set(cards):
            card_name = [word.capitalize() for word in i.split()]
            reply += "[" + ' '.join(card_name) + "](https://yugioh.fandom.com/wiki/" + '_'.join(card_name) + ")\n\n"
        if reply:
            try:
                comment.reply(reply)
            except Exception as err: 
                print(str(err))
    return

while True:
    reply()
    sleep(20)