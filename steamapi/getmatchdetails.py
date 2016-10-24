import requests
import time
from steamapi.steamapikey import SteamAPIKey
#from reddit.botinfo import message
message = False

def getMatchDetails(matchID, q=None):

    try:
        response = {}
        attempt = 0

        while response == {}:

            if message: print('[getmatchdetails] get match details')

            URL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key=" + SteamAPIKey + "&match_id=" + str(matchID)
            response = requests.get(URL)
            response.connection.close()
            response = response.json()

            # careful Steam API sometimes returns empty JSONs!
            # handle this error!

            if response == {}:
                attempt += 1
                if (attempt == 10):
                    print('Tried %s times, cancelling API request. (Skipped counter increases)')
                    if q == None:
                        return response
                    else:
                        q.put(response)
                    break
                print('Failed API request, retrying in %s seconds' %(2))
                print(URL)
                time.sleep(attempt * 2)
                continue
            else:
                if q == None:
                    return response
                else:
                    q.put(response)


    except:
        print('[getmatchdetails] there was an error, match is skipped! %s' %matchID)

        response = {}
        if q == None:
            return response
        else:
            q.put(response)

        # future, retry until it works!
