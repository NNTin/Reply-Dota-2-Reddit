from steamapi import getmatchdetails, getplayersummaries
from displayreddit import drmatch
from odotaapi import requestparsematch
import threading

def match(matchID):


    t = threading.Thread(target=requestparsematch.requestParseMatch, args = (matchID,))
    t.start()

    matchJson = getmatchdetails.getMatchDetails(matchID)

    accountIDs = []
    for player in matchJson['result']['players']:
        accountIDs.append(player['account_id'])

    playerSummariesJson = getplayersummaries.getPlayerSummaries(accountIDs)

    reply = drmatch.displayResult(matchJson, playerSummariesJson)

    return reply