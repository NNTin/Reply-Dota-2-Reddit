import traceback
import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
import sqlite3
import OAuth2Util
import requests
import re
import queue
import threading

from steamapi.steamapikey import SteamAPIKey
APIKey = SteamAPIKey


#My old bot that has been running for over 4 months.
#New bot is planned to be running in April with source open sourced on github
#This is a single py file. You have to create your own oauth.ini file (google praw oauth2util)
#oauth.ini is used to log into reddit.


'''USER CONFIGURATION'''

USERAGENT = "/u/lumbdi analyze Dota 2 matches v0.1"
# This is a short description of what the bot does.
# For example "Python automatic replybot v2.0 (by /u/GoldenSights)"
SUBREDDIT = "AnalyzeLast100Games+Dota2+LearnDota2"
# This is the sub or list of subs to scan for new posts. For a single sub, use "sub1". For multiple subreddits, use "sub1+sub2+sub3+..."
KEYWORDS = ["dotabuff.com/players/", "yasp.co/players/", "!matchCommon"]
# These are the words you are looking for
KEYAUTHORS = []
# These are the names of the authors you are looking for
# The bot will only reply to authors on this list
# Keep it empty to allow anybody.
IGNOREAUTHORS = ["dotamatch", "hamstergulasch"]
# Ignore these authors
REPLYSTRING = "blubb."
# This is the word you want to put in reply
MAXPOSTS = 100
# This is how many posts you want to retrieve all at once. PRAW can download 100 at a time.
WAIT = 30

CLEANCYCLES = 10
# After this many cycles, the bot will clean its database
# Keeping only the latest (2*MAXPOSTS) items

playedHeroes = {}
q = queue.Queue()
q2 = queue.Queue()
#global variable

r = praw.Reddit(USERAGENT)


