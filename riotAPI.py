from settings import RIOT_API_KEY, URL, VERSION, REGION, QUEUE_ID
from datetime import datetime #figure out how to import just the one function you need
import utils
import requests
from functools import lru_cache


def riotRequest(region,url,version,queryval):
    #should add error handling based on the queryval data type and request response code

    args = {"api_key": RIOT_API_KEY}
    response = requests.get(URL['base'].format(REGION=REGION[region])+
                            URL[url].format(VER=VERSION[version],queryval=queryval),params=args)

    #print(response.json())
    return response.json()

@lru_cache(100)
def clashStats(teamid):
    #run requests, compile the info
    clash_team = riotRequest('north_america', 'clash_by_team', 'clash', teamid)

    #set vars
    team_name = clash_team['name']
    team_tier = clash_team['tier']
    team_players = clash_team['players']

    cptn_acct_id = 0

    match_ids = []

    #print(team_players)

    for playerDto in team_players:
        summoner = riotRequest('north_america', 'summoner_by_id', 'summoner', playerDto['summonerId'])
        #print(summoner)
        if playerDto['role'] == 'CAPTAIN':
            cptn_acct_id = summoner['accountId']
        playerDto['summonerId'] = summoner['name']

    #can assume the matches are returned newest to oldest - index also goes 0-newest 0+n-older
    cptn_matches = riotRequest('north_america', 'match_by_account', 'match', cptn_acct_id)
    #print(cptn_matches)

    matches = cptn_matches['matches']
    match_hist = {}
    win_count = 0

    for match in matches:

        match_by_match = riotRequest('north_america', 'match_by_match', 'match', match['gameId'])

        #print(match_by_match)

        #initialize variables
        cptn_part_id = 0
        winloss = ''

        #get captain's participant id
        for participant in match_by_match['participantIdentities']:
            player = participant['player']

            if player['currentAccountId'] == cptn_acct_id:
                cptn_part_id = participant['participantId']

        #use participant id to get match win loss
        for participant in match_by_match['participants']:
            if participant['participantId'] == cptn_part_id:
                stats = participant['stats']
                if stats['win'] == True:
                    winloss = 'W'
                    win_count += 1
                else:
                    winloss = 'L'

        #format time
        human_time = datetime.fromtimestamp(match['timestamp']/1000)

        #sanity check
        if cptn_part_id != 0 and winloss != '':
            if matches.index(match) <= 4:
                match_hist.update({human_time:winloss})
        else:
            print("didn't find captains participant id or match's winloss")
            break

    winrate = str(int(win_count/len(matches)*100))+'%\n'

    team_data = {
        'team':team_name,
        'tier':team_tier,
        'players':team_players,
        'winrate':winrate,
        'matches':match_hist
    }

    clash_stats = utils.formatClashStats(team_data)
    return clash_stats

