import discord
import asyncio
from discord import user
from discord.ext import commands
from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def getLog(self, id):
        dic = self.bot.col.find_one({"_id": "server_configs"})
        returnId = dic[str(id)]["log"]
        return returnId

    #logging for messages being deleted
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        log_channel = self.bot.get_channel(self.getLog(message.guild.id))
        embed = discord.Embed(title = f"{message.author.name} deleted a message, heads up!!!", description = "", color = discord.Color.red())
        embed.add_field(name= message.content, value= f"Logged in <#{log_channel.id}>")
        embed.set_author(name=message.author.name, icon_url=  message.author.icon_url)
        embed.set_footer(text =dt_string)
        await log_channel.send(embed=embed)

    #logging for messages being edited
    @commands.Cog.listener()
    async def on_message_edit(self, messageOrig, messageEdit):
        embed = discord.Embed(title = f"{messageOrig.author.name} edited a message, heads up!!!", description = "", color = discord.Color.orange())
        embed.add_field(name= messageOrig.content, value= "The message before the edit.")
        embed.add_field(name= messageEdit.content, value= "The message after being edited.")
        embed.set_author(name= messageEdit.author.name, icon_url= messageEdit.author.avatar_url)
        channel = self.bot.get_channel(self.getLog(messageOrig.guild.id))
        embed.set_footer(text =dt_string)
        await channel.send(embed = embed)

    #logging for member joining
    @commands.Cog.listener()
    async def on_member_join(self, member):
        dic = self.bot.col.find_one({"_id": "server_configs"})
        returnId = dic[str(member.guild.id)]["door"]
        door_channel = self.bot.get_channel(returnId)
        embed = discord.Embed(title = "Member joined!!!!", description =member.name,color = discord.Color.green())
        embed.set_author(name= member.name, icon_url=member.avatar_url)
        await door_channel.send(embed = embed)
        try:
            welcome_channel = self.bot.get_channel(dic[str(member.guild.id)]["welcome_config"]["channel"])
            welcome_str = dic[str(member.guild.id)]["welcome_config"]['welcome']
            try:
                welcome_str = welcome_str.replace("{member.mention}", f"<@{member.id}>")
            except:
                pass
            try:
                welcome_str = welcome_str.replace("{member.name}", f"{member.name}")
            except:
                pass
            await welcome_channel.send(welcome_str)
        except:
            pass

    #logging for member leaving
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        dic = self.bot.col.find_one({"_id": "server_configs"})
        returnId = dic[str(member.guild.id)]["door"]
        door_channel = self.bot.get_channel(returnId)
        embed = discord.Embed(title = "Member left!!!!", description = member.name,color = discord.Color.red())
        embed.set_author(name= member.name, icon_url=member.avatar_url)
        await door_channel.send(embed = embed)
        goodbye_channel = self.bot.get_channel(dic[str(member.guild.id)]["welcome_config"]["channel"])
        goodbye_str = dic[str(member.guild.id)]["welcome_config"]['goodbye']
        try:
            goodbye_str =goodbye_str.replace("{member.mention}", f"<@{member.id}>")
        except:
            pass
        try:
            goodbye_str = goodbye_str.replace("{member.name}", f"{member.name}")
        except:
            pass
        await goodbye_channel.send(goodbye_str)

    #logging for member updates
    @commands.Cog.listener()
    async def on_user_update(self,userb4, userafter):
        changeTitleDict = {"av": "Heads up! Avatar changed!", "un" : "Heads up! Username changed!", "dc": "Heads up! Discriminator changed!"}
        changetype = None
        if userb4.avatar != userafter.avatar:
            changetype = "av"
        elif userb4.name != userafter.name:
            changetype = "un"
        elif userb4.discriminator != userafter.discriminator:
            changetype = "dc"
        embed1 = discord.Embed(title= changeTitleDict[changetype], color= discord.Colour.green())
        if changetype == "av":
            embed1.set_thumbnail(url = userafter.avatar_url)
        elif changetype == "un":
            embed1.add_field(name= "Before:", value= userb4.name)
            embed1.add_field(name= "After:", value= userafter.name)
        elif changetype == "dc":
            embed1.add_field(name= "Before:", value= userb4.discriminator)
            embed1.add_field(name= "After:", value= userafter.discriminator)
        embed1.set_author(name= userafter.name, icon_url= userafter.avatar_url)
        for guild in userafter.mutual_guilds:
            dic = self.bot.col.find_one({"_id": "server_configs"})
            log_channel = self.bot.get_channel(dic[str(guild.id)]["log"])
            await log_channel.send(embed= embed1)

    #logging for when a member updates their guild attributes
    @commands.Cog.listener()
    async def on_member_update(self, userb4, useraft):
        changeTitleDict = {"nick": "Heads Up!! Nickname changed!!!!", "r": "Heads Up!!! Roles updated for a user!"}
        changetype = None
        if userb4.nick != useraft.nick:
            changetype = "nick"
        elif userb4.roles != useraft.roles:
            changetype = "r"

        embed = discord.Embed(title = changeTitleDict[changetype], color = discord.Color.green())
        embed.set_author(name= useraft.name, icon_url=useraft.avatar_url)
        if changetype == "nick":
            embed.add_field(name = "Nickname before:", value= userb4.nick)
            embed.add_field(name="Nickname after:", value= useraft.nick)
        elif changetype == "r":
            textb4 = ""
            for roles in userb4.roles:
                textb4 += (roles.mention + ", ")
            textaft = ""
            for roles in useraft.roles:
                textaft += (roles.mention + ", ")
            embed.add_field(name = "Roles before:", value= textb4)
            embed.add_field(name = "Roles after:", value= textaft)
        dic = self.bot.col.find_one({"_id": "server_configs"})
        log_channel = self.bot.get_channel(dic[str(useraft.guild.id)]["log"])
        await log_channel.send(embed= embed)

    #A command for setting the logging channel to be a different one
    @commands.command(description = "Changes the log channel to be a different one for a more QOL channel to be set separately.")
    async def setlog(self, ctx, channel: discord.TextChannel):
        
        config = self.bot.col.find_one({"_id": "server_configs"})
        config[str(ctx.guild.id)]["log"] = channel.id

        self.bot.col.find_and_modify({"_id": "server_configs"}, config)

        await ctx.send("Log channel updated!!!")

    #A command for setting the door channel (The channel where the entries and exits are logged) to be a different one
    @commands.command(description = "Sets the door channel to be a different one, where the member entries and exits are logged.")
    async def setdoor(self, ctx, channel : discord.TextChannel):

        config = self.bot.col.find_one({"_id": "server_configs"})
        config[str(ctx.guild.id)]["door"] = channel.id

        self.bot.col.find_and_modify({"_id": "server_configs"}, config)

        await ctx.send("Door channel updated!!!")

    #A command to set a command log
    @commands.command(
        description = "A command that lets you set the command logs where I send embeds everytime a moderation command is used.",
    )
    async def setcommandlog(self, ctx, channel : discord.TextChannel):
        config = self.bot.col.find_one({"_id": "server_configs"})
        config[str(ctx.guild.id)]["Command Log"] = channel.id

        self.bot.col.find_and_modify({"_id": "server_configs"}, config)
        await ctx.send("Command Logs Updated!!!")

    #A command to set a welcome message
    @commands.command(
        description = "Adds a welcome message and channel prompt incase you want the user to get a special welcome message!"
    )
    async def setsocialdoor(self, ctx):
        await ctx.send("Alright, beginning the welcome prompt. What channel do I send the welcome and goodbye message in?")
        def check(message):
            return message.author.id == ctx.author.id
        try:
            message = await self.bot.wait_for('message', timeout = 30, check= check)
        except asyncio.TimeoutError:
            await ctx.send("Timeout! Restart the prompt to set the social door!")
        else:
            try:
                channel = message.raw_channel_mentions[0]
                await ctx.send("Okay, got the channel mention now. What message do you want me to send when welcoming the peeps? Use {member.mention} for mentioning the member and {member.name} for the name of the member.")
                try:
                    message2 = await self.bot.wait_for('message', timeout= 60, check= check)
                except asyncio.TimeoutError:
                    await ctx.send("Timeout! Restart the prompt to be able to set all the datasets properly.")
                else:
                    await ctx.send("Perfect, I have got the welcome message finely. Now, what message do you want me to send when it's time to bid goodbye? Remember the same rules we set above.")
                    try:
                        message3 = await self.bot.wait_for('message', timeout= 60, check= check)
                    except asyncio.TimeoutError:
                        await ctx.send("Timeout! You gotta do all that process all over again, mortal. Why can't you be a bit faster?")
                    else:
                        data = self.bot.col.find_one({"_id": "server_configs"})
                        config = data[str(ctx.guild.id)]
                        if "welcome_config" not in config.keys():
                            config["welcome_config"] = {"channel": channel, "welcome": message2.content, "goodbye" : message3.content}
                            data[str(ctx.guild.id)] = config
                            self.bot.col.find_and_modify({"_id": "server_configs"}, data)
                            await ctx.send("Social welcome and goodbye config has been updated successfully!!!")
                        else:
                            config["welcome_config"]["channel"] = channel
                            config["welcome_config"]["welcome"] = message2.content
                            config["welcome_config"]["goodbye"] = message3.content
                            data[str(ctx.guild.id)] = config
                            self.bot.col.find_and_modify({"_id": "server_configs"}, data)
                            await ctx.send("Social welcome and goodbye config has been updated successfully!!!")

                
            except:
                await ctx.send("Channel mention not detected. Try again.")

def setup(bot):
    bot.add_cog(Logging(bot))