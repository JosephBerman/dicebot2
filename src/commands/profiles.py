# global
import asyncio
import random
import sys
import bootkeys
import discord
import logging
logger = logging.getLogger(__name__)

from ..embeds import embeddHandler as embedHandle
from ..database.mongoHandler import MongoHandler
from ..database.mongoHandler import MongoErr


def initProfiles(boot, mongo: MongoHandler):
    profiles = boot.create_group(
        "profile", "Profile commands"
    )

    @profiles.command(guild_ids=bootkeys.test_servers,
                      description="You must register before creating profiles")
    async def register(ctx: discord.ApplicationContext):
        await ctx.response.defer()
        embed = embedHandle.embedInit(ctx, title="Profile")

        validId = mongo.createProfile(ctx.author.id)

        if validId > 0:
            embed.add_field(name="profile added", value=validId, inline=False)
        else:
            embed.add_field(name="Error Adding Profile", value=validId, inline=False)

        await ctx.followup.send(embed=embed)


