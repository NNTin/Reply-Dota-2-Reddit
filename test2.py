from botcommands.matchcommon import matchCommon

from steamapi import getproplayerlist
from steamapi import getheroes

getheroes.requestGetHeroes()
getproplayerlist.requestGetProPlayerList()


matchCommon(40547474)
#matchCommon(76627815)
