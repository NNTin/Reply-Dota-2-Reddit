import requests
from steamapi.steamapikey import SteamAPIKey
from reddit.botinfo import message
#message = True

heroDictionary = {}
heroDictionaryDotabuff = {}

def requestGetHeroes():
    if message: print('[getheroes] request get heroes...')

    URL = "https://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001/?key=" + SteamAPIKey + "&language=en_us"
    response = requests.get(URL)
    response.connection.close()
    response = response.json()

    global heroDictionary
    global heroDictionaryDotabuff

    for heroID in response['result']['heroes']:
        # print str(heroID['id']) + " " + heroID['name']
        heroID['localized_name'] = heroID['localized_name'].lower().replace(" ", "-").replace("'", "").replace("_", "")
        heroDictionaryDotabuff[heroID['id']] = heroID['localized_name']

        heroID['localized_name'] = heroID['localized_name'].lower().replace("-", "").replace("_", "").replace("'", "")
        heroDictionary[heroID['id']] = heroID['localized_name']




    heroDictionary[0] = 'not picked'

    if message: print('[getheroes] request set heroes success')

    return heroDictionary