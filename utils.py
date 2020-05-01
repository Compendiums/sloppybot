import functools
import time

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