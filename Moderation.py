import discord
from discord.ext import commands
from discord.ext import tasks

def Update(cpage, cdict, tpage):
    key = cdict.keys()
    cpagekey = list(key)[cpage-1]
    updEmbed = discord.Embed(title=cpagekey, description=f"Displaying the {cpagekey} now.")
    for user in cdict[cpagekey]:
        updEmbed.add_field(name=f"Case {list(cdict[cpagekey].keys()).index(user) + 1}", value= f"<@{int(user)}>: {cdict[cpagekey][user]}")
    return updEmbed

class ForwardButton(discord.ui.Button):
    def __init__(self, currentpage, c, totalpages):
        super().__init__(style= discord.ButtonStyle.blurple, label= "Forward", row= 0)
        self.currentpage = currentpage
        self.c = c
        self.totalpages = totalpages

    async def callback(self, interaction : discord.Interaction):
        if self.currentpage != self.totalpages:
            self.currentpage +=1
            await interaction.response.edit_message(embed = Update(self.currentpage, self.c, self.totalpages))
            for component in self.view.children:
                component.currentpage = self.currentpage

class BackwardButton(discord.ui.Button):
    def __init__(self, currentpage, c, totalpages):
        super().__init__(style=discord.ButtonStyle.blurple, label= "Backward", row = 0)
        self.currentpage = currentpage
        self.c = c
        self.totalpages = totalpages

    async def callback(self, interaction : discord.Interaction):
        if self.currentpage > 1:
            self.currentpage -=1
            await interaction.response.edit_message(embed = Update(self.currentpage, self.c, self.totalpages))
            for component in self.view.children:
                component.currentpage = self.currentpage

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Here, I loop the task of cleaning the spam file every 20 seconds
    @tasks.loop(seconds = 15)
    async def clean_spam(seconds = 15):
        with open("spam_detect.txt", "w+") as file:
            file.truncate(0)

    class helpView(discord.ui.View):
        def __init__(self, currentpage, c, totalpages):
            super().__init__()
            self.currentpage = currentpage
            self.c = c
            self.totalpages = totalpages
            self.add_item(BackwardButton(self.currentpage, self.c, self.totalpages))
            self.add_item(ForwardButton(self.currentpage, self.c, self.totalpages))

    #This listener detects spam in the channels except those marked for spam
    @commands.Cog.listener()
    async def on_message(self, message):
        dic = self.bot.col.find_one({"_id": "server_configs"})
        words = dic[str(message.guild.id)]["Words"]
        mod = self.bot.col.find_one({"_id": "role_configs"})[str(message.guild.id)]["Moderator"]

        for word in words:
            if word in message.content:
                await message.channel.send(f"Usage of prohibited word detected!!! Pinging <@{mod}> to take action now.")
        spamchannels = []
        Spambool = False
        data = dict(self.bot.col.find_one({"_id": "server_configs"}))
        spamchannels = data[str(message.guild.id)]["Spam Ignore"]
        Spambool = data[str(message.guild.id)]["Spam"]

        if Spambool and (not spamchannels or message.channel.id not in spamchannels):
            counter = 0
            with open ("spam_detect.txt", "r+") as file:
                for lines in file:
                    if lines.strip("\n") == str(message.author.id) + str(message.channel.id) + message.content:
                        counter += 1

                #If messages sent by the user and the channel + the content of the message is the same for 5 times, we ping the mods
                file.writelines(f"{str(message.author.id) + str(message.channel.id) + message.content}\n")
                if counter > 5:
                    file.truncate(0)
                    id = 0
                    data = dict(self.bot.col.find_one({"_id": "role_configs"}))
                    id = data[str(message.guild.id)]["Moderator"]
                    await message.channel.send(f"You are spamming. Proceeding to ping <@&{id}> to take action.")

    #This is the kick command, pretty self explanatory imo
    @commands.command(description = "Kicks members, supa simple lil command all of ya folks should know right?", aliases = ["yeet"])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason = "No reason provided"):
        await member.kick(reason= reason)
        await ctx.send(f"{member.name} has been kicked for {reason}. All hail Da YEETs!!!")
        await member.send(f"Thou hast been kicked, pestilence, for {reason}.")
        config = self.bot.col.find_one({"_id": "server_configs"})
        try:
            commandlog = self.bot.get_channel(config[str(ctx.guild.id)]["Command Log"])
            embed = discord.Embed(title= "Kick case administered", description= f"<@{member.id}> was kicked by <@{ctx.author.id}> for {reason}")
            embed.set_footer(text=f"Kick command recorded in {ctx.channel.name}")
            await commandlog.send(embed = embed)
        except:
            pass

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

        config = self.bot.col.find_one({"_id": "server_configs"})
        try:
            commandlog = self.bot.get_channel(config[str(ctx.guild.id)]["Command Log"])
            embed = discord.Embed(title= "Ban case administered", description= f"<@{member.id}> was banned by <@{ctx.author.id}> for {reason}")
            embed.set_footer(text=f"Ban command recorded in {ctx.channel.name}")
            await commandlog.send(embed = embed)
        except:
            pass

    @ban.error
    async def banerror(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Hey mods! We have an imposter tryna ban someone without thy permissions. Do with him as thou wisheth.")

    #Unban command to not indulge in the manual hassle of unbanning
    @commands.command(
        description = "Unbans reformed exiles who have redeemed themselves. Do remember, don't hesitate to ban again if you must.",
        aliases = ["unyeet"]
    )
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, memberID, reason):
        member = await self.bot.fetch_user(memberID)
        await ctx.guild.unban(member, reason= reason)
        await ctx.send(f"Member Unbanned!!!! All hail {ctx.guild.name}")

    @unban.error
    async def ubanerror(self,ctx,error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the supreme power to unyeet the yeeted! Begone before I yeet you as well.")

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
        role = None
        MuteRole = None
        data = dict(self.bot.col.find_one({"_id": "role_configs"}))
        role = data[str(ctx.guild.id)]["Member"]
        MuteRole = data[str(ctx.guild.id)]["Mute"]
        if MuteRole is not None and role is not None:
            Role = ctx.guild.get_role(role)
            muteRole = ctx.guild.get_role(MuteRole)
            await user.remove_roles(Role, reason= reason)
            await user.add_roles(muteRole, reason= reason)
            await ctx.send(f"{user.name} has been muted for {reason}!!! All hail {ctx.guild.name}!!!")
            config = self.bot.col.find_one({"_id": "server_configs"})
            try:
                commandlog = self.bot.get_channel(config[str(ctx.guild.id)]["Command Log"])
                embed = discord.Embed(title= "Mute case administered", description= f"<@{user.id}> was muted by <@{ctx.author.id}> for {reason}")
                embed.set_footer(text=f"Mute command recorded in {ctx.channel.name}")
                await commandlog.send(embed = embed)
            except:
                pass
            await ctx.send("You have not configured either the member or the muted role. Configure both to be able to mute members.")

    @mute.error
    async def muteError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You tried to mute someone but can't! Hah! Why shut others' mouths when you can't zip it up yourself?")

    @commands.command(description = "Gives the disabled peasants their ability to talk back. There should be a reward for bad boys when they turn good, right?", aliases = ["unvoid"])
    @commands.has_permissions(kick_members = True)
    async def unmute(self, ctx, user : discord.Member, *, reason= "No reason provided."):
        role = None
        MuteRole = None
        data = dict(self.bot.col.find_one({"_id": "role_configs"}))
        role = data[str(ctx.guild.id)]["Member"]
        MuteRole = data[str(ctx.guild.id)]["Mute"]
        if MuteRole is not None and role is not None:
            Role = ctx.guild.get_role(role)
            muteRole = ctx.guild.get_role(MuteRole)
            await user.remove_roles(muteRole, reason= reason)
            await user.add_roles(Role, reason= reason)
            await ctx.send(f"{user.name} has been unmuted for {reason}!!! All hail {ctx.guild.name}!!!")
            config = self.bot.col.find_one({"_id": "server_configs"})
            try:
                commandlog = self.bot.get_channel(config[str(ctx.guild.id)]["Command Log"])
                embed = discord.Embed(title= "Unmute case administered", description= f"<@{user.id}> was unmuted by <@{ctx.author.id}> for {reason}")
                embed.set_footer(text=f"Unmute command recorded in {ctx.channel.name}")
                await commandlog.send(embed = embed)
            except:
                pass
        else:
            await ctx.send("You have not configured either the member or the muted role. Configure both to be able to mute members.")

    @mute.error
    async def unmuteError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You tried to unmute someone but can't! Hah! You shouldn't try to be a god by giving other their speech back, mortal.")

    #A warm command to give members warnings before voiding them :kekw:
    @commands.command(description = "Warns members that might commit wrongdoings. I mean you have to be merciful since our Satan isn't. [Note: A reason is compulsory for using this command.")
    @commands.has_permissions(kick_members = True)
    async def warn(self, ctx, user : discord.Member, *, reason):
        #Check if the user has warns from the file
        warns = {}
        data = self.bot.col.find_one({"_id": "warns"})
        warns = data[str(ctx.guild.id)]["Warns"]
        if str(user.id) in warns:
            if warns[str(user.id)] == 2:
                #we use the same code we used with mute
                data = self.bot.col.find_one({"_id": "role_configs"})
                role = data[str(ctx.guild.id)]["Member"]
                MuteRole = data[str(ctx.guild.id)]["Mute"]
                if MuteRole is not None and role is not None:
                    Role = ctx.guild.get_role(role)
                    muteRole = ctx.guild.get_role(MuteRole)
                    await user.remove_roles(Role, reason= reason)
                    await user.add_roles(muteRole, reason= reason)
                    warns.pop(str(user.id))
                    await ctx.send(f"{user.name} has been muted over accumulation of 3 warnings. The current reason for warning was {reason}!!! All hail Satan!!!")
                    config = self.bot.col.find_one({"_id": "server_configs"})
                    try:
                        commandlog = self.bot.get_channel(config[str(ctx.guild.id)]["Command Log"])
                        embed = discord.Embed(title= "Warn/Mute case administered", description= f"<@{user.id}> was muted by warning by <@{ctx.author.id}> for {reason}")
                        embed.set_footer(text=f"Warn command recorded in {ctx.channel.name}")
                        await commandlog.send(embed = embed)
                    except:
                        pass
                else:
                    await ctx.send("Cannot warn further, muted role has not been set up. What kind of moderation do you think I'd do if you don't give me the roles, dummy.")
                data[str(ctx.guild.id)]["Warns"] = warns
                self.bot.col.find_and_modify({"_id": "warns"}, data)
            else:
                warnnum = warns[str(user.id)]
                warnnum += 1
                warns.pop(str(user.id))
                warns[str(user.id)] = warnnum
                data[str(ctx.guild.id)]["Warns"] = warns
                await ctx.send(f"{user.name} has been warned for {reason}. Behave yourself or I'm getting the spaceship. Warnings remaining = 1.")
                self.bot.col.find_and_modify({"_id": "warns"}, data)
                config = self.bot.col.find_one({"_id": "server_configs"})
                try:
                    commandlog = self.bot.get_channel(config[str(ctx.guild.id)]["Command Log"])
                    embed = discord.Embed(title= "Warn case administered", description= f"<@{user.id}> was warned by <@{ctx.author.id}> for {reason}")
                    embed.set_footer(text=f"Warn command recorded in {ctx.channel.name}")
                    await commandlog.send(embed = embed)
                except:
                    pass

        else:
            await ctx.send(f"{user.mention} has been warned for {reason}. Behave yourself or I'm getting the spaceship. Warnings remaining = 2.")
            warns[str(user.id)] = 1
            data[str(ctx.guild.id)]["Warns"] = warns
            self.bot.col.find_and_modify({"_id": "warns"}, data)
            config = self.bot.col.find_one({"_id": "server_configs"})
            try:
                commandlog = self.bot.get_channel(config[str(ctx.guild.id)]["Command Log"])
                embed = discord.Embed(title= "Warn case administered", description= f"<@{user.id}> was warned by <@{ctx.author.id}> for {reason}")
                embed.set_footer(text=f"Warn command recorded in {ctx.channel.name}")
                await commandlog.send(embed = embed)
            except:
                pass



    @warn.error
    async def warnError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You can't even handle your own habit of stealing the job of Mods, why try to warn others?")

    #A superwarn commands for more serious stuff
    @commands.command(description = "Warns pestilence for more serious stuff. These get YEETed instantly on 3 warns instead of being muted")
    @commands.has_permissions(kick_members = True)
    async def superwarn(self, ctx, user : discord.Member, *, reason):
        superwarns = {}
        data = self.bot.col.find_one({"_id": "warns"})
        superwarns = data[str(ctx.guild.id)]["Superwarns"]
        if superwarns:
            if str(user.id) in superwarns:
                if superwarns[str(user.id)] == 2:
                    await user.kick(reason= reason)
                    await ctx.send(f"{user.name} has been kicked after the accumulation of 3 superwarnings. The reason for the last superwarning was {reason}. All hail Da YEETs!!!")
                    await user.send(f"Thou hast been kicked, pestilence, after 3 superwarnings. The reason for thy last warning was {reason}.")
                    superwarns.pop(str(user.id))
                    data[str(ctx.guild.id)]["Superwarns"] = superwarns
                    self.bot.col.find_and_modify({"_id": "warns"}, data)
                    config = self.bot.col.find_one({"_id": "server_configs"})
                    try:
                        commandlog = self.bot.get_channel(config[str(ctx.guild.id)]["Command Log"])
                        embed = discord.Embed(title= "Superwarn/Kick case administered", description= f"<@{user.id}> was kicked by superwarning by <@{ctx.author.id}> for {reason}")
                        embed.set_footer(text=f"Superwarn command recorded in {ctx.channel.name}")
                        await commandlog.send(embed = embed)
                    except:
                        pass
                else:
                    superwarns[str(user.id)] += 1
                    data[str(ctx.guild.id)]["Superwarns"] = superwarns
                    await ctx.send(f"{user.name} has been superwarned for {reason}. Behave yourself or face the wrath of Quatara!! Superwarnings remaining = 1.")
                    self.bot.col.find_and_modify({"_id": "warns"}, data)
            else:
                superwarns[str(user.id)] = 1
                data[str(ctx.guild.id)]["Superwarns"] = superwarns
                await ctx.send(f"{user.name} has been superwarned for {reason}. Behave yourself or face the wrath of Quatara!! Superwarnings remaining = 2.")
                self.bot.col.find_and_modify({"_id": "warns"}, data)
                config = self.bot.col.find_one({"_id": "server_configs"})
                try:
                    commandlog = self.bot.get_channel(config[str(ctx.guild.id)]["Command Log"])
                    embed = discord.Embed(title= "Superwarn case administered", description= f"<@{user.id}> was superwarned by <@{ctx.author.id}> for {reason}")
                    embed.set_footer(text=f"Superwarn command recorded in {ctx.channel.name}")
                    await commandlog.send(embed = embed)
                except:
                    pass
        else:
            superwarns[str(user.id)] = 1
            data[str(ctx.guild.id)]["Superwarns"] = superwarns
            await ctx.send(f"{user.name} has been superwarned for {reason}. Behave yourself or face the wrath of Quatara!! Superwarnings remaining = 2.")
            self.bot.col.find_and_modify({"_id": "warns"}, data)
            config = self.bot.col.find_one({"_id": "server_configs"})
            try:
                commandlog = self.bot.get_channel(config[str(ctx.guild.id)]["Command Log"])
                embed = discord.Embed(title= "Superwarn case administered", description= f"<@{user.id}> was superwarned by <@{ctx.author.id}> for {reason}")
                embed.set_footer(text=f"Superwarn command recorded in {ctx.channel.name}")
                await commandlog.send(embed = embed)
            except:
                pass
            
    @superwarn.error
    async def superwarnError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You tried to superwarn without permissions. Satan surely has a separate role reserved for you in hell.")

    #A forgive command in case someone did a lot of good work and you are like, okay let's pardon this guy's warnings
    @commands.command(description = "Clears the warnings from a redeemed soul. Good work, boi!")
    @commands.has_permissions(kick_members = True)
    async def forgive(self, ctx, user : discord.Member):
        data = self.bot.col.find_one({"_id": "warns"})
        warns = data[str(ctx.guild.id)]["Warns"]
        superwarns = data[str(ctx.guild.id)]["Superwarns"]
        if str(user.id) in warns and str(user.id) in superwarns:
            warns.pop(str(user.id))
            superwarns.pop(str(user.id))
            await ctx.send(f"{user.name}, you have been forgiven for your good deeds from the sins of your pasts. You live as a free man now. Just remember: Try not to repeat the mistakes you made. Have a good day.")
            data[str(ctx.guild.id)]["Warns"] = warns
            data[str(ctx.guild.id)]["Superwarns"] = superwarns
            self.bot.col.find_and_modify({"_id": "warns"}, data)
            config = self.bot.col.find_one({"_id": "server_configs"})
            try:
                commandlog = self.bot.get_channel(config[str(ctx.guild.id)]["Command Log"])
                embed = discord.Embed(title= "Forgive case administered", description= f"<@{user.id}> was forgived by <@{ctx.author.id}>.")
                embed.set_footer(text=f"Forgive command recorded in {ctx.channel.name}")
                await commandlog.send(embed = embed)
            except:
                pass
        elif str(user.id) in warns:
            warns.pop(str(user.id))
            await ctx.send(f"{user.name}, you have been forgiven for your good deeds from the sins of your pasts. You live as a free man now. Just remember: Try not to repeat the mistakes you made. Have a good day.")
            data[str(ctx.guild.id)]["Warns"] = warns
            self.bot.col.find_and_modify({"_id": "warns"}, data)
            config = self.bot.col.find_one({"_id": "server_configs"})
            try:
                commandlog = self.bot.get_channel(config[str(ctx.guild.id)]["Command Log"])
                embed = discord.Embed(title= "Forgive case administered", description= f"<@{user.id}> was forgived by <@{ctx.author.id}>.")
                embed.set_footer(text=f"Forgive command recorded in {ctx.channel.name}")
                await commandlog.send(embed = embed)
            except:
                pass
        elif str(user.id) in superwarns:
            superwarns.pop(str(user.id))
            await ctx.send(f"{user.name}, you have been forgiven for your good deeds from the sins of your pasts. You live as a free man now. Just remember: Try not to repeat the mistakes you made. Have a good day.")
            data[str(ctx.guild.id)]["Superwarns"]
            self.bot.col.find_and_modify({"_id": "warns"}, data)
            config = self.bot.col.find_one({"_id": "server_configs"})
            try:
                commandlog = self.bot.get_channel(config[str(ctx.guild.id)]["Command Log"])
                embed = discord.Embed(title= "Forgive case administered", description= f"<@{user.id}> was forgived by <@{ctx.author.id}>.")
                embed.set_footer(text=f"Forgive command recorded in {ctx.channel.name}")
                await commandlog.send(embed = embed)
            except:
                pass
        else:
            await ctx.send("We can't find any warns for our good boi. I don't think they've sinned before, mind checking your records?")

    @forgive.error
    async def forgiveError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You can't forgive when you don't have the power to. So don't try to act smart, it's scummy. And sus.")

    #A command to add spam channels.
    @commands.command(description = "Adds spam channels where spamming is allowed.")
    @commands.has_permissions(administrator = True)
    async def addspam(self, ctx, channel : discord.TextChannel):
        spam_channels = []
        data = dict(self.bot.col.find_one({"_id": "server_configs"}))
        spam_channels = data[str(ctx.guild.id)]["Spam Ignore"]
        if channel.id in spam_channels:
            await ctx.send("This channel already exists in our spam list.")
        else:
            data[str(ctx.guild.id)]["Spam Ignore"].append(channel.id)
            self.bot.col.find_and_modify({"_id": "server_configs"}, data)
            
            await ctx.send(f"Spam channel has been added to our list. We shall  not ping the moderators on spams in {channel.name} from now on.")

    @addspam.error
    async def addspamError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not decide which channels I do not detect spam in! Begone thot!")

    #Aaaaaand another command to remove them
    @commands.command(description = "Removes a channel from spam channels where spamming is allowed.")
    @commands.has_permissions(administrator = True)
    async def rmspam(self, ctx, channel : discord.TextChannel):
        spam_channels =  []
        data = dict(self.bot.col.find_one({"_id": "server_configs"}))
        spam_channels = data[str(ctx.guild.id)]["Spam Ignore"]
        if channel.id in spam_channels:
            data[str(ctx.guild.id)]["Spam Ignore"].remove(channel.id)
            self.bot.col.find_and_modify({"_id": "server_configs"}, data)
            await ctx.send("Spam channel removed!!!")
        else:
            await ctx.send("The channel isn't in the list of channels where spamming is allowed. Look again, maybe?")

    @rmspam.error
    async def rmspamError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not decide which channels I detect spam in! Begone thot!")

    #Flips the spam on or off
    @commands.command(description = "Toggles the spam to on or off on your server. Gotta keep spammers at bay!")
    @commands.has_permissions(administrator = True)
    async def togglespam(self, ctx):
        data = dict(self.bot.col.find_one({"_id": "server_configs"}))
        data[str(ctx.guild.id)]["Spam"] = not(data[str(ctx.guild.id)]["Spam"])
        truth = data[str(ctx.guild.id)]["Spam"]
        self.bot.col.find_and_modify({"_id": "server_configs"}, data)
        await ctx.send(f"Spam detection has been set to {truth} on your server.")
    
    @togglespam.error
    async def tserror(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the authorisation to decide to toggle the spam for this server! Next time, consult your superiors.")

    #Sets the Moderator role to be pinged when Spam occurs on your server
    @commands.command(description = "Sets the role to be mentioned when spam is detected on your server to start the spicy drama.")
    @commands.has_permissions(administrator = True)
    async def setMod(self, ctx, role : discord.Role):
        data = dict(self.bot.col.find_one({"_id": "role_configs"}))
        data[str(ctx.guild.id)]["Moderator"] = role.id
        self.bot.col.find_and_modify({"_id": "role_configs"}, data)
        await ctx.send(f"Moderator role is now set to {role.mention}. This role will now be pinged when spam is detected.")

    @setMod.error
    async def sMerror(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Begone mortal! You cannot set the moderator role for this server! Have an admin try to use the command!")

    @commands.command(description = "Sets the Member role which is to logged to members when they join and removed when they are muted.")
    @commands.has_permissions(kick_members = True)
    async def setMember(self, ctx, role : discord.Role):
        data = {}
        data = dict(self.bot.col.find_one({"_id": "role_configs"}))
        data[str(ctx.guild.id)]["Member"] = role.id
        self.bot.col.find_and_modify({"_id": "role_configs"}, data)
        await ctx.send(f"The Member role is now set to {role.mention}. This role will now be given to members when they join the server and will be taken away when muted.")

    @setMember.error
    async def sMembError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cannot set the member role when your own role in the server is negligible. Begone!")

    @commands.command(description = "Sets the mute role to be given to members whence they are muted. Have to make a specification of disability to cause it, after all.")
    @commands.has_permissions(kick_members = True)
    async def setMute(self, ctx, role : discord.Role):
        data = {}
        data = dict(self.bot.col.find_one({"_id": "role_configs"}))
        data[str(ctx.guild.id)]["Mute"] = role.id
        self.bot.col.find_and_modify({"_id": "role_configs"}, data)
        await ctx.send(f"The Muted role is now set to {role.mention}. This role will now be given to members when they are muted in replacement of the general Member role.")

    @setMute.error
    async def setMuteError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cannot set the muted role when your own role in the server is negligible. Begone!")

    #Flips the spam on or off
    @commands.command(description = "Toggles the autorole to on or off on your server. Autorole on gives the new joining members the Member role automatically.")
    @commands.has_permissions(administrator = True)
    async def toggleautorole(self, ctx):
        data = dict(self.bot.col.find_one({"_id": "server_configs"}))
        data[str(ctx.guild.id)]["Autorole"] = not(data[str(ctx.guild.id)]["Autorole"])
        truth = data[str(ctx.guild.id)]["Spam"]
        self.bot.col.find_and_modify({"_id": "server_configs"}, data)
        await ctx.send(f"Autoroles has been set to {truth} on your server.")
    
    @toggleautorole.error
    async def tarerror(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        await ctx.send("You are not authorised to decide who gets what role. Begone!")

    #A display command to display the Warnings and Superwarnings in the server
    @commands.command(
        description = "A command which enables you to view the warns and superwarns of the members in your server. A quick peek is always cool, y'know.",
        aliases = ["viewwarns", "warns"]
    )
    async def displaywarns(self, ctx):
        data = self.bot.col.find_one({"_id": "warns"})
        Warns = data[str(ctx.guild.id)]
        if Warns["Warns"].__len__() == 0 and Warns["Superwarns"].__len__() == 0:
            await ctx.send("No data to show, nobody has warns or superwarns in your server!")
        else:
            totalPages = 2
            currentPage = 1
            message = await ctx.send(embed= Update(currentPage, Warns, totalPages), view = self.helpView(currentPage, Warns, totalPages))

#            #Here we control the page configuration by adding emotes for reaction that can be detected by bot to change the page.
#            await message.add_reaction("◀️")
#            await message.add_reaction("▶️")
#
#            #This is the check function, which is passed to ensure the user is the same as the one who asked for help, and the reaction is among the emojis specified
#            def check(reaction, user):
#                return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
#
#            while True:
#                #We wait for a reaction from the user
#                reaction, user = await self.bot.wait_for("reaction_add", timeout=3000, check=check)
#
#                #Check if the emoji is the forward one and current page is not the last, we go onto the next page
#                if str(reaction.emoji) == "▶️" and currentPage != totalPages:
#                    currentPage += 1
#                    await message.edit(embed= Update(currentPage, Warns, totalPages))
#                    await message.remove_reaction(reaction, user)
#                #Check if the emoji is the backward one and current page is not the first, we go onto the previous page
#                elif str(reaction.emoji) == "◀️" and currentPage > 1:
#                    currentPage -= 1
#                    await message.edit(embed= Update(currentPage, Warns, totalPages))
#                    await message.remove_reaction(reaction, user)
#                #Otherwise
#                else:
#                    await message.remove_reaction(reaction, user)

    #Now a command to add to the moderation of certain special words
    @commands.command(
        description = "Adds new keywords to moderate. You don't want those dum dums to spoil the kids after all, do you?",
    )
    async def addWord(self, ctx, *, word):
        dic = self.bot.col.find_one({"_id": "server_configs"})
        if "Words" not in dic[str(ctx.guild.id)]:
            words = [word]
            await ctx.send("The word has now been registered!!! We shall now ping the moderators whenever said word or phrase is detected in chat. ")
            dic[str(ctx.guild.id)]["Words"] = words
        else:
            words = dic[str(ctx.guild.id)]["Words"]
            if word in words:
                await ctx.send("The word/phrase already exists in our record!")
            else:
                words.append(word)
                await ctx.send("The word has now been registered!!! We shall now ping the moderators whenever said word or phrase is detected in chat. ")
                dic[str(ctx.guild.id)]["Words"] = words
        self.bot.col.find_and_modify({"_id": "server_configs"}, dic)
        try:
            commandlog = self.bot.get_channel(dic[str(ctx.guild.id)]["Command Log"])
            embed = discord.Embed(title= "Word Remove case administered", description= f"<@{ctx.author.id}> has added ||{word}|| to moderated words!!")
            embed.set_footer(text=f"Remove Word command recorded in {ctx.channel.name}")
            await commandlog.send(embed = embed)
        except:
            pass

    #And now a command to remove said words.
    @commands.command(
        description = "Adds new keywords to moderate. You don't want those dum dums to spoil the kids after all, do you?",
    )
    async def rmWord(self, ctx, *, word):
        dic = self.bot.col.find_one({"_id": "server_configs"})
        if "Words" not in dic[str(ctx.guild.id)]:
            await ctx.send("Word not found in our record. Mind checking it again?")
        else:
            words = dic[str(ctx.guild.id)]["Words"]
            if word in words:
                words.remove(word)
                await ctx.send("The word/phrase has been removed from the record!")
                dic[str(ctx.guild.id)]["Words"] = words
            else:
                await ctx.send("Word not found in our record. Mind checking it again?")
        self.bot.col.find_and_modify({"_id": "server_configs"}, dic)
        try:
            commandlog = self.bot.get_channel(dic[str(ctx.guild.id)]["Command Log"])
            embed = discord.Embed(title= "Word Remove case administered", description= f"<@{ctx.author.id}> has added ||{word}|| to moderated words!!")
            embed.set_footer(text=f"Remove Word command recorded in {ctx.channel.name}")
            await commandlog.send(embed = embed)
        except:
            pass
                
def setup(bot):
    bot.add_cog(Moderation(bot))