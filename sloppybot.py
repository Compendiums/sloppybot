#sloppybot.py
from settings import DISCORD_KEY, PATHS, TEAM
from discord.ext import commands
import riotAPI
import utils

#-----------------------intialize bot-----------------------#

bot = commands.Bot(
    command_prefix='!'
    ,case_insensitive=True
)

@bot.event
async def on_ready():
    print('logged in as {} with user id {}'.format(bot.user.name,bot.user.id))
    print('------')

#-----------------------/intialize bot-----------------------#

#-----------------------Commands-----------------------#

@bot.command(
    name='sloppytoppy'
    ,help='get the stats on team Sloppy Toppy. Striving for that 50% win rate!'
)
async def sloppytoppy(ctx):
    msg = riotAPI.clashTeam(TEAM['sloppy_toppy'])
    await ctx.send(msg)

@bot.command(
    name='version'
    ,help='learn about my recent changes'
)
async def version(ctx):
    msg = utils.readText(PATHS['version'])
    await ctx.send(msg)

@bot.command(
    name='clashStats'
    ,help='''get the stats on a clash team by summoner name (!clashStats Hiitman).
    Use quotes for summoner names with multiple words (!clashStats "Meme Weaver")'''
)
async def clashStats(ctx, summonerName):
    name = ctx.message.author
    msg = riotAPI.clashTeam_by_summoner(summonerName)
    await ctx.send(msg)

@bot.command(
    name='summoner'
    ,help='get the stats on a summoner. Use quotes for summoner names with multiple words (!summoner "Meme Weaver")'
)
async def summoner(ctx, summonerName):
    #author = ctx.message.author.mention()
    disclaimer = "{author} This could take a minute, riot's stingy with their api limits".format(author=ctx.message.author.mention)
    await ctx.send(disclaimer)
    msg = riotAPI.summonerStats(summonerName)
    await ctx.send(msg)

#-----------------------/Commands-----------------------#

if __name__ == '__main__':
    
    bot.run(DISCORD_KEY)
