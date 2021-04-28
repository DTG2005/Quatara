import discord
from discord.ext import commands

# Here I proceed to read the token
def readToken():
    with open("Token", 'r') as File:
        lines = File.readlines()
        return lines[0].strip()

token = readToken()

class YeetBot (commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = "y!",
            case_insensitive = True,
            self_bot = False,
            activity = discord.Activity(type=discord.ActivityType.competing, name = "Yolo!!!!!!"),
        )

        self.load_extension("Misc")
        
        async def on_ready(self):
            print("YEEEEEEEEEEEEEEEET")


if __name__ == "__main__":
    YeetBot().run(token)
    