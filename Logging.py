import discord
from discord.ext import commands


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #logging for messages being deleted
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        embed = discord.Embed(title = f"{message.author.name} deleted a message, heads up!!!", description = "", color = discord.Color(0x350cf9))
        embed.add_field(name= message.content, value= f"Logged in <#{self.bot.log_channel.id}>")
        embed.set_author(name= message.author.name, icon_url=message.author.avatar_url)
        await self.bot.log_channel.send(embed=embed)

    #logging for messages being edited
    @commands.Cog.listener()
    async def on_message_edit(self, messageOrig, messageEdit):
        embed = discord.Embed(title = f"{messageOrig.author.name} edited a message, heads up!!!", description = "", color = discord.Color(0x350cf9))
        embed.add_field(name= messageOrig.content, value= "The message before the edit.")
        embed.add_field(name= messageEdit.content, value= "The message after being edited.")
        embed.set_author(name= messageOrig.author.name, icon_url=messageOrig.author.avatar_url)
        channel = self.bot.log_channel
        await channel.send(embed = embed)

    #logging for member joining
    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(title = "Member joined!!!!", description = member.name,color = discord.Color(0x350cf9))
        embed.set_author(name= member.name, icon_url=member.avatar_url)
        await self.bot.door_channel.send(embed = embed)

    #logging for member leaving
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(title = "Member left!!!!", description = member.name,color = discord.Color(0x350cf9))
        embed.set_author(name= member.name, icon_url=member.avatar_url)
        await self.bot.door_channel.send(embed = embed)

    #A command for setting the logging channel to be a different one
    @commands.command(description = "Changes the log channel to be a different one for a more QOL channel to be set separately.")
    async def setlog(self, ctx, channel: discord.TextChannel):
        self.bot.log_channel = channel
        await ctx.send("Log channel updated!!!")

    #A command for setting the door channel (The channel where the entries and exits are logged) to be a different one
    @commands.command(description = "Sets the door channel to be a different one, where the member entries and exits are logged.")
    async def setdoor(self, ctx, channel : discord.TextChannel):
        self.bot.door_channel = channel
        await ctx.send("Door channel updated!!!")


def setup(bot):
    bot.add_cog(Logging(bot))