# global
import random
import sys
import bootkeys
import discord

from ..embeds import embeddHandler as embedHandle

UNUSED_DICE_DEFAULT = sys.maxsize

profile_options = ["Create", "Edit", "Delete"]


def initProfiles(boot, sqldb):
    @boot.slash_command(guild_ids=bootkeys.test_servers,
                        description="Create, view, or delete user profile")
    async def profile(
            ctx: discord.ApplicationContext,
            options: discord.Option(str, choices=profile_options,
                                    description="Create, Edit, or Delete profiles",
                                    required=False),

    ):
        embed = embedHandle._embedInit(ctx, title="Profile")

        print(options)
        if options == profile_options[0]:
            sql = "INSERT INTO profiles (user_id) VALUES (%s)"
            value = [f'{ctx.author.id}']

            sqldb.insertRecord(sql, value)
            embed.add_field(name="Created new profile", value=f"{options}")

        await ctx.respond(embed=embed)
