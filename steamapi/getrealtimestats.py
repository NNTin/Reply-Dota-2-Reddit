import requests
from steamapi.steamapikey import SteamAPIKey
#from reddit.botinfo import message
message = False

def getRealtimeStats(serverSteamID):
    try:
        if message: print('[getmatchdetails] get match details')

        URL = 'https://api.steampowered.com/IDOTA2MatchStats_570/GetRealtimeStats/v1?key=' + SteamAPIKey + '&server_steam_id=' + str(serverSteamID)
        print(URL)
        response = requests.get(URL)
        response.connection.close()
        response = response.json()

        # careful Steam API sometimes returns empty JSONs!
        # handle this error!


    except:
        response = {}

        # future, retry until it works!
    return response