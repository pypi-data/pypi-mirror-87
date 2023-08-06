from discord.ext.commands import HelpCommand, DefaultHelpCommand, Cog
from . import force_async

argparse_command_registry = {}

def register_argparse_command(coro):
    argparse_command_registry[coro] = True
    return coro

class ArgparseHelpCommand(HelpCommand):
    async def send_command_help(self, command):
        if argparse_command_registry.get(command.callback): # no False default value, None is falsy
            await self.context.invoke(command, args="--help")
        else:
            await super().send_command_help(command)


class ArgparseDefaultHelpCommand(ArgparseHelpCommand, DefaultHelpCommand):
    pass


class Help(Cog):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = ArgparseDefaultHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

def setup(bot):
    bot.add_cog(Help(bot))
