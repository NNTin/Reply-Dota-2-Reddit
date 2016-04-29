from steamapi import getrealtimestats
from steamapi import getschema, getleaguelisting
from botcommands.toplivegames import topLiveGamesDict, updateTopLiveGamesDict
from misc.idnamedict import gameMode
import time

serverSteamIDVar = 90101063958206464

getschema.requestGetSchema()
getleaguelisting.requestGetLeagueListing()

updateTopLiveGamesDict() #update topLiveGamesDict

#generate these information once

game = topLiveGamesDict[str(serverSteamIDVar)]


averageMMROrLeague = ''
gameModeDisplay = '%s' %gameMode(game['game_mode'])

if(game.get('league_id', 0) != 0):
    leagueID = game['league_id']
    itemdef = getleaguelisting.leagueListingDictionary[game['league_id']]['itemdef']
    leagueName = getschema.dota2schema['items_game']['items'][str(itemdef)]['name']
    averageMMROrLeague = 'League: %s' %leagueName

if(game.get('average_mmr', 0) != 0):
    averageMMR = game['average_mmr']
    averageMMROrLeague = 'Average MMR: %s' %averageMMR


print(averageMMROrLeague)
print(gameModeDisplay)

matchID = ''

while True:
    response = getrealtimestats.getRealtimeStats(serverSteamIDVar)
    if response == {}:
        time.sleep(5)
        continue

    if matchID == '':
        matchID = response['match']['matchid']

    durationM, durationS = divmod(response['match']['game_time'], 60)
    matchTime = '%02d:%02d' %(durationM, durationS)

    print('%s Game Mode: %s' %(averageMMROrLeague, gameModeDisplay))
    print('matchid: %s game time: %s' %(matchID, matchTime))



    for team in response['teams']:
        teamName = 'abcdefg'
        if team['team_name'] != '': teamName = team['team_name']
        print(teamName)



#message_template = 'https://www.reddit.com/message/compose/?to=' + botName + '&subject=deletion&message={fullname}'
#delete_link = message_template.format(fullname=my_new_comment.fullname)


    #TODO: implement break condition via GetMatchDetails and timestamp (not game_time!)

    time.sleep(5)