# global
import bootkeys
import discord
import logging
logger = logging.getLogger(__name__)

# local
from .rolling import initRollingCommands
from .profiles import initProfiles
from src.commands.character.characters import initCharacters
from src.commands.character.skills import initSkills


def initCommands(boot, mongo):

    initRollingCommands(boot)  # from rolling.py
    initSkills(boot, mongo)
    initProfiles(boot, mongo)  # TODO move inits
    initCharacters(boot, mongo)

    logger.debug("Initiated all commands")

    @boot.slash_command(guild_ids=bootkeys.test_servers)
    async def ping(ctx):
        embed = discord.Embed(color=0x81a1c1)

        embed.add_field(name="Ping", value=f"You rolled **{round(boot.latency * 1000)}**ms", inline=False)

        await ctx.respond(embed=embed)

