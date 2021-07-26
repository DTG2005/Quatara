from discord.shard import EventItem
import discord
from discord.ext import commands, tasks
import datetime as Dt
import time
import json
import pymongo
import asyncio

QOTDPingDict = {1:734436945689706519, 2:305403872438910977, 3:384331120755474442, 4: 698218252119179365, 5:762010102059237397, 6: 690967030299361310, 7:802770234292436992}
T3PingDict = {1:734436945689706519, 2: 745907752844394537, 3:384331120755474442, 4:698218252119179365, 5:305403872438910977, 6:690967030299361310, 7:802770234292436992}

EastTimeDict = {"1": ["+0", True], "2": [1, False], "3": [1, True], "4": [2, False], "5": [2, True], "6": [3, False], "7": [3, True], "8": [4, False], "9": [4, True], "10": [5, False], "11": [5, True], "12": [6, False], "13": [6, True], "14": [7, False], "15": [7, True], "16": [8, False], "17": [8, True], "18": [9, False], "19": [9, True], "20": [10, False], "21": [10, True], "22": [11, False], "23": [11, True], "24": [12, False], }

WestTimeDict = {"1": ["-0", True], "2": [-1, False], "3": [-1, True], "4": [-2, False], "5": [-2, True], "6": [-3, False], "7": [-3, True], "8": [-4, False], "9": [-4, True], "10": [-5, False], "11": [-5, True], "12": [-6, False], "13": [-6, True], "14": [-7, False], "15": [-7, True], "16": [-8, False], "17": [-8, True], "18": [-9, False], "19": [-9, True], "20": [-10, False], "21": [-10, True], "22": [-11, False], "23": [-11, True], "24": [-12, False], }

