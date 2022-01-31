import praw  
import re

# Create reddit instance using the credentials in the praw.ini
reddit = praw.Reddit('bot1') 
                     
# Create subreddit instance to r/test (A subreddit intended for testing with the reddit API)
subreddit = reddit.subreddit('test') 

# # Iterate over the top X posts of all time in the subreddit
# for submission in subreddit.top(limit = 1): 
#     # displays the submission title 
#     print(submission.title)   
#     # displays the net upvotes of the submission 
#     print(submission.score)   
#     # displays the submission's ID 
#     print(submission.id)    
#     # displays the url of the submission 
#     print(submission.url)  

#     # comments = reddit.submission(url=submission.url)
#     # # Comment on this post
#     # print(submission.reply("test comment"))
#     # # Comment a link using markdown formatting
#     # print(submission.reply("[google](https://google.ca)"))

# # Create a comment instance by comment ID 
# comment = reddit.comment("hq4605q")
# print(comment.body)
# print(comment.author)
# print("Score before downvoting : " + str(comment.score)) 
# comment.downvote() 
# print("Score after downvoting : " + str(comment.score))
# comment.reply("test reply")

# # Create a post in the subreddit with the specified title and text
# post_title="Test Post"
# post_body="This is a bot post"
# # Bind post ID to variable
# post_id = subreddit.submit(title=post_title, selftext=post_body)

# # Create submission object that gets a reddit post by id
# submission = reddit.submission(id="ksb5rx")
# # Remove the "More Comments" links that exist in longer comment chains
# submission.comments.replace_more(limit=None)
# # Iterate through all comments in the post
# for comment in submission.comments.list():
#     print(comment.body)


# Post a comment to fetch a MTG card 
# Create submission object that gets a reddit post by id
# submission = reddit.submission(id="rrnvsn")
# comment_id = submission.reply("[[fireball]]")
# comment = reddit.comment(str(comment_id)) # must cast to string lol
# cards = re.findall("\[\[([^\[\]]*)\]\]", comment.body)
# reply = ""
# for i in set(cards):
#     reply += "[" + i + "](https://gatherer.wizards.com/Pages/Card/Details.aspx?name=" + i + ")"
# comment.reply(reply)

# Post a comment to fetch a yugioh card
# Create submission object that gets a reddit post by id
submission = reddit.submission(id="rrnvsn")
comment_id = submission.reply("[[Droll & Lock Bird]]")
comment = reddit.comment(str(comment_id)) # must cast to string lol
cards = re.findall("\[\[([^\[\]]*)\]\]", comment.body)
reply = ""
for i in set(cards):
    reply += "[" + i + "](https://yugioh.fandom.com/wiki/" + '_'.join(i.split()) + ")"
comment.reply(reply)