import pymongo
import logging
from .mongoEnum import MongoErr

logger = logging.getLogger(__name__)


class MongoHandler:

    def __init__(self, url):
        self.__client = pymongo.MongoClient(url)
        self.__boot_db = self.__client["boot"]
        self.__users = self.__boot_db["users"]
        self.__characters = self.__boot_db["characters"]

        logger.debug("Created Mongo Handler")

    def createProfile(self, uid):

        if self.__users.count_documents({"_id": uid}) > 0:
            logger.debug("UID already registered")
            return MongoErr.EXISTS

        x = self.__users.insert_one({"_id": uid, "Active_character": 0})

        logger.debug("Successfully added user profile")
        return x.inserted_id

    def createCharacter(self, uid, name, stats: dict):
        if self.__characters.count_documents({"name": name, "_id": uid}) > 0:
            logger.debug("UID already registered")
            return MongoErr.EXISTS

        x = self.__characters.insert_one({"name": name, "user_id": uid, "stats": stats})

        logger.debug("Successfully added user profile")
        return x.inserted_id

    def getCharacter(self, uid, name):

        character = self.__characters.find_one({"name": name, "user_id": uid})

        if character:
            return character
        else:
            return "Could not find %s" % name

    # TODO get all characters to dynamic select active character
