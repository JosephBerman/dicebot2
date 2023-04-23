# global
import random
import sys
import secrets
import discord

# local
from .rolling import initRollingCommands


def initCommands(boot):
    initRollingCommands(boot)  # from rolling.py

    @boot.slash_command(guild_ids=secrets.test_servers)
    async def ping(ctx):
        await ctx.respond("pong")

