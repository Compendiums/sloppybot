import os

DISCORD_KEY = os.getenv('DISCORD_KEY')

RIOT_API_KEY = os.getenv('RIOT_API_KEY')

WORKING_DIR = os.getcwd()

PATHS = {
     'cwd':WORKING_DIR
    ,'help':os.path.join(WORKING_DIR,'helptext.txt')
    ,'version':os.path.join(WORKING_DIR, 'version.txt')
}

URL = {
     'base':'https://{REGION}.api.riotgames.com/lol'
    ,'summoner_by_name':'/summoner/v{VER}/summoners/by-name/{queryval}' #summonername
    ,'summoner_by_id':'/summoner/v{VER}/summoners/{queryval}' #SummonerId
    ,'match_by_account':'/match/v{VER}/matchlists/by-account/{queryval}?queue=700' #accountid
    ,'match_by_match':'/match/v{VER}/matches/{queryval}' #matchId
    ,'clash_by_team':'/clash/v{VER}/teams/{queryval}' #teamId
    ,'clash_by_summoner':'/clash/v{VER}/players/by-summoner/{queryval}' #summonerId
    ,'clash_tourn_by_team':'clash/v1/tournaments/by-team/{queryval}' #teamId
}

VERSION = {
     'summoner':'4'
    ,'match':'4'
    ,'clash':'1'
}

REGION = {
    'north_america':'NA1'
}

QUEUE_ID = {
    'clash':'700'
}

TEAM = {
    'sloppy_toppy':'926281'
}