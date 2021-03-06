from steamapi.getheroes import heroDictionary
from steamapi.getproplayerlist import proPlayerDictionary
from misc.idnamedict import gameMode
from converter import playerconverter

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

    resultHeroes = str(name) + ' | '

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

def displayResult(playerID, analysis, detailedAnalysis, detailedMatches, getMMR=True):
    youDescription = playerconverter.playerConverter(playerID)
    MMR = None
    if getMMR:
        MMR = playerconverter.getMMR(playerID)

    matchesPlayed = len(detailedMatches) - len(analysis['general']['skipped'])

    durationM, durationS = divmod((analysis['general']['duration'])/matchesPlayed, 60)
    fbM, fbS = divmod((analysis['general']['first_blood_time'])/matchesPlayed, 60)
    towersDestroyed = (analysis['enemyTeam']['tier1'] + analysis['enemyTeam']['tier2'] + analysis['enemyTeam']['tier3'] + analysis['enemyTeam']['tier4'] \
                    + analysis['allyTeam']['tier1']  + analysis['allyTeam']['tier2']  + analysis['allyTeam']['tier3']  + analysis['allyTeam']['tier4'])/matchesPlayed
    barracksDestroyed = (analysis['enemyTeam']['meleeBarracks'] + analysis['enemyTeam']['rangeBarracks'] \
                         + analysis['allyTeam']['meleeBarracks'] +analysis['allyTeam']['rangeBarracks'])/matchesPlayed

    numbers = (durationM,durationS,fbM,fbS,round(towersDestroyed,2),round(barracksDestroyed,2))

    averageInformation = 'Average match duration: %02d:%02d, average first blood time: %02d:%02d, average towers destroyed: %s, average barracks destroyed: %s' %numbers



    playedModes = {}
    for i in range(0, 23):
    #for i in range(-1, 23):
        if (len(analysis['general'][gameMode(i)]) != 0):

            playedModes[gameMode(i)] = len(analysis['general'][gameMode(i)])


    sortedModes = sorted(playedModes.keys(), key=lambda x:playedModes[x], reverse=1)

    modeString = ''

    for mode in sortedModes:
        modeString = modeString + ', %s %s' %(playedModes[mode], mode)

    skippedMessage = ''
    if(len(analysis['general']['skipped']) != 0):
        skippedMessage = ' (%s skipped)' %len(analysis['general']['skipped'])

    intro = '####&#009;\n#####&#009; Hover to view player analysis %s\n######&#009;\n\n' %youDescription
    if MMR != None:
        MMRText = ''
        for key in MMR.keys():
            MMRText = MMRText + '%s MMR **%s**, ' %(key, MMR[key])
        MMRText = MMRText[:-2]
        intro = intro + 'Player MMR (powered by OpenDota): %s.   \n' %MMRText
    intro = intro + 'Analyzed a total of %s matches%s. (%s wins' %(len(detailedMatches), skippedMessage, len(analysis['general']['wins']))
    intro = intro + modeString
    intro = intro + ') '
    intro = intro + '  \n[Hover over links to display more information.](#a "%s")\n\n' %averageInformation



    resultTable = 'average | kills | deaths | assists | last hits | denies | gpm | xpm | hero damage | tower damage | hero healing | leaver count (total)\n'
    resultTable = resultTable + '-------|-----|------|-------|---------|------|---|---|-----------|------------|------------|--------------------\n'
    resultTable = resultTable + printTableLine(youDescription, analysis['you'], matchesPlayed)


    destroyedBuildings = (analysis['enemyTeam']['tier1'], analysis['enemyTeam']['tier2'], analysis['enemyTeam']['tier3'], analysis['enemyTeam']['tier4'], analysis['enemyTeam']['rangeBarracks'], analysis['enemyTeam']['meleeBarracks'])
    allyTeamDescription = '[ally team](#a "Ally team destroyed %s tier 1 towers, %s tier 2 towers, %s tier 3 towers, %s tier 4 towers, %s ranged barracks and %s melee barracks")' %destroyedBuildings

    resultTable = resultTable + printTableLine(allyTeamDescription, analysis['allyTeam'], matchesPlayed*5)

    destroyedBuildings = (analysis['allyTeam']['tier1'], analysis['allyTeam']['tier2'], analysis['allyTeam']['tier3'], analysis['allyTeam']['tier4'], analysis['allyTeam']['rangeBarracks'], analysis['allyTeam']['meleeBarracks'])
    enemyTeamDescription = '[enemy team](#a "Enemy team destroyed %s tier 1 towers, %s tier 2 towers, %s tier 3 towers, %s tier 4 towers, %s ranged barracks and %s melee barracks")' %destroyedBuildings

    resultTable = resultTable + printTableLine(enemyTeamDescription, analysis['enemyTeam'], matchesPlayed*5)
    if(detailedAnalysis):
        resultTable = resultTable + printTableLine('ally support', analysis['allySupport'], matchesPlayed)
        resultTable = resultTable + printTableLine('enemy support', analysis['enemySupport'], matchesPlayed)
        resultTable = resultTable + printTableLine('ally carry', analysis['allyCarry'], matchesPlayed)
        resultTable = resultTable + printTableLine('enemy carry', analysis['enemyCarry'], matchesPlayed)

    resultHeroes =''
    if(detailedAnalysis):
        resultHeroes = '\n | played heroes (hover hero icons to display wins and losses)\n---|---\n'
    else:
        resultHeroes = '\n\n'

    allDescription = '[all](/a "lists all picked heroes")'
    supportDescription = '[support](/a "determined by lowest amount of lasthits")'
    carryDescription = '[carry](/a "determined by highest amount of lasthits")'

    resultHeroes = resultHeroes + printHeroLine(youDescription, analysis['you']['hero_id'])
    if(detailedAnalysis):
        resultHeroes = resultHeroes + printHeroLine(allDescription, analysis['general']['all']['hero_id'])
        resultHeroes = resultHeroes + printHeroLine(supportDescription, analysis['general']['support']['hero_id'])
        resultHeroes = resultHeroes + printHeroLine(carryDescription, analysis['general']['carry']['hero_id'])

    resultEnd = '\n\n---\n\n'

    return intro + resultTable + resultHeroes + resultEnd


