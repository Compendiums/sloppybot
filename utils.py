def readText(path):
    text = open(path,'r')
    return text.read()

def formatClashStats(team_dict={}): #can probably use automatic dictionary unpacking here
    
    seperator = '**--------------------------------**\n'
    
    heading = '**{team}**    tier {tier}\n'.format(team=team_dict['team'],tier=team_dict['tier'])+seperator

    members = ''
    players_dict = team_dict['players']

    for player in players_dict:
        members += '**{name}**     {position}\n'.format(name=player['summonerId'],position=player['position'])
    members += seperator

    winrate = '**win rate**: '+team_dict['winrate']+seperator

    matches_heading = '**Match History**\n'

    matches = ''
    matches_dict = team_dict['matches']

    for date,winloss in matches_dict.items():
        matches += '{date}     {winloss}\n'.format(date=date,winloss=winloss)

    final_text = (
        heading
        +members
        +winrate
        +matches_heading
        +matches
    )

    print(final_text)
    return final_text
