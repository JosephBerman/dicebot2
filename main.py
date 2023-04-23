import sys

import secrets
import discord
from src.commands import commands

UNUSED_DICE_DEFAULT = sys.maxsize



boot = discord.Bot()

@boot.event
async def on_ready():
    print(f"We have logged in as {boot.user}")

commands.initCommands(boot)

boot.run(secrets.privateKey)
