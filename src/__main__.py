# !/usr/bin/python
# -*- coding: utf8 -*-
"""
App entry point.

Something meaningful here, eventually.
"""
import asyncio
import json
import logging
import random
import traceback
import os

import discord
from discord.ext import commands

from src.config.config import LoadConfig
from src.shared_libs.loggable import Loggable
from src.shared_libs.ioutils import in_here


# Init logging to output on INFO level to stderr.
logging.basicConfig(level='INFO')        


# If uvloop is installed, change to that eventloop policy as it 
# is more efficient
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    del uvloop
except BaseException as ex:
    logging.warning(f'Could not load uvloop. {type(ex).__qualname__}: {ex};',
                    'reverting to default impl.')
else:
    logging.info(f'Using uvloop for asyncio event loop policy.')


# Bot Class
# Might be worth moving this to it's own file? 
class SebiMachine(commands.Bot, LoadConfig, Loggable):
    """This discord is dedicated to http://www.discord.gg/GWdhBSp"""
    def __init__(self):
        # Initialize and attach config / settings
        LoadConfig.__init__(self)
        commands.Bot.__init__(self, command_prefix=self.defaultprefix)

        # Load plugins
        # Add your cog file name in this list
        with open(in_here('cogs.txt')) as cog_file:
            cogs = cog_file.readlines()
            
        for cog in cogs:
            # Could this just be replaced with `strip()`?
            cog = cog.replace('\n', '')
            self.load_extension(f'src.cogs.{cog}')
            self.logger.info(f'Loaded: {cog}')
            
    async def on_ready(self):
        """On ready function"""
        self.maintenance and self.logger.warning('MAINTENANCE ACTIVE')

client = SebiMachine()
# Make sure the key stays private.
# I am 99% certain this is valid!
with open(in_here('config', 'PrivateConfig.json')) as fp:
    PrivateConfig = json.load(fp)
if PrivateConfig["bot-key"] == '':
    PrivateConfig["bot-key"] = os.getenv('botkey')

client.run(PrivateConfig["bot-key"])
