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

ids = []

try:
    with open('done.txt', 'r') as f:
        for i in f:
            ids.append(i.replace("\n", ""))
except FileNotFoundError:
    print("No done.txt file to read from")

def reply():
    current_ids = []
    sub_comments = subreddit.comments()
    for comment in sub_comments:
        current_ids.append(comment.id)
        if comment.id not in ids:
            cards = re.findall("{([^\[\]]*)}", comment.body)
            reply = ""
            for i in set(cards):
                reply += "[" + i + "](https://yugioh.fandom.com/wiki/" + '_'.join(i.split()) + ")"
            if reply:
                try:
                    comment.reply(reply)
                except Exception as err: 
                    print(str(err))
            ids.append(comment.id)
    return current_ids

while True:
    new_ids = reply()
    with open("done.txt", "w") as f:
        for i in new_ids:
            f.write(str(i) + '\n')
    print("sleeping")
    sleep(60)