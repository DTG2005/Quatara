import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #This listener detects spam in the channels except those marked for spam
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel not in self.bot.spam_channels:
            counter = 0
            with open ("spam_detect.txt", "r+") as file:
                for lines in file:
                    if lines.strip("\n") == str(message.author.id) + str(message.channel.id):
                        counter += 1

                file.writelines(f"{str(message.author.id) + str(message.channel.id)}\n")
                if counter > 5:
                    file.truncate(0)
                    await message.channel.send("You are spamming. Proceeding to ping <@305403872438910977>, <@698218252119179365> and <@384331120755474442> to take action.")

    #This is the kick command, pretty self explanatory imo
    @commands.command(description = "Kicks members, supa simple lil command all of ya folks should know right?", aliases = ["yeet"])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason = "No reason provided"):
        await member.kick(reason= reason)
        await ctx.send(f"{member.name} has been kicked for {reason}. All hail Da YEETs!!!")
        await member.send(f"Thou hast been kicked, pestilence, for {reason}.")

    #If the user doesn't have the permission, we display this message
    @kick.error
    async def kickerror(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Hey mods! We have an imposter tryna kick someone without thy permissions. Do with him as thou wisheth.")
        else:
            print(error)

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
    @commands.command(description = "Clears the given set of commands so you don't have to dirty your hands.", aliases = ["clean", "tidy", "purge"])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amt):
        await ctx.channel.purge(limit = int(amt) + 1)

    @clear.error
    async def clearError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry but it seems you do not have the permissions to use this command. Thanks with the goodwill for cleannup though! :thumbsup:.")

    @commands.command(description = "Voids the pestilence into your void! After all, there's no sound in space.", aliases = ["void"])
    @commands.has_permissions(kick_members = True)
    async def mute(self, ctx, user : discord.Member, *, reason= "No reason provided."):
        role = discord.utils.get(member.guild, name='noobmaster69')
        voider = discord.utils.get(member.guild, name='voider')
        await user.remove_roles(role, reason= reason)
        await user.add_roles(voider, reason= reason)
        await ctx.send(f"{user.name} has been muted for {reason}!!! All hail Da YEET GOD!!!")

    @mute.error
    async def muteError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You tried to mute someone but can't! Hah! Why shut others' mouths when you can't zip it up yourself?")

    #A warm command to give members warnings before voiding them :kekw:
    @commands.command(description = "Warns members that might commit wrongdoings. I mean you have to be merciful since our Satan isn't. [Note: A reason is compulsory for using this command.")
    @commands.has_permissions(kick_members = True)
    async def warn(self, ctx, user : discord.Member, *, reason):
        if self.bot.warns:
            if user in self.bot.warns:
                if self.bot.warns[user] == 4:
                    role = discord.utils.get(member.guild, name='noobmaster69')
                    voider = discord.utils.get(member.guild, name='voider')
                    await user.remove_roles(role, reason= reason)
                    await user.add_roles(voider, reason= reason)
                    await ctx.send(f"{user.name} has been muted over accumulation of 3 warnings. The current reason for warning was {reason}!!! All hail Da YEET GOD!!!")
                self.bot.warns[user] += 1
                await ctx.send(f"{user.name} has been warned for {reason}. Behave yourself or I'm getting the spaceship. Warnings remaining = {3 - self.bot.warns[user]}.")
            else:
                self.bot.warns[user] = 1
                await ctx.send(f"{user.name} has been warned for {reason}. Behave yourself or I'm getting the spaceship. Warnings remaining = {3 - self.bot.warns[user]}.")

    @warn.error
    async def warnError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You can't even handle your own habit of stealing the job of Mods, why try to warn others?")

    #A superwarn commands for more serious stuff
    @commands.command(description = "Warns pestilence for more serious stuff. These get YEETed instantly on 3 warns instead of being muted")
    @commands.has_permissions(kick_members = True)
    async def superwarn(self, ctx, user : discord.Member, *, reason):
        if self.bot.superwarns:
            if user in self.bot.superwarns:
                if self.bot.superwarns[user] == 4:
                    await user.kick(reason= reason)
                    await ctx.send(f"{user.name} has been kicked after the accumulation of 3 superwarnings. The reason for the last superwarning was {reason}. All hail Da YEETs!!!")
                    await user.send(f"Thou hast been kicked, pestilence, after 3 superwarnings. The reason for thy last warning was {reason}.")
                self.bot.superwarns[user] += 1
                await ctx.send(f"{user.name} has been superwarned for {reason}. Behave yourself or face the wrath of Da YEETS!! Superwarnings remaining = {3 - self.bot.superwarns[user]}.")
            else:
                self.bot.warns[user] = 1
                await ctx.send(f"{user.name} has been warned for {reason}. Behave yourself or face the wrath of Da YEETS!! Superwarnings remaining = {3 - self.bot.superwarns[user]}.")
            
    @superwarn.error
    async def superwarnError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You tried to superwarn without permissions. Satan surely has a separate role reserved for you in hell.")

    #A forgive command in case someone did a lot of good work and you are like, okay let's pardon this guy's warnings
    @commands.command(description = "Clears the warnings from a redeemed soul. Good work, boi!")
    @commands.has_permissions(kick_members = True)
    async def forgive(self, ctx, user : discord.Member):
        if self.bot.warns and self.bot.superwarns:
            if user in self.bot.warns and self.bot.superwarns:
                self.bot.warns.pop(user)
                self.bot.warns.pop(user)
                await ctx.send(f"{user.name}, you have been forgiven for your good deeds from the sins of your pasts. You live as a free man now. Just remember: Try not to repeat the mistakes you made. Have a good day.")
            elif user in self.bot.warns:
                self.bot.warns.pop(user)
                await ctx.send(f"{user.name}, you have been forgiven for your good deeds from the sins of your pasts. You live as a free man now. Just remember: Try not to repeat the mistakes you made. Have a good day.")
            elif user in self.bot.sueprwarns:
                await ctx.send(f"{user.name}, you have been forgiven for your good deeds from the sins of your pasts. You live as a free man now. Just remember: Try not to repeat the mistakes you made. Have a good day.")
            else:
                await ctx.send("We can't find any warns for our good boi. I don't think he's sinned before, mind checking your records?")
        else:
            await ctx.send("We can't find any warns for our good boi. I don't think he's sinned before, mind checking your records?")

    @forgive.error
    async def forgiveError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You can't forgive when you don't have the power to. So don't try to act smart, it's scummy. And sus.")

    #A command to add spam channels.
    @commands.command(description = "Adds spam channels where spamming is allowed.")
    @commands.has_permissions(administrator = True)
    async def addspam(self, ctx, channel : discord.TextChannel):
        if channel in self.bot.spam_channels:
            await ctx.send("This channel already exists in our spam list.")
        else:
            self.bot.spam_channels.append(channel)
            await ctx.send("Spam channels added!!!!")

    @addspam.error
    async def addspamError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not decide which channels I do not detect spam in! Begone thot!")

    #Aaaaaand another command to remove them
    @commands.command(description = "Removes a channel from spam channels where spamming is allowed.")
    @commands.has_permissions(administrator = True)
    async def rmspam(self, ctx, channel : discord.TextChannel):
        if channel in self.bot.spam_channels:
            self.bot.spam_channels.remove(channel)
            await ctx.send("Spam channel removed!!!")
        else:
            await ctx.send("The channel isn't in the list of channels where spamming is allowed. Look again, maybe?")

    @addspam.error
    async def rmspamError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not decide which channels I detect spam in! Begone thot!")

def setup(bot):
    bot.add_cog(Moderation(bot))