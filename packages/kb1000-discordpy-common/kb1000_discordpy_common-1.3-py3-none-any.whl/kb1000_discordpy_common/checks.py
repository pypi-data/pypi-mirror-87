import functools
import typing

from discord.ext import commands


@functools.lru_cache(maxsize=None)
def in_guild(id_: int) -> typing.Callable[[commands.Command], commands.Command]:
    # this decorator turns this into a decorator itself
    @commands.check
    def actual_check(ctx: commands.Context) -> bool:
        return ctx.guild.id == id_
    return actual_check
