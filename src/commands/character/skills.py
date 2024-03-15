# global
import random
import sys
import bootkeys
import discord
import logging

logger = logging.getLogger(__name__)

from src.commands import d4, d6, d8, d10, d12, d20
from src.commands.rolling import initRollingCommands
from src.embeds import embeddHandler as embedHandle
from src.database.mongoHandler import MongoHandler
from src.database.mongoHandler import MongoErr

base_stats = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]


def initSkills(boot, mongo: MongoHandler):
    # TODO change this to options from skill commands. Personal preference
    skillCommands = boot.create_group(
        "skill", "Skill commands"
    )
    skillList = [
        "Acrobatics",
        "Animal Handling",
        "Arcana",
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

    # TODO move this to a better position? Also change how get active character is done
    @skillCommands.command(guild_ids=bootkeys.test_servers,
                           description="Roll with Active Character skill")
    async def saving(
            ctx: discord.ApplicationContext,
            save: discord.Option(str, choices=base_stats, description="Save to check", required=True),
    ):
        await ctx.response.defer()

        embed = embedHandle.embedInitCxt(ctx, title="Saving Throw")
        active = mongo.getActiveCharacter(ctx.author.id)

        activeSkill = active["stats"][save.lower()]

        logger.debug("Active character's %s: %d" % (save, activeSkill))

        if activeSkill == MongoErr.EMPTY:
            logger.debug("Could not find character")
            embed.add_field(name="Active Character", value="Could not find character")

        if activeSkill:
            logger.debug("Found active character")

            roll = d20()

            mod = (activeSkill - 10) // 2

            result = int(roll + mod)

            embed.add_field(name=save,
                            value="%s rolled a %d + %d (%s) for a total __**%d**__"
                                  % (active["name"], roll, mod, activeSkill, result))

        await ctx.followup.send(embed=embed)

    # TODO link this to monogo
    # TODO make it respond so only uesr can see it
    class skillView(discord.ui.View):
        @discord.ui.select(
            placeholder="Skills",
            min_values=0,
            max_values=18,
            options=selectOptions
        )
        async def select_callback(self, select, interaction):
            logger.debug(f"Got selected skills {select.values}\n")
            embed = embedHandle.embedInitCallBacks(interaction, title="Skill Selector")
            embed.add_field(name="Selected Skill", value=select.values)
            await interaction.response.send_message(embed=embed)

    @skillCommands.command(guild_ids=bootkeys.test_servers,
                           description="Menu select")
    async def set_skills(
            ctx: discord.ApplicationContext,
    ):
        logger.debug("Skill select")
        embed = embedHandle.embedInitCxt(ctx, title="Select the skills you are proficient in")
        await ctx.send(embed=embed, view=skillView())

    #   Need to find a way to dynamically check their active skills so they can change expertise
    #   Thinking of pulling stats from mongo and having the class view being defined and have the life of the function
    #

    # TODO implement
    # @skillCommands.command(guild_ids=bootkeys.test_servers,
    #                        description="Roll skill with advantage")
    # async def advantage(
    #         ctx: discord.ApplicationContext,
    #         #TODO decide how to choose between skill or save
    #         save: discord.Option(str, choices=base_stats, description="Save to check", required=True),
    # ):

    # TODO implement
    # @skillCommands.command(guild_ids=bootkeys.test_servers,
    #                        description="Roll skill with disadvantage")
    # async def disadvantage(
    #         ctx: discord.ApplicationContext,
    #         #TODO decide how to choose between skill or save
    #         save: discord.Option(str, choices=base_stats, description="Save to check", required=True),
    # ):


    # TODO change skills to list of skills, need to add proficeincies and skills to base of character stats
    # async def skill(
    #         ctx: discord.ApplicationContext,
    #         skill: discord.Option(str, choices=skill_types, description="Skill to check", required=True),
    # ):
    #
    #     await ctx.response.defer()
    #
    #     embed = embedHandle.embedInitCxt(ctx, title="Skill check")
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
