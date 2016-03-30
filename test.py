import re

# pattern matching for this issue: https://github.com/NNTin/Reply-Dota-2-Reddit/issues/2
# https://docs.python.org/2/library/re.html

# <player link> [amount:<variable>] [view:<variable>] [heroes:<variable>{+<variable>}]

someText = 'yasp.co/plaYers/40547474' \
           'yadayadayada' \
           'dotabuff.com/players/40547474 amount:150 view:detailed heroes:juGGernaut\n' \
           'yasp.co/players/40547474 heroes:juGGernaut+sveN' \
           'some wild text' \
           'dotabuff.com/players/40547474 heroes:dragonknight+clockwerk+facelessvoid+lifestealer'

#(yasp\.co|dotabuff\.com)\/players\/(?P<player_id>\d{0,8})( amount:( )?(?P<amount>\d+))?( view:( )?(?P<view>\w+))?( heroes:( )?(?P<heroes>[\w+]+))?
#(yasp\.co|dotabuff\.com)\/players\/(?P<player_id>\d{0,8})( amount:( )?(?P<amount>\d+))?( view:( )?(?P<view>\w+))?( heroes:( )?(?P<heroes>[\w+]+))?



pattern = '(yasp\.co|dotabuff\.com)\/players\/(?P<player_id>\d{0,8})( amount:( )?(?P<amount>\d+))?( view:( )?(?P<view>\w+))?( heroes:( )?(?P<heroes>[\w+]+))?'

patternMatches = re.findall(pattern, someText, re.I)

players = []

for patternMatch in patternMatches:
    player = {}
    player['player_id'] = patternMatch[1]
    player['amount'] = patternMatch[4]
    player['view'] = patternMatch[7]
    player['heroes'] = patternMatch[10]
    print(patternMatch)
    print(patternMatch[1] + ' amount: ' + patternMatch[4] + ' view: ' +  patternMatch[7] + ' heroes: ' +  patternMatch[10])
    print('')
    players.append(player)

print(players)




# when doing patternmatching I want to retrieve the following information
# <player link> [amount:<variable>] [view:<variable>] [heroes:<variable>{+<variable>}]
playerID = [40547474, 40547474, 40547474, 40547474]
amount = ['', 150, '', '']
view = ['', 'detailed', '', '']
heroes = ['', 'juggernaut', 'juGGernaut+sveN', 'dragonknight+clockwerk+faceless void+lifestealer']