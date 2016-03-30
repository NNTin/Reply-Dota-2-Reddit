import re

# pattern matching for this issue: https://github.com/NNTin/Reply-Dota-2-Reddit/issues/2
# https://docs.python.org/2/library/re.html

# <player link> [amount:<variable>] [view:<variable>] [heroes:<variable>{+<variable>}]

someText = 'yasp.co/players/40547474' \
           'yadayadayada' \
           'dotabuff.com/players/40547474 amount:150 view:detailed heroes:juggernaut' \
           'yasp.co/players/40547474 heroes:juGGernaut+sveN' \
           'some wild text' \
           'dotabuff.com/players/40547474 heroes:dragonknight+clockwerk+faceless void+lifestealer'

# when doing patternmatching I want to retrieve the following information
# <player link> [amount:<variable>] [view:<variable>] [heroes:<variable>{+<variable>}]
playerID = [40547474, 40547474, 40547474, 40547474]
amount = ['', 150, '', '']
view = ['', 'detailed', '', '']
heroes = ['', 'juggernaut', 'juGGernaut+sveN', 'dragonknight+clockwerk+faceless void+lifestealer']