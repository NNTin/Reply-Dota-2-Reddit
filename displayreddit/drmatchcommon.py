from steamapi.getproplayerlist import proPlayerDictionary
from steamapi.getheroes import heroDictionary

def displayResult (playerID, playedMatchesTogether, general):


#message_template = 'https://www.reddit.com/message/compose/?to=' + botName + '&subject=deletion&message={fullname}'
#delete_link = message_template.format(fullname=my_new_comment.fullname)


    intro_template = 'Looking at the last **{amountOfMatches}** games: {playerName} played with pro players in **{amountTogether}** games:'
    intro_sub_template = ' {playerName} {amount} times,'

    body_template = '\n\nEach player played the following heroes:\n\n'

    body_sub_template = ' {playerName} |{hero_template}\n\n'
    hero_template = ' {amount}x[](/hero-{hero})'

    end_template = '\n\n---\n\n'


    playerName = getPlayerString(playerID)


    if(general['amountTogether'] == 0):
        #Note: Return empty string if bot should provide no answer!

        template = 'Looking at the last **{amountOfMatches}** games: {playerName} played with no pro player.  \n\n---\n\n'
        all = template.format(amountOfMatches=general['totalGames'], playerName=playerName)
        print(all)
        return(all)


    intro = intro_template.format(amountOfMatches=general['totalGames'], playerName=playerName, amountTogether=general['amountTogether'])
    body = body_template
    end = end_template


    #print('playedMatchesTogether: %s' %playedMatchesTogether)

    #sortedPlayedHeroes = sorted(playedHeroes.keys(), key=lambda x:playedHeroes[x].get('count', 0), reverse=1)

    sortedPlayedMatchesTogetherIndex = sorted(playedMatchesTogether.keys(), key=lambda x:playedMatchesTogether[x].get('count', 0), reverse=1)
    #print('sortedPlayedMatchesTogetherIndex: %s' %sortedPlayedMatchesTogetherIndex)

    i = 0


    for index in sortedPlayedMatchesTogetherIndex:
        if playedMatchesTogether[index]['count'] == 0:
            break
        playerName = getPlayerString(index)


        print('playedMatchesTogether[index]: %s' %playedMatchesTogether[index])

        if (index != playerID):
            intro += intro_sub_template.format(playerName=playerName, amount=playedMatchesTogether[index]['count'])



        pickedHeroes = playedMatchesTogether[index]['hero_picks']
        sortedPickedHeroesIndex = sorted(pickedHeroes.keys(), key=lambda x:pickedHeroes[x], reverse=1)

        heroes = ''
        j = 0
        for index2 in sortedPickedHeroesIndex:


            print('%s %s' %(index2, pickedHeroes[index2]))

            heroes += hero_template.format(amount=pickedHeroes[index2], hero=heroDictionary[index2])

            j = j + 1
            if j == 5:
                break

        body += body_sub_template.format(playerName=playerName, hero_template=heroes)


        i = i + 1
        if i == 8:
            break



    all = intro[:-1] + body + end

    print(all)
    return(all)

def getPlayerString(playerID):
    player_name_template = '**[DB](http://dotabuff.com/players/{playerID} "Dotabuff: Lookup people\'s match history")/[YASP](http://yasp.co/players/{playerID} "Yasp: Provides free replay analysis")**'
    pro_player_name_template = '**[](/{flag})[{name}](/http://www.dotabuff.com/esports/players/{playerID} "team name: {teamName}, sponsor: {sponsor}")**'

    if (playerID in proPlayerDictionary and proPlayerDictionary[playerID].get('is_pro', False) == True):
        return(pro_player_name_template.format(flag=proPlayerDictionary[playerID].get('country_code', 0), name=proPlayerDictionary[playerID].get('name', 'Pro Player!'), playerID=playerID, teamName=proPlayerDictionary[playerID].get('team_name', 'N/A'), sponsor=proPlayerDictionary[playerID].get('sponsor', 'N/A')))
    else:
        return(player_name_template.format(playerID=playerID))
