import time
import sqlite3
import threading
from reddit.redditconstants import WAIT, SUBREDDIT, IGNOREAUTHORS, KEYWORDS, MAXPOSTS, CLEANCYCLES
from reddit import workeranalyzecontent
from reddit.botinfo import message
message2 = False

def findComments(r):

    subreddit = r.subreddit(SUBREDDIT)


    cycles = 0
    if message: print('[workerfindcomments] Opening SQL Database')
    sql = sqlite3.connect('sql.db')
    cur = sql.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS oldposts(id TEXT)')

    time.sleep(2)

    while True:
        try:
            if message: print('[workerfindcomments] Searching %s' % SUBREDDIT)

            posts = subreddit.stream.comments()


            for post in posts:
                pid = post.id


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


                cur.execute('SELECT * FROM oldposts WHERE ID=?', [pid])
                if cur.fetchone():
                    if message2: print('[workerfindcomments] already replied to comment')
                    continue

                cur.execute('INSERT INTO oldposts VALUES(?)', [pid])
                sql.commit()


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

            cycles += 1
        except:
            if message: print('[workerfindcomments] Could not search for comments')


        if cycles >= CLEANCYCLES:
            if message: print('[workerfindcomments] Cleaning database')
            cur.execute('DELETE FROM oldposts WHERE id NOT IN (SELECT id FROM oldposts ORDER BY id DESC LIMIT ?)', [MAXPOSTS * 2])
            sql.commit()
            cycles = 0
        if message: print('[workerfindcomments] Running again in %d seconds' % WAIT)
        time.sleep(WAIT)