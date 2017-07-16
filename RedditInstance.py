#!/usr/bin/env python

from praw import Reddit
from prawcore.exceptions import ResponseException
from prawcore.exceptions import Redirect
from prawcore.exceptions import Forbidden
from prawcore.exceptions import NotFound
from prawcore.exceptions import BadRequest


class RedditInstance:
    # Enter credentials
    objInstance = Reddit(client_id='PT6EgydVhXGgUg',
                         client_secret='-AnhGdjFhCtn4FimP6SR-1ud79Y',
                         user_agent='Telegram Bot:TopPost_Bot:Version 1.0 (by /u/Outer_Space_Ace)'
                         )
    def __init__(self):
        # Kill objReddit instance if there is a problem connecting
        if not self.testConnection():
            print("Shutting Down...")
            quit()

    # Test connection to Reddit
    def testConnection(self):
        try:
            for objTestSubmission in self.objInstance.subreddit('all').top('all', limit=1):
                strTestTitle = objTestSubmission.title
            print("Successfully connected to objReddit API")
            return True

        # If a ResponseException is thrown, it likely has to do with the authenticity of credentials provided
        except ResponseException:
            print("ERROR: COULD NOT CONNECT TO REDDIT API ||| CHECK CREDENTIALS")
            return False

    # Return information about requested reddit content
    def grabPostContent(self, strSubreddit, strTimelineString):
        arrData = []
        base_url = "https://www.reddit.com"
        try:
            counter = 0
            for post in self.objInstance.subreddit(strSubreddit).top(strTimelineString, limit=1):
                counter += 1
                # [Post title, Link to comments, Link to post content, T/F whether the post is a self (text) post]
                arrData = [post.title, str(base_url + post.permalink), post.url, post.is_self]
            if counter != 0:
                return arrData
            else:
                return ["I couldn't find any posts for the selected timeline. Try another timeline."]
        except Redirect:
            return ["I cannot find r/" + strSubreddit]

        except Forbidden:
            return ["None shall pass here..."]

        except NotFound:
            return ["r/" + strSubreddit + " cannot be found or has been banned."]

        except BadRequest:
            return ["I cannot find r/" + strSubreddit]
