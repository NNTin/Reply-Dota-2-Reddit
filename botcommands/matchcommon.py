from steamapi import getproplayerlist
from steamapi.getmatchhistory import requestGetMatchHistory
from displayreddit.drmatchcommon import displayResult


getproplayerlist.requestGetProPlayerList()

proPlayerDictionary = getproplayerlist.proPlayerDictionary



def matchCommon(comparePlayerID, withPlayerIDs=None, amount=100):
    withPlayerIDs_ = {}


    if withPlayerIDs == None:
        for player in proPlayerDictionary:
            #if player != comparePlayerID:      #TODO: only temporaryy, revert back!
            withPlayerIDs_[player] = proPlayerDictionary[player]


        #withPlayerIDs_ = proPlayerDictionary
    else:
        #withPlayerIDs_ = withPlayerIDs     #TODO: only temporary, revert back when comparing to individual player(s) works
        withPlayerIDs_ = proPlayerDictionary


    #if comparePlayerID in withPlayerIDs_:
    #    del withPlayerIDs_[comparePlayerID]


    matches = requestGetMatchHistory(comparePlayerID, amount)

    playedMatchesTogether = {}

    for match in matches:
        for player in match['players']:
            if player['account_id'] in withPlayerIDs_:

                if player['account_id'] in playedMatchesTogether.keys():
                    playedMatchesTogether[player['account_id']]['count'] = playedMatchesTogether[player['account_id']].get('count', 0) + 1
                    playedMatchesTogether[player['account_id']]['hero_picks'][player['hero_id']] = playedMatchesTogether[player['account_id']]['hero_picks'].get(player['hero_id'], 0) + 1

                else:
                    playedMatchesTogether[player['account_id']] = {}
                    playedMatchesTogether[player['account_id']]['count'] = 1
                    playedMatchesTogether[player['account_id']]['hero_picks'] = {}
                    playedMatchesTogether[player['account_id']]['hero_picks'][player['hero_id']] = 1



    displayResult(comparePlayerID, playedMatchesTogether)




