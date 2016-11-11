import requests, time

def requestParseMatch(matchID, holdUntilParsed=False):
    try:
        #check if match is already parsed
        url = 'https://api.opendota.com/api/matches/%s' %matchID
        response = requests.get(url)
        response.connection.close()
        response = response.json()

        if response['version'] == None:
            #send parse request to odota
            print('[requestparsematch] Match is not parsed on OpenDota, sending parse request')
            url = 'https://api.opendota.com/api/request/%s' %matchID
            response = requests.post(url)
            response.connection.close()
            response = response.json()
            print('[requestparsematch] Parse request sent to ODota, response %s' %response)

            counter = 0
            while holdUntilParsed:
                if isParsed(response['job']['jobId']):
                    print('[requestparsematch] match has been parsed on ODota just now')
                    break
                else:
                    counter += 1
                    time.sleep(5)
                    if counter > 60:
                        print('[requestparsematch] 5 minutes passed, failed to parse match on ODota')
                        break
        else:
            print('[requestparsematch] Match is already parsed on OpenDota')
    except:
        print('[requestparsematch] Parse request failed.')

def isParsed(jobId):
    url = 'https://api.opendota.com/api/request/%s' %jobId
    response = requests.get(url)
    response.connection.close()
    response = response.json()

    if response['state'] == 'active':
        return False
    else:
        #Note: This means the state is either completed or failed.
        return True