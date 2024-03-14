import discord
from .._version_ import __version__
import logging

logger = logging.getLogger(__name__)


## TODO make this a class
def embedInit(ctx, title, color=0x81a1c1):
    embed = discord.Embed(title=title, color=color)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
    embed.set_footer(text=__version__)

    return embed

def embedInitMenus(interaction, title, color=0x81a1c1):
    embed = discord.Embed(title=title, color=color)
    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
    embed.set_footer(text=__version__)

    return embed

def rollInit(embed, amount, die, mod):
    embed.add_field(name=f"Dice Input:", value=f"{amount}d{die}+{mod}", inline=False)


def characterInit(embed, character: dict):
    statDict = character["stats"]
    logger.info("Got character: %s" % character)

    parsedStats = "Class: **%s**\n" \
                  "Race: **%s**\n" \
                  "Strength: **%d**\n" \
                  "Dexterity: **%d**\n" \
                  "Constitution: **%d**\n" \
                  "Intelligence: **%d**\n" \
                  "Wisdom: **%d**\n" \
                  "Charisma: **%d**\n" % (statDict["class"],
                                          statDict["race"],
                                          statDict["strength"],
                                          statDict["dexterity"],
                                          statDict["constitution"],
                                          statDict["intelligence"],
                                          statDict["wisdom"],
                                          statDict["charisma"])

    embed = embed.add_field(name="Stats:", value=parsedStats, inline=False)

    return embed
