import discord
import json
from discord.ext import commands

def getLog(id):
    with open("server_configs.json", "r") as f:
        dict = json.load(f)
        returnId = dict[str(id)]["log"]
        return returnId

def getDoor(id):
    with open("server_configs.json", "r") as f:
        dict = json.load(f)
        returnId = dict[str(id)]["door"]
        return returnId


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #logging for messages being deleted
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.channel not in self.bot.log_ignores:
            log_channel = self.bot.get_channel(getLog(message.guild.id))
            embed = discord.Embed(title = f"{message.author.name} deleted a message, heads up!!!", description = "", color = discord.Color.red())
            embed.add_field(name= message.content, value= f"Logged in <#{log_channel.id}>")
            embed.set_author(name= message.author.name, icon_url=message.author.avatar_url)
            embed.set_footer(text = message.channel.name)
            await log_channel.send(embed=embed)

    #logging for messages being edited
    @commands.Cog.listener()
    async def on_message_edit(self, messageOrig, messageEdit):
        if messageOrig.channel not in self.bot.log_ignores:
            embed = discord.Embed(title = f"{messageOrig.author.name} edited a message, heads up!!!", description = "", color = discord.Color.orange())
            embed.add_field(name= messageOrig.content, value= "The message before the edit.")
            embed.add_field(name= messageEdit.content, value= "The message after being edited.")
            embed.set_author(name= messageOrig.author.name, icon_url=messageOrig.author.avatar_url)
            embed.set_footer(text= messageOrig.channel.name)
            channel = self.bot.get_channel(getLog(messageOrig.guild.id))
            await channel.send(embed = embed)

    #logging for member joining
    @commands.Cog.listener()
    async def on_member_join(self, member):
      door_channel = getDoor(member.guild.id)
      embed = discord.Embed(title = "Member joined!!!!", description =member.name,color = discord.Color.green())
      embed.set_author(name= member.name, icon_url=member.avatar_url)
      await door_channel.send(embed = embed)

    #logging for member leaving
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        door_channel = getDoor(member.guild.id)
        embed = discord.Embed(title = "Member left!!!!", description = member.name,color = discord.Color.red())
        embed.set_author(name= member.name, icon_url=member.avatar_url)
        await door_channel.send(embed = embed)

    #A command for setting the logging channel to be a different one
    @commands.command(description = "Changes the log channel to be a different one for a more QOL channel to be set separately.")
    async def setlog(self, ctx, channel: discord.TextChannel):
        
        config = {}
        with open("server_configs.json", "r") as f:
            config = json.load(f)
        config[str(ctx.guild.id)]["log"] = channel.id

        with open("server_configs.json", "w") as f:
            json.dump(config, f)

        await ctx.send("Log channel updated!!!")

    #A command for setting the door channel (The channel where the entries and exits are logged) to be a different one
    @commands.command(description = "Sets the door channel to be a different one, where the member entries and exits are logged.")
    async def setdoor(self, ctx, channel : discord.TextChannel):

        config = {}
        with open("server_configs.json", "r") as f:
            config = json.load(f)
        config[str(ctx.guild.id)]["door"] = channel.id

        with open("server_configs.json", "w") as f:
            json.dump(config, f)

        await ctx.send("Door channel updated!!!")

    #here we add channels we want to ignore for logging (e.g. Spam, Pokemon, etc.)
    @commands.command(description = "Sets channels that you want the logging to ignore.")
    async def ignorelogs(self, ctx, channel : discord.TextChannel):
        self.bot.log_ignores.append(channel)
        await ctx.send("New channels to ignore message logs added!!!")

    #And another one to remove a channel you accidentally added to the log ignores.
    @commands.command(description = "Removes channels you don't want in log ignores. After all, silly humans make mistakes unlike us bots.")
    async def rmlogignore(self, ctx, channel : discord.TextChannel):
        try:
            self.bot.log_ignores.remove(channel)
            await ctx.send("Channel removed from log ignores!!!")
        except ValueError:
            await ctx.send("Channel not in log ignores!!! Look for mistakes, puny human.")


def setup(bot):
    bot.add_cog(Logging(bot))