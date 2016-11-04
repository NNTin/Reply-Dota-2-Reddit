from odotaapi import getodmatchdetails, requestparsematch
from displayreddit import drodotachat

def odotaChat(matchID):
    requestparsematch.requestParseMatch(matchID, holdUntilParsed=True)
    matchJson = getodmatchdetails.getODMatchDetails(matchID)

    if matchJson['chat'] is not None:
        reply = drodotachat.displayResult(matchJson)
        return reply