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
    @boot.slash_command(guild_ids=bootkeys.test_servers,
                        description="Create new character")
    async def new_character(
            ctx: discord.ApplicationContext,
            name: discord.Option(str, description="Name", required=True),
            cl: discord.Option(str, name="class", description="Class", required=True),

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
            "Class": cl,
            "Strength": strength,
            "Dexterity": dexterity,
            "Constitution": constitution,
            "Intelligence": intelligence,
            "Wisdom": wisdom,
            "Charisma": charisma
        }


        mongo.createCharacter(uid=ctx.author.id, name=name, stats=stats)

        embed.add_field(name="Created new character", value=f"{name}")

        await ctx.followup.send(embed=embed)

    @boot.slash_command(guild_ids=bootkeys.test_servers,
                        description="Get all your characters")
    async def get_character(
            ctx: discord.ApplicationContext,
            name: discord.Option(str, description="Name", required=True),
    ):
        await ctx.response.defer()
        embed = embedHandle.embedInit(ctx, title="Profile")

        character = mongo.getCharacter(uid=ctx.author.id, name=name)
        logger.info(character)
        #embed.add_field(name="Characters", value=character)
        logger.info("Got Character")
        await ctx.followup.send(embed=embed)
