from steamapi import getheroes, getproplayerlist, getschema, getleaguelisting
from steamapi import gettoplivegame
from misc.idnamedict import gameMode

getheroes.requestGetHeroes()
getproplayerlist.requestGetProPlayerList()
getschema.requestGetSchema()
getleaguelisting.requestGetLeagueListing()

topLiveGames = gettoplivegame.requestGetTopLiveGame(2)

for game in topLiveGames['game_list']:
    leagueName = ''
    averageMMR = ''

    if(game.get('league_id', 0) != 0):
        leagueID = game['league_id']
        itemdef = getleaguelisting.leagueListingDictionary[game['league_id']]['itemdef']
        leagueName = getschema.dota2schema['items_game']['items'][str(itemdef)]['name']
        print(leagueName)

    if(game.get('average_mmr', 0) != 0):
        averageMMR = game['average_mmr']
        print(averageMMR)

    serverSteamID = game['server_steam_id']

