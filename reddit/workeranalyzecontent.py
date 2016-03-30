from botcommands import averagelastxgames
from reddit.botinfo import message
from steamapi import getheroes
import time
#message = True

def analyzeContent(post):
    if message: print('[workeranalyzecontent')

    replyWorthy = False

    pbody = post.body.lower()

    partialReply = ''

    #try:
    if True:
        # need help cleaning this shit up, I'm too dumb for this
        # add support for analyzing multiple player ids at once!

        playerID = pbody.split('/players/')[1]
        playerID = playerID.split(' ')[0]
        playerID = playerID.split('/')[0]
        playerID = playerID.split('\n')[0]
        playerID = playerID.split('?')[0]
        playerID = playerID.split('#')[0]
        playerID = playerID.split(')')[0]

        amount = ''
        try:
            amount = pbody.split('amount:')[1]
            amount = amount.split(' ')[0]
            amount = amount.split('\n')[0]
        except:
            amount = 'amount not found'

        view = 'simple'
        try:
            view = pbody.split('view:')[1]
            view = view.split(' ')[0]
            view = view.split('\n')[0]
        except:
            view = 'simple'

        playedHeroes = []
        try:
            playedHeroesString = pbody.split('playedheroes:')[1]
            playedHeroesString = playedHeroesString.split(' ')[0]
            playedHeroesString = playedHeroesString.split('\n')[0]

            playedHeroesString = playedHeroesString.split('+')
            for hero in playedHeroesString:
                if hero.lower() in getheroes.heroDictionary.values():
                    playedHeroes.append(hero.lower())

        except:
            playedHeroes = []

        playedGameModes = []

        playedRegions = []

        filterWith = {}
        filterWith['heroes'] = playedHeroes
        filterWith['game_modes'] = playedGameModes
        filterWith['regions'] = playedRegions


        if(RepresentsInt(playerID)):
            #try:
            if True:
                if message: print('[workeranalyzecontent] found /players/<number> -> averagelastxgames')

                print(playerID)
                amountVar = 100
                viewVar = False

                if(RepresentsInt(amount)):
                    amountVar = int(amount)

                if(view.lower() == 'detailed'):
                    viewVar = True



                partialReply += str(averagelastxgames.averageLastXGames(int(playerID), amountVar, viewVar, filterWith))

                #TODO: hero and/or game mode specified...

                if(len(partialReply) > 20):
                    replyWorthy = True
            #except:
            #    print('[workeranalyzecontent] failed to average last x games on %s' %playerID)
            #    partialReply += 'Failed to average last X games on player id: %s' %playerID


    #except:
        #print('[workeranalyzecontent] failed to average last x games on')

        #partialReply += 'Failed to average last X games on player id: %s' %playerID

    #try:
    #    print('add another partial reply')
    #except:
    #    print('add another partial reply')

    #"<player link> [amount:<amount of games up to 500>] [view:detailed]\n e.g. yasp.co/players/40547474 amount:75 view:detailed"

    replyIntro = ''

    replyEnd = '\n\n---------------\n\n[^^source](http://github.com/NNTin/Reply-Dota-2-Reddit) ^^on ^^github, [^^summon](/a "<player link> [amount:<amount of games>] [view:detailed] TODO: provide link to thread") ^^the ^^bot'


    reply = replyIntro + partialReply + replyEnd

    print(reply)



    if(replyWorthy):
        i = 0
        while i < 100:
            i += 1
            try:
                post.reply(reply)
                print('reply success')

                break
            except:
                print('reply was not a success, retrying in %s' %(5*i))
                time.sleep(5*i)



def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False