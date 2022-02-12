import praw  
import re
import os
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

subreddit = reddit.subreddit('TCGBotTest937+test') 

def main():
    # subreddit.stream yields new comments/submissions as they are created
    # skip_existing=True ignores all comments/submissions created prior to the stream's creation
    # pause_after=-1 stream yields None after each request (allows monitoring 2 streams without blocking each other) 
    new_comments = subreddit.stream.comments(skip_existing=True, pause_after=-1)
    new_submissions = subreddit.stream.submissions(skip_existing=True, pause_after=-1)
    while True:
        for comment in new_comments:
            if comment is None:
                break
            cards = re.findall("{([^\[\]]*?)}", comment.body)
            reply = ""
            for i in set(cards):  # cast cards to set to remove duplicates
                print(i)
                card_name = [word.capitalize() for word in i.split()]
                reply += "[" + ' '.join(card_name) + "](https://yugioh.fandom.com/wiki/" + '_'.join(card_name) + ")\n\n"
            if reply:  # only reply when any card names are found
                try:
                    comment.reply(reply)
                except Exception as err: 
                    print(str(err))
    
        for submission in new_submissions:
            if submission is None:
                break
            cards = re.findall("{([^\[\]]*?)}", submission.selftext)
            reply = ""
            for i in set(cards):
                print(i)
                card_name = [word.capitalize() for word in i.split()]
                reply += "[" + ' '.join(card_name) + "](https://yugioh.fandom.com/wiki/" + '_'.join(card_name) + ")\n\n"
            if reply:
                try:
                    submission.reply(reply)
                except Exception as err: 
                    print(str(err))


if __name__ == "__main__":
    main()

