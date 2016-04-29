import requests, time
from steamapi.steamapikey import SteamAPIKey
#from reddit.botinfo import message
message = False

def getRealtimeStats(serverSteamID):
    try:
        if message: print('[getmatchdetails] get match details')


        response = {}
        attempt = 0

        while response == {}:

            URL = 'https://api.steampowered.com/IDOTA2MatchStats_570/GetRealtimeStats/v1?key=' + SteamAPIKey + '&server_steam_id=' + str(serverSteamID)
            print(URL)
            response = requests.get(URL)
            response.connection.close()
            response = response.json()

            if response == {}:
                attempt += 1
                if (attempt == 5):
                    print('Tried %s times, cancelling API request. (Skipped counter increases)')
                    break
                print('Failed API request, retrying in %s seconds' %(attempt * 2))
                time.sleep(attempt * 2)
                continue
            else:
                break


        # careful Steam API sometimes returns empty JSONs!
        # handle this error!


    except:
        response = {}

        # future, retry until it works!
    return response