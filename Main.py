import discord
from discord.ext import commands
import json
import pymongo

# Here I proceed to read the token
def readToken():
    with open("Token.txt", 'r') as File:
        lines = File.readlines()
        return lines[0].strip()

token = readToken()

intents = discord.Intents.all()
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

        self.version = "v2.2.1"
        self.author = 305403872438910977

Client = YeetBot()

@Client.event
async def on_ready():
    print("Da return of da yeeeeet!!!")

    await Client.load_extension("Misc")
    await Client.load_extension("Moderation")
    await Client.load_extension("Fun")
    await Client.load_extension("Math")
    await Client.load_extension("Logging")
    await Client.load_extension("Utility")
    await Client.load_extension("Conversions")

    await Client.tree.sync()

@Client.command(hidden= True)
async def reload(ctx, Cog):
    await Client.reload_extension(Cog)
    await Client.tree.sync()
    await ctx.send("Cog reloaded!")

if __name__ == "__main__":
    Client.run(token)
    