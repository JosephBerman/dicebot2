# global
import asyncio
import random
import sys
import bootkeys
import discord
import logging
logger = logging.getLogger(__name__)

from ..embeds import embeddHandler as embedHandle
from ..database.mongoHandler import MongoHandler
from ..database.mongoHandler import MongoErr


def initProfiles(boot, mongo: MongoHandler):
    profiles = boot.create_group(
        "profile", "Profile commands"
    )
    pass
