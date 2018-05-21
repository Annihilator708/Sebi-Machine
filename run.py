# !/usr/bin/python
# -*- coding: utf8 -*-

# Import packages
import asyncio
import discord
from discord.ext import commands
import json
import traceback
import random

# Import custom files
from src.config.config import LoadConfig

# If uvloop is installed, change to that eventloop policy as it 
# is more efficient
try:
    # Temp fix for https://github.com/MagicStack/uvloop/pull/138
    # until it hopefully gets fixed by next week?
    import sys
    if sys.version_info()[1] > 6:
        raise RuntimeError('Disabling uvloop for Python3.7 and newer.')
    
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    del uvloop
except BaseException as ex:
    print(f'Could not load uvloop. {type(ex).__name__}: {ex};',
          'reverting to default impl.')
else:
    print(f'Using uvloop for asyncio event loop policy.')


# Bot Class
class SebiMachine(commands.Bot, LoadConfig):
    """This discord is dedicated to http://www.discord.gg/GWdhBSp"""
    def __init__(self):
        # Initialize and attach config / settings
        LoadConfig.__init__(self)
        commands.Bot.__init__(self, command_prefix=self.defaultprefix)
        self.embed_color = discord.Color(0x00FFFF)

        # Load plugins
        # Add your cog file name in this list
        with open('cogs.txt', 'r') as cog_file:
            cogs = cog_file.readlines()
        for cog in cogs:
            print(f'Loaded:{cog}')
            cog = cog.replace('\n', '')
            self.load_extension(f'src.cogs.{cog}')

    async def on_ready(self):
        """On ready function"""
        if self.maintenance:
            print('MAINTENANCE ACTIVE')

    async def on_command_error(self, ctx, error):
        """
        The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception
        """
        jokes = ["I\'m a bit tipsy, I took to many screenshots...",
                      "I am rushing to the 24/7 store to get myself anti-bug spray...",
                      "Organizing turtle race...",
                      "There is no better place then 127.0.0.1...",
                      "Recycling Hex Decimal...",
                      "No worry, I get fixed :^)...",
                      "R.I.P, press F for respect...",
                      "The bug repellent dit not work...",
                      "You found a bug in the program. Unfortunately the joke did not fit here, better luck next time..."]

        # catch error
        error = error.__cause__ or error
        tb = traceback.format_exception(type(error), error, error.__traceback__, limit=2, chain=False)
        tb = ''.join(tb)
        joke = random.choice(jokes)
        fmt = f'**`{self.defaultprefix}{ctx.command}`**\n{joke}\n\n**{type(error).__name__}:**:\n```py\n{tb}\n```'
        simple_fmt = f'**`{self.defaultprefix}{ctx.command}`**\n{joke}\n\n**{type(error).__name__}:**:\n**`{error}`**'
        await ctx.send(fmt)


if __name__ == '__main__':
    client = SebiMachine()
    # Make sure the key stays private.
    with open('src/config/PrivateConfig.json') as fp:
        PrivateConfig = json.load(fp)
        fp.close()
    client.run(PrivateConfig["bot-key"])
