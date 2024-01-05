# global
import random
import sys
import bootkeys
import discord
import logging
logger = logging.getLogger(__name__)

from ..embeds import embeddHandler as embedHandle


def _roll(amount, die, total, embedMessage):
    for i in range(amount):
        result = random.randint(1, die)
        total += result
        embedMessage = embedMessage + f"On die {i + 1} of {amount}d{die}: **{result}**\n"
    return total, embedMessage


def initRollingCommands(boot):
    @boot.slash_command(guild_ids=bootkeys.test_servers,
                        description="Roll multiple types of dice")
    async def rollmulti(
            ctx: discord.ApplicationContext,
            die1amount: discord.Option(int, description="Amount of dice to roll", min_value=1, required=True),
            die1size: discord.Option(int, description="Sides on die", min_value=1, required=True),
            modifier: discord.Option(int, description="Modifier", default=0, required=True),
            die2amount: discord.Option(int, description="Amount of dice to roll on die 2",
                                       default=None,
                                       required=False, min_value=1),
            die2size: discord.Option(int, description="Sides on die 2", default=None, min_value=1),
            die3amount: discord.Option(int, description="Amount of dice to roll on die 3",
                                       default=None,
                                       required=False, min_value=1),
            die3size: discord.Option(int, description="Sides on die 3", default=None, min_value=1),
            die4amount: discord.Option(int, description="Amount of dice to roll on die 4",
                                       default=None,
                                       required=False, min_value=1),
            die4size: discord.Option(int, description="Sides on die 4", default=None, min_value=1),
            die5amount: discord.Option(int, description="Amount of dice to roll on die 5",
                                       default=None,
                                       required=False, min_value=1),
            die5size: discord.Option(int, description="Sides on die 5", default=None, min_value=1)
    ):
        dice = [die1size, die2size, die3size, die4size, die5size]
        amounts = [die1amount, die2amount, die3amount, die4amount, die5amount]

        embed = embedHandle.embedInit(ctx, "Multiple Dice Roll")

        total = 0
        for j in range(len(dice)):
            embedMessage = ""
            if dice[j] is not None and amounts[j] is not None:
                total, embedMessage = _roll(amounts[j], dice[j], total, embedMessage)
                embed.add_field(name=f"Die {j + 1}: {amounts[j]}d{dice[j]}", value=embedMessage, inline=False)
            if amounts[j] is None and dice[j] is not None:
                embed.add_field(name=f"Die {j + 1}", value=f"Requires amount of sides on die {j + 1}", inline=False)
            if dice[j] is None and amounts[j] is not None:
                embed.add_field(name=f"Die {j + 1}", value=f"Requires amount of dice {j + 1}", inline=False)

        embed.add_field(name=f"Total", value=f"**{total}** + {modifier} = __**{total + modifier}**__", inline=False)

        embed.set_footer(text="dicebot 2.0.0-alpha")

        await ctx.respond(embed=embed)

    @boot.slash_command(guild_ids=bootkeys.test_servers,
                        description="Roll one type of dice")
    async def roll(
            ctx: discord.ApplicationContext,
            amount: discord.Option(int, description="Amount of dice to roll", min_value=1, required=True),
            die: discord.Option(int, description="Sides on die", min_value=1, required=True),
            modifier: discord.Option(int, description="Modifier", required=True),
    ):
        embed = embedHandle.embedInit(ctx, "Dice Roll")
        embedHandle._rollInit(embed, amount, die, modifier)

        total = 0

        total, embedMessage = _roll(amount, die, total, "")
        embed.add_field(name=f"Die 1", value=embedMessage, inline=False)

        embed.add_field(name=f"Total", value=f"**{total}** + {modifier} = __**{total + modifier}**__", inline=False)

        await ctx.respond(embed=embed)

    @boot.slash_command(guild_ids=bootkeys.test_servers,
                        description="Roll with advantage")
    async def advantage(
            ctx: discord.ApplicationContext,
            modifier: discord.Option(int, description="Modifier", required=True),
    ):

        amount = 2
        die = 20

        embed = embedHandle.embedInit(ctx, "Advantage")
        embedHandle._rollInit(embed, amount, die, modifier)

        total = 0
        embedMessage = ""
        rolls = []
        for i in range(2):
            rolls.append(random.randint(1, 20))
            embedMessage = embedMessage + f"On die {i + 1} of 2d20: **{rolls[i]}**\n"

        roll = 0
        if rolls[0] >= rolls[1]:
            roll = rolls[0]
            embedMessage = embedMessage + f"Selecting die 1 of 2d20: **{rolls[0]}**\n"
        else:
            roll = rolls[1]
            embedMessage = embedMessage + f"Selecting die 2 of 2d20: **{rolls[1]}**\n"

        embed.add_field(name=f"Die 1", value=embedMessage, inline=False)

        embed.add_field(name=f"Total", value=f"**{roll}** + {modifier} = __**{roll + modifier}**__", inline=False)

        await ctx.respond(embed=embed)

    @boot.slash_command(guild_ids=bootkeys.test_servers,
                        description="Roll with disadvantage")
    async def disadvantage(
            ctx: discord.ApplicationContext,
            modifier: discord.Option(int, description="Modifier", required=True),
    ):

        amount = 2
        die = 20

        embed = embedHandle.embedInit(ctx, "Disadvantage")
        embedHandle._rollInit(embed, amount, die, modifier)

        total = 0
        embedMessage = ""
        rolls = []
        for i in range(2):
            rolls.append(random.randint(1, 20))
            embedMessage = embedMessage + f"On die {i + 1} of 2d20: **{rolls[i]}**\n"

        roll = 0
        if rolls[0] <= rolls[1]:
            roll = rolls[0]
            embedMessage = embedMessage + f"Selecting die 1 of 2d20: **{rolls[0]}**\n"
        else:
            roll = rolls[1]
            embedMessage = embedMessage + f"Selecting die 2 of 2d20: **{rolls[1]}**\n"

        embed.add_field(name=f"Die 1", value=embedMessage, inline=False)

        embed.add_field(name=f"Total", value=f"**{roll}** + {modifier} = __**{roll + modifier}**__", inline=False)

        await ctx.respond(embed=embed)

    @boot.slash_command(guild_ids=bootkeys.test_servers,
                        description="Roll for initiative with Dexterity")
    async def initiative(

            ctx: discord.ApplicationContext,
            dex: discord.Option(int, description="Dexterity Modifier", required=True),
    ):

        amount = 1
        die = 20

        embed = embedHandle.embedInit(ctx, "Initiative")
        embedHandle._rollInit(embed, amount, die, dex)

        total = 0
        embedMessage = ""
        total, embedMessage = _roll(amount, die, total, embedMessage)
        embed.add_field(name=f"Die 1", value=embedMessage, inline=False)

        embed.add_field(name=f"Total", value=f"**{total}** + {dex} = __**{total + dex}**__", inline=False)

        await ctx.respond(embed=embed)
