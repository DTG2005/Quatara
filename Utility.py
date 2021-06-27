import discord
from discord.ext import commands, tasks
import datetime as Dt
import os
import json
import asyncio

QOTDPingDict = {1:734436945689706519, 2:305403872438910977, 3:384331120755474442, 4: 698218252119179365, 5:762010102059237397, 6: 690967030299361310, 7:802770234292436992}
T3PingDict = {1:734436945689706519, 2: 745907752844394537, 3:384331120755474442, 4:698218252119179365, 5:305403872438910977, 6:690967030299361310, 7:802770234292436992}

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Prints Yeet when our bot's ready 
    @commands.Cog.listener()
    async def on_ready(self):
        print("Starting countdown...YEEEEEEEEEEEEEEEEEEEEET!!!!")

        datap = {}
        for server in self.bot.guilds:
            with open("prefixes.json", "r") as f:
                data = json.load(f)
                if server not in data:
                    data["server"] = "y!"
                datap = data
            
            with open("prefixes.json", "w") as f:
                json.dump(datap, f)

        datab = {}
        for server in self.bot.guilds:
            with open("server_configs.json", "r") as f:
                data = json.load(f)
                if server not in data:
                    data["server"] = {"log": None, "Spam": None, "door": None, "Spam Ignore": []}
                datab = data
            with open("server_configs.json", "w") as f:
                json.dump(datab, f)

        datar = {}
        for server in self.bot.guilds:
            with open("role_configs.json", "r") as f:
                data = json.load(f)
                if server not in data:
                    data["server"] = {"Moderator": None, "Member": None, "Mute": None}
                datar = data
            with open("server_configs.json", "w") as f:
                json.dump(datar, f)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = None
        with open("role_configs.json", "r") as f:
            data = json.load(f)
            role = data[str(member.guild.id)]["Member"]
        if role is not None:
            membrole = member.guild.get_role(role)
            await member.add_roles(membrole, reason = "Member joined")

    #Loads the JSON file to add a new prefix into the JSON before dumping it to store the new prefix data.
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        prefixes = {};
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = "y!"

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f)
            f.close()

        
        config = {}
        with open("server_configs.json", "r") as f:
            config = json.load(f)

        config[str(guild.id)] = {"log":None,"Spam": False, "door": None, "Spam Ignore": []}

        with open("server_configs.json", "w") as f:
            json.dump(config, f)

        roles = {}
        with open("role_configs.json", "r") as f:
            roles = json.load(f)
        roles[str(guild.id)] = {"Moderator": None, "Member": None, "Mute": None}

        with open("role_configs.json", "w") as f:
            json.dump(roles, f)

        warns = {}
        with open("warns.json", "r") as f:
            warns = json.load(f)
        warns[str(guild.id)] = {"Warns": {}, "Superwarns": {}}

        with open("role_configs.json", "w") as f:
            json.dump(roles, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.mentions[0] == self.bot.user:
                with open("prefixes.json", "r") as f:
                    prefixes = json.load(f)

                prefix = prefixes[str(message.guild.id)]

                await message.channel.send(f"You forgetful mortals. My prefix for your server was {prefix}.")
        except:
            pass

    @commands.command(description = "Pings the person whose QOTD it is, after all, world's pretty much full of forgetful dumbasses.", aliases = ["pingQOTD"])
    async def qotd(self, ctx):
        await ctx.send(f"Today it is the turn of <@{QOTDPingDict[Dt.datetime.today().isoweekday()]}>. Ask your question before I have to use my tasers.")

    @commands.command(description = "Pings the person whose Top 3 it is. I swear humans forget so much, how do they even have more romantic partners than us bots?", aliases = ["pingT3", "top3", "t3"])
    async def t3Ping(self, ctx):
        await ctx.send(f"Today it is the turn of <@{T3PingDict[Dt.datetime.today().isoweekday()]}>. Send in your Top 3 or I'll ping Satan to banish your soul to the lowest pits of hell.")

    @commands.command(description = "Changes the prefix incase muscle memory makes you miss the right keys.")
    @commands.has_permissions(administrator = True)
    async def changeprefix(self, ctx, prefix):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f)
        
        await ctx.send(f"I will now be summoned with the prefix {prefix}.")

    @changeprefix.error
    async def CPError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("We cannot let anyone but admins rewrite our prefixes because others are weaklings.")

    
#   @commands.command(description = "Sets up autoroles in the given channel using setup.", aliases = ["rr"])
#   async def reactionrole(self, ctx):
#       await ctx.send("The reaction role setup is up. What channel do you want the reaction role in?")
#
#       def check(m):
#           return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and m.content in m.guild.text_channels
#
#       await self.bot.wait_for('message', check = check, timeout = 30)
#       try:
#           await ctx.send("Channel registered.")
#       except asyncio.TimeoutError:
#           await ctx.send("Timeout. Restart the setup to finish the reaction role.")

def setup(bot):
    bot.add_cog(Utility(bot))