def isTimeFormat(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Prints Yeet when our bot's ready 
    @commands.Cog.listener()
    async def on_ready(self):
        print("Starting countdown...YEEEEEEEEEEEEEEEEEEEEET!!!!")

        for server in self.bot.guilds:
            data = self.bot.col.find_one({"_id": "Prefixes"})
            if data is None:
                data1 = {"_id" : "Prefixes", str(server.id) : "y!"}
                self.bot.col.insert(data1)
            elif str(server.id) not in dict(data):
                data2 = data
                data2[str(server.id)] = "y!"
                self.bot.col.find_and_modify({"_id": "Prefixes"}, data2)
            
        for server in self.bot.guilds:
            data = self.bot.col.find_one({"_id": "server_configs"})
            if data is None:
                data1 = {"_id" : "server_configs", str(server.id) : {"log": None, "Spam": False, "Autorole": False, "door": None, "Spam Ignore": []}}
                self.bot.col.insert(data1)
            elif str(server.id) not in data:
                data2 = data
                data2[str(server.id)] = {"log": None, "Spam": False, "Autorole": False, "door": None, "Spam Ignore": []}
                self.bot.col.find_and_modify({"_id": "server_configs"}, data2)

        for server in self.bot.guilds:
            data = self.bot.col.find_one({"_id": "role_configs"})
            if data is None:
                data1 = {"_id" : "role_configs", str(server.id) : {"Moderator" : None, "Member" : None, "Mute" : None}}
                self.bot.col.insert(data1)
            elif str(server.id) not in data:
                data2 = data
                data2[str(server.id)] = {"Moderator" : None, "Member" : None, "Mute" : None}
                self.bot.col.find_and_modify({"_id": "server_configs"}, data2)

        for server in self.bot.guilds:
            data = self.bot.col.find_one({"_id": "warns"})
            if data is None:
                data1 = {"_id" : "warns", str(server.id) : {"Warns": {}, "Superwarns": {}}}
                self.bot.col.insert(data1)
            elif str(server.id) not in data:
                data2 = data
                data2[str(server.id)] = {"Warns": {}, "Superwarns": {}}
                self.bot.col.find_and_modify({"_id": "warns"}, data2)
            
            
    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = None
        data = self.bot.col.find_one({"_id": "role_configs"})
        role = data[str(member.guild.id)]["Member"]
        data2 = self.bot.col.find_one({"_id": "server_configs"})
        truth = data2[str(member.guild.id)]["Autorole"]
        if role is not None:
            if truth:
                membrole = member.guild.get_role(role)
                await member.add_roles(membrole, reason = "Member joined")

    #Loads the JSON file to add a new prefix into the JSON before dumping it to store the new prefix data.
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        prefixes = {};
        prefixes = self.bot.col.find_one({"_id": "Prefixes"})

        prefixes[str(guild.id)] = "y!"

        self.bot.col.find_and_modify({"_id": "Prefixes"}, prefixes)

        
        config = self.bot.col.find_one({"_id": "server_configs"})

        config[str(guild.id)] = {"log":None,"Spam": False, "Autorole": False, "door": None, "Spam Ignore": []}

        self.bot.col.find_and_modify({"_id": "server_configs"}, config)

        roles = self.bot.col.find_one({"_id": "role_configs"})
        roles[str(guild.id)] = {"Moderator": None, "Member": None, "Mute": None}

        self.bot.col.find_and_modify({"_id": "role_configs"}, roles)

        warns = {}
        with open("warns.json", "r") as f:
            warns = json.load(f)
        warns[str(guild.id)] = {"Warns": {}, "Superwarns": {}}

        with open("warns.json", "w") as f:
            json.dump(warns, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            for word in message.content.split():
                if isTimeFormat(word) and message.content.split()[message.content.split().index(word) + 1] in ["am", "pm"]:
                    await message.add_reaction("🕒")
    
                    def check(reaction, user):
                        return message.id == reaction.message.id and str(reaction.emoji) == "🕒" and not user.bot
    
                    while True:
                        reaction, user = await self.bot.wait_for("reaction_add", timeout = 3000, check = check)
    
                        timeDat = []
                        am_pm = message.content.split()[message.content.split().index(word) + 1]
                        try:
                            data = self.bot.col.find_one({"_id": "Times"})
                            timeDat = data[str(message.author.id)]
    
                            GMT_Hrs = int(word.split(":")[0]) - int(timeDat[0])
                            GMT_mins = int(word.split(":")[1])
                            if timeDat[1]:
                                if timeDat[0] < 0 or timeDat[0] == "-0":
                                    GMT_mins + 30 
                                else:
                                    GMT_mins - 30
                                
                            if GMT_mins < 0:
                                GMT_mins +=60
                                GMT_Hrs -= 1
                            if GMT_mins > 60:
                                GMT_mins -= 60
                                GMT_Hrs += 1
                            if GMT_Hrs < 1:
                                GMT_Hrs += 12
                                if am_pm == "am":
                                    am_pm = "pm"
                                else:
                                    am_pm = "am"
                            if GMT_Hrs > 12:
                                GMT_Hrs -= 12
                                if am_pm == "pm":
                                    am_pm = "am"
                                else:
                                    am_pm = "pm"
                            
                            timeDat1 = []
                            data2 = self.bot.col.find_one({"_id": "Times"})
                            timeDat1 = data2[str(user.id)]
    
                            GMT_Hrs += int(timeDat1[0])
                            if timeDat1[1]:
                                if int(timeDat1[0]) < 0 or timeDat1[0] == "-0":
                                    GMT_mins - 30 
                                else:
                                    GMT_mins + 30
                                
                            if GMT_mins < 0:
                                GMT_mins +=60
                                GMT_Hrs -= 1
                            if GMT_mins > 60:
                                GMT_mins -= 60
                                GMT_Hrs += 1
                            if GMT_Hrs < 1:
                                GMT_Hrs += 12
                                if am_pm == "am":
                                    am_pm = "pm"
                                else:
                                    am_pm = "am"
                            if GMT_Hrs > 12:
                                GMT_Hrs -= 12
                                if am_pm == "pm":
                                    am_pm = "am"
                                else:
                                    am_pm = "pm"
    
                            Time_Complete = f"{GMT_Hrs:02d}:{GMT_mins:02d} {am_pm}"
    
                            channel = await user.create_dm()
                            await channel.send(Time_Complete)
    
                        except KeyError:
                            channel = await user.create_dm()
                            await channel.send("Error: Either you or the message's author has not set their timezones. Do the same to gain access to the TimeZone Converter feature.")
    
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
        if ctx.guild.id == 828926478661320744:
            await ctx.send(f"Today it is the turn of <@{QOTDPingDict[Dt.datetime.today().isoweekday()]}>. Ask your question before I have to use my tasers.")
        else:
            await ctx.send("Don't mind this command it's just for a special server I'm in. Have a nice day.")

    @commands.command(description = "Pings the person whose Top 3 it is. I swear humans forget so much, how do they even have more romantic partners than us bots?", aliases = ["pingT3", "top3", "t3"])
    async def t3Ping(self, ctx):
        if ctx.guild.id == 828926478661320744:
            await ctx.send(f"Today it is the turn of <@{T3PingDict[Dt.datetime.today().isoweekday()]}>. Send in your Top 3 or I'll ping Satan to banish your soul to the lowest pits of hell.")
        else:
            await ctx.send("Don't mind this command it's just for a special server I'm in. Have a nice day.")

    @commands.command(description = "Changes the prefix incase muscle memory makes you miss the right keys.", aliases = ["setprefix"])
    @commands.has_permissions(administrator = True)
    async def changeprefix(self, ctx, prefix):
        prefixes = self.bot.col.find_one({"_id": "Prefixes"})

        prefixes[str(ctx.guild.id)] = prefix

        self.bot.col.find_and_modify({"_id": "Prefixes"}, prefixes)
        
        await ctx.send(f"I will now be summoned with the prefix {prefix}.")

    @changeprefix.error
    async def CPError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("We cannot let anyone but admins rewrite our prefixes because others are weaklings.")

    
#    @commands.command(description = "Sets up autoroles in the given channel using setup.", aliases = ["rr"])
#    async def reactionrole(self, ctx):
#        await ctx.send("The reaction role setup is up. What channel do you want the reaction role in?")
#
#        def check(m):
#            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
#
#        channelM = await self.bot.wait_for('message', check = check, timeout = 30)
#        try:
#            try:
#                channel = channelM.raw_channel_mentions[0]
#                await ctx.send("Channel registered. What must be the body of the message?")
#                try:
#                    message = await self.bot.wait_for("message", timeout = 60, check= check)
#                except asyncio.TimeoutError:
#                    await ctx.send("Timeout! Restart the setup to finish the reaction role.")
#            except:
#                await ctx.send("Channel not detected in the message. Restart the prompt.")
#        except asyncio.TimeoutError:
#            await ctx.send("Timeout. Restart the setup to finish the reaction role.")

    @commands.command(description = "Sets your timezones to convert times.", aliases = ["setzone"])
    async def setTime(self, ctx):
        embedTime = discord.Embed(title= "Time Zone selector", description= "Update your time to be able to convert time from others' times to yours.")
        embedTime.add_field(name = "Hemispheres", value = "1. Eastern Hemisphere\n2. Western Hemisphere")
        message = await ctx.send(embed= embedTime)

        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["1️⃣", "2️⃣"]

        while True:
            #We wait for a reaction from the user
            reaction, user = await self.bot.wait_for("reaction_add", timeout=3000, check=check)

            if str(reaction.emoji) == "1️⃣":
                embedTime.clear_fields()
                embedTime.add_field(name="Time Zones", value= "1. GMT+00:30\n2. GMT+01:00\n3. GMT+01:30\n4. GMT+02:00\n5. GMT+02:30\n6. GMT+03:00\n7. GMT+03:30\n8. GMT+04:00\n9. GMT+04:30\n10. GMT+05:00\n11. GMT+05:30\n12. GMT+06:00\n13. GMT+06:30\n14. GMT+07:00\n15. GMT+07:30\n16. GMT+08:00\n17. GMT+08:30\n18. GMT+09:00\n19. GMT+09:30\n20. GMT+10:00\n21. GMT+10:30\n22. GMT+11:00\n23. GMT+11:30\n24. GMT+12:00")
                await message.clear_reactions()
                embedTime.set_footer(text = "Send the number next to your timezone")
                await message.edit(embed=embedTime)

                def check2(message):
                    return message.author.id == ctx.author.id and int(message.content) in list(range(1, 24))

                message = await self.bot.wait_for('message', check= check2, timeout=60)
                try:
                    data2 = self.bot.col.find_one({"_id": "Times"})
                    if data2 is None:
                        data2 = {"_id": "Times", str(ctx.author.id) : EastTimeDict[message.content]}
                        self.bot.col.insert(data2)
                    elif str(ctx.author.id) in data2:
                        data2[str(ctx.author.id)] = EastTimeDict[message.content]
                        self.bot.col.find_and_modify({"_id": "Times"},data2)
                    else:
                        data2[str(ctx.author.id)] = EastTimeDict[message.content]
                        self.bot.col.find_and_modify({"_id": "Times"}, data2)
                    await ctx.send("Time Zone updated successfully!! Click the clock reaction below any time to see the same time in your time zone.")
                except asyncio.TimeoutError:
                    await ctx.send("Timeout! Try again you slow mortals!")

            elif str(reaction.emoji) == "2️⃣":
                embedTime.clear_fields()
                embedTime.add_field(name="Time Zones", value= "1. GMT-00:30\n2. GMT-01:00\n3. GMT-01:30\n4. GMT-02:00\n5. GMT-02:30\n6. GMT-03:00\n7. GMT-03:30\n8. GMT-04:00\n9. GMT-04:30\n10. GMT-05:00\n11. GMT-05:30\n12. GMT-06:00\n13. GMT-06:30\n14. GMT-07:00\n15. GMT-07:30\n16. GMT-08:00\n17. GMT-08:30\n18. GMT-09:00\n19. GMT-09:30\n20. GMT-10:00\n21. GMT-10:30\n22. GMT-11:00\n23. GMT-11:30\n24. GMT-00:00")
                await message.clear_reactions()
                embedTime.set_footer(text = "Send the number next to your timezone")
                await message.edit(embed=embedTime)

                def check3(message):
                    return message.author.id == ctx.author.id and int(message.content) in list(range(1, 24))

                message = await self.bot.wait_for('message', check= check3, timeout=60)
                try:
                    data2 = self.bot.col.find_one({"_id": "Times"})
                    if data2 is None:
                        data2 = {"_id": "Times", str(ctx.author.id): WestTimeDict[message.content]}
                        self.bot.col.insert(data2)
                    elif str(ctx.author.id) in data2:
                        data2[str(ctx.author.id)] = WestTimeDict[message.content]
                        self.bot.col.find_and_modify({"_id": "Times"}, data2)
                    else:
                        data2[str(ctx.author.id)] = WestTimeDict[message.content]
                        self.bot.col.find_and_modify({"_id": "Times"}, data2)
                    await ctx.send("Time Zone updated successfully!! Click the clock reaction below any time to see the same time in your time zone.")
                except TimeoutError:
                    await ctx.send("Timeout! Try again you slow mortals!")

    @commands.command(
        description = "Adds a new role to the guild to be used for a specific time period."
    )
    @commands.has_permissions(manage_roles = True)
    async def event(self, ctx, *, rolename):
        try:
            role = await ctx.guild.create_role(name= rolename, mentionable = True)
        except discord.HTTPException as e:
            await ctx.send("Failed at role creation")
            print (e)
        message = await ctx.send(f"Role {role.mention} has been created for an event! Make sure to react to this message with a ✅ to get the event role!")
        await message.add_reaction(emoji = "✅")
        data = self.bot.col.find_one({"_id": "server_configs"})
        if "Events" in data[str(ctx.guild.id)]:
            data[str(ctx.guild.id)]["Events"].append(rolename)
        else:
            data[str(ctx.guild.id)]["Events"] = [rolename]
        self.bot.col.find_and_modify({"_id": "server_configs"}, data)

        def checkf(reaction, user):
            return str(reaction.emoji) == "✅" and not(user.bot)
        while True:
            reaction, user = await self.bot.wait_for("reaction_add", check = checkf)

            await user.add_roles(role)
            await message.remove_reaction(reaction, user)
    
    @event.error
    async def eventError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the authority of event manager to manage events! Be careful or next time you don't get to participate in the event at all.")

    @commands.command(
        description= "A command to end the already running events in the Server."
    )
    @commands.has_permissions(manage_roles = True)
    async def endevent(self, ctx, *, rolename):
        role = discord.utils.get(ctx.guild.roles, name = rolename)
        if role:
            await role.delete()
            data = self.bot.col.find_one({"_id": "server_configs"})
            data[str(ctx.guild.id)]["Events"].remove(rolename)
            self.bot.col.find_and_modify({"_id": "server_configs"}, data)
            await ctx.send(f"Event {rolename} has now ended! The role will no longer be in use.")
        else:
            await ctx.send("This event wasn't found! Check again to see if it is the same event.")

    @endevent.error
    async def eeError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Only Event Managers can handle time when an event stays! Do not interfere!")

def setup(bot):
    bot.add_cog(Utility(bot))
