import requests
from steamapi.steamapikey import SteamAPIKey
#message = True

leagueListingDictionary = {}

def requestGetLeagueListing():

    keyValues = ['name', 'description', 'tournament_url', 'itemdef']

    URL = "https://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v1?key=" + SteamAPIKey
    response = requests.get(URL)
    response.connection.close()
    response = response.json()

    global leagueListingDictionary

    for league in response['result']['leagues']:
        leagueListingDictionary[league['leagueid']] = {}
        for key in keyValues:
            leagueListingDictionary[league['leagueid']][key] = league.get(key, 0)