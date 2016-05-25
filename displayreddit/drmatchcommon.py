def displayResult (playerID, playedMatchesTogether):

    print(playedMatchesTogether)


    #sortedPlayedHeroes = sorted(playedHeroes.keys(), key=lambda x:playedHeroes[x].get('count', 0), reverse=1)

    sortedPlayedMatchesTogetherIndex = sorted(playedMatchesTogether.keys(), key=lambda x:playedMatchesTogether[x].get('count', 0), reverse=1)
    print(sortedPlayedMatchesTogetherIndex)

    i = 0

    for index in sortedPlayedMatchesTogetherIndex:
        if playedMatchesTogether[index]['count'] == 0:
            break


        print(playedMatchesTogether[index])

        pickedHeroes = playedMatchesTogether[index]['hero_picks']
        sortedPickedHeroesIndex = sorted(pickedHeroes.keys(), key=lambda x:pickedHeroes[x], reverse=1)


        j = 0
        for index2 in sortedPickedHeroesIndex:


            print('%s %s' %(index2, pickedHeroes[index2]))

            j = j + 1
            if j == 5:
                break



        i = i + 1
        if i == 8:
            break