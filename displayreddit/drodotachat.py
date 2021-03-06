from converter import timeconverter
from steamapi.getheroes import heroDictionary
from dataIO import dataIO

def displayResult(matchOdotaJson):
    chatLog = matchOdotaJson['chat']
    players = {}
    for player in matchOdotaJson['players']:
        players[player['player_slot']] = {'account_id': player.get('account_id', None),
                                          'personaname': player.get('personaname', None),
                                          'hero_id': player.get('hero_id', None)}

    introTemplate = '####&#009;\n#####&#009; Hover to view [chat log](https://www.opendota.com/matches/{matchid}/chat)\n######&#009;\n\n' \
                    'This chat log was provided by [**OpenDota**](https://www.opendota.com/matches/{matchid}/chat)\'s free replay parsing.\n\n'
    chatHeader = 'Player | Time | Message\n' \
                 ':-- | :-- | :--\n'
    chatLineTemplate = '[](/hero-{heroName}) {playerName} | {time} | {message}\n'

    intro = introTemplate.format(matchid=matchOdotaJson['match_id'])

    print(chatLog)
    chatResult = chatHeader
    for i in range(0, len(chatLog)):
        time = timeconverter.durationTimeConverter(chatLog[i]['time'])
        heroName = heroDictionary[players[chatLog[i]['player_slot']]['hero_id']]
        if players[chatLog[i]['player_slot']]['personaname'] is not None:
            playerName = '%.9s' %players[chatLog[i]['player_slot']]['personaname']
        else:
            playerName = ''

        if chatLog[i]['type'] == 'chat':
            message = chatLog[i]['key']
        elif chatLog[i]['type'] == 'chatwheel':
            chatwheelFile = 'data/chatwheel.json'
            chatwheel = dataIO.load_json(chatwheelFile)
            message = '▶ ' + chatwheel[chatLog[i]['key']]


        chatResult += chatLineTemplate.format(heroName=heroName, playerName=playerName, time=time, message = message)

    return (intro + chatResult + '\n---\n\n')

