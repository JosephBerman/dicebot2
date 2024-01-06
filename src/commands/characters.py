# global
import random
import sys
import bootkeys
import discord
import logging

logger = logging.getLogger(__name__)

from ..embeds import embeddHandler as embedHandle
from ..database.mongoHandler import MongoHandler
from ..database.mongoHandler import MongoErr


def initCharacters(boot, mongo: MongoHandler):
    # TODO change this to options from character commands. Personal preference
    characterCommands = boot.create_group(
        "character", "Character commands"
    )

    @characterCommands.command(guild_ids=bootkeys.test_servers,
                       description="Create new character")
    async def new(
            ctx: discord.ApplicationContext,
            name: discord.Option(str, description="Name", required=True),
            cl: discord.Option(str, name="class", description="Class", required=True),
            race: discord.Option(str, description="Race", required=True),
            strength: discord.Option(int, description="Strength", required=True),
            dexterity: discord.Option(int, description="Dexterity", required=True),
            constitution: discord.Option(int, description="Constitution", required=True),
            intelligence: discord.Option(int, description="Intelligence", required=True),
            wisdom: discord.Option(int, description="Wisdom", required=True),
            charisma: discord.Option(int, description="Charisma", required=True),
    ):
        await ctx.response.defer()

        embed = embedHandle.embedInit(ctx, title="Character")

        stats = {
            "class": cl,
            "race": race,
            "strength": strength,
            "dexterity": dexterity,
            "constitution": constitution,
            "intelligence": intelligence,
            "wisdom": wisdom,
            "charisma": charisma
        }

        mongo.insertCharacter(uid=ctx.author.id, name=name, stats=stats)

        embed.add_field(name="Created new character", value=f"{name}")

        await ctx.followup.send(embed=embed)

    @characterCommands.command(guild_ids=bootkeys.test_servers,
                       description="Set your active character")
    async def set_active(
            ctx: discord.ApplicationContext,
            name: discord.Option(str, description="Name", required=True),
    ):
        await ctx.response.defer()

        embed = embedHandle.embedInit(ctx, title="Set Active Character")

        if mongo.setActiveCharacter(ctx.author.id, name) == MongoErr.SUCCESS:
            logger.debug("Found and setting active character")
            embed.add_field(name="Active Character", value="Set active character to **%s**" % name)
        else:
            logger.debug("Could not find character")
            embed.add_field(name="Active Character", value="Could not find character")


        await ctx.followup.send(embed=embed)

    @characterCommands.command(name="active",
                       guild_ids=bootkeys.test_servers,
                       description="Get your active character")
    async def active_character(
            ctx: discord.ApplicationContext,
    ):
        await ctx.response.defer()

        embed = embedHandle.embedInit(ctx, title="Get Active Character")
        active = mongo.getActiveCharacter(ctx.author.id)["name"]

        logger.debug("active character name: %s" % active)

        if active == MongoErr.EMPTY:
            logger.debug("Could not find character")
            embed.add_field(name="Active Character", value="Could not find character")

        if active:
            logger.debug("Found active character")
            embed.add_field(name="Active Character", value="Your active character is **%s**" % active)

        await ctx.followup.send(embed=embed)

    async def getCharacterList(ctx: discord.AutocompleteContext):

        logger.info("In Get Character List")
        characters = mongo.getCharacterNames(uid=ctx.interaction.user.id)
        logger.info("Got characters %s" % characters)

        return characters

    @characterCommands.command(guild_ids=bootkeys.test_servers,
                       description="Look up your character by name")
    async def search(
            ctx: discord.ApplicationContext,
            choice: discord.Option(str, "Pick your character", autocomplete=getCharacterList)
    ):
        await ctx.response.defer()

        embed = embedHandle.embedInit(ctx, title=choice)

        character = mongo.getCharacter(ctx.author.id, choice)

        embed = embedHandle.characterInit(embed, character)
        await ctx.followup.send(embed=embed)



