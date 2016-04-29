from steamapi import gettoplivegame, getrealtimestats
from displayreddit import drtoplivegames

topLiveGamesDict = {}

def updateTopLiveGamesDict():
    global topLiveGamesDict
    for i in range (0, 4):
        tmpTopLiveGamesVar = gettoplivegame.requestGetTopLiveGame(i)

        for game in tmpTopLiveGamesVar['game_list']:

            if (game['server_steam_id'] not in topLiveGamesDict.keys()):
                topLiveGamesDict[game['server_steam_id']] = game
                #print('%s aaa %s %s' %(i, game['league_id'], game['spectators']))
            else:
                if (game['spectators'] > topLiveGamesDict[game['server_steam_id']]['spectators']):
                    topLiveGamesDict[game['server_steam_id']] = game
                #else:
                #    print('spectators count is lower (Volvo fix this please)')


def topLiveGames(filterBy):
    defaultFilter = 'spectators'

    if (filterBy.lower().__contains__('mmr')): filterBy ='average_mmr'
    elif (filterBy != 'average_mmr'):
        filterBy = defaultFilter
    #TODO: add option to display or MMR league only games


    global topLiveGamesDict
    topLiveGamesDict = {}
    updateTopLiveGamesDict()


    #for game in topLiveGamesDict:
    #    print('Unsorted: %s %s' %(topLiveGamesDict[game]['league_id'], topLiveGamesDict[game]['spectators']))

    sortedTopLiveGamesIndices = sorted(topLiveGamesDict.keys(), key=lambda x:topLiveGamesDict[x].get(filterBy, 0), reverse=1)

    ##debugging code
    #for index in sortedTopLiveGamesIndices:
    #    print('%s %s' %(topLiveGamesDict[index]['spectators'], topLiveGamesDict[index]['average_mmr']))




    topLiveGamesList = []

    i = 0
    for index in sortedTopLiveGamesIndices:
        if (topLiveGamesDict[index]['spectators'] == 0):
            break

        #print('Sorted: %s %s' %(topLiveGamesDict[index]['league_id'], topLiveGamesDict[index]['spectators']))

        #this provides more information such as KDA, LH/D, levels, gold but I can't put it in 1 post
        topLiveGamesDict[index]['realtime'] = getrealtimestats.getRealtimeStats(topLiveGamesDict[index]['server_steam_id'])

        topLiveGamesList.append(topLiveGamesDict[index])

        i = i + 1
        if (i == 3):                #increase to 5 later
            break

    reply = drtoplivegames.displayTopLiveGames(topLiveGamesList)

    return reply
