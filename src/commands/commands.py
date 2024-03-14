# global
import random
import sys
import bootkeys
import discord
import logging
logger = logging.getLogger(__name__)

# local
from . import d4, d6, d8, d10, d12, d20
from .rolling import initRollingCommands
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

    save_types = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]



    # TODO move this to a better position? Also change how get active character is done
    @boot.slash_command(guild_ids=bootkeys.test_servers,
                        description="Roll with Active Character skill")
    async def saving(
            ctx: discord.ApplicationContext,
            save: discord.Option(str, choices=save_types, description="Save to check", required=True),
    ):

        await ctx.response.defer()

        embed = embedHandle.embedInit(ctx, title="Saving Throw")
        active = mongo.getActiveCharacter(ctx.author.id)

        activeSkill = active["stats"][save.lower()]

        logger.debug("Active character's %s: %d" % (save, activeSkill))

        if activeSkill == MongoErr.EMPTY:
            logger.debug("Could not find character")
            embed.add_field(name="Active Character", value="Could not find character")

        if activeSkill:
            logger.debug("Found active character")

            roll = d20()

            mod = (activeSkill-10)//2

            result = int(roll + mod)

            embed.add_field(name=save,
                            value="%s rolled a %d + %d (%s) for a total __**%d**__"
                                  % (active["name"], roll, mod, activeSkill, result))

        await ctx.followup.send(embed=embed)



    skillList = [
        "Acrobatics",
        "Animal Handling",
        "Arcana" ,
        "Athletics",
        "Deception",
        "History",
        "Insight",
        "Intimidation",
        "Investigation",
        "Medicine",
        "Nature",
        "Perception",
        "Performance",
        "Persuasion",
        "Religion",
        "Sleight of Hand",
        "Stealth",
        "Survival"
    ]
    selectOptions = []
    for i in skillList:
        selectOptions.append(
            discord.SelectOption(
                label=i
            )
        )

    #TODO link this to monogo
    #TODO find a better location for these functions
    #TODO make it respond so only uesr can see it
    class skillView(discord.ui.View):
        @discord.ui.select(
            placeholder="Skills",
            min_values=0,
            max_values=18,
            options=selectOptions
        )
        async def select_callback(self, select, interaction):
            logger.debug(f"Got selected skills {select.values}\n")
            embed = embedHandle.embedInitMenus(interaction, title="Skill Selector")
            embed.add_field(name="Selected Skill", value=select.values)
            await interaction.response.send_message(embed=embed)

    @boot.slash_command(guild_ids=bootkeys.test_servers,
                        description="Menu select")
    async def set_skills(
            ctx: discord.ApplicationContext,
    ):
        logger.debug("Skill select")
        embed = embedHandle.embedInit(ctx, title="Select the skills you are proficient in")
        await ctx.send(embed=embed, view=skillView())





    # TODO change skills to list of skills, need to add proficeincies and skills to base of character stats
    # async def skill(
    #         ctx: discord.ApplicationContext,
    #         skill: discord.Option(str, choices=skill_types, description="Skill to check", required=True),
    # ):
    #
    #     await ctx.response.defer()
    #
    #     embed = embedHandle.embedInit(ctx, title="Skill check")
    #     active = mongo.getActiveCharacter(ctx.author.id)
    #
    #     activeSkill = active["stats"][skill.lower()]
    #
    #     logger.debug("Active character's %s: %d" % (skill, activeSkill))
    #
    #     if activeSkill == MongoErr.EMPTY:
    #         logger.debug("Could not find character")
    #         embed.add_field(name="Active Character", value="Could not find character")
    #
    #     if activeSkill:
    #         logger.debug("Found active character")
    #
    #         roll = rolling.d20()
    #
    #         mod = (activeSkill - 10) // 2
    #
    #         result = int(roll + mod)
    #
    #         embed.add_field(name=skill,
    #                         value="%s rolled a %d + %d (%s) for a total __**%d**__"
    #                               % (active["name"], roll, mod, activeSkill, result))
    #
    #     await ctx.followup.send(embed=embed)
