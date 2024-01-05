# global
import random
import sys
import bootkeys
import discord
import logging
logger = logging.getLogger(__name__)

# local
from .rolling import initRollingCommands, _roll
from .profiles import initProfiles
from .characters import initCharacters
from ..embeds import embeddHandler as embedHandle
from ..database.mongoHandler import MongoHandler
from ..database.mongoHandler import MongoErr


def initCommands(boot, mongo):
    initRollingCommands(boot)  # from rolling.py

    initProfiles(boot, mongo)  # TODO move inits
    initCharacters(boot, mongo)

    logger.debug("Initiated all commands")

    @boot.slash_command(guild_ids=bootkeys.test_servers)
    async def ping(ctx):
        embed = discord.Embed(color=0x81a1c1)

        embed.add_field(name="Ping", value=f"You rolled **{round(boot.latency * 1000)}**ms", inline=False)

        await ctx.respond(embed=embed)

    skill_types = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

    # TODO move this to a better position? Also change how get active character is done
    @boot.slash_command(guild_ids=bootkeys.test_servers,
                        description="Roll with Active Character skill")
    async def skill(
            ctx: discord.ApplicationContext,
            skill: discord.Option(str, choices=skill_types, description="Skill to check", required=True),
    ):

        await ctx.response.defer()

        embed = embedHandle.embedInit(ctx, title="Skill check")
        active = mongo.getActiveCharacter(ctx.author.id)
        logger.info(active)
        activeSkill = active["stats"][skill.lower()]

        logger.debug("Active character's %s: %d" % (skill, activeSkill))

        if activeSkill == MongoErr.EMPTY:
            logger.debug("Could not find character")
            embed.add_field(name="Active Character", value="Could not find character")

        if activeSkill:
            logger.debug("Found active character")

            roll = random.randint(1, 20)

            mod = (activeSkill-10)//2

            result = int(roll + mod)

            embed.add_field(name=skill,
                            value="%s rolled a %d + %d (%s) for a total __**%d**__"
                                  % (active["name"], roll, mod, activeSkill, result))

        await ctx.followup.send(embed=embed)
