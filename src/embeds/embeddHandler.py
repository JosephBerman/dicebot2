import discord
from .._version_ import __version__


def _embedInit(ctx, title, color=0x81a1c1):
    test = discord.ApplicationContext

    embed = discord.Embed(title=title, color=color)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
    embed.set_footer(text=__version__)

    return embed

def _rollInit(embed, amount, die, mod):

    embed.add_field(name=f"Dice Input:", value=f"{amount}d{die}+{mod}", inline=False)
