import sys
sys.path.append('/Users/waffles/PycharmProjects/bootkeys')

import discord
import bootkeys
from src.commands import commands
from src.database import sqlHandler
UNUSED_DICE_DEFAULT = sys.maxsize

#todo make cleaner

boot = discord.Bot()

@boot.event
async def on_ready():
    print(f"We have logged in as {boot.user}")

sqldb = sqlHandler.sqlServer()

commands.initCommands(boot, sqldb)

boot.run(bootkeys.privateKey)
