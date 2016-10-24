import requests

def requestParseMatch(matchID):
    try:
        #check if match is already parsed
        url = 'https://api.opendota.com/api/matches/%s' %matchID
        response = requests.get(url)
        response.connection.close()
        response = response.json()

        if response['version'] == None:
            #send parse request to odota
            print('[requestparsematch] Match is not parsed on OpenDota, sending parse request')
            url = 'https://www.opendota.com/api/request_job'
            data  = {"match_id": (None, str(matchID))}
            response = requests.post(url, files=data)
            response.connection.close()
            print('[requestparsematch] Parse request sent to Odota, response %s' %response.text)
        else:
            print('[requestparsematch] Match is already parsed on OpenDota')
    except:
        print('[requestparsematch] Parse request failed.')
