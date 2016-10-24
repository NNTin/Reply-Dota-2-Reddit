import requests
import time
from steamapi.steamapikey import SteamAPIKey

def getPlayerSummaries(accountIDs):
    accountIDString = ''
    for accountID in accountIDs:
        accountIDString += str(76561197960265728 + accountID) + ','
    accountIDString = accountIDString[:-1]

    try:
        response = {}
        attempt = 0

        while response == {}:

            URL = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=" + SteamAPIKey + "&steamids=" + accountIDString
            response = requests.get(URL)
            response.connection.close()
            response = response.json()

            # careful Steam API sometimes returns empty JSONs!
            # handle this error!

            if response == {}:
                attempt += 1
                if (attempt == 10):
                    print('Tried %s times, cancelling API request. (Skipped counter increases)')
                    return response
                    break
                print('Failed API request, retrying in %s seconds' %(2))
                print('URL')
                time.sleep(attempt * 2)
                continue
            else:
                if True:
                    print(response)
                    for i in range(0, len(response['response']['players'])):
                        try:
                            response['response']['players'][i]['steam32id'] = int(response['response']['players'][i]['steamid']) - 76561197960265728
                        except:
                            print('[getplayersummaries] steam id missing')
                    return response


    except:
        print('[getplayersummaries] there was an error, accountIDs are skipped! %s' %accountIDs)
        return response


