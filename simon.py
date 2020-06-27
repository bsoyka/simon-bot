from discord import Member
from discord.utils import get
from discord.ext.commands import Cog, command, has_any_role

from helpers import gen_embed, get_role


class Simon(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=["e"])
    @has_any_role(get_role("Simon"), get_role("Admin"), get_role("Owner"))
    async def elim(self, ctx, *users: Member):
        """
        Eliminate users
        """
        player_role = get(ctx.guild.roles, name=get_role("Player"))
        loser_role = get(ctx.guild.roles, name=get_role("Loser"))

        for user in users:
            await user.remove_roles(player_role)
            await user.add_roles(loser_role)

        await ctx.send("", embed=gen_embed("Eliminated user(s)."))

    @command(aliases=["r"])
    @has_any_role(get_role("Simon"), get_role("Admin"), get_role("Owner"))
    async def revive(self, ctx, *users: Member):
        """
        Revive users
        """
        player_role = get(ctx.guild.roles, name=get_role("Player"))
        loser_role = get(ctx.guild.roles, name=get_role("Loser"))

        for user in users:
            await user.remove_roles(loser_role)
            await user.add_roles(player_role)

        await ctx.send("", embed=gen_embed("Revived user(s)."))

    @command()
    @has_any_role(get_role("Simon"), get_role("Admin"), get_role("Owner"))
    async def gameover(self, ctx):
        """
        Remove all Simon Says roles
        """
        simon_role = get(ctx.guild.roles, name=get_role("Simon"))
        player_role = get(ctx.guild.roles, name=get_role("Player"))
        loser_role = get(ctx.guild.roles, name=get_role("Loser"))
        giveaway_role = get(ctx.guild.roles, name=get_role("Giveaways"))

        total_members = 0
        lines = []

        for member in simon_role.members:
            await member.remove_roles(simon_role, giveaway_role)
            total_members += 1
            lines.append(f"Removed {simon_role.mention} and {giveaway_role.mention} roles from {member}.")

        for role in [player_role, loser_role]:
            members = 0
            for member in role.members:
                await member.remove_roles(role)
                members += 1

            if members != 0:
                total_members += members
                lines.append(f"Removed the {role.mention} role from {members} member(s).")

        if total_members == 0:
            lines.append(f"There were no roles to remove.")

        await ctx.send("", embed=gen_embed("Game Over", "\n".join(lines)))

    @command(aliases=["w"])
    @has_any_role(get_role("Simon"), get_role("Admin"), get_role("Owner"))
    async def winner(self, ctx, winner: Member):
        """
        Sets the last winner
        """
        winner_role = get(ctx.guild.roles, name=get_role("Winner"))

        for member in winner_role.members:
            await member.remove_roles(winner_role)

        await winner.add_roles(winner_role)
        await ctx.send("", embed=gen_embed(f"Set {winner} as {winner_role.name}."))