import os
import requests
from dotenv import load_dotenv

load_dotenv()
DISCORD_KEY = os.getenv('DISCORD_KEY')
RIOT_API_KEY = os.getenv('RIOT_API_KEY')

WORKING_DIR = os.getcwd()

PATHS = {
     'cwd':WORKING_DIR
    ,'help':os.path.join(WORKING_DIR,'helptext.txt')
    ,'version':os.path.join(WORKING_DIR, 'version.txt')
}

REQUEST_COUNT = 0

SEASONS = requests.get('http://static.developer.riotgames.com/docs/lol/seasons.json').json()
CURR_SEASON = SEASONS[-1]['id']

VERSION = {
     'summoner':'4'
    ,'match':'4'
    ,'clash':'1'
    ,'league':'4'
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

URL = {
     'base':'https://{REGION}.api.riotgames.com/lol'
    ,'summoner_by_name':'/summoner/v{VER}/summoners/by-name/{queryval}' #summonername
    ,'summoner_by_id':'/summoner/v{VER}/summoners/{queryval}' #SummonerId
    ,'clash_match_by_account':'/match/v{VER}/matchlists/by-account/{queryval}'+'?queue={queue}'.format(queue=QUEUE_ID['clash']) #accountid
    ,'match_by_account':'/match/v{VER}/matchlists/by-account/{queryval}'+'?endIndex=50' #accountid
    ,'match_by_match':'/match/v{VER}/matches/{queryval}' #matchId
    ,'clash_by_team':'/clash/v{VER}/teams/{queryval}' #teamId
    ,'clash_by_summoner':'/clash/v{VER}/players/by-summoner/{queryval}' #summonerId
    ,'clash_tourn_by_team':'/clash/v{VER}/tournaments/by-team/{queryval}' #teamId
    ,'league_by_summoner':'/league/v{VER}/entries/by-summoner/{queryval}' #summonerId
    ,'dd_champion':'http://ddragon.leagueoflegends.com/cdn/10.9.1/data/en_US/champion.json'
}

CHAMP_JSON = requests.get(URL['dd_champion']).json()
CHAMP_DATA = CHAMP_JSON['data']
CHAMP_NAME_LOOKUP = {}
for champ in CHAMP_DATA:
    champ_id = int(CHAMP_DATA[champ]['key'])
    champ_name = CHAMP_DATA[champ]['name']
    CHAMP_NAME_LOOKUP.update({champ_id:champ_name})

#for item in CHAMP_NAME_LOOKUP:
    #print(item + ' ' + CHAMP_NAME_LOOKUP[item])