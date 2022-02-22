# Reddit Bot for Yu-Gi-Oh cards 

Implemented in Python 3.9 using PRAW 7.5

## Features

Works on submission bodies as well as comments

Matches card names as long as the user input is "close enough" using difflib's get_close_matches function (E.G. {bllue eye wheat dragoon} will output Blue-Eyes White Dragon)

Handles special characters which are required to fetch certain cards (E.G. {evil twin lilla} will output Evil★Twin_Lil-la)

Matches card names if they are a substring of the full card name (E.G. {garnet} will output Gem-Knight Garnet)

{CARDNAME} outputs links containing an image of the card as well as its wiki article, price data and Master Duel entry

{{CARDNAME}} outputs all of the above as well as full information about the card in text 

## Installation

Install the requirements with pip
```
pip install -r requirements.txt
```

Sign into Reddit using the account you want to use to for the bot

Create a Reddit Application using this link (https://www.reddit.com/prefs/apps/) and following the template below
![Bot Creation Template](./images/Create_Bot.png)

Note down the CLIENT ID and CLIENT SECRET 
![Bot Credentials Page](./images/Bot_Credentials.png)

Create a .env file in the same folder and set the required environment variables 
```
REDDIT_USERNAME="BOT ACCOUNT USERNAME"
REDDIT_PASSWORD="BOT ACCOUNT PASSWORD"
REDDIT_CLIENT_ID="APPLICATION CLIENT_ID"
REDDIT_CLIENT_SECRET="APPLICATION CLIENT_SECRET"
REDDIT_USER_AGENT="USER_AGENT (a short description of the bot)"
REDDIT_SUBREDDITS="SUBREDDITS (separated by plus signs E.G. botwatch+test)"
```

## Usage

```
python .\replybot.py
```
Go to any of the subreddits entered into the REDDIT_SUBREDDITS field of the .env

Either Comment in a post or create a post with the name of any number of Yu-Gi-Oh cards in either single curly brackets or double curly brackets

## Inspirations 

Creating a Reddit bot using Python (https://levelup.gitconnected.com/creating-a-reddit-bot-using-python-5464d4a5dff2) - A comprehensive tutorial in creating a Reddit bot using PRAW

MTGCardFetcher (https://github.com/XSlicer/RedditMTGBot) - A bot that fetches Magic: The Gathering cards which inspired this project 

YugiohLinkBot (https://github.com/Nihilate/YugiohLinkBot) - A retired bot that fetches Yu-Gi-Oh cards programmed in Python2

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html)