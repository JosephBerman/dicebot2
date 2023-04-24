# global
import random
import sys
import bootkeys
import discord

from ..embeds import embeddHandler as embedHandle

UNUSED_DICE_DEFAULT = sys.maxsize


def initCharacters(boot, sqldb):
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
        embed = embedHandle._embedInit(ctx, title="Profile")

        sql = "INSERT INTO characters (name, " \
              "class, profiles_user_id, " \
              "strength, dexterity, " \
              "constitution, intelligence, " \
              "wisdom, charisma) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        value = [name, cl, f"{ctx.author.id}",
                 strength, dexterity,
                 constitution, intelligence,
                 wisdom, charisma]

        sqldb.insertRecord(sql, value)

        embed.add_field(name="Created new profile", value=f"{name}")

        await ctx.respond(embed=embed)

    @boot.slash_command(guild_ids=bootkeys.test_servers,
                        description="Get all your characters")
    async def get_character(
            ctx: discord.ApplicationContext,
            name: discord.Option(str, description="Name", required=True),
    ):
        embed = embedHandle._embedInit(ctx, title="Profile")

        ch = 'characters'
        pi = 'profiles_user_id'

        sql = "SELECT * FROM characters WHERE profiles_user_id LIKE %s AND name LIKE %s"

        val = [f"{ctx.author.id}", name]

        tables = sqldb.retrieveRecord(sql, val)

        embed.add_field(name="Characters", value=tables)
        await ctx.respond(embed=embed)