from Settings import DISCORD_KEY, RIOT_API_KEY, PATHS, URL, VERSION, REGION, QUEUE_ID, TEAM
import requests
import time
import discord

'''
#print(URL['base'].format(REGION=REGION['north_america'])+URL['summoner_by_name'].format(VER=VERSION['summoner'],summonername='compendium'))

response = requests.get(URL['base'].format(REGION=REGION['north_america'])+URL['summoner_by_name'].format(VER=VERSION['summoner'],summonername='compendium',api_key=API_KEY['compendium']))

print(response.json())

class MatchGrabber:

    def __init__(self, region=REGION['north_america']):
        self.region = region

    def _request():
            #take everything, put it in a request, output results readibly(maybe another function)
            response = request.get(URL['base'].format+URL['summoner_by_name'].format(VER=VERSION['summoner'],summonername='compendium')'''

def readText(path):
    text = open(path,'r')
    return text.read()

def request(region,url,version,keyname,queryval):
    #should add error handling based on the queryval data type and request response code
    #print(URL['base'].format(REGION=REGION[region]) +
    #URL[url].format(VER=VERSION[version], queryval=queryval))

    args = {"api_key": RIOT_API_KEY}
    response = requests.get(URL['base'].format(REGION=REGION[region])+
                            URL[url].format(VER=VERSION[version],queryval=queryval),params=args)

    #print(response.json())
    return response.json()

def matchInfo():
    #run requests, compile the info
    clash_team = request('north_america', 'clash_by_team', 'clash', 'compendium', TEAM['sloppy_toppy'])

    #set vars
    team_name = clash_team['name']
    team_tier = clash_team['tier']
    team_players = clash_team['players']

    cptn_acct_id = 0

    match_ids = []

    #print(team_players)

    for playerDto in team_players:
        summoner = request('north_america', 'summoner_by_id', 'summoner', 'compendium', playerDto['summonerId'])
        #print(summoner)
        if playerDto['role'] == 'CAPTAIN':
            cptn_acct_id = summoner['accountId']
        playerDto['summonerId'] = summoner['name']

    #can assume the matches are returned newest to oldest - index also goes 0-newest 0+n-older
    cptn_matches = request('north_america', 'match_by_account', 'match', 'compendium', cptn_acct_id)
    #print(cptn_matches)

    matches = cptn_matches['matches']
    match_hist = {}
    win_count = 0

    for match in matches:
        match_by_match = request('north_america', 'match_by_match', 'match', 'compendium', match['gameId'])

        #print(match_by_match)

        #initialize variable
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
        epoch_time = match['timestamp']/1000
        #print(type(epoch_time))
        #print(time.localtime(epoch_time))
        human_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))
        #record in match_hist dict
        if cptn_part_id != 0 and winloss != '':
            if matches.index(match) <= 4:
                match_hist.update({human_time:winloss})
        else:
            print('something fucked up')
            break

    #print(match_hist)

    print(win_count)
    print(len(matches))
    winrate = win_count/len(matches)*100
    winrate_str = str(int(winrate))+'%\n'
    print(winrate)

    sloppydata = {
        'team':team_name,
        'tier':team_tier,
        'players':team_players,
        'winrate':winrate_str,
        'matches':match_hist
    }

    print(sloppydata)
    return sloppydata

def formatter(team_dict={}):
    heading = '**{team}**    tier {tier}\n'.format(team=team_dict['team'],tier=team_dict['tier'])
    seperator = '**--------------------------------**\n'

    members = ''
    players_dict = team_dict['players']

    for player in players_dict:
        members += '**{name}**     {position}\n'.format(name=player['summonerId'],position=player['position'])

    winrate = '**win rate**: '+team_dict['winrate']

    #print(members)
    #print(seperator)

    matches_heading = '**Match History**\n'

    matches = ''
    matches_dict = team_dict['matches']

    for date,winloss in matches_dict.items():
        matches += '{date}     {winloss}\n'.format(date=date,winloss=winloss)

    final_text = heading+seperator+members+seperator+winrate+seperator+matches_heading+matches
    print(final_text)
    return final_text

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!sloppytoppy'):
        sloppydata = matchInfo()
        msg = formatter(sloppydata)
        await message.channel.send(msg)
    if message.content.startswith('!help'):
        msg = readText(PATHS['help'])
        await message.channel.send(msg)
    if message.content.startswith('!version'):
        msg = readText(PATHS['version'])
        await message.channel.send(msg)


@client.event
async def on_ready():
    print('logged in as {} with user id {}'.format(client.user.name,client.user.id))
    print('------')

if __name__ == '__main__':

    client.run(DISCORD_KEY)



