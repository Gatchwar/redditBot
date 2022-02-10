import praw  
import re
from time import sleep

# Create reddit instance using the credentials in the praw.ini
reddit = praw.Reddit('bot1') 

subreddit = reddit.subreddit('TCGBotTest937') 

ids = []
with open('done.txt', 'r') as f:
    for i in f:
        ids.append(i.replace("\n", ""))

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