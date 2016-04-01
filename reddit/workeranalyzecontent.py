from botcommands import averagelastxgames
from reddit.botinfo import message
from steamapi import getheroes
import time
import re
#message = True

def analyzeContent(post):
    if message: print('[workeranalyzecontent')

    replyWorthy = False

    pbody = post.body.lower()

    partialReply = ''

    #try:
    if True:
        # https://regex101.com/#python

        pattern = '(yasp\.co|dotabuff\.com)\/players\/(?P<player_id>\d{0,9})( amount:( )?(?P<amount>\d+))?( view:( )?(?P<view>\w+))?( heroes:( )?(?P<heroes>[\w+]+))?'

        patternMatches = re.findall(pattern, pbody, re.I)

        players = []

        alreadyAdded = []

        for patternMatch in patternMatches:
            playedRegions = []
            playedGameModes = []
            playedHeroes = []
            player = {}
            player['player_id'] = patternMatch[1]
            player['amount'] = patternMatch[4]
            player['view'] = patternMatch[7]


            playedHeroesString = patternMatch[10].split('+')
            for hero in playedHeroesString:
                if hero.lower() in getheroes.heroDictionary.values():
                    playedHeroes.append(hero.lower())

            filterWith = {}
            filterWith['heroes'] = playedHeroes
            filterWith['game_modes'] = playedGameModes
            filterWith['regions'] = playedRegions

            player['filter_with'] = filterWith

            if(player['player_id'] not in alreadyAdded):
                if(len(alreadyAdded) < 1): #anaylze a maxmium of 1 (after hover to view works 3) players in 1 post because of character limit
                    players.append(player)
                    alreadyAdded.append(player['player_id'])

        print(players)



        for player in players:
            playerID = player['player_id']
            amount = player['amount']
            view = player['view']
            filterWith = player['filter_with']
            if(RepresentsInt(playerID)):
                try:
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
                except:
                    print('[workeranalyzecontent] failed to average last x games on %s' %playerID)
                    partialReply += 'Failed to average last X games on player id: %s' %playerID


    #except:
        #print('[workeranalyzecontent] failed to average last x games on')

        #partialReply += 'Failed to average last X games on player id: %s' %playerID

    #try:
    #    print('add another partial reply')
    #except:
    #    print('add another partial reply')

    #"<player link> [amount:<amount of games up to 500>] [view:detailed]\n e.g. yasp.co/players/40547474 amount:75 view:detailed"

    replyIntro = ''

    replyEnd = '[^^source](http://github.com/NNTin/Reply-Dota-2-Reddit) ^^on ^^github, [^^summon](https://www.reddit.com/r/DotA2/comments/4cl7cl/uanalyzelast100games_now_supports_filtering_by/ "<player link> [amount:<amount of games>] [view:detailed] [heroes:<hero name>{+<hero name>}]") ^^the ^^bot'


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
