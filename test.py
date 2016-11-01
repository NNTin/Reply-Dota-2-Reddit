import re

if True:
    pattern = '(?P<website>yasp\.co|dotabuff\.com|opendota\.com)\/players\/(?P<playerID>\d{1,9})(\/(?P<tab>\w+)((?P<queryParameters>\S+))?)?'
    patternHero = '[?&](hero|hero_id)=(?P<heroID>\w+)'
    patternGameMode = '[?&]game_mode=(?P<gameModeID>\w+)'

    text = 'http://www.dotabuff.com/players/114560539/matches?hero=meepo\n' \
            'http://www.dotabuff.com/players/114560539/matches?date=year&game_mode=all_pick&hero=meepo\n' \
            'http://www.dotabuff.com/players/114560539/matches?date=year&hero=meepo&game_mode=all_pick\n' \
            'http://www.dotabuff.com/players/114560539/matches?game_mode=all_pick&hero=meepo&date=year\n' \
            'http://www.dotabuff.com/players/114560539/matches?date=year&game_mode=all_pick\t' \
            '​https://www.opendota.com/players/114560539/matches\n' \
            'https://www.opendota.com/players/114560539/matches some text\n' \
            'https://www.opendota.com/players/114560539/matches\n' \
            'https://www.opendota.com/players/114560539/matches)\n' \
            'https://www.opendota.com/players/114560539/matches?hero_id=82 some text\n' \
            'https://www.opendota.com/players/114560539/matches?hero_id=82\n' \
            'https://www.opendota.com/players/114560539/matches?hero_id=82\n' \
            'https://www.opendota.com/players/114560539/matches?hero_id=82)\n' \
            'https://www.opendota.com/players/114560539/matches?with_hero_id=82&hero_id=82&against_hero_id=106&is_radiant=1&win=1&patch=18&game_mode=22&lobby_type=7&region=3&date=180&limit=\n' \
            'https://www.opendota.com/players/114560539/matches?hero_id=82&with_hero_id=82&against_hero_id=106&is_radiant=1&win=1&patch=18&game_mode=22&lobby_type=7&region=3&date=180&limit=\n' \
            'https://www.opendota.com/players/114560539/matches?with_hero_id=82&against_hero_id=106&hero_id=82&is_radiant=1&win=1&patch=18&game_mode=22&lobby_type=7&region=3&date=180&limit=\n' \
            'https://www.opendota.com/players/114560539/matches\n' \
            'https://www.yasp.co/players/114560539/matches\n' \
            'https://www.yasp.co/players/114560539/chat?hero_id=82\n' \

    counter = 0
    for m in re.finditer(pattern, text, re.I):
        counter += 1
        playerID = m.group('playerID')
        queryParameters = m.group('queryParameters')
        website = m.group('website')
        heroID = None
        gameModeID = None

        if queryParameters != None:
            n = re.search(patternHero, queryParameters, re.I)
            if n != None:
                heroID = n.group('heroID')
            n = re.search(patternGameMode, queryParameters, re.I)
            if n != None:
                gameModeID = n.group('gameModeID')

        print('result #%s: website = %s, playerID = %s, heroID = %s, gameMode = %s' %(counter, website, playerID, heroID, gameModeID))

