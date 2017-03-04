import time
import threading
from reddit.redditconstants import WAIT, SUBREDDIT, IGNOREAUTHORS, KEYWORDS
from reddit import workeranalyzecontent
from reddit.botinfo import message
message2 = False

def findComments(r):

    subreddit = r.subreddit(SUBREDDIT)

    time.sleep(2)

    while True:
        try:
            if message: print('[workerfindcomments] Searching %s' % SUBREDDIT)

            posts = subreddit.stream.comments()


            for post in posts:

                try:
                    pauthor = post.author.name
                except AttributeError:
                    if message2: print('[workerfindcomments] author is deleted, don\' care about this post')
                    continue



                if pauthor.lower() == r.user.me():
                    # Don't reply to yourself, robot!
                    if message2: print('[workerfindcomments] will not reply to myself')
                    continue

                if IGNOREAUTHORS != [] and any(auth2.lower() == pauthor.lower() for auth2 in IGNOREAUTHORS):
                    # This post was made by a ignoreauthor
                    if message2: print('[workerfindcomments] Post made by ignore author: ' + pauthor.lower())
                    continue



                pbody = post.body.lower()
                if any(key.lower() in pbody for key in KEYWORDS):
                    try:
                        #post.reply('reply success!')

                        if message: print('[@@@][workerfindcomments] starting analyzecontent thread')
                        t = threading.Thread(target=workeranalyzecontent.analyzeContent, args = (post,True,)) #isPost = True
                        t.start()

                    except:
                        if message: print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                        if message: print('[workerfindcomments] bot could not reply')
                        if message: print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

        except:
            if message: print('[workerfindcomments] Could not search for comments')


        if message: print('[workerfindcomments] Running again in %d seconds' % WAIT)
        time.sleep(WAIT)