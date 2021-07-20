import discord
from discord.ext import commands
import json
import pymongo

# Here I proceed to read the token
def readToken():
    with open("Token", 'r') as File:
        lines = File.readlines()
        return lines[0].strip()

token = readToken()

intents = discord.Intents.default()
intents.members = True

client2 = pymongo.MongoClient("mongodb+srv://Quatara:Dev_is_a_pussy@quatara.ehvj6.mongodb.net/Quatara?retryWrites=true&w=majority")

def get_prefix(client, message):
    #Loading the DB to read the prefix through the guild id
    prefixes = dict(client2["Quatara"]["Data"].find_one({"_id": "Prefixes"}))

    return prefixes[str(message.guild.id)]

class YeetBot (commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = get_prefix,
            intents = intents,
            case_insensitive = True,
            self_bot = False,
            activity = discord.Activity(type=discord.ActivityType.competing, name = "Yolo!!!!!!"),
        )
        self.db = client2["Quatara"]
        self.col = self.db["Data"]
        self.load_extension("Misc")
        self.load_extension("Moderation")
        self.load_extension("Logging")
        self.load_extension("Utility")

        self.version = "v2.2.1"
        self.author = 305403872438910977

if __name__ == "__main__":
    YeetBot().run(token)
    