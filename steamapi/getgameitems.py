import requests
from steamapi.steamapikey import SteamAPIKey
from reddit.botinfo import message
#message = True

itemDictionary = {}

def requestGetGameItems():
    if message: print('[getgameitems] request get items...')

    URL = "https://api.steampowered.com/IEconDOTA2_570/GetGameItems/v1/?key=" + SteamAPIKey + "&language=en_us"
    response = requests.get(URL)
    response.connection.close()
    response = response.json()

    global heroDictionary

    for itemID in response['result']['items']:
        # print str(heroID['id']) + " " + heroID['name']
        itemID['localized_name'] = itemID['localized_name'].lower().replace(" ", "").replace("-", "").replace("_", "").replace("'", "")
        itemDictionary[itemID['id']] = itemID


    if message: print('[getgameitems] request set items success')

    return itemDictionary