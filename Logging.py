import discord
import json
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
        embed.set_footer(text =dt_string)
        await log_channel.send(embed=embed)

    #logging for messages being edited
    @commands.Cog.listener()
    async def on_message_edit(self, messageOrig, messageEdit):
        embed = discord.Embed(title = f"{messageOrig.author.name} edited a message, heads up!!!", description = "", color = discord.Color.orange())
        embed.add_field(name= messageOrig.content, value= "The message before the edit.")
        embed.add_field(name= messageEdit.content, value= "The message after being edited.")
        channel = self.bot.get_channel(self.getLog(messageOrig.guild.id))
        embed.set_footer(text =dt_string)
        await channel.send(embed = embed)

    #logging for member joining
    @commands.Cog.listener()
    async def on_member_join(self, member):
        dic = self.bot.col.find_one({"_id": "server_configs"})
        returnId = dic[str(id)]["door"]
        door_channel = self.bot.get_channel(returnId)
        embed = discord.Embed(title = "Member joined!!!!", description =member.name,color = discord.Color.green())
        embed.set_author(name= member.name, icon_url=member.avatar_url)
        await door_channel.send(embed = embed)

    #logging for member leaving
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        dic = self.bot.col.find_one({"_id": "server_configs"})
        returnId = dic[str(id)]["door"]
        door_channel = self.bot.get_channel(returnId)
        embed = discord.Embed(title = "Member left!!!!", description = member.name,color = discord.Color.red())
        embed.set_author(name= member.name, icon_url=member.avatar_url)
        await door_channel.send(embed = embed)

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



def setup(bot):
    bot.add_cog(Logging(bot))