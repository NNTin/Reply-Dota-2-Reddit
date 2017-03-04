import time, obot
from reddit.botinfo import botName
from reddit.redditconstants import MAXPOSTS, WAIT
from reddit.botinfo import message
#message = True


def deleteBadComments(r):


    while True:
        try:
            if message: print('[workerdeletebadcomments] Searching for bad comments on bot...')
            for comment in r.redditor(obot.username).comments.new(limit=MAXPOSTS):
                if comment.score < 1:
                    if message: print('[workerdeletebadcomments] Attempting to delete bad comment')
                    if message: print(comment)
                    comment.delete()
                    if message: print('[workerdeletebadcomments] bad comment deleted')
            time.sleep(6*WAIT)
        except:
            time.sleep(6*WAIT)

