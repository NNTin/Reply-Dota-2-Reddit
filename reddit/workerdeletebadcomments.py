import time
from reddit.botinfo import botName
from reddit.redditconstants import MAXPOSTS, WAIT
from reddit.botinfo import message
#message = True


def deleteBadComments(r):

    user = r.get_redditor(botName)
    print(botName)

    while True:
        try:
            if message: print('[workerdeletebadcomments] Searching for bad comments on bot...')
            for comment in user.get_comments(limit=MAXPOSTS):
                if comment.score < 1:
                    if message: print('[workerdeletebadcomments] Attempting to delete bad comment')
                    if message: print(comment)
                    comment.delete()
                    if message: print('[workerdeletebadcomments] bad comment deleted')
            time.sleep(6*WAIT)
        except:
            if message: print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            if message: print('[workerdeletebadcomments] There was a fatal error')
            if message: print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            time.sleep(6*WAIT)

