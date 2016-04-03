from steamapi.getproplayerlist import requestGetProPlayerList, proPlayerDictionary

requestGetProPlayerList()

for playerID in proPlayerDictionary:
    youDescription = ''
    if(proPlayerDictionary[playerID].get('is_pro', False) == True):
        if(proPlayerDictionary[playerID].get('country_code', 0) != 0 and proPlayerDictionary[playerID].get('country_code', 0) != ''):
            youDescription += '[](/%s)' %proPlayerDictionary[playerID]['country_code']
        youDescription += '[Pro player!](http://www.dotabuff.com/esports/players/%s "' %playerID
        if(proPlayerDictionary[playerID].get('name', 0) != 0 and proPlayerDictionary[playerID].get('name', 0) != ''):
            youDescription += 'name: %s' %(proPlayerDictionary[playerID]['name'])
        if(proPlayerDictionary[playerID].get('team_name', 0) != 0 and proPlayerDictionary[playerID].get('team_name', 0) != ''):
            youDescription += ' team name: %s' %(proPlayerDictionary[playerID]['team_name'])
        if(proPlayerDictionary[playerID].get('is_locked', 0) != 0 and proPlayerDictionary[playerID].get('is_locked', 0) != ''):
            youDescription += ' is locked: %s' %(proPlayerDictionary[playerID]['is_locked'])
        if(proPlayerDictionary[playerID].get('sponsor', 0) != 0 and proPlayerDictionary[playerID].get('sponsor', 0) != ''):
            youDescription += ' sponsor: %s' %(proPlayerDictionary[playerID]['sponsor'])
        youDescription += '")  '


        print(youDescription)
        playerString = ''
