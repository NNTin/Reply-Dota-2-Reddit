from steamapi.getheroes import heroDictionary

#from steamapi.getheroes import heroDictionary, requestGetHeroes

def printTableLine(name, source, divider):
    keyValues = ['kills', 'deaths', 'assists', 'last_hits', 'denies', 'gold_per_min', 'xp_per_min', 'hero_damage', 'tower_damage', 'hero_healing']
    #'level', 'gold', 'gold_spent',

    tableLine = '**%s**' %name
    for key in keyValues:
        tableLine = tableLine + ' | ' +  str(round((source[key]/divider), 2))
    tableLine = tableLine + ' | ' + str(source.get('leaver_status', 0))
    #TODO provide match ids of leaver games (fuck this shit)

    return tableLine + '\n'

def printHeroLine(name, playedHeroes):
    sortedPlayedHeroes = sorted(playedHeroes.keys(), key=lambda x:playedHeroes[x].get('count', 0), reverse=1)
    i = 0

    resultHeroes = name + ' | '

    for heroID in sortedPlayedHeroes:
        if (playedHeroes[heroID]['count'] == 0):
            break

        heroValues = (playedHeroes[heroID]['count'],heroDictionary[heroID],playedHeroes[heroID]['wins'],playedHeroes[heroID]['count'] - playedHeroes[heroID]['wins'], round(100 * playedHeroes[heroID]['wins'] / playedHeroes[heroID]['count'],2))
        resultHeroes = resultHeroes + '%sx[](/hero-%s "%s wins, %s losses (%s' %heroValues + '%' + ')") '

        i = i + 1
        if (i == 8):
            break
    resultHeroes = resultHeroes + '\n'

    return resultHeroes

