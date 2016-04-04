import praw
import OAuth2Util
from steamapi import getheroes, getproplayerlist, getschema, getleaguelisting
from reddit import botinfo
from reddit import workerdeletebadcomments, workerfindcomments
import threading
from reddit.botinfo import message
#message = True


class LoginReddit:

    def __init__(self):
        if message: print('[loginreddit] setting user agent')
        r = praw.Reddit(botinfo.app_ua)
        if message: print('[loginreddit] login into reddit')
        o = OAuth2Util.OAuth2Util(r)
        if message: print('[loginreddit] auto-login enabled')
        o.refresh(force=True)
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

        if message: print('[loginreddit] updating dota 2 league listing')
        getleaguelisting.requestGetLeagueListing()
        if message: print('[loginreddit] updating dota 2 league listing success')



        if message: print('[loginreddit] starting threads')

        print('[loginreddit] starting deleteBadComments thread')
        t = threading.Thread(target=workerdeletebadcomments.deleteBadComments , args = (r,))
        t.start()

        if message: print('[loginreddit] starting findComments thread')
        t = threading.Thread(target=workerfindcomments.findComments, args = (r,))
        t.start()

        if message: print('[loginreddit] starting threads success')



        self.r = r
        self.o = o



