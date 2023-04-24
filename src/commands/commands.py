# global
import random
import sys
import bootkeys
import discord

# local
from .rolling import initRollingCommands
from .profiles import initProfiles
from .characters import initCharacters
from ..embeds import embeddHandler as embedHandle

def initCommands(boot, sqldb):
    initRollingCommands(boot, sqldb)  # from rolling.py
    initProfiles(boot, sqldb)
    initCharacters(boot, sqldb)

    @boot.slash_command(guild_ids=bootkeys.test_servers)
    async def ping(ctx):
        embed = discord.Embed(color=0x81a1c1)

        embed.add_field(name="Ping", value=f"You rolled **{round(boot.latency * 1000)}**ms", inline=False)

        await ctx.respond(embed=embed)




    skill_types = ["Strength","Dexterity","Constitution","Intelligence","Wisdom","Charisma"]

    @boot.slash_command(guild_ids=bootkeys.test_servers,
                        description="Roll with advantage")
    async def skill(
            ctx: discord.ApplicationContext,
            skill: discord.Option(str, choices=skill_types, description="Skill to check", required=True),
    ):



        await ctx.respond(skill)