def displayResult(playerID, analysis, detailedAnalysis, detailedMatches):

    durationM, durationS = divmod((analysis['general']['duration'])/len(detailedMatches), 60)
    fbM, fbS = divmod((analysis['general']['first_blood_time'])/len(detailedMatches), 60)
    towersDestroyed = (analysis['enemyTeam']['tier1'] + analysis['enemyTeam']['tier2'] + analysis['enemyTeam']['tier3'] + analysis['enemyTeam']['tier4'] \
                    + analysis['allyTeam']['tier1']  + analysis['allyTeam']['tier2']  + analysis['allyTeam']['tier3']  + analysis['allyTeam']['tier4'])/len(detailedMatches)
    barracksDestroyed = (analysis['enemyTeam']['meleeBarracks'] + analysis['enemyTeam']['rangeBarracks'] \
                         + analysis['allyTeam']['meleeBarracks'] +analysis['allyTeam']['rangeBarracks'])/len(detailedMatches)

    numbers = (durationM,durationS,fbM,fbS,round(towersDestroyed,2),round(barracksDestroyed,2))

    averageInformation = 'Average match duration: %02d:%02d, average first blood time: %02d:%02d, average towers destroyed: %s, average barracks destroyed: %s' %numbers



    playedModes = {}
    for i in range(0, 24):
        if (len(analysis['general'][gameMode(i)]) != 0):

            print(analysis['general'][gameMode(i)])


            playedModes[gameMode(i)] = len(analysis['general'][gameMode(i)])

    sortedModes = sorted(playedModes.keys(), key=lambda x:playedModes[x], reverse=1)

    print(analysis['general'])
    print(playedModes)
    print(sortedModes)

    modeString = ''
    for mode in sortedModes:
        modeString = modeString + ', [%s %s](/a "' %(playedModes[mode], mode)
        for matchid in analysis['general'][mode]:
                modeString = modeString + '%s ' %matchid
        modeString = modeString + '")'

    intro = 'Analyzed a total of %s matches. (%s wins' %(len(detailedMatches), len(analysis['general']['wins']))
    intro = intro + modeString
    intro = intro + ')  \n[Hover over links to display more information.](/a "%s")\n\n' %averageInformation


    resultTable = 'average | kills | deaths | assists | last hits | denies | gpm | xpm | hero damage | tower damage | hero healing | leaver count (total)\n'
    resultTable = resultTable + '-------|-----|------|-------|---------|------|---|---|-----------|------------|------------|--------------------\n'
    youDescription = '[DB](http://dotabuff.com/players/%s "Dotabuff: Lookup people\'s match history")/[YASP](http://yasp.co/players/%s "Yasp: Provides free replay analysis")' %(playerID, playerID)
    resultTable = resultTable + printTableLine(youDescription, analysis['you'], len(detailedMatches))


    destroyedBuildings = (analysis['enemyTeam']['tier1'], analysis['enemyTeam']['tier2'], analysis['enemyTeam']['tier3'], analysis['enemyTeam']['tier4'], analysis['enemyTeam']['rangeBarracks'], analysis['enemyTeam']['meleeBarracks'])
    allyTeamDescription = '[ally team](/a "Ally team destroyed %s tier 1 towers, %s tier 2 towers, %s tier 3 towers, %s tier 4 towers, %s ranged barracks and %s melee barracks")' %destroyedBuildings

    resultTable = resultTable + printTableLine(allyTeamDescription, analysis['allyTeam'], len(detailedMatches)*5)

    destroyedBuildings = (analysis['allyTeam']['tier1'], analysis['allyTeam']['tier2'], analysis['allyTeam']['tier3'], analysis['allyTeam']['tier4'], analysis['allyTeam']['rangeBarracks'], analysis['allyTeam']['meleeBarracks'])
    enemyTeamDescription = '[enemy team](/a "Enemy team destroyed %s tier 1 towers, %s tier 2 towers, %s tier 3 towers, %s tier 4 towers, %s ranged barracks and %s melee barracks")' %destroyedBuildings

    resultTable = resultTable + printTableLine(enemyTeamDescription, analysis['enemyTeam'], len(detailedMatches)*5)
    if(detailedAnalysis):
        resultTable = resultTable + printTableLine('ally support', analysis['allySupport'], len(detailedMatches))
        resultTable = resultTable + printTableLine('enemy support', analysis['enemySupport'], len(detailedMatches))
        resultTable = resultTable + printTableLine('ally carry', analysis['allyCarry'], len(detailedMatches))
        resultTable = resultTable + printTableLine('enemy carry', analysis['enemyCarry'], len(detailedMatches))

    resultHeroes =''
    if(detailedAnalysis):
        resultHeroes = '\n | played heroes (hover hero icons to display wins and losses)\n---|---\n'
    else:
        resultHeroes = '\n\n'

    youDescription = '[DB](http://dotabuff.com/players/%s "Dotabuff: Lookup people\'s match history")/[YASP](http://yasp.co/players/%s "Yasp: Provides free replay analysis")' %(playerID, playerID)
    allDescription = '[all](/a "lists all picked heroes")'
    supportDescription = '[support](/a "determined by lowest amount of lasthits")'
    carryDescription = '[carry](/a "determined by highest amount of lasthits")'

    resultHeroes = resultHeroes + printHeroLine(youDescription, analysis['you']['hero_id'])
    if(detailedAnalysis):
        resultHeroes = resultHeroes + printHeroLine(allDescription, analysis['general']['all']['hero_id'])
        resultHeroes = resultHeroes + printHeroLine(supportDescription, analysis['general']['support']['hero_id'])
        resultHeroes = resultHeroes + printHeroLine(carryDescription, analysis['general']['carry']['hero_id'])



    return intro + resultTable + resultHeroes

def gameMode(gameModeID):
    return {
        0 : 'Unknown',
        1 : 'All Pick',
        2 : 'Captains Mode',
        3 : 'Random Draft',
        4 : 'Single Draft',
        5 : 'All Random',
        6 : '?? INTRO/DEATH ??',
        7 : 'The Diretide',
        8 : 'Reverse Captains Mode',
        9 : 'Greeviling',
        10 : 'Tutorial',
        11 : 'Mid Only',
        12 : 'Least Played',
        13 : 'New Player Pool',
        14 : 'Compendium Matchmaking',
        15 : 'Custom',
        16 : 'Captains Draft',
        17 : 'Balanced Draft',
        18 : 'Ability Draft',
        19 : '?? Event ??',
        20 : 'All Random Death Match',
        21 : '1vs1 Solo Mid',
        22 : 'Ranked All Pick',
        23 : 'skipped',
    }.get(gameModeID, 'Unkown')

