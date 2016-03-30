from steamapi import getheroes

if True:
    getheroes.requestGetHeroes()

    for hero in getheroes.heroDictionary:
        print('%s %s' %(hero, getheroes.heroDictionary[hero]))


playedHeroesString = 'oraCLe+techies+notahero+abaDDon+axe'
playedHeroesString = playedHeroesString.split('+')

playedHeroes = []

for hero in playedHeroesString:
    if hero.lower() in getheroes.heroDictionary.values():
        playedHeroes.append(hero.lower())

print(playedHeroes)
