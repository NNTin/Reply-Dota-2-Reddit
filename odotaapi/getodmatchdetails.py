import requests
import time
#from reddit.botinfo import message
message = False

def getODMatchDetails(matchID, q=None):

    try:
        response = {}
        attempt = 0

        while response == {}:

            if message: print('[getodmatchdetails] get match details on OpenDota')

            URL = 'https://api.opendota.com/api/matches/' + str(matchID)
            response = requests.get(URL)
            response.connection.close()
            response = response.json()

            # careful Steam API sometimes returns empty JSONs!
            # handle this error!

            if response == {}:
                attempt += 1
                if (attempt == 10):
                    print('Tried %s times, cancelling API request. (Skipped counter increases)')
                    if q == None:
                        return response
                    else:
                        q.put(response)
                    break
                print('Failed API request, retrying in %s seconds' %(2))
                print(URL)
                time.sleep(attempt * 2)
                continue
            else:
                if q == None:
                    return response
                else:
                    q.put(response)


    except:
        print('[getodmatchdetails] there was an error, match is skipped on OpenDota! %s' %matchID)

        response = {}
        if q == None:
            return response
        else:
            q.put(response)

        # future, retry until it works!