def displayResult(resultDictionary, matchHistoryJSON, heroDictionary, playerID):

    displayDictionary = {}

    # @@@@@@@@@@@@@@@@@@@@@ T E A M
    displayDictionary['teamKills'] = round(float(resultDictionary['teamKills'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['teamDeaths'] = round(float(resultDictionary['teamDeaths'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['teamAssists'] = round(float(resultDictionary['teamAssists'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)

    displayDictionary['teamLastHits'] = round(float(resultDictionary['teamLastHits'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['teamDenies'] = round(float(resultDictionary['teamDenies'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['teamGpm'] = round(float(resultDictionary['teamGpm'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['teamXpm'] = round(float(resultDictionary['teamXpm'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['teamHeroDamage'] = round(float(resultDictionary['teamHeroDamage'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['teamTowerDamage'] = round(float(resultDictionary['teamTowerDamage'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['teamHeroHealing'] = round(float(resultDictionary['teamHeroHealing'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)

    displayDictionary['teamLeaverCount'] = resultDictionary['teamLeaverCount']

    # @@@@@@@@@@@@@@@@@@@@@ E N E M Y
    displayDictionary['enemyKills'] = round(float(resultDictionary['enemyKills'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['enemyDeaths'] = round(float(resultDictionary['enemyDeaths'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['enemyAssists'] = round(float(resultDictionary['enemyAssists'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)

    displayDictionary['enemyLastHits'] = round(float(resultDictionary['enemyLastHits'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['enemyDenies'] = round(float(resultDictionary['enemyDenies'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['enemyGpm'] = round(float(resultDictionary['enemyGpm'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['enemyXpm'] = round(float(resultDictionary['enemyXpm'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['enemyHeroDamage'] = round(float(resultDictionary['enemyHeroDamage'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['enemyTowerDamage'] = round(float(resultDictionary['enemyTowerDamage'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['enemyHeroHealing'] = round(float(resultDictionary['enemyHeroHealing'] / float(5 * (resultDictionary['total'] - resultDictionary['skipped']))), 2)

    displayDictionary['enemyLeaverCount'] = resultDictionary['enemyLeaverCount']

    # @@@@@@@@@@@@@@@@@@@@@ Y O U
    displayDictionary['kills'] = round(float(resultDictionary['kills'] / float((resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['deaths'] = round(float(resultDictionary['deaths'] / float((resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['assists'] = round(float(resultDictionary['assists'] / float((resultDictionary['total'] - resultDictionary['skipped']))), 2)

    displayDictionary['lastHits'] = round(float(resultDictionary['lastHits'] / float((resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['denies'] = round(float(resultDictionary['denies'] / float((resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['gpm'] = round(float(resultDictionary['gpm'] / float((resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['xpm'] = round(float(resultDictionary['xpm'] / float((resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['heroDamage'] = round(float(resultDictionary['heroDamage'] / float((resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['towerDamage'] = round(float(resultDictionary['towerDamage'] / float((resultDictionary['total'] - resultDictionary['skipped']))), 2)
    displayDictionary['heroHealing'] = round(float(resultDictionary['heroHealing'] / float((resultDictionary['total'] - resultDictionary['skipped']))), 2)

    displayDictionary['leaverCount'] = resultDictionary['leaverCount']


    resultIntro = "Analyzed a total of " + str(resultDictionary['total']) + " matches. (" + str(resultDictionary['wins']) + " wins; "
    resultIntro = resultIntro + str(resultDictionary['all pick']) + " all pick, " + str(resultDictionary['ranked all pick'])
    resultIntro = resultIntro + " ranked all pick, " + str(resultDictionary['single draft']) + " single draft, " + str(resultDictionary['unspecified']) + " other and " + str(resultDictionary['skipped']) + " skipped.)  \n"
    resultIntro = resultIntro + "This bot attempts to analyze your last 100 games and averages out the stats.\n\n"


    resultTable = "average | kills | deaths | assists | last hits | denies | gpm | xpm | hero damage | tower damage | hero healing | leaver count (total)\n"
    resultTable = resultTable + "-------|-----|------|-------|---------|------|---|---|-----------|------------|------------|--------------------\n"

    stringYou = "**[DB](http://www.dotabuff.com/players/" + str(playerID) + ")/[YASP](http://yasp.co/players/" + str(playerID) + ")**"

    resultTable = resultTable + stringYou + " | " + str(displayDictionary['kills']) + " | " + str(displayDictionary['deaths']) + " | " + str(displayDictionary['assists'])
    resultTable = resultTable + " | " + str(displayDictionary['lastHits']) + " | " + str(displayDictionary['denies']) + " | " + str(displayDictionary['gpm'])
    resultTable = resultTable + " | " + str(displayDictionary['xpm']) + " | " + str(displayDictionary['heroDamage']) + " | " + str(displayDictionary['towerDamage'])
    resultTable = resultTable + " | " + str(displayDictionary['heroHealing']) + " | " + str(displayDictionary['leaverCount']) + "\n"


    resultTable = resultTable + "**ally team** | " + str(displayDictionary['teamKills']) + " | " + str(displayDictionary['teamDeaths']) + " | " + str(displayDictionary['teamAssists'])
    resultTable = resultTable + " | " + str(displayDictionary['teamLastHits']) + " | " + str(displayDictionary['teamDenies']) + " | " + str(displayDictionary['teamGpm'])
    resultTable = resultTable + " | " + str(displayDictionary['teamXpm']) + " | " + str(displayDictionary['teamHeroDamage']) + " | " + str(displayDictionary['teamTowerDamage'])
    resultTable = resultTable + " | " + str(displayDictionary['teamHeroHealing']) + " | " + str(displayDictionary['teamLeaverCount']) + "\n"

    resultTable = resultTable + "**enemy team** | "  + str(displayDictionary['enemyKills']) + " | " + str(displayDictionary['enemyDeaths']) + " | " + str(displayDictionary['enemyAssists'])
    resultTable = resultTable + " | " + str(displayDictionary['enemyLastHits']) + " | " + str(displayDictionary['enemyDenies']) + " | " + str(displayDictionary['enemyGpm'])
    resultTable = resultTable + " | " + str(displayDictionary['enemyXpm']) + " | " + str(displayDictionary['enemyHeroDamage']) + " | " + str(displayDictionary['enemyTowerDamage'])
    resultTable = resultTable + " | " + str(displayDictionary['enemyHeroHealing']) + " | " + str(displayDictionary['enemyLeaverCount']) + "\n\n"

    global playedHeroes

    sortedPlayedHeroes = sorted(playedHeroes.keys(), key=lambda x:playedHeroes[x], reverse=1)


    i = 0
    resultHeroes = ""

    for heroID in sortedPlayedHeroes:
        #print playedHeroes[heroID] + " x",
        if (heroID == 0):
            break
        resultHeroes = resultHeroes + str(playedHeroes[heroID]) + "x[](/hero-" + heroDictionary[heroID] +  ") "
        i = i + 1
        if (i == 10):
            break



    #resultEnd = "\n\n---------------\n\n[^^Message ^^lumbdi](https://www.reddit.com/message/compose/?to=lumbdi)^^, ^^drop ^^suggestions ^^over ^^at ^^/r/AnalyzeLast100Games"
    resultEnd = "\n\n---------------\n\n[^^Message ^^lumbdi](https://www.reddit.com/message/compose/?to=lumbdi)^^, ^^drop ^^suggestions ^^over ^^at ^^/r/AnalyzeLast100Games"


    return resultIntro + resultTable + resultHeroes + resultEnd

queueAnalyze = queue.Queue()

def requestGetMatchHistory2(APIKey, accountID, matchID):
    URL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key=" + APIKey + "&account_id=" + str(accountID) + "&start_at_match_id=" + str(matchID)
    #https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key=F79627788CAF92984B8B0E77FB29E9B8&account_id=114560539&start_at_match_id=1195510042
    response = requests.get(URL)
    response = response.json()

    return response

def diff(list1, list2):
    c = set(list1).union(set(list2))
    d = set(list1).intersection(set(list2))
    return list(c - d)


def matchCommon(player1ID, player2ID):

    player1Matches = []
    player2Matches = []
    player1MatchesLast100 = []
    player2MatchesLast100 = []
    player1StartingMatchID = ""
    player2StartingMatchID = ""


    moreMatches = True
    firstRun = True
    while moreMatches:
        matchHistoryJson = requestGetMatchHistory2(APIKey, player1ID, player1StartingMatchID)
        for match in matchHistoryJson['result']['matches']:
            player1Matches.append(match['match_id'])
            player1StartingMatchID = match['match_id']
            if (firstRun):
                player1MatchesLast100.append(match['match_id'])
            #print(match['match_id'])
        if (len(matchHistoryJson['result']['matches']) == 1):
            moreMatches = False
        firstRun = False

    moreMatches = True
    firstRun = True
    while moreMatches:
        matchHistoryJson = requestGetMatchHistory2(APIKey, player2ID, player2StartingMatchID)
        for match in matchHistoryJson['result']['matches']:
            player2Matches.append(match['match_id'])
            player2StartingMatchID = match['match_id']
            if (firstRun):
                player2MatchesLast100.append(match['match_id'])
            #print(match['match_id'])
        if (len(matchHistoryJson['result']['matches']) == 1):
            moreMatches = False
        firstRun = False

    #print(player1Matches)
    #print(player2Matches)
    #print(player1MatchesLast100)
    #print(player2MatchesLast100)

    commonMatches = set(player1Matches).intersection(player2Matches)
    commonMatchesLast100 = set(player1MatchesLast100).intersection(player2MatchesLast100)

    commonMatchesWithoutLast100 = diff(commonMatches, commonMatchesLast100)

    #print("\n\n")
    #print(commonMatchesLast100)
    #print(commonMatchesWithoutLast100)

    resultIntro = "Interpreted command: !matchCommon " + str(player1ID) + "+" + str(player2ID) + "\n\n"

    resultBody = "They have played together in: "
    for match in commonMatchesLast100:
        resultBody = resultBody + "**[" + str(match) + "](http://www.dotabuff.com/matches/" + str(match) + " \"bold = recentish games\")** "
    for match in commonMatchesWithoutLast100:
        resultBody = resultBody + "[" + str(match) + "](http://www.dotabuff.com/matches/" + str(match) + ") "


    if (not commonMatchesLast100):
        if (not commonMatchesWithoutLast100):
            resultBody = "No matches found."

    #http://www.dotabuff.com/matches/1830444596

    resultEnd = "\n\n---------------\n\n[^^Message ^^lumbdi](https://www.reddit.com/message/compose/?to=lumbdi)^^, ^^drop ^^suggestions ^^over ^^at ^^/r/AnalyzeLast100Games"

    return(resultIntro + resultBody + resultEnd)


def analyzeMatch(queueAnalyze, APIKey, matchID, playerID):
    try:
        URL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key=" + APIKey + "&match_id=" + str(matchID)
        response = requests.get(URL)
        response = response.json()

        partialResultDictionary = {'all pick': 0, 'ranked all pick': 0, 'single draft': 0, 'unspecified': 0,
                                   'teamKills': 0, 'teamDeaths': 0, 'teamAssists': 0,
                                   'enemyKills': 0, 'enemyDeaths': 0, 'enemyAssists':0,
                                   'kills': 0, 'deaths': 0, 'assists': 0, 'wins': 0, 'total': 0,
                                   'lastHits': 0, 'denies': 0, 'gpm':0, 'xpm':0, 'heroDamage':0,
                                   'towerDamage':0, 'heroHealing':0, 'leaverCount':0,
                                   'teamLastHits': 0, 'teamDenies': 0, 'teamGpm':0, 'teamXpm':0, 'teamHeroDamage':0,
                                   'teamTowerDamage':0, 'teamHeroHealing':0, 'teamLeaverCount':0,
                                   'enemyLastHits': 0, 'enemyDenies': 0, 'enemyGpm':0, 'enemyXpm':0,
                                   'enemyHeroDamage':0, 'enemyTowerDamage':0, 'enemyHeroHealing':0,
                                   'enemyLeaverCount':0, 'skipped': 0}

        if (response['result']['game_mode'] == 1):
            partialResultDictionary['all pick'] = partialResultDictionary['all pick'] + 1
        elif (response['result']['game_mode'] == 4):
            partialResultDictionary['single draft'] = partialResultDictionary['single draft'] + 1
        elif (response['result']['game_mode'] == 22):
            partialResultDictionary['ranked all pick'] = partialResultDictionary['ranked all pick'] + 1
        else:
            partialResultDictionary['unspecified'] = partialResultDictionary['unspecified'] + 1

        #find out who you are and in which team you belong in
        i = 0
        slot = 0
        global playedHeroes
        for player in response['result']['players']:
            #print(player['account_id'])
            if (player['account_id']==int(playerID)):
                #print i
                slot = i
                partialResultDictionary['kills'] = player['kills']
                partialResultDictionary['deaths'] = player['deaths']
                partialResultDictionary['assists'] = player['assists']
                partialResultDictionary['lastHits'] = player['last_hits']
                partialResultDictionary['denies'] = player['denies']
                partialResultDictionary['gpm'] = player['gold_per_min']
                partialResultDictionary['xpm'] = player['xp_per_min']
                partialResultDictionary['heroDamage'] = player['hero_damage']
                partialResultDictionary['towerDamage'] = player['tower_damage']
                partialResultDictionary['heroHealing'] = player['hero_healing']
                if 'leaver_status' in player:
                    if (str(player['leaver_status']) !=  str(0)):
                        if (str(player['leaver_status']) != str(1)):
                            partialResultDictionary['leaverCount'] = 1
                else:
                    partialResultDictionary['leaver_status'] = 0
                playedHeroes[player['hero_id']] = playedHeroes.get(player['hero_id'], 0) + 1
                break
            i = i + 1;



        #def get():
        #    foo = {}
        #    for bar in RANDLIST:
        #        foo[bar] = foo.get(bar, 0) + 1



        #print "test" + str(i)

        length = int(len(response['result']['players']))

        if (slot <= 4):
            for x in range(0,int(length/2)):
                partialResultDictionary['teamKills'] = partialResultDictionary['teamKills'] + response['result']['players'][x]['kills']
                partialResultDictionary['teamAssists'] = partialResultDictionary['teamAssists'] + response['result']['players'][x]['assists']
                partialResultDictionary['teamDeaths'] = partialResultDictionary['teamDeaths'] + response['result']['players'][x]['deaths']

                partialResultDictionary['teamLastHits'] = partialResultDictionary['teamLastHits'] + response['result']['players'][x]['last_hits']
                partialResultDictionary['teamDenies'] = partialResultDictionary['teamDenies'] + response['result']['players'][x]['denies']
                partialResultDictionary['teamGpm'] = partialResultDictionary['teamGpm'] + response['result']['players'][x]['gold_per_min']
                partialResultDictionary['teamXpm'] = partialResultDictionary['teamXpm'] + response['result']['players'][x]['xp_per_min']
                partialResultDictionary['teamHeroDamage'] = partialResultDictionary['teamHeroDamage'] + response['result']['players'][x]['hero_damage']
                partialResultDictionary['teamTowerDamage'] = partialResultDictionary['teamTowerDamage'] + response['result']['players'][x]['tower_damage']
                partialResultDictionary['teamHeroHealing'] = partialResultDictionary['teamHeroHealing'] + response['result']['players'][x]['hero_healing']
                if 'leaver_status' in response['result']['players'][x]:
                    if (str(response['result']['players'][x]['leaver_status']) != str(0)):
                        if (str(response['result']['players'][x]['leaver_status']) != str(1)):
                            partialResultDictionary['teamLeaverCount'] = 1
                else:
                    partialResultDictionary['teamLeaverCount'] = 0

            for x in range(int(length/2),length):
                partialResultDictionary['enemyKills'] = partialResultDictionary['enemyKills'] + response['result']['players'][x]['kills']
                partialResultDictionary['enemyAssists'] = partialResultDictionary['enemyAssists'] + response['result']['players'][x]['assists']
                partialResultDictionary['enemyDeaths'] = partialResultDictionary['enemyDeaths'] + response['result']['players'][x]['deaths']

                partialResultDictionary['enemyLastHits'] = partialResultDictionary['enemyLastHits'] + response['result']['players'][x]['last_hits']
                partialResultDictionary['enemyDenies'] = partialResultDictionary['enemyDenies'] + response['result']['players'][x]['denies']
                partialResultDictionary['enemyGpm'] = partialResultDictionary['enemyGpm'] + response['result']['players'][x]['gold_per_min']
                partialResultDictionary['enemyXpm'] = partialResultDictionary['enemyXpm'] + response['result']['players'][x]['xp_per_min']
                partialResultDictionary['enemyHeroDamage'] = partialResultDictionary['enemyHeroDamage'] + response['result']['players'][x]['hero_damage']
                partialResultDictionary['enemyTowerDamage'] = partialResultDictionary['enemyTowerDamage'] + response['result']['players'][x]['tower_damage']
                partialResultDictionary['enemyHeroHealing'] = partialResultDictionary['enemyHeroHealing'] + response['result']['players'][x]['hero_healing']
                if 'leaver_status' in response['result']['players'][x]:
                    if (str(response['result']['players'][x]['leaver_status']) != str(0)):
                        if (str(response['result']['players'][x]['leaver_status']) != str(1)):
                            partialResultDictionary['enemyLeaverCount'] = 1
                else:
                    partialResultDictionary['enemyLeaverCount'] = 0

            if(response['result']['radiant_win']):
                #print "Radiant won & player was in Radiant"
                partialResultDictionary['wins'] = partialResultDictionary['wins'] + 1
            #else:
                #print response['result']['radiant_win']


        else:
            for x in range(0,int(length/2)):


                partialResultDictionary['enemyKills'] = partialResultDictionary['enemyKills'] + response['result']['players'][x]['kills']
                partialResultDictionary['enemyAssists'] = partialResultDictionary['enemyAssists'] + response['result']['players'][x]['assists']
                partialResultDictionary['enemyDeaths'] = partialResultDictionary['enemyDeaths'] + response['result']['players'][x]['deaths']

                partialResultDictionary['enemyLastHits'] = partialResultDictionary['enemyLastHits'] + response['result']['players'][x]['last_hits']
                partialResultDictionary['enemyDenies'] = partialResultDictionary['enemyDenies'] + response['result']['players'][x]['denies']
                partialResultDictionary['enemyGpm'] = partialResultDictionary['enemyGpm'] + response['result']['players'][x]['gold_per_min']
                partialResultDictionary['enemyXpm'] = partialResultDictionary['enemyXpm'] + response['result']['players'][x]['xp_per_min']
                partialResultDictionary['enemyHeroDamage'] = partialResultDictionary['enemyHeroDamage'] + response['result']['players'][x]['hero_damage']
                partialResultDictionary['enemyTowerDamage'] = partialResultDictionary['enemyTowerDamage'] + response['result']['players'][x]['tower_damage']
                partialResultDictionary['enemyHeroHealing'] = partialResultDictionary['enemyHeroHealing'] + response['result']['players'][x]['hero_healing']
                if 'leaver_status' in response['result']['players'][x]:
                    if (str(response['result']['players'][x]['leaver_status']) != str(0)):
                        if (str(response['result']['players'][x]['leaver_status']) != str(1)):
                            partialResultDictionary['enemyLeaverCount'] = 1
                else:
                    partialResultDictionary['enemyLeaverCount'] = 0
            for x in range(int(length/2),10):
                partialResultDictionary['teamKills'] = partialResultDictionary['teamKills'] + response['result']['players'][x]['kills']
                partialResultDictionary['teamAssists'] = partialResultDictionary['teamAssists'] + response['result']['players'][x]['assists']
                partialResultDictionary['teamDeaths'] = partialResultDictionary['teamDeaths'] + response['result']['players'][x]['deaths']

                partialResultDictionary['teamLastHits'] = partialResultDictionary['teamLastHits'] + response['result']['players'][x]['last_hits']
                partialResultDictionary['teamDenies'] = partialResultDictionary['teamDenies'] + response['result']['players'][x]['denies']
                partialResultDictionary['teamGpm'] = partialResultDictionary['teamGpm'] + response['result']['players'][x]['gold_per_min']
                partialResultDictionary['teamXpm'] = partialResultDictionary['teamXpm'] + response['result']['players'][x]['xp_per_min']
                partialResultDictionary['teamHeroDamage'] = partialResultDictionary['teamHeroDamage'] + response['result']['players'][x]['hero_damage']
                partialResultDictionary['teamTowerDamage'] = partialResultDictionary['teamTowerDamage'] + response['result']['players'][x]['tower_damage']
                partialResultDictionary['teamHeroHealing'] = partialResultDictionary['teamHeroHealing'] + response['result']['players'][x]['hero_healing']
                if 'leaver_status' in response['result']['players'][x]:
                    if (str(response['result']['players'][x]['leaver_status']) != str(0)):
                        if (str(response['result']['players'][x]['leaver_status']) != str(1)):
                            partialResultDictionary['teamLeaverCount'] = 1
                else:
                    partialResultDictionary['teamLeaverCount'] = 0


            if(not response['result']['radiant_win']):
            #    print "Dire won & player was in Dire"
                partialResultDictionary['wins'] = partialResultDictionary['wins'] + 1
            #else:
            #    print response['result']['radiant_win']

        partialResultDictionary['total'] = 1

        queueAnalyze.put(partialResultDictionary)
    except:
        partialResultDictionary2 = {'all pick': 0, 'ranked all pick': 0, 'single draft': 0, 'unspecified': 0,
                                   'teamKills': 0, 'teamDeaths': 0, 'teamAssists': 0,
                                   'enemyKills': 0, 'enemyDeaths': 0, 'enemyAssists':0,
                                   'kills': 0, 'deaths': 0, 'assists': 0, 'wins': 0, 'total': 1,
                                   'lastHits': 0, 'denies': 0, 'gpm':0, 'xpm':0, 'heroDamage':0,
                                   'towerDamage':0, 'heroHealing':0, 'leaverCount':0,
                                   'teamLastHits': 0, 'teamDenies': 0, 'teamGpm':0, 'teamXpm':0, 'teamHeroDamage':0,
                                   'teamTowerDamage':0, 'teamHeroHealing':0, 'teamLeaverCount':0,
                                   'enemyLastHits': 0, 'enemyDenies': 0, 'enemyGpm':0, 'enemyXpm':0,
                                   'enemyHeroDamage':0, 'enemyTowerDamage':0, 'enemyHeroHealing':0,
                                   'enemyLeaverCount':0, 'skipped': 1}
        queueAnalyze.put(partialResultDictionary2)
        print("One match was skipped!")

def requestGetHeroes(APIKey):
    URL = "https://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001/?key=" + APIKey + "&language=en_us"
    response = requests.get(URL)
    response = response.json()

    heroDictionary = {}

    for heroID in response['result']['heroes']:
        # print str(heroID['id']) + " " + heroID['name']
        heroID['localized_name'] = heroID['localized_name'].lower().replace(" ", "").replace("-", "").replace("_", "").replace("'", "")
        heroDictionary[heroID['id']] = heroID['localized_name']

    return heroDictionary

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def requestGetMatchHistory(APIKey, accountID):
    URL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key=" + APIKey + "&account_id=" + str(accountID)
    response = requests.get(URL)
    response = response.json()

    return response

print('Get hero dictionary...')
heroDictionary = requestGetHeroes(APIKey)

def replybot(r, sql, cur):
    global q
    global q2

    print('Searching %s.' % SUBREDDIT)
    subreddit = r.get_subreddit(SUBREDDIT)
    posts = list(subreddit.get_comments(limit=MAXPOSTS))
    posts.reverse()
    for post in posts:
        # Anything that needs to happen every loop goes here.
        pid = post.id

        try:
            pauthor = post.author.name
        except AttributeError:
            # Author is deleted. We don't care about this post.
            continue

        if pauthor.lower() == r.user.name.lower():
            # Don't reply to yourself, robot!
            #print('Will not reply to myself.')
            continue

        if KEYAUTHORS != [] and all(auth.lower() != pauthor for auth in KEYAUTHORS):
            # This post was not made by a keyauthor
            continue

        if IGNOREAUTHORS != [] and any(auth2.lower() == pauthor.lower() for auth2 in IGNOREAUTHORS):
            # This post was made by a ignoreauthor
            print("Post made by ignore author: " + pauthor.lower())
            continue

        #print(pauthor.lower(), end=" ")

        cur.execute('SELECT * FROM oldposts WHERE ID=?', [pid])
        if cur.fetchone():
            # Post is already in the database
            continue

        cur.execute('INSERT INTO oldposts VALUES(?)', [pid])
        sql.commit()
        pbody = post.body.lower()
        if any(key.lower() in pbody for key in KEYWORDS[0:2]):
            #print('Replying to %s by %s' % (pid, pauthor))
            #try:
            #    post.reply(REPLYSTRING)
            #except praw.requests.exceptions.HTTPError as e:
            #    if e.response.status_code == 403:
            #        print('403 FORBIDDEN - is the bot banned from %s?' % post.subreddit.display_name)

            post.upvote()
            print('Replying to %s by %s' % (pid, pauthor))
            try:
                splitString = pbody.split('/players/')[1]
                splitString = splitString.split(' ')[0]
                splitString = splitString.split('/')[0]
                splitString = splitString.split('\n')[0]
                splitString = splitString.split('?')[0]
                splitString = splitString.split('#')[0]
                splitString = splitString.split(')')[0]


                #How to get pattern??
                #urlFind = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', splitString)
                #re.search("(?P<url>https?://[^\s]+)", splitString).group("url")
                #re.findall(r'(https?://[^\s]+)', splitString)
                #re.findall(r'http[s]?://dotabuff.com', splitString)


                if(RepresentsInt(splitString)):
                    queueMessage = [splitString, post]
                    q.put(queueMessage)
                    print("Putting work (analyze match) onto queue.")


            except praw.requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    print('403 FORBIDDEN - is the bot banned from %s?' % post.subreddit.display_name)

        if any(key.lower() in pbody for key in KEYWORDS[2:3]):
            print('Replying to %s by %s MatchCommon' % (pid, pauthor))
            #post.upvote()
            try:
                pbody = pbody.lower()

                splitString = pbody.split(('!matchCommon ').lower())[1]


                player1 = splitString.split(('+').lower())[0]
                try:
                    player1 = player1.split(("/players/").lower())[1]
                except:
                    print("")

                player2 = splitString.split(('+').lower())[1]
                player2 = player2.split(' ')[0]
                player2 = player2.split('\n')[0]
                player2 = player2.split('?')[0]
                player2 = player2.split('#')[0]
                player2 = player2.split(')')[0]
                try:
                    player2 = player2.split(("/players/").lower())[1]
                except:
                    print("")
                player2 = player2.split('/')[0]

                if(RepresentsInt(player1)):
                    if(RepresentsInt(player2)):
                        queueMessage = [player1, player2, post]
                        q2.put(queueMessage)
                        print("Putting work (match common) onto queue.")
            except:
                print("Syntax error!")


def workerWorkEternity(queue):
    cycles = 0

    print('Opening SQL Database')
    sql = sqlite3.connect('sql.db')
    cur = sql.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS oldposts(id TEXT)')

    print('Logging in...')
    global r
    #r = praw.Reddit(USERAGENT)
    o = OAuth2Util.OAuth2Util(r)
    o.refresh(force=True)


    while True:
        try:
            replybot(r, sql, cur)
            cycles += 1
        except Exception as e:
            traceback.print_exc()
        if cycles >= CLEANCYCLES:
            print('Cleaning database')
            cur.execute('DELETE FROM oldposts WHERE id NOT IN (SELECT id FROM oldposts ORDER BY id DESC LIMIT ?)', [MAXPOSTS * 2])
            sql.commit()
            cycles = 0
        print('Running again in %d seconds' % WAIT)
        time.sleep(WAIT)

def workerAnalyzePlayerID(queue):
    while True:
        try:
            #get your data off the queue, and do some work
            #url= queue.get(False)
            if (q.empty()):
                print("no work for analyze player")
                time.sleep(10)
                continue
            else:
                print("There's work for analyze player: " + str(q.qsize()))
            queueMessage = queue.get(False)
            splitString = queueMessage[0]
            post = queueMessage[1]
            playerID = splitString
            print('Found a player ID: ' + playerID)


            try:
                matchHistoryJSON = requestGetMatchHistory(APIKey, playerID)
            except requests.exceptions.Timeout:
                time.sleep(5)
                matchHistoryJSON = requestGetMatchHistory(APIKey, playerID)
            except requests.exceptions.RequestException as e:
                continue




            resultDictionary = {'all pick': 0, 'ranked all pick': 0, 'single draft': 0, 'unspecified': 0,
                                'teamKills': 0, 'teamDeaths': 0, 'teamAssists': 0,
                                'enemyKills': 0, 'enemyDeaths': 0, 'enemyAssists':0,
                                'kills': 0, 'deaths': 0, 'assists': 0, 'wins': 0, 'total': 0,
                                'lastHits': 0, 'denies': 0, 'gpm':0, 'xpm':0, 'heroDamage':0,
                                'towerDamage':0, 'heroHealing':0, 'leaverCount':0,
                                'teamLastHits': 0, 'teamDenies': 0, 'teamGpm':0, 'teamXpm':0, 'teamHeroDamage':0,
                                'teamTowerDamage':0, 'teamHeroHealing':0, 'teamLeaverCount':0,
                                'enemyLastHits': 0, 'enemyDenies': 0, 'enemyGpm':0, 'enemyXpm':0,
                                'enemyHeroDamage':0, 'enemyTowerDamage':0, 'enemyHeroHealing':0,
                                'enemyLeaverCount':0, 'skipped': 0}

            global playedHeroes
            playedHeroes = {}

            threads = []

            print("Firing all Steam API requests.......")

            for match in matchHistoryJSON['result']['matches']:
                t = threading.Thread(target=analyzeMatch, args = (queueAnalyze, APIKey, match['match_id'], playerID))
                t.daemon = True
                t.start()
                time.sleep(0.1)
                threads.append(t)

            print(".... all Steam API requests fired. Joining all threads.......")

            for x in threads:
                x.join()

            print(".... all threads joined." + str(q.qsize()))

            for i in range(queueAnalyze.qsize()):
            #for match in matchHistoryJSON['result']['matches']:
                partialResultDictionary = queueAnalyze.get()
                for k in resultDictionary:
                    resultDictionary[k] = resultDictionary[k]+partialResultDictionary[k]
                #print("Analyzed " + str(resultDictionary['total']) + " out of " + str(matchHistoryJSON['result']['num_results']) + "! " + str(q.qsize()))
                if (int(queueAnalyze.qsize()) == 0):
                    break


            print ("Analyze success! " + str(q.qsize()))
            resultString = displayResult(resultDictionary, matchHistoryJSON, heroDictionary, playerID)
            print("Reply success!")
            post.reply(resultString)




        except:
            print("There was a big error!")
            time.sleep(10)

def workerCompareTwoPlayers(queue):
    while True:
        try:
            if (queue.empty()):
                print("no work for match common")
                time.sleep(20)
                continue
            else:
                print("There's work for match common: " + str(queue.qsize()))

            queueMessage = queue.get(False)
            player1 = queueMessage[0]
            print(player1)
            player2 = queueMessage[1]
            print(player2)
            post = queueMessage[2]

            print("Performing match Common")
            resultString = matchCommon(player1, player2)
            print("Replying...")
            print(resultString)
            post.reply(resultString)


        except:
            print("There was a big error! (matchCommon)")

def workerRemoveBotComments():
    global r
    user = r.get_redditor('AnalyzeLast100Games')
    while True:
        try:
            print("Searching for negative comments on bot....")
            for comment in user.get_comments(limit=MAXPOSTS):
                if comment.score < 0:
                    comment.delete()
                    print("Deleting comment @@@@@@@@@@@@@@@@@@@@@@@@@")
            time.sleep(60)
        except:
            traceback.print_exc()
            print('Resuming in 60 seconds...')
            time.sleep(60)

#print("threading")

t = threading.Thread(target=workerWorkEternity, args = (q,))
t.start()
t = threading.Thread(target=workerAnalyzePlayerID, args = (q,))
t.start()
t = threading.Thread(target=workerCompareTwoPlayers, args = (q2,))
t.start()
t = threading.Thread(target=workerRemoveBotComments, args = ())
t.start()
