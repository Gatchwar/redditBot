import praw  
import re
import os
import json
import requests
from difflib import get_close_matches
from dotenv import load_dotenv  # import dotenv to get environment variables from .env file
load_dotenv()

username = os.environ.get("REDDIT_USERNAME")

reddit = praw.Reddit(client_id=os.environ.get("REDDIT_CLIENT_ID"),  
                        client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),  
                        username=username,  
                        password=os.environ.get("REDDIT_PASSWORD"), 
                        user_agent=os.environ.get("REDDIT_USER_AGENT")) 

subreddit = reddit.subreddit('TCGBotTest937+test') 

req = requests.get("http://yugiohprices.com/api/card_names")
card_names_list = json.loads(json.dumps(req.json())) # get every card name and put into a list

def main():
    # subreddit.stream yields new comments/submissions as they are created
    # skip_existing=True ignores all comments/submissions created prior to the stream's creation
    # pause_after=-1 stream yields None after each request (allows monitoring 2 streams without blocking each other) 
    new_comments = subreddit.stream.comments(skip_existing=True, pause_after=-1)
    new_submissions = subreddit.stream.submissions(skip_existing=True, pause_after=-1)
    while True:
        for comment in new_comments:
            #If the post has been deleted, getting the author will return an error
            try:
                author = comment.author.name
            except Exception:
                break
            if comment is None or author == username:
                break
            cards = re.findall("{([^\[\]]*?)}", comment.body)
            reply = ""
            for i in set(cards):  # cast cards to set to remove duplicates
                print(i)
                card_input = ' '.join([word.capitalize() for word in i.split()]) # capitalize first letter of each word to make matching easier
                closest = get_close_matches(card_input, card_names_list, 1, 0.7) # finds card with name closest to input name if exists
                if closest:
                    card_name = closest[0].split()
                    reply += "[" + ' '.join(card_name) + "](http://yugiohprices.com/api/card_image/" + '+'.join(card_name) + ")"
                    reply += ' - '
                    reply += "[(wiki)](https://yugioh.fandom.com/wiki/" + '_'.join(card_name) + ") "
                    reply += "[($)](http://yugiohprices.com/card_price?name=" + '+'.join(card_name) + ")"
                    reply += '\n\n'
            if reply:  # only reply when any card names are found
                try:
                    reply += '^^{CARDNAME} ^^to ^^invoke ^^a ^^card'
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
                card_input = ' '.join([word.capitalize() for word in i.split()]) # capitalize first letter of each word to make matching easier
                closest = get_close_matches(card_input, card_names_list, 1, 0.7) # finds card with name closest to input name if exists
                if closest:
                    card_name = closest[0].split()
                    reply += "[" + ' '.join(card_name) + "](http://yugiohprices.com/api/card_image/" + '+'.join(card_name) + ")"
                    reply += ' - '
                    reply += "[(wiki)](https://yugioh.fandom.com/wiki/" + '_'.join(card_name) + ") "
                    reply += "[($)](http://yugiohprices.com/card_price?name=" + '+'.join(card_name) + ")"
                    reply += '\n\n'
            if reply:
                try:
                    reply += '^^{CARDNAME} ^^to ^^invoke ^^a ^^card'
                    submission.reply(reply)
                except Exception as err: 
                    print(str(err))


if __name__ == "__main__":
    main()

