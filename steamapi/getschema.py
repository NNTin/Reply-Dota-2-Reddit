import requests
import vdf
import json
from steamapi.steamapikey import SteamAPIKey
#message = True

dota2schema = {}

def requestGetSchema():
    URL = "https://api.steampowered.com/IEconItems_570/GetSchemaURL/v1?key=" + SteamAPIKey
    print(URL)
    response = requests.get(URL)
    response.connection.close()
    response = response.json()
    print(response)

    global dota2schema

    URL = response['result']['items_game_url']

    with open ("items_game_url.txt", "r") as text_file:
        data=text_file.read()

    print(data)
    print(URL)

    if (data != URL):

        response = requests.get(URL)
        response.connection.close()

        response = response.text

        dota2schema = vdf.loads(response)

        with open('dota2schema.txt', 'w') as outfile:
            json.dump(dota2schema, outfile)

        with open("items_game_url.txt", "w") as text_file:
            text_file.write(URL)

    else:
        with open ("dota2schema.txt", "r") as text_file:
            data=text_file.read()
            dota2schema = json.loads(data)
