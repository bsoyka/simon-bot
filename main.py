from discord.ext.commands import Bot, has_role, has_any_role
from discord import Embed, Color, Member
from discord.utils import get
from asyncio import sleep
from configparser import ConfigParser
from os import getenv

from simon import Simon
from helpers import gen_embed, get_role

config = ConfigParser()
config.read("config.ini")


bot = Bot("$")


@bot.command()
@has_any_role(get_role("Admin"), get_role("Owner"))
async def setsimon(ctx, user: Member = None):
    """
    Set a user as Simon
    """
    if user == None:
        user = ctx.author

    simon_role = get(ctx.guild.roles, name=get_role("Simon"))
    player_role = get(ctx.guild.roles, name=get_role("Player"))
    loser_role = get(ctx.guild.roles, name=get_role("Loser"))
    giveaway_role = get(ctx.guild.roles, name=get_role("Giveaways"))

    await user.add_roles(simon_role, giveaway_role)
    await user.remove_roles(player_role, loser_role)

    await ctx.send("", embed=gen_embed("Updated Simon List", ", ".join(map(str, simon_role.members))))


@bot.command()
async def simon(ctx):
    """
    Get the current Simon
    """
    simon_role = get(ctx.guild.roles, name=get_role("Simon"))

    if len(simon_role.members) == 0:
        await ctx.send("", embed=gen_embed("Current Simon", f"There are currently no users with the {simon_role.mention} role."))
    else:
        await ctx.send("", embed=gen_embed("Current Simon", ", ".join(map(str, simon_role.members))))


@bot.command()
async def remaining(ctx):
    """
    Get the remaining Simon Says players
    """
    player_role = get(ctx.guild.roles, name=get_role("Player"))

    title = f"{len(player_role.members)} Player(s) Remaining"
    description = ', '.join(map(str, player_role.members))

    await ctx.send("", embed=gen_embed(title, description))


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_raw_reaction_remove(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    await get(channel.guild.channels, name=config["Channels"]["ReactionLog"]).send(f"<@{payload.user_id}> removed the reaction {payload.emoji} on this message: <{message.jump_url}>.")

bot.add_cog(Simon(bot))
bot.run(getenv("SIMON_BOT_KEY"))

