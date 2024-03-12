import pymongo
from pymongo import ReturnDocument
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

    def __profileExist(self, uid):
        if self.__users.count_documents({"uesr_id": uid}) > 0:
            logger.debug("UID registered")
            return True
        else:
            logger.debug("UID NOT registered")
            return False

    def __createProfile(self, uid):

        x = self.__users.insert_one({"user_id": uid,
                                     "active_character": 0})

        logger.debug("Successfully added user profile")
        return x.inserted_id

    def __setActiveCharacter(self, uid, character_id):

        self.__users.update_one({"user_id": uid},
                                {'$set': {"active_character": character_id}})

    # Seperated for out facing api
    def setActiveCharacter(self, uid, name):
        character = self.__getCharacter(uid, name)
        if character:
            self.__setActiveCharacter(uid, character_id=character["_id"])
            return MongoErr.SUCCESS
        else:
            return MongoErr.EMPTY

    def __getActiveCharacter(self, uid):
        return self.__users.find_one({"user_id": uid})


    def getActiveCharacter(self, uid):
        character = self.__getActiveCharacter(uid)
        if character:
            return self.__characters.find_one(character["active_character"])
        else:
            return MongoErr.EMPTY

    def __insertCharacter(self, uid, name, stats):
        return self.__characters.insert_one({"name": name,
                                             "user_id": uid,
                                             "stats": stats})

    def insertCharacter(self, uid, name, stats: dict):

        if self.__profileExist(uid) is False:
            logger.debug("profile does not exist, creating")
            self.__createProfile(uid)
            logger.debug("created profile")

        x = self.__insertCharacter(uid, name, stats)

        logger.debug("Successfully added character")
        return x.inserted_id

    def __getCharacter(self, uid, name):
        return self.__characters.find_one({"name": name,
                                           "user_id": uid})

    def getCharacter(self, uid, name):

        character = self.__getCharacter(uid, name)

        if character:
            return character
        else:
            return "Could not find %s" % name

    # TODO Find a way to make this generic, current use is for search function
    # This method will require another query which will only slow things down
    # If not possible, conert this to only retreiving a list of names, dont need excess data
    def __getCharacterNames(self, uid):
        query = {"user_id": uid}

        x = list(self.__characters.find(query))

        logger.info("query: %s" % x)
        return x

    def getCharacterNames(self, uid):

        character = self.__getCharacterNames(uid)

        names = [x['name'] for x in character]

        if names:
            return names
        else:
            return None
