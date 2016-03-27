import requests
from steamapi.steamapikey import SteamAPIKey
#from reddit.botinfo import message
message = False

def getMatchDetails(q,matchID):
    try:
        if message: print('[getmatchdetails] get match details')

        URL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key=" + SteamAPIKey + "&match_id=" + str(matchID)
        response = requests.get(URL)
        response = response.json()

        # careful Steam API sometimes returns empty JSONs!
        # handle this error!

        q.put(response)


    except:
        print('[getmatchdetails] match was skipped! %s' %matchID)

        response = {}
        q.put(response)

        # future, retry until it works!
