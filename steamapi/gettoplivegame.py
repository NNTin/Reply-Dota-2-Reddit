import requests
from steamapi.steamapikey import SteamAPIKey
#message = True


def requestGetTopLiveGame(partner):

    #https://api.steampowered.com/IDOTA2Match_570/GetTopLiveGame/v1/?key=F79627788CAF92984B8B0E77FB29E9B8&partner=3

    URL = "https://api.steampowered.com/IDOTA2Match_570/GetTopLiveGame/v1/?key=" + SteamAPIKey + "&partner=" + str(partner)
    response = requests.get(URL)
    response.connection.close()
    response = response.json()

    return(response)
