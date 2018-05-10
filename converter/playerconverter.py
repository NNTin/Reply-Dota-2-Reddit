from steamapi import getproplayerlist
from odotaapi import getodplayerdetails



def playerConverter(playerID, playerSummariesJson=None, includeMMR=False):

    MMR = None
    if includeMMR:
        MMR = getMMR(playerID)


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
                  '[OD](http://opendota.com/players/%s "OpenDota: Provides free replay analysis")/' \
                  '[STRATZ](https://stratz.com/player/%s "STRATZ: Every match, every player, every stat. Free.") %s' \
                  '[%s](#proplayer "name: %s, team name: %s, is locked: %s, sponsor: %s")' %(playerID, playerID, playerID,
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
            result = '[DB](http://dotabuff.com/players/%s "Dotabuff: Lookup people\'s match history")/' \
                     '[OD](http://opendota.com/players/%s "OpenDota: Provides free replay analysis")/' \
                     '[STRATZ](https://stratz.com/player/%s "STRATZ: Every match, every player, every stat. Free.")' %(playerID, playerID, playerID)
        else:
            for player in playerSummariesJson['response']['players']:
                if int(player['steam32id']) == playerID:
                    try:
                        playerName = '%.12s' %player['personaname']
                    except:
                        playerName = ''
                    break

            result = '[DB](http://dotabuff.com/players/%s "Dotabuff: Lookup people\'s match history")/' \
                     '[OD](http://opendota.com/players/%s "OpenDota: Provides free replay analysis")/' \
                     '[STRATZ](https://stratz.com/player/%s "STRATZ: Every match, every player, every stat. Free.") %s' %(playerID, playerID, playerID, playerName)

            result = result.replace('|','').replace('\\','').replace('*','')
        return result


def getMMR(playerID):
    try:
        odPlayerJson = getodplayerdetails.getODPlayerDetails(playerID)
        MMR = {}
        if odPlayerJson['solo_competitive_rank'] != None:
            MMR['solo'] = odPlayerJson['solo_competitive_rank']
        if odPlayerJson['competitive_rank'] != None:
            MMR['party'] = odPlayerJson['competitive_rank']
        if odPlayerJson['mmr_estimate']['estimate'] != None:
            MMR['estimate'] = odPlayerJson['mmr_estimate']['estimate']

        #if MMR dict is empty it returns False
        if bool(MMR):
            return MMR
        else:
            return None
    except:
        return None