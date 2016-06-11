

from steamapi.getproplayerlist import proPlayerDictionary
from steamapi.getproplayerlist import requestGetProPlayerList

requestGetProPlayerList()

print (proPlayerDictionary)

youDescription = ''

if False:
    for playerID in proPlayerDictionary.keys():
        if (playerID in proPlayerDictionary and proPlayerDictionary[playerID].get('is_pro', False) == True):
            if(proPlayerDictionary[playerID].get('country_code', 0) != 0 and proPlayerDictionary[playerID].get('country_code', 0) != ''):
                youDescription += '[](/%s)' %proPlayerDictionary[playerID]['country_code']
            youDescription += '[%s](http://www.dotabuff.com/esports/players/%s "' %(proPlayerDictionary[playerID].get('name', 'Pro Player!'), playerID)
            if(proPlayerDictionary[playerID].get('name', 0) != 0 and proPlayerDictionary[playerID].get('name', 0) != ''):
                youDescription += 'name: %s' %(proPlayerDictionary[playerID]['name'])
            if(proPlayerDictionary[playerID].get('team_name', 0) != 0 and proPlayerDictionary[playerID].get('team_name', 0) != ''):
                youDescription += ' team name: %s' %(proPlayerDictionary[playerID]['team_name'])
            if(proPlayerDictionary[playerID].get('is_locked', 0) != 0 and proPlayerDictionary[playerID].get('is_locked', 0) != ''):
                youDescription += ' is locked: %s' %(proPlayerDictionary[playerID]['is_locked'])
            if(proPlayerDictionary[playerID].get('sponsor', 0) != 0 and proPlayerDictionary[playerID].get('sponsor', 0) != ''):
                youDescription += ' sponsor: %s' %(proPlayerDictionary[playerID]['sponsor'])
            youDescription += '")  '
        else:
            youDescription = '[DB](http://dotabuff.com/players/%s "Dotabuff: Lookup people\'s match history")/[YASP](http://yasp.co/players/%s "Yasp: Provides free replay analysis")' %(playerID, playerID)
        youDescription += '  \n'

else:
    player_name_template = '[DB](http://dotabuff.com/players/{playerID} "Dotabuff: Lookup people\'s match history")/[YASP](http://yasp.co/players/{playerID} "Yasp: Provides free replay analysis")'
    pro_player_name_template = '[](/{flag})[{name}](/http://www.dotabuff.com/esports/players/{playerID})'

    for playerID in proPlayerDictionary.keys():
        youDescription += player_name_template.format(playerID=playerID)

        youDescription += '  \n'
        youDescription += pro_player_name_template.format(flag=proPlayerDictionary[playerID].get('country_code', 0), name=proPlayerDictionary[playerID].get('name', 'Pro Player!'), playerID=playerID)

        youDescription += '  \n'


print(youDescription)