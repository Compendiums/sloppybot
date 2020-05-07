import functools
import time
import settings

def readText(path):
    text = open(path,'r')
    return text.read()


def formatSummoner(summoner_dict : dict):
    seperator = '**--------------------------------**\n'

    heading = '**{summoner}**    {rank}\n'.format(summoner=summoner_dict['summoner'],rank=summoner_dict['rank'])

    overview_heading = seperator + '**Season {season} Matches:** {total}\n'.format(season=summoner_dict['season'],total=summoner_dict['match_count'])
    overview = 'Last 50 matches:\n    W: {won}    L: {lost}\n'.format(won=summoner_dict['win_count'],lost=summoner_dict['loss_count'])

    champ_heading = seperator + '**Top Played Champions:**\n'
    
    champ_data = summoner_dict['champ_data']
    champ=''
    for data in champ_data:
        champ += data+'\n    Matches: {count}    Win Rate: {winrate}%\n'.format(count=champ_data[data]['total'],winrate=champ_data[data]['won'])

    
    matches_heading = seperator + '**Match History**\n'

    matches_dict = summoner_dict['matches']
    matches = ''
    for date,winloss in matches_dict.items():
        matches += '{date}     {winloss}\n'.format(date=date,winloss=winloss)

    final_text = (
        heading
        +overview_heading
        +overview
        +champ_heading
        +champ
        +matches_heading
        +matches
    )

    print(final_text)
    return final_text

def formatClashStats(team_dict : dict): #can probably use automatic dictionary unpacking here
    
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

def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer

def requestCounter(func):
    """Every 50 requests, wait 2 mins"""
    @functools.wraps(func)
    def wrapper_counter(*args, **kwargs):
        if settings.REQUEST_COUNT >= 98:
            print('waiting 2 minutes')
            time.sleep(60)
            settings.REQUEST_COUNT = 0
        else:
            settings.REQUEST_COUNT += 1
            #print("request count is " + str(settings.REQUEST_COUNT))
        value = func(*args, **kwargs)
        return value
    return wrapper_counter