from steamapi import getproplayerlist



def playerConverter(playerID, playerSummariesJson=None):
    proPlayerDictionary = getproplayerlist.proPlayerDictionary

    if playerID == 4294967295:
        return 'anon'

    result = ''
    if (playerID in proPlayerDictionary and proPlayerDictionary[playerID].get('is_pro', False) == True):
        if False:
            if(proPlayerDictionary[playerID].get('country_code', 0) != 0 and proPlayerDictionary[playerID].get('country_code', 0) != ''):
                result += '[](/%s)' %proPlayerDictionary[playerID]['country_code']
            result += '[%s](http://www.dotabuff.com/esports/players/%s "' %(proPlayerDictionary[playerID].get('name', 'Pro Player!'), playerID)
            if(proPlayerDictionary[playerID].get('name', 0) != 0 and proPlayerDictionary[playerID].get('name', 0) != ''):
                result += 'name: %s' %(proPlayerDictionary[playerID]['name'])
            if(proPlayerDictionary[playerID].get('team_name', 0) != 0 and proPlayerDictionary[playerID].get('team_name', 0) != ''):
                result += ' team name: %s' %(proPlayerDictionary[playerID]['team_name'])
            if(proPlayerDictionary[playerID].get('is_locked', 0) != 0 and proPlayerDictionary[playerID].get('is_locked', 0) != ''):
                result += ' is locked: %s' %(proPlayerDictionary[playerID]['is_locked'])
            if(proPlayerDictionary[playerID].get('sponsor', 0) != 0 and proPlayerDictionary[playerID].get('sponsor', 0) != ''):
                result += ' sponsor: %s' %(proPlayerDictionary[playerID]['sponsor'])
            result += '")  '

        if proPlayerDictionary[playerID].get('country_code', 0) != 0 and proPlayerDictionary[playerID].get('country_code', 0) != '':
            countryFlag = '[](/%s)' %proPlayerDictionary[playerID]['country_code']
        else: countryFlag = ''

        playerName = '%.12s' %proPlayerDictionary[playerID]['name'] #trimming name length because of some people

        result += '[DB](http://dotabuff.com/players/%s "Dotabuff: Lookup people\'s match history")/' \
                  '[OD](http://opendota.com/players/%s "OpenDota: Provides free replay analysis") %s' \
                  '[%s](#proplayer "name: %s, team name: %s, is locked: %s, sponsor: %s")' %(playerID, playerID,
                                                                                          countryFlag,
                                                                                          playerName,
                                                                                          proPlayerDictionary[playerID]['name'],
                                                                                          proPlayerDictionary[playerID]['team_name'],
                                                                                          proPlayerDictionary[playerID]['is_locked'],
                                                                                          proPlayerDictionary[playerID]['sponsor'])
        result = result.replace('|','').replace('\\','').replace('*','')
        return result

    else:
        if playerSummariesJson==None:
            result = '[DB](http://dotabuff.com/players/%s "Dotabuff: Lookup people\'s match history")/[OD](http://opendota.com/players/%s "OpenDota: Provides free replay analysis")' %(playerID, playerID)
        else:
            for player in playerSummariesJson['response']['players']:
                if int(player['steam32id']) == playerID:
                    try:
                        playerName = '%.12s' %player['personaname']
                    except:
                        playerName = ''
                    break

            result = '[DB](http://dotabuff.com/players/%s "Dotabuff: Lookup people\'s match history")/' \
                     '[OD](http://opendota.com/players/%s "OpenDota: Provides free replay analysis") %s' %(playerID, playerID, playerName)

            result = result.replace('|','').replace('\\','').replace('*','')
        return result


