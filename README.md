# Reddit_Top_Post_Telegram_Bot
Telegram bot which sends users a formatted reply with information about a top post in a specific subReddit.

## Start a Conversation
To converse with this bot, you will need an account for [Telegram Messenger](https://telegram.org/). You will also need Telegram downloaded on one or more of the available platforms (iOS, Android, Windows, Mac, Linux, Web).

Once you are set up, navigate to contacts and enter [@RedditTopPostBot](https://telegram.me/RedditTopPostBot) into the search bar, then add the bot as a contact. Alternatively, click the hyperlink, and you will be prompted to open a new conversation with the bot with an instance of Telegram already open on your computer.

## Features
Using the '/grab' command to initiate a query is simple. Type /grab followed by a mandatory subReddit argument, and optionally a timeline filter (hour, day, week, month, year, all).

**Example of /grab without providing a timeline argument:**
![Pic](https://raw.github.com/MaxCowan/Reddit_Top_Post_Telegram_Bot/master/Screenshots/EG_no_timeline_arg.png)

**Example of /grab with a timeline argument provided:**
![Pic](https://raw.github.com/MaxCowan/Reddit_Top_Post_Telegram_Bot/master/Screenshots/EG_timeline_included.png)

If you need to reference the manual, type /help.

## Deployment
I am currently hosting this bot on my own server pretty much 24/7. If it needs to be taken down for a substantial amount of time, I will update the description here on GitHub.

If you wish to deploy this bot locally on your machine, just clone the repo and run the Main.py file indefinitely.
To do this, you will need a couple things installed.

### Dependencies:
* Python 3.X 
* PRAW ```pip3 install praw```
* python-telegram-bot ```python-telegram-bot```
* A reddit account and an API token for a 'script' type app for that account (you also need to fill in a couple strings on lines 13-15 in RedditInstance.py). '''client_id''' and '''client_secret''' can be obtained from reddit, while '''user_agent''' should be some concatenation of the app name, version, and author.

**Fill in with Reddit API credentials**
![Pic](https://raw.github.com/MaxCowan/Reddit_Top_Post_Telegram_Bot/master/Screenshots/RedditInstance_Login.png)
