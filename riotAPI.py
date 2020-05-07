from settings import RIOT_API_KEY,CURR_SEASON, URL, VERSION, REGION, QUEUE_ID, CHAMP_NAME_LOOKUP
import time
import utils
import requests
from functools import lru_cache


def clashTeam_by_summoner(summonerName):

    # get summonerID
    summoner = riotRequest('north_america', 'summoner_by_name', 'summoner', summonerName)
    print(summoner)
    # get teamId
    team = riotRequest('north_america', 'clash_by_summoner', 'clash', summoner['id'])
    # get rundown
    if not team:
        return "This summoner isn't on an active team"
    else:
        clashStats = clashTeam(team['teamId'])
        return clashStats


@lru_cache(100)
def clashTeam(teamid):
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
    cptn_matches = riotRequest('north_america', 'clash_match_by_account', 'match', cptn_acct_id)
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
        cptn_part_id = getParticipantId(cptn_acct_id,match_by_match['participantIdentities'])

        #use participant id to get match win loss
        winloss = getWinloss(cptn_part_id,match_by_match['participants'])
        if winloss == 'W':
            win_count += 1

        #format time
        human_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(match['timestamp']/1000))

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


def summonerStats(summonerName):
    '''
    present name and rank
    total won an lost matches this season
    top 3 most played champs
    winrate on champ
    last 5 matches history
    '''

    #get summonerID
    summoner = riotRequest('north_america', 'summoner_by_name', 'summoner', summonerName)

    #get ranked info
    league = riotRequest('north_america', 'league_by_summoner', 'league', summoner['id'])

    if not league:
        rank = 'Unranked'
    else:
        for item in league:
            if item['queueType'] == 'RANKED_SOLO_5X5':
                rank = item['tier'] + ' ' + item['rank']

    summonerMatches = riotRequest('north_america', 'match_by_account', 'match', summoner['accountId'])

    matches = summonerMatches['matches']
    match_hist = {}
    win_count = 0
    allChamps = {}
    #get loss count by subtracting the wincount from summonerMatches[totalGames]

    for match in matches:
        match_by_match = riotRequest('north_america', 'match_by_match', 'match', match['gameId'])

        #print(match_by_match)

        #initialize variables
        part_id = 0
        winloss = ''

        #get captain's participant id
        part_id = getParticipantId(summoner['accountId'],match_by_match['participantIdentities'])

        partList = ['championId']
        statsList = ['win']

        #use participant id to get match win loss
        part_data = getParticipantData(match_by_match['participants'],part_id,partList,statsList)
        part_partData = part_data['participant']
        part_statsData = part_data['stats']

        if part_statsData['win']:
            winloss = 'W'
            win_count += 1
        else:
            winloss = 'L'

        #populate matchHist
        #format time
        human_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(match['timestamp']/1000))

        #sanity check
        if part_id != 0 and winloss != '':
            if matches.index(match) <= 4:
                match_hist.update({human_time:winloss})
        else:
            print("didn't find captains participant id or match's winloss")
            break
        
        #add champion data to to allChamps
        championId = part_partData['championId']
        championName = CHAMP_NAME_LOOKUP[championId]

        if championName in allChamps:
            champion = allChamps[championName]
            champion['total'] += 1

            if winloss == 'W':
                champion['won'] += 1
        else: 
            allChamps.update({championName:{'total':1,'won':1}})
        
    topChamps = {}
    top1={}
    top2={}
    top3={}

    for name in allChamps.keys():
        total=allChamps[name]['total']
        won=allChamps[name]['won']

        #add value if dict is empty
        if len(topChamps) == 0:
            topChamps.update({name:{'total':total,'won':won}})
            top1 = {name:total}
        #add value and reassess top1 if dict has one item
        elif len(topChamps) == 1:
            topChamps.update({name:{'total':total,'won':won}})
            if list(top1.values())[0] < total:
                top2 = top1
                top1 = {name:total}
            else:
                top2 = {name:total}
        #add value and reassess top1&2 and assign top3 if dict have 2 items
        elif len(topChamps) == 2:
            topChamps.update({name:{'total':total,'won':won}})
            if list(top2.values())[0] < total < list(top1.values())[0]:
                top3 = top2
                top2 = {name:total}
            elif list(top2.values())[0] < total:
                top3 = top2
                top2 = top1
                top1 = {name:total}
            else:
                top3 = {name:total}
        #if dict has 3 items
        elif len(topChamps) == 3:
            #if the total beats the lowest of the 3 top values, delete top3, add current item, reassess top1-3
            if (list(top3.values())[0] < total):
                topChamps.pop(list(top3)[0])
                topChamps.update({name:{'total':total,'won':won}})
                if list(top1.values())[0] < total:
                    top3 = top2
                    top2 = top1
                    top1 = {name:total}
                elif list(top2.values())[0] < total < list(top1.values())[0]:
                    top3 = top2
                    top2 = {name:total}
                else:
                    top3 = {name:total}
        #if dict has over 3 items
        else:
            print('dictionary has too many items')
            break
    
    for name in topChamps:
        champWinrate = str(int(topChamps[name]['won']/topChamps[name]['total']*100))
        topChamps[name]['won'] = champWinrate
    
    loss_count = str(len(matches)-win_count)

    summoner_data = {
        'summoner':summoner['name'],
        'rank':rank,
        'season':CURR_SEASON,
        'match_count':summonerMatches['totalGames'],
        'win_count':win_count,
        'loss_count':loss_count,
        'champ_data':topChamps,
        'matches':match_hist
    }

    summonerStats = utils.formatSummoner(summoner_data)
    return summonerStats

@utils.requestCounter
def riotRequest(region,url,version,queryval):
    #should add error handling based on the queryval data type and request response code

    args = {"api_key": RIOT_API_KEY}
    response = requests.get(URL['base'].format(REGION=REGION[region])+
                            URL[url].format(VER=VERSION[version],queryval=queryval),params=args)

    #print(response.json())
    return response.json()


def getParticipantId(accountId : str, identities : list):
    for participant in identities:
            player = participant['player']

            if player['currentAccountId'] == accountId:
                participantId = participant['participantId']
                return participantId

def getWinloss(part_id : str, participants : list):
    for participant in participants:
            if participant['participantId'] == part_id:
                stats = participant['stats']
                
                winloss = stats['win']
                if winloss == True:
                    winloss = 'W'
                else:
                    winloss = 'L'
                return winloss

def getParticipantData(participants : list, part_id : str, partKwList : list, statsKwList : list):
    #move this even higher level so it can part through the match_by_match data
    #print('in participant stats')
    for participant in participants:
            if participant['participantId'] == part_id:
                partDict = {}
                statsDict = {}
                
                for kw in partKwList:
                    #print(kw + ' ' + str(participant[kw]))
                    partDict.update({kw:participant[kw]})

                stats = participant['stats']
                for kw in statsKwList:
                    #print(kw + ' ' + str(stats[kw]))
                    statsDict.update({kw:stats[kw]})
                
                partData = {'participant':partDict,'stats':statsDict}
                #print(partData)
                #print('leaving participant stats')
                return partData