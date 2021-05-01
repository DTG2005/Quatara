import discord
from discord.ext import commands

# Here I proceed to read the token
def readToken():
    with open("Token", 'r') as File:
        lines = File.readlines()
        return lines[0].strip()

token = readToken()

intents = discord.Intents.default()
intents.members = True

class YeetBot (commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = "y-",
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
        self.version = "v1.0.0"
        self.author = 305403872438910977
        self.door_channel = self.get_channel(831066790238879764)
        self.log_ignores = []
        self.warns = {}
        self.superwarns = {}
        self.spam_channels = []


if __name__ == "__main__":
    YeetBot().run(token)
    