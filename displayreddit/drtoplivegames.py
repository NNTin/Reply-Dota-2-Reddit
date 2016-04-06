from steamapi import getheroes, getschema, getleaguelisting
from steamapi.getproplayerlist import proPlayerDictionary
from misc.idnamedict import gameMode

def displayTopLiveGames(games):

    partialReply = ''

    for game in games:

        averageMMROrLeague = ''

        if(game.get('league_id', 0) != 0):
            leagueID = game['league_id']
            itemdef = getleaguelisting.leagueListingDictionary[game['league_id']]['itemdef']
            leagueName = getschema.dota2schema['items_game']['items'][str(itemdef)]['name']
            averageMMROrLeague = 'League: %s' %leagueName

        if(game.get('average_mmr', 0) != 0):
            averageMMR = game['average_mmr']
            averageMMROrLeague = 'average MMR: %s' %averageMMR

        serverSteamID = game['server_steam_id']
        delay = '%s seconds' %game['delay']
        spectators = game['spectators']
        radiantScore = game['radiant_score']
        direScore = game['dire_score']
        durationM, durationS = divmod(game['game_time'], 60)
        gameModeDisplay = '%s' %gameMode(game['game_mode'])


        intro = 'Server steam id: [%s](/a "needed for upcoming bot command (display real time stats)"), stream delay: %s, spectators: %s, %s, game mode: %s' %(serverSteamID, delay, spectators, averageMMROrLeague,gameModeDisplay)
        intro += '  \n[Score: %s:%s @ %02d:%02d game time](/spoiler)' %(radiantScore, direScore, durationM, durationS)

        if(int(len(game['players'])) != 10):
            intro += '  \n**Radiant/Dire placement may be inaccurate! Known issue.**'

        intro += '\n\n'

        radiantName = 'Radiant'
        direName = 'Dire'

        if (game['team_name_radiant'] != ''): radiantName = game['team_name_radiant']
        if (game['team_name_dire'] != ''): direName = game['team_name_dire']

        radiantPlayer = []
        direPlayer = []

        count = 0
        for player in game['players']:
            if (count < len(game['players']) / 2 ):
                radiantPlayer.append(player)
            else:
                direPlayer.append(player)
            count += 1


        radiantPlayerString = []
        for player in radiantPlayer:
            playerID = player['account_id']
            singlePlayerString = '[](/hero-%s) ' %(getheroes.heroDictionary[player['hero_id']])

            if (playerID in proPlayerDictionary and proPlayerDictionary[playerID].get('is_pro', False) == True):
                if(proPlayerDictionary[playerID].get('country_code', 0) != 0 and proPlayerDictionary[playerID].get('country_code', 0) != ''):
                    singlePlayerString += '[](/%s)' %proPlayerDictionary[playerID]['country_code']
                singlePlayerString += '[Pro player!](http://www.dotabuff.com/esports/players/%s "' %playerID
                if(proPlayerDictionary[playerID].get('name', 0) != 0 and proPlayerDictionary[playerID].get('name', 0) != ''):
                    singlePlayerString += 'name: %s' %(proPlayerDictionary[playerID]['name'])
                if(proPlayerDictionary[playerID].get('team_name', 0) != 0 and proPlayerDictionary[playerID].get('team_name', 0) != ''):
                    singlePlayerString += ' team name: %s' %(proPlayerDictionary[playerID]['team_name'])
                if(proPlayerDictionary[playerID].get('is_locked', 0) != 0 and proPlayerDictionary[playerID].get('is_locked', 0) != ''):
                    singlePlayerString += ' is locked: %s' %(proPlayerDictionary[playerID]['is_locked'])
                if(proPlayerDictionary[playerID].get('sponsor', 0) != 0 and proPlayerDictionary[playerID].get('sponsor', 0) != ''):
                    singlePlayerString += ' sponsor: %s' %(proPlayerDictionary[playerID]['sponsor'])
                singlePlayerString += '")  '
            else:
                singlePlayerString += '[DB](http://dotabuff.com/players/%s "Dotabuff: Lookup people\'s match history")/[YASP](http://yasp.co/players/%s "Yasp: Provides free replay analysis")' %(playerID, playerID)


            radiantPlayerString.append(singlePlayerString)


        direPlayerString = []
        for player in direPlayer:
            playerID = player['account_id']
            singlePlayerString = '[](/hero-%s)' %(getheroes.heroDictionary[player['hero_id']])

            if (playerID in proPlayerDictionary and proPlayerDictionary[playerID].get('is_pro', False) == True):



                if(proPlayerDictionary[playerID].get('country_code', 0) != 0 and proPlayerDictionary[playerID].get('country_code', 0) != ''):
                    singlePlayerString += '[](/%s)' %proPlayerDictionary[playerID]['country_code']

                singlePlayerString += '**[Pro player!](http://www.dotabuff.com/esports/players/%s "' %playerID
                if(proPlayerDictionary[playerID].get('name', 0) != 0 and proPlayerDictionary[playerID].get('name', 0) != ''):
                    singlePlayerString += 'name: %s' %(proPlayerDictionary[playerID]['name'])
                if(proPlayerDictionary[playerID].get('team_name', 0) != 0 and proPlayerDictionary[playerID].get('team_name', 0) != ''):
                    singlePlayerString += ' team name: %s' %(proPlayerDictionary[playerID]['team_name'])
                if(proPlayerDictionary[playerID].get('is_locked', 0) != 0 and proPlayerDictionary[playerID].get('is_locked', 0) != ''):
                    singlePlayerString += ' is locked: %s' %(proPlayerDictionary[playerID]['is_locked'])
                if(proPlayerDictionary[playerID].get('sponsor', 0) != 0 and proPlayerDictionary[playerID].get('sponsor', 0) != ''):
                    singlePlayerString += ' sponsor: %s' %(proPlayerDictionary[playerID]['sponsor'])
                singlePlayerString += '")**  '

            else:
                singlePlayerString += '**[DB](http://dotabuff.com/players/%s "Dotabuff: Lookup people\'s match history")/[YASP](http://yasp.co/players/%s "Yasp: Provides free replay analysis")**' %(playerID, playerID)

            direPlayerString.append(singlePlayerString)



        radiantLine = '%s' %radiantName
        middleLine = '---'
        direLine = '**%s**' %direName
        for singlePlayerString in radiantPlayerString:
            radiantLine += '|%s' %singlePlayerString
            middleLine += '|---'

        for singlePlayerString in direPlayerString:
            direLine += '|%s' %singlePlayerString

        table = radiantLine + '\n' + middleLine + '\n' + direLine

        end = '\n\n--------\n\n'

        partialReply += intro + table + end


    return partialReply
