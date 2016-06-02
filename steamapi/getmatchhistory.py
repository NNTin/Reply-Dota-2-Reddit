import requests, time
from steamapi.steamapikey import SteamAPIKey
from reddit.botinfo import message
#message = True

def requestGetMatchHistory(playerID, amount):
    if message: print('[getmatchhistory] Getting matchhistory of player id: %s' %playerID)

    start_at_match_id = 0
    results_remaining = True
    matches = []

    while(results_remaining and amount-len(matches) > 0):



        response = {}
        attempt = 0

        while response == {}:


            url = "https://api.steampowered.com/idota2match_570/getmatchhistory/v001/?key=" + SteamAPIKey + "&account_id=" \
                  + str(playerID) + "&matches_requested=" + str(amount - len(matches)) + "&start_at_match_id=" + str(start_at_match_id)
            response = requests.get(url)
            response.connection.close()
            response = response.json()

            if response == {}:
                attempt += 1
                if (attempt == 30):
                    print('Tried %s times, cancelling API request. (Skipped counter increases)')
                    break
                print('Failed API request (empty json), retrying in %s seconds; attempt #%s' %(2, attempt))
                time.sleep(1)
                continue
            else:
                break






        #TODO handle error when response has no result
        matches += response['result']['matches']

        start_at_match_id = matches[len(matches)-1]['match_id'] - 1
        if (response['result']['results_remaining'] == 0):
            results_remaining = False

    if message: print('[getmatchhistory] Getting matchhistory successful, match ids fetched: %s' %len(matches))
    return matches




#start_at_match_id decrement once from last
#pay attention to results_remaining parameter


