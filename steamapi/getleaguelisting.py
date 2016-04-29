import requests
import time
from steamapi.steamapikey import SteamAPIKey
#message = True

leagueListingDictionary = {}

def requestGetLeagueListing():

    keyValues = ['name', 'description', 'tournament_url', 'itemdef']



    response = {}
    attempt = 0

    while response == {}:


        URL = "https://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v1?key=" + SteamAPIKey
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


    global leagueListingDictionary

    for league in response['result']['leagues']:
        leagueListingDictionary[league['leagueid']] = {}
        for key in keyValues:
            leagueListingDictionary[league['leagueid']][key] = league.get(key, 0)