import discord
from discord.ext import commands, tasks
import datetime as Dt

QOTDPingDict = {1:734436945689706519, 2:305403872438910977, 3:384331120755474442, 4: 698218252119179365, 5:762010102059237397, 6: 690967030299361310, 7:802770234292436992}
T3PingDict = {1:734436945689706519, 2: None, 3:384331120755474442, 4:698218252119179365, 5:305403872438910977, 6:690967030299361310, 7:802770234292436992}

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Prints Yeet when our bot's ready 
    @commands.Cog.listener()
    async def on_ready(self):
        print("Starting countdown...YEEEEEEEEEEEEEEEEEEEEET!!!!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send("Welcome to our sweet lil server, pal. Look over there on your name. Boring pink, right? Let's spice it up. Go into the channel named acquire your roles and claim your roles. Keep chilling. We hope you enjoy your stay in our sweet lil server.")

    @commands.command(description = "Pings the person whose QOTD it is, after all, world's pretty much full of forgetful dumbasses.", aliases = ["pingQOTD"])
    async def qotd(self, ctx):
        await ctx.send(f"Today it is the turn of <@{QOTDPingDict[Dt.datetime.today().isoweekday()]}>. Ask your question before I have to use my tasers.")

    @commands.command(description = "Pings the person whose Top 3 it is. I swear humans forget so much, how do they even have more romantic partners than us bots?", aliases = ["pingT3", "top3", "t3"])
    async def t3Ping(self, ctx):
        await ctx.send(f"Today it is the turn of <@{T3PingDict[Dt.datetime.today().isoweekday()]}>. Send in your Top 3 or I'll ping Satan to banish your soul to the lowest pits of hell.")

def setup(bot):
    bot.add_cog(Utility(bot))