import praw  
import re
import os
import json
import requests
from difflib import get_close_matches
from dotenv import load_dotenv  # import dotenv to get environment variables from .env file
load_dotenv()

REGEX = '(?<=(?<!\{)\{)([^{}]*)(?=\}(?!\}))'
LONG_REGEX = '{{([^\[\]]*?)}}'
ABOUT_BOT = '^^{CARDNAME} ^^to ^^invoke ^^a ^^card, ^^{{CARDNAME}} ^^to ^^also ^^get ^^information'
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

def format_card_data(card):
    try:
        try:
            req = requests.get(BASE_URL + 'api/card_data/' + card.replace(' ', '+'))
        except Exception as e:
            print(e)
            return None
        else:
            req.connection.close()
            if req.ok:
                json = req.json()
                text = ''
                if json.get('status', '') == 'success':
                    data = json['data']
                    if data['card_type'] == 'monster':
                        types = data['type'].replace(' ', '').split('/')
                        text += '{} Monster\n\n{} / {}\n\n{}\n\nAtk: {}'.format(types[1], data['family'].capitalize(), types[0], data['text'].replace('\n\n', ''), data['atk'])
                    else:
                        text += '{} {}\n\n{}'.format(data['property'], data['card_type'].capitalize(), data['text'].replace('\n\n', ' '))
                return text 

    except Exception as e:
        print(e)
        return None

def reply_builder(cards):
    reply = ''
    for i in cards:
        print(i)
        card_input = ' '.join([word.capitalize() for word in i.split()]) # capitalize first letter of each word to make matching easier
        closest = get_close_matches(card_input, card_names_list, 1, 0.7) # finds card with name closest to input name if exists
        if closest:
            card_name = closest[0]
            reply += "[" + card_name + "](" + BASE_URL + "api/card_image/" + card_name.replace(' ', '+') + ")"
            reply += ' - '
            reply += "[(wiki)](" + WIKI_URL + card_name.replace(' ', '_') + ") "
            reply += "[($)](" + BASE_URL + "card_price?name=" + card_name.replace(' ', '+').replace('&', '%26') + ") "
            reply += "[(MD)](" + MASTER_DUEL_URL + closest[0] + ")"
            reply += '\n\n'
    return reply

def long_reply_builder(cards):
    reply = ''
    for i in cards:
            print(i)
            card_input = ' '.join([word.capitalize() for word in i.split()]) # capitalize first letter of each word to make matching easier
            closest = get_close_matches(card_input, card_names_list, 1, 0.7) # finds card with name closest to input name if exists
            if closest:
                card_name = closest[0]
                reply += "[" + card_name + "](" + BASE_URL + "api/card_image/" + card_name.replace(' ', '+') + ")\n\n"
                reply += format_card_data(card_name) + '\n\n'
                reply += "[(wiki)](" + WIKI_URL + card_name.replace(' ', '_') + ") "
                reply += "[($)](" + BASE_URL + "card_price?name=" + card_name.replace(' ', '+').replace('&', '%26') + ") "
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
            cards = re.findall(REGEX, comment.body)  # Find all instances of {CARDNAME}
            long_cards = re.findall(LONG_REGEX, comment.body)  # Find all instances of {{CARDNAME}}
            reply = ''
            reply += reply_builder(set(cards))
            reply += long_reply_builder(set(long_cards))
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
            long_cards = re.findall(LONG_REGEX, submission.selftext)  # Find all instances of {{CARDNAME}}
            reply = reply_builder(set(cards))
            reply += long_reply_builder(set(long_cards))
            if reply:
                try:
                    reply += ABOUT_BOT
                    submission.reply(reply)
                except Exception as err: 
                    print(str(err))


if __name__ == "__main__":
    main()
