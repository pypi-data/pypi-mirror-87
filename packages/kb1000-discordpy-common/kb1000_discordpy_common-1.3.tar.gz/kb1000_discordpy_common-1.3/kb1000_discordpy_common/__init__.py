import asyncio
import functools
import logging
import discord
import os
from discord.ext import commands

logger = logging.getLogger(__name__)


def force_async(coro):
    """\
    Small decorator to trick asyncio to identify Cython coroutines
    .. warning:: Never compile this with Cython!
    """
    if asyncio.iscoroutinefunction(coro):
        return coro

    @functools.wraps(coro)
    async def new_coro(*args, **kwargs):
        return await coro(*args, **kwargs)

    return new_coro


def log_exception(coro, exception=Exception, prefix=""):
    logger = logging.getLogger(prefix + coro.__module__)

    @force_async  # in case this is compiled using Cython...
    @functools.wraps(coro)
    async def new_coro(*args, **kwargs):
        try:
            return await coro(*args, **kwargs)
        except exception as e:
            logger.error(
                f"Exception caught during execution of {coro.__name__}", exc_info=e)

    return new_coro


guild_logger = logger.getChild("guild")
guild_join_logger = guild_logger.getChild("join")
guild_leave_logger = guild_logger.getChild("leave")


@force_async
async def on_guild_join(guild):
    guild_join_logger.info(str(guild))


@force_async
async def on_guild_leave(guild):
    guild_leave_logger.info(str(guild))


class InviteCog(commands.Cog):
    bot: commands.Bot
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.prepare())

    @force_async
    async def prepare(self):
        await self.bot.wait_until_ready()
        with open("bot_url.txt", "rt", encoding="utf-8") as fp:
            self.invite_text = f"Invite for {self.bot.user.name}:\n{fp.read()}"

    @commands.command()
    @force_async
    async def invite(self, ctx):
        try:
            await ctx.author.send(self.invite_text)
        except discord.Forbidden:
            await ctx.send("You don't want an invite! Couldn't send you a DM")
        else:
            if getattr(self.bot, "gitgud"):
                await ctx.send("You got a bot invite!")


def setup(bot):
    bot.event(on_guild_join)
    bot.event(on_guild_leave)
    if os.path.isfile("bot_url.txt"):
        bot.add_cog(InviteCog(bot))
