import requests
import time
from steamapi.steamapikey import SteamAPIKey
#from reddit.botinfo import message
message = False

def getMatchDetails(q,matchID):

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
                if (attempt == 3):
                    print('Tried %s times, cancelling API request. (Skipped counter increases)')
                    break
                print('Failed API request, retrying in %s seconds' %(attempt * 2))
                time.sleep(attempt * 2)
                continue
            else:
                q.put(response)


    except:
        print('[getmatchdetails] there was an error, match is skipped! %s' %matchID)

        response = {}
        q.put(response)

        # future, retry until it works!
