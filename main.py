import datetime
import discord
from discord.ext import commands
import json
import sys

from webhook_logging import setup_logger, logger

webhook_urls = sys.argv[1:]

setup_logger(webhook_urls[0], webhook_urls[1])

file = open("env.json", 'r')
env = json.load(file)

HELP = """```
!help …… ヘルプ
!time …… 現在時刻
```"""

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.remove_command("help")

@bot.event
async def on_ready():
    logger.info("Logged in as %s" % bot.user)

@bot.event
async def on_message(message):
    if message.author.bot: return
    logger.info("%s: %s" % (message.author, message.content))

    await bot.process_commands(message)

@bot.command()
async def help(ctx):
    await ctx.send(HELP)

@bot.command()
async def time(ctx):
    await ctx.send("現在の時刻は %s です。" % nowtime().strftime('%Y/%m/%d %H:%M:%S'))

def nowtime():
    JST = datetime.timezone(datetime.timedelta(hours=9), 'JST')
    return datetime.datetime.now(JST)

bot.run(env["DISCORD_TOKEN"], log_handler=None)
