import praw
import obot
from steamapi import getheroes, getproplayerlist, getschema, getleaguelisting
from reddit import botinfo
from reddit import workerdeletebadcomments, workerfindcomments, workerdeleterequestedcomments
import threading
from reddit.botinfo import message
#message = True


class LoginReddit:

    def __init__(self):
        if message: print('[loginreddit] logging in')
        r = praw.Reddit(client_id=obot.client_id,
                        client_secret=obot.client_secret,
                        user_agent=obot.user_agent,
                        username=obot.username,
                        password=obot.password)


        if message: print('[loginreddit] logging successful')

        if message: print('[loginreddit] updating heroDictionary')
        getheroes.requestGetHeroes()
        if message: print('[loginreddit] updating heroDictionary success')

        if message: print('[loginreddit] updating proPlayerDictionary')
        getproplayerlist.requestGetProPlayerList()
        if message: print('[loginreddit] updating proPlayerDictionary success')

        if message: print('[loginreddit] updating dota 2 items_game schema')
        getschema.requestGetSchema()
        if message: print('[loginreddit] updating dota 2 items_game schema success')



        if message: print('[loginreddit] starting threads')

        if message: print('[loginreddit] starting deleteBadComments thread')
        t = threading.Thread(target=workerdeletebadcomments.deleteBadComments , args = (r,))
        t.start()

        if message: print('[loginreddit] starting findComments thread')
        t = threading.Thread(target=workerfindcomments.findComments, args = (r,))
        t.start()

        if message: print('[loginreddit] starting deleteRequestedComments thread')
        t = threading.Thread(target=workerdeleterequestedcomments.deleteRequestedComments, args = (r,))
        t.start()

        if message: print('[loginreddit] starting threads success')



        self.r = r
        self.o = o



