from time import strftime
import sys
import discord
import logging

logging.basicConfig(
    format='%(asctime)s.%(msecs)d %(name)s %(funcName)s():%(lineno)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO,
    handlers={
        logging.FileHandler(strftime("logs/bootlog_%H_%M_%m_%d_%Y.log")),
        logging.StreamHandler()

    })

logger = logging.getLogger("main.py")

sys.path.append('/Users/waffles/PycharmProjects/bootkeys')
logger.info("Added bootkeys to python path")

import bootkeys
from src.commands import commands
from src.database.mongoHandler import MongoHandler

mongo = MongoHandler(bootkeys.mongodb_url)

# todo make cleaner


boot = discord.Bot()


@boot.event
async def on_ready():
    print(f"We have logged in as {boot.user}")


commands.initCommands(boot, mongo)

boot.run(bootkeys.privateKey)
