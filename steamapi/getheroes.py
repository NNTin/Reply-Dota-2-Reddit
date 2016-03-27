import requests
from steamapi.steamapikey import SteamAPIKey
from reddit.botinfo import message
#message = True

heroDictionary = {}

def requestGetHeroes():
    if message: print('[getheroes] request get heroes...')

    URL = "https://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001/?key=" + SteamAPIKey + "&language=en_us"
    response = requests.get(URL)
    response = response.json()

    global heroDictionary

    for heroID in response['result']['heroes']:
        # print str(heroID['id']) + " " + heroID['name']
        heroID['localized_name'] = heroID['localized_name'].lower().replace(" ", "").replace("-", "").replace("_", "").replace("'", "")
        heroDictionary[heroID['id']] = heroID['localized_name']

    if message: print('[getheroes] request set heroes success')

    return heroDictionary