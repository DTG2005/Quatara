import discord
from discord.ext import commands
import json

# Here I proceed to read the token
def readToken():
    with open("Token", 'r') as File:
        lines = File.readlines()
        return lines[0].strip()

token = readToken()

intents = discord.Intents.default()
intents.members = True

def get_prefix(client, message):
    #Loading the JSON file to read the prefix through the guild id
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

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
        self.load_extension("Misc")
        self.load_extension("Moderation")
        self.load_extension("Logging")
        self.load_extension("Utility")

        self.log_channel = self.get_channel(837631613390028800)
        self.version = "v2.2.1"
        self.author = 305403872438910977
        self.door_channel = self.get_channel(831066790238879764)

if __name__ == "__main__":
    YeetBot().run(token)
    