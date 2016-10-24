from steamapi.getproplayerlist import proPlayerDictionary
from steamapi.getheroes import heroDictionary
from steamapi.getgameitems import itemDictionary
from converter import timeconverter, playerconverter

def displayResult(matchJson, playerSummariesJson):

    introTemplate = '####&#009;\n#####&#009; Hover to view match ID: {matchid} [DB](http://www.dotabuff.com/matches/{matchid})/[OD](https://www.opendota.com/matches/{matchid})\n######&#009;\n\n' \
                    '[**{teamwinner} wins {winnerkills}-{loserkills} @ {time}**](#lumbdi "{additionalinformation}")\n\n'
    tableTemplate = 'Lvl | Hero | Player| K/D/A | LH/D | XPM | GPM | HD | HH | TD\n' \
                    ':--|:--:|:--|:--|:--|:--|:--|:--|:--|:--\n'
    tableLineTemplate = '{level}|{hero}|{account}|{kda}|{lhd}|{xpm}|{gpm}|{hd}|{hh}|{td}\n'
    dividerTemplate = '{level}||↑Radiant↑ ↓Dire↓ |{kda}|{lhd}|{xpm}|{gpm}|{hd}|{hh}|{td}\n'
    outtro = '\n\n---\n\n'

    #print(introTemplate + tableTemplate + tableLineTemplate + outtroTemplate)

    matchID = matchJson['result']["match_id"]
    if matchJson['result']['radiant_win']:
        teamwinner = 'Radiant'
        winnerkills = matchJson['result']["radiant_score"]
        loserkills = matchJson['result']["dire_score"]
    else:
        teamwinner = 'Dire'
        winnerkills = matchJson['result']["dire_score"]
        loserkills = matchJson['result']["radiant_score"]
    time = timeconverter.durationTimeConverter(matchJson['result']["duration"])

    #TODO: Provide additional information if match is tournament
    matchDate = timeconverter.unixTimeConverter(matchJson['result']["start_time"])
    firstBloodTime = timeconverter.durationTimeConverter(matchJson['result']["first_blood_time"])
    additionalInformation = 'Match ID: %s, match date: %s, first blood time: %s' %(matchID,matchDate,firstBloodTime)

    intro = introTemplate.format(matchid=matchID, teamwinner=teamwinner, winnerkills=winnerkills, loserkills=loserkills, time=time, additionalinformation=additionalInformation)

    radiantTable = ''
    direTable = ''
    teamStats = [{'level': 0, 'kills': 0, 'deaths': 0, 'assists': 0, 'lasthits': 0, 'denies': 0,
                  'xpm': 0, 'gpm': 0, 'hd': 0, 'hh': 0, 'td': 0
                  },
                {'level': 0, 'kills': 0, 'deaths': 0, 'assists': 0, 'lasthits': 0, 'denies': 0,
                 'xpm': 0, 'gpm': 0, 'hd': 0, 'hh': 0, 'td': 0
                }]
    for player in matchJson['result']['players']:
        #level, hero, player, kda, lh d, xpm, gpm, hd, hh, td

        stats = {'level': player['level'], 'kills': player['kills'], 'deaths': player['deaths'],
                 'assists': player['assists'], 'lasthits': player['last_hits'],
                 'denies': player['denies'], 'xpm': player["xp_per_min"], 'gpm': player["gold_per_min"],
                 'hd': player["hero_damage"], 'hh': player["hero_healing"], 'td': player["tower_damage"]}

        hero = '[](/hero-%s)' %heroDictionary[player['hero_id']]
        account = playerconverter.playerConverter(player['account_id'], playerSummariesJson)
        kda = '%s/%s/%s' %(stats['kills'],stats['deaths'], stats['assists'])
        lhd = '%s/%s' %(player['last_hits'], player['denies'])

        if player['player_slot'] < 127:     #<127 -> Radiant
            radiantTable += tableLineTemplate.format(level=stats['level'], hero=hero, account=account, kda=kda, lhd=lhd, xpm=stats['xpm'],
                                                     gpm=stats['gpm'], hd=stats['hd'], hh=stats['hh'], td=stats['td'])
            for stat in stats:
                teamStats[0][stat] += stats[stat]
        else:
            direTable    += tableLineTemplate.format(level=stats['level'], hero=hero, account=account, kda=kda, lhd=lhd, xpm=stats['xpm'],
                                                     gpm=stats['gpm'], hd=stats['hd'], hh=stats['hh'], td=stats['td'])
            for stat in stats:
                teamStats[1][stat] += stats[stat]


    teamStatsDict = {}
    for i in range(0, len(teamStats)):
        teamStats[i]['kda'] = '%s/%s/%s' %(teamStats[i]['kills'], teamStats[i]['deaths'], teamStats[i]['assists'])
        teamStats[i]['lhd'] = '%s/%s' %(teamStats[i]['lasthits'], teamStats[i]['denies'])
        teamStats[i].pop('kills')
        teamStats[i].pop('deaths')
        teamStats[i].pop('assists')
        teamStats[i].pop('lasthits')
        teamStats[i].pop('denies')
        for stat in teamStats[i]:
            teamStatsDict[stat] = teamStatsDict.get(stat, '') + ' ' + str(teamStats[i][stat])

    divider = dividerTemplate.format(level=teamStatsDict['level'], kda=teamStatsDict['kda'], lhd=teamStatsDict['lhd'], xpm=teamStatsDict['xpm'],
                                     gpm=teamStatsDict['gpm'], hd=teamStatsDict['hd'], hh=teamStatsDict['hh'], td=teamStatsDict['td'])


    table = tableTemplate + radiantTable + divider + direTable

    return intro + table + '\n\n---\n\n'