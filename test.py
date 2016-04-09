from botcommands import toplivegames
from steamapi import getheroes, getproplayerlist, getschema, getleaguelisting

getheroes.requestGetHeroes()
getproplayerlist.requestGetProPlayerList()
getschema.requestGetSchema()
getleaguelisting.requestGetLeagueListing()

reply = toplivegames.topLiveGames('fjklsd')
print(reply)

