import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #This is the kick command, pretty self explanatory imo
    @commands.command(description = "Well, uh, kicks da hoe. Supa basic command all mods should know right?", aliases = ["yeet"])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member, *, reason = "No reason provided."):
        await member.kick(reason= reason)
        await ctx.send("The pestilence has been Yeeted. All hail YEET GOD.")
        await member.send(f"Hey punk, by the grace of the Yeet GOD, you have been kicked for {reason}.")

    #If the user doesn't have the permission, we display this message
    @kick.error
    async def kickerror(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Hey mods! We have an imposter tryna kick someone without thy permissions. Do with him as thou wisheth.")

    #Repeat the same thing for ban command
    @commands.command(description = "Bans pesky motherlovers from the server once and for all for greater good of the server.", aliases = ["superyeet"])
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason = "No reason provided."):
        await ctx.guild.ban(member, reason= reason)
        await ctx.send("The pestilence has been Banned. All hail YEET GOD.")
        await member.send(f"Hey punk, by the grace of the Yeet GOD, you have been banned for {reason}.")

    @ban.error
    async def kickerror(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Hey mods! We have an imposter tryna ban someone without thy permissions. Do with him as thou wisheth.")

    #repeat the same thing for clean command as well so yep
    @commands.command(description = "Clears the given set of commands so you don't have to dirty your hands.", aliases = ["clean", "tidy"])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amt):
        await ctx.channel.purge(limit = int(amt) + 1)

    @clear.error
    async def clearError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry but it seems you do not have the permissions to use this command.")

def setup(bot):
    bot.add_cog(Moderation(bot))