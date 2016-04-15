import requests
from steamapi.steamapikey import SteamAPIKey
#message = True

proPlayerDictionary = {}
playerOnLeaderboard = {}

def requestGetProPlayerList():

    keyValues = ['locked_until', 'team_id', 'sponsor', 'is_locked', 'fantasy_role', 'team_tag',
                 'name', 'country_code', 'is_pro', 'team_name']

    URL = "https://api.steampowered.com/IDOTA2Fantasy_570/GetProPlayerList/v1?key=" + SteamAPIKey
    response = requests.get(URL)
    response.connection.close()
    response = response.json()

    global proPlayerDictionary

    for player in response['player_infos']:
        proPlayerDictionary[player['account_id']] = {}
        for key in keyValues:
            proPlayerDictionary[player['account_id']][key] = player.get(key, 0)

    global playerOnLeaderboard
    for divison in response.get('leaderboards', []):
        for player in divison['account_ids']:
            playerOnLeaderboard[player] = True