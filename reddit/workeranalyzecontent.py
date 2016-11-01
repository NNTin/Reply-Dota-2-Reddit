from botcommands import averagelastxgames, match
from reddit.botinfo import message,botName
from steamapi import getheroes
import time
import re
#message = True

def analyzeContent(post):
    if message: print('[workeranalyzecontent')

    pbody = post.body.lower()
    partialReply = ''

    analyzedMatches = []
    analyzedPlayers = []
    commandCounter = 0


    try:
        pattern = '(?P<website>yasp\.co|dotabuff\.com|opendota\.com)\/players\/(?P<playerID>\d{1,9})((\/(?P<tab>\w+))?((?P<queryParameters>\S+))?)?'
        patternHero = '[?&](hero|hero_id)=(?P<heroID>\w+)'
        #TODO: check if gameMode filtering is working, as of 2016-11-01 query parameter broken in SteamAPI
        patternGameMode = '[?&]game_mode=(?P<gameModeID>\w+)'

        for m in re.finditer(pattern, pbody, re.I):
            if commandCounter < 3:                      #Reddit has character limit, only have room for 3 player analysis
                playerID = m.group('playerID')
                if playerID not in analyzedPlayers:
                    queryParameters = m.group('queryParameters')
                    website = m.group('website')
                    heroID = None
                    gameModeID = None
                    if queryParameters != None and (website == 'opendota.com' or website == 'yasp.co'):
                        n = re.search(patternHero, queryParameters, re.I)
                        if n != None:
                            heroID = n.group('heroID')
                        n = re.search(patternGameMode, queryParameters, re.I)
                        if n != None:
                            gameModeID = n.group('gameModeID')
                    partialReply += str(averagelastxgames.averageLastXGames(int(playerID), amount=100, detailedAnalysis=False, heroID=heroID, gameModeID=gameModeID))
                    commandCounter += 1
                    analyzedPlayers.append(playerID)
            else:
                break
    except:
        print('[workeranalyzecontent] failed to average last x games on')

    try:
        pattern = '(yasp\.co|dotabuff\.com|opendota\.com)\/matches\/(?P<matchID>\d{1,10})'

        for m in re.finditer(pattern, pbody, re.I):
            if commandCounter < 3:                      #Reddit has character limit, only have room for 3 match analysis
                matchID = m.group('matchID')
                if matchID not in analyzedMatches:
                    partialReply += str(match.match(matchID))
                    commandCounter += 1
                    analyzedMatches.append(matchID)
            else:
                break

    except:
        print('[workeranalyzecontent] failed to get match')



    replyIntro = ''

    replyEnd = '[^^source](http://github.com/NNTin/Reply-Dota-2-Reddit) ^^on ^^github, [^^message](https://www.reddit.com/message/compose/?to=lumbdi) ^^the ^^owner'


    reply = replyIntro + partialReply + replyEnd


    if(commandCounter != 0):
        i = 0
        while i < 20:
            i += 1
            try:
                my_new_comment = post.reply(reply)
                print('reply success')

                j = 0
                while j < 20:
                    j += 1
                    try:
                        message_template = 'https://www.reddit.com/message/compose/?to=' + botName + '&subject=deletion&message={fullname}'
                        delete_link = message_template.format(fullname=my_new_comment.fullname)

                        footer_template = ', [^^deletion ^^link]({url} "Only works for bot summoner and /r/dota2 mods! Do not change already filled out form!")'
                        footer = footer_template.format(url=delete_link)
                        my_new_comment.edit(my_new_comment.body + footer)

                        break
                    except:
                        time.sleep(2*j)

                break
            except:
                print('reply was not a success, retrying in %s' %(2*i))
                time.sleep(2*i)



def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
