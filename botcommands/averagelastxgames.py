from steamapi import getmatchhistory, getmatchdetails
from displayreddit.draveragelastxgames import displayResult
import threading
import time
import queue
from reddit.botinfo import message
from steamapi.getheroes import heroDictionary
from misc.idnamedict import gameMode
#message = True


def averageLastXGames(playerID, amount=100, detailedAnalysis=False, heroID=None, gameModeID=None, tournamentGamesOnly=False, getMMR=False):
    matches = getmatchhistory.requestGetMatchHistory(playerID=playerID, amount=amount, heroID=heroID, gameModeID=gameModeID, tournamentGamesOnly=tournamentGamesOnly)


    q = queue.Queue()
    threads = []

    if message: print('[averagelastxgames] Firing all Steam API requests.......')

    detailedMatches = []

    for match in matches:
        t = threading.Thread(target=getmatchdetails.getMatchDetails, args = (match['match_id'],q,))
        t.daemon = True
        t.start()
        time.sleep(0.1)
        threads.append(t)


    if message: print('[averagelastxgames] .... all Steam API requests fired. Joining all threads.......')

    for x in threads:
        x.join()

    if message: print('[averagelastxgames] .... all threads joined.')




    for i in range(q.qsize()):
        #if message: print('[averagelastxgames] put everything into an array')
        detailedMatch = q.get()
        detailedMatches.append(detailedMatch)
        if (int(q.qsize()) == 0):
            break


    if(len(detailedMatches) != len(matches)):
        print('[averagelastxgames] @@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print('[averagelastxgames] SOMETHING WENT HORRIBLY WRONG')
        print('[averagelastxgames] @@@@@@@@@@@@@@@@@@@@@@@@@@@@@')




    analysis = analyzeMatches(playerID, detailedMatches)

    reply = displayResult(playerID, analysis, detailedAnalysis, detailedMatches, getMMR=getMMR)

    return reply




def analyzeMatches(playerID, detailedMatches):

    analysis = {'general': {}, 'you': {},
                 'allyTeam': {},  'allySupport': {},  'allyCarry': {},
                'enemyTeam': {}, 'enemySupport': {}, 'enemyCarry': {}}

    analysis['you']['hero_id'] = {}
    analysis['general']['all'] = {}
    analysis['general']['all']['hero_id'] = {}
    analysis['general']['carry'] = {}
    analysis['general']['carry']['hero_id'] = {}
    analysis['general']['support'] = {}
    analysis['general']['support']['hero_id'] = {}

    #for heroID in heroDictionary:
    #for heroID in range(0, 200):
    heroDictionaryWithNoHero = heroDictionary
    heroDictionaryWithNoHero[0] = 'no hero'
    for heroID in heroDictionaryWithNoHero:
        analysis['you']['hero_id'][heroID] = {'count': 0, 'wins': 0}
        analysis['general']['all']['hero_id'][heroID] = {'count': 0, 'wins': 0}
        analysis['general']['carry']['hero_id'][heroID] = {'count': 0, 'wins': 0}
        analysis['general']['support']['hero_id'][heroID] = {'count': 0, 'wins': 0}


    for i in range(0,23):
        analysis['general'][gameMode(i)] = []

    analysis['general']['wins'] = []
    analysis['general']['skipped'] = []

    for detailedMatch in detailedMatches:
        #try:
        if True:
            if ('result' in detailedMatch and not 'error' in detailedMatch['result']):



                game_mode = gameMode(detailedMatch['result']['game_mode'])


                #analysis['general'][game_mode]           = analysis['general'].get(game_mode,           0) + 1
                analysis['general'][game_mode].append(detailedMatch['result']['match_id'])




                analysis['general']['first_blood_time']  = analysis['general'].get('first_blood_time',  0) + detailedMatch['result']['first_blood_time']
                analysis['general']['duration']          = analysis['general'].get('duration',          0) + detailedMatch['result']['duration']


                #find if you in radiant or dire team
                #find player with highest/lowest lasthit in each team

                radiantSupport = {'last_hits':5000}
                radiantCarry = {'last_hits':0}
                direSupport = {'last_hits':5000}
                direCarry = {'last_hits':0}

                lstA = amountOfTowersDestroyed(detailedMatch['result']['tower_status_radiant'])
                lstB = amountOfBarracksDestroyed(detailedMatch['result']['barracks_status_radiant'])
                radiantTeam = { k: lstA.get(k, 0) + lstB.get(k, 0) for k in set(lstA) | set(lstB) }

                lstA = amountOfTowersDestroyed(detailedMatch['result']['tower_status_dire'])
                lstB = amountOfBarracksDestroyed(detailedMatch['result']['barracks_status_dire'])
                direTeam = { k: lstA.get(k, 0) + lstB.get(k, 0) for k in set(lstA) | set(lstB) }

                carry = [-1, -1]
                support = [-1, -1]


                for player in detailedMatch['result']['players']:

                    if(player['player_slot'] < 127):

                        radiantTeam = addStatsTogether(radiantTeam, player, True)

                        if(player['last_hits'] < radiantSupport['last_hits']):
                            radiantSupport = addStatsTogether(radiantSupport, player, False)
                            support[0] = player['player_slot']

                        if(player['last_hits'] > radiantCarry['last_hits']):
                            radiantCarry = addStatsTogether(radiantCarry, player, False)
                            carry[0] = player['player_slot']

                    else:

                        direTeam = addStatsTogether(direTeam, player, True)

                        if(player['last_hits'] < direSupport['last_hits']):
                            direSupport = addStatsTogether(direSupport, player, False)
                            support[1] = player['player_slot']

                        if(player['last_hits'] > direCarry['last_hits']):
                            direCarry = addStatsTogether(direCarry, player, False)
                            carry[1] = player['player_slot']

                for player in detailedMatch['result']['players']:

                    analysis['general']['all']['hero_id'][player['hero_id']] = {'count': analysis['general']['all']['hero_id'][player['hero_id']]['count'] + 1,
                                                                         'wins': analysis['general']['all']['hero_id'][player['hero_id']]['wins']}

                    if(player['player_slot'] < 128):
                        if(detailedMatch['result']['radiant_win']):
                            analysis['general']['all']['hero_id'][player['hero_id']] = {'count': analysis['general']['all']['hero_id'][player['hero_id']]['count'],
                                                                                 'wins': analysis['general']['all']['hero_id'][player['hero_id']]['wins'] + 1}
                    else:
                        if(not detailedMatch['result']['radiant_win']):
                            analysis['general']['all']['hero_id'][player['hero_id']] = {'count': analysis['general']['all']['hero_id'][player['hero_id']]['count'],
                                                                                 'wins': analysis['general']['all']['hero_id'][player['hero_id']]['wins'] + 1}


                    for playerslot in support:
                        if(player['player_slot'] == playerslot):
                            analysis['general']['support']['hero_id'][player['hero_id']] = {'count': analysis['general']['support']['hero_id'][player['hero_id']]['count'] + 1,
                                                                         'wins': analysis['general']['support']['hero_id'][player['hero_id']]['wins']}
                            if(player['player_slot'] < 128):
                                if(detailedMatch['result']['radiant_win']):
                                    analysis['general']['support']['hero_id'][player['hero_id']] = {'count': analysis['general']['support']['hero_id'][player['hero_id']]['count'],
                                                                         'wins': analysis['general']['support']['hero_id'][player['hero_id']]['wins'] + 1}
                            else:
                                if(not detailedMatch['result']['radiant_win']):
                                    analysis['general']['support']['hero_id'][player['hero_id']] = {'count': analysis['general']['support']['hero_id'][player['hero_id']]['count'],
                                                                         'wins': analysis['general']['support']['hero_id'][player['hero_id']]['wins'] + 1}

                    for playerslot in carry:
                        if(player['player_slot'] == playerslot):
                            analysis['general']['carry']['hero_id'][player['hero_id']] = {'count': analysis['general']['carry']['hero_id'][player['hero_id']]['count'] + 1,
                                                                         'wins': analysis['general']['carry']['hero_id'][player['hero_id']]['wins']}
                            if(player['player_slot'] < 128):
                                if(detailedMatch['result']['radiant_win']):
                                    analysis['general']['carry']['hero_id'][player['hero_id']] = {'count': analysis['general']['carry']['hero_id'][player['hero_id']]['count'],
                                                                         'wins': analysis['general']['carry']['hero_id'][player['hero_id']]['wins'] + 1}
                            else:
                                if(not detailedMatch['result']['radiant_win']):
                                    analysis['general']['carry']['hero_id'][player['hero_id']] = {'count': analysis['general']['carry']['hero_id'][player['hero_id']]['count'],
                                                                         'wins': analysis['general']['carry']['hero_id'][player['hero_id']]['wins'] + 1}





                    if(player.get('account_id', 0) == playerID):
                        analysis['you'] = addStatsTogether(analysis['you'], player, True)


                        analysis['you']['hero_id'][player['hero_id']] = {'count': analysis['you']['hero_id'][player['hero_id']]['count'] + 1,
                                                                         'wins': analysis['you']['hero_id'][player['hero_id']]['wins']}



                        if(player['player_slot'] < 128):

                            analysis['allyTeam'] = { k: analysis['allyTeam'].get(k, 0) + radiantTeam.get(k, 0) for k in set(analysis['allyTeam']) | set(radiantTeam) }
                            analysis['allySupport'] = { k: analysis['allySupport'].get(k, 0) + radiantSupport.get(k, 0) for k in set(analysis['allySupport']) | set(radiantSupport) }
                            analysis['allyCarry'] = { k: analysis['allyCarry'].get(k, 0) + radiantCarry.get(k, 0) for k in set(analysis['allyCarry']) | set(radiantCarry) }

                            analysis['enemyTeam'] = { k: analysis['enemyTeam'].get(k, 0) + direTeam.get(k, 0) for k in set(analysis['enemyTeam']) | set(direTeam) }
                            analysis['enemySupport'] = { k: analysis['enemySupport'].get(k, 0) + direSupport.get(k, 0) for k in set(analysis['enemySupport']) | set(direSupport) }
                            analysis['enemyCarry'] = { k: analysis['enemyCarry'].get(k, 0) + direCarry.get(k, 0) for k in set(analysis['enemyCarry']) | set(direCarry) }

                            if(detailedMatch['result']['radiant_win']):
                                analysis['general']['wins'].append(detailedMatch['result']['match_id'])

                                analysis['you']['hero_id'][player['hero_id']] = {'count': analysis['you']['hero_id'][player['hero_id']]['count'],
                                                                                   'wins': analysis['you']['hero_id'][player['hero_id']]['wins'] + 1}




                            else:
                                nothing = 5

                        else:
                            analysis['enemyTeam'] = { k: analysis['enemyTeam'].get(k, 0) + radiantTeam.get(k, 0) for k in set(analysis['enemyTeam']) | set(radiantTeam) }
                            analysis['enemySupport'] = { k: analysis['enemySupport'].get(k, 0) + radiantSupport.get(k, 0) for k in set(analysis['enemySupport']) | set(radiantSupport) }
                            analysis['enemyCarry'] = { k: analysis['enemyCarry'].get(k, 0) + radiantCarry.get(k, 0) for k in set(analysis['enemyCarry']) | set(radiantCarry) }

                            analysis['allyTeam'] = { k: analysis['allyTeam'].get(k, 0) + direTeam.get(k, 0) for k in set(analysis['allyTeam']) | set(direTeam) }
                            analysis['allySupport'] = { k: analysis['allySupport'].get(k, 0) + direSupport.get(k, 0) for k in set(analysis['allySupport']) | set(direSupport) }
                            analysis['allyCarry'] = { k: analysis['allyCarry'].get(k, 0) + direCarry.get(k, 0) for k in set(analysis['allyCarry']) | set(direCarry) }

                            if(detailedMatch['result']['radiant_win']):
                                nothing = 5

                            else:
                                analysis['general']['wins'].append(detailedMatch['result']['match_id'])

                                analysis['you']['hero_id'][player['hero_id']] = {'count': analysis['you']['hero_id'][player['hero_id']]['count'],
                                                                                 'wins': analysis['you']['hero_id'][player['hero_id']]['wins'] + 1}







            else:
                print('[averagelastxgames] match skipped, reason: %s' %(detailedMatch))
                #analysis['general']['skipped'] = analysis['general'].get('skipped', 0) + 1


                if('result' in detailedMatch):
                    if('match' in detailedMatch['result']):
                        analysis['general']['skipped'].append(detailedMatch['result']['match_id'])
                    else:
                        analysis['general']['skipped'].append('N/A')
                else:
                    analysis['general']['skipped'].append('N/A')


        #except:
        #    print('[averagelastxgames] @@@@@@@@@@@@@@@@@@@@@@')
        #    print('[averagelastxgames] INVESTIGATE THIS ERROR')
        #    print('[averagelastxgames] @@@@@@@@@@@@@@@@@@@@@@')


    return analysis




def addStatsTogether(storage, player, addTogether):
    keyValues = ['kills', 'deaths', 'assists', 'last_hits', 'denies', 'gold_per_min', 'xp_per_min', 'level',
               'gold', 'gold_spent', 'hero_damage', 'tower_damage', 'hero_healing']

    for keyValue in keyValues:
        if(addTogether):
            storage[keyValue] = storage.get(keyValue, 0) +  player.get(keyValue, 0)

        else:
            #storage[keyValue] = player[keyValue]
            storage[keyValue] = player.get(keyValue, 0)

    if(player.get('leaver_status', 0) != 0 and player.get('leaver_status', 0) != 1):
        if(addTogether):
            storage['leaver_status'] = storage.get('leaver_status', 0) +  1

        else:
            storage['leaver_status'] = 1

    elif(not addTogether):
        storage['leaver_status'] = 0

    return storage


def testBit(int_type, offset):
     mask = 1 << offset
     if((int_type & mask) != 0):
        return True
     else:
         False

def amountOfTowersDestroyed(tower_status):
    mask = 65535
    tower_status = tower_status ^ mask
    tier1 = 0
    tier2 = 0
    tier3 = 0
    tier4 = 0

    if testBit(tower_status, 0): tier1 += 1
    if testBit(tower_status, 3): tier1 += 1
    if testBit(tower_status, 6): tier1 += 1
    if testBit(tower_status, 1): tier2 += 1
    if testBit(tower_status, 4): tier2 += 1
    if testBit(tower_status, 7): tier2 += 1
    if testBit(tower_status, 2): tier3 += 1
    if testBit(tower_status, 5): tier3 += 1
    if testBit(tower_status, 8): tier3 += 1
    if testBit(tower_status, 9): tier4 += 1
    if testBit(tower_status,10): tier4 += 1

    return {'tier1' : tier1, 'tier2' : tier2, 'tier3' : tier3, 'tier4' : tier4}

def amountOfBarracksDestroyed(barracks_status):
    mask = 255
    barracks_status = barracks_status ^ mask
    rangeBarracks = 0
    meleeBarracks = 0
    if testBit(barracks_status, 0): meleeBarracks += 1
    if testBit(barracks_status, 1): rangeBarracks += 1
    if testBit(barracks_status, 2): meleeBarracks += 1
    if testBit(barracks_status, 3): rangeBarracks += 1
    if testBit(barracks_status, 4): meleeBarracks += 1
    if testBit(barracks_status, 5): rangeBarracks += 1

    return {'meleeBarracks': meleeBarracks, 'rangeBarracks': rangeBarracks}


