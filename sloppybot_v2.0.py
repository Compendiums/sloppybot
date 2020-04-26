#sloppybot_v2.0.pys
from settings import DISCORD_KEY, PATHS, TEAM
from discord.ext import commands
import riotAPI
import utils

#-----------------------intialize bot-----------------------#

bot = commands.Bot(
    command_prefix='!'
    ,case_insensitive=True
)

#-----------------------/intialize bot-----------------------#

#-----------------------Commands-----------------------#

@bot.command(
    name='sloppytoppy'
    ,help='get the stats on team Sloppy Toppy. Striving for that 50% win rate!'
)
async def sloppytoppy(ctx):
    msg = riotAPI.clashStats(TEAM['sloppy_toppy'])
    await ctx.send(msg)

@bot.command(
    name='version'
    ,help='learn about my recent changes'
)
async def version(ctx):
    msg = utils.readText(PATHS['version'])
    await ctx.send(msg)


@bot.event
async def on_ready():
    print('logged in as {} with user id {}'.format(bot.user.name,bot.user.id))
    print('------')

#-----------------------/Commands-----------------------#

if __name__ == '__main__':
    
    bot.run(DISCORD_KEY)