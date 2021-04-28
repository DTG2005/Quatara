import discord
from discord.ext import commands
import asyncio

c = {}
# Made the function so I don't have to repeat iterating through the dictionary again and again, mostly cuz I'm lazy :p XD XD
def updateEmbed(cpage, cdict, tpage):
    key = cdict.keys()
    cpageKey = list(key)[cpage - 1]
    hlp = discord.Embed(title= cpageKey, description = "Commands for this cog", color = discord.Color(0x350cf9))
    for command in cdict[cpageKey]:
        hlp.add_field(name= command, value= cdict[cpageKey][command])

    hlp.add_field(name="page", value=f"{cpage}/{tpage}", inline=False)
    return hlp

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Commands that are more or less QOL and don't fall in the above categories."
        self.cogName = "Misc"

    @commands.command(description = "Displays this message, what do you think you're doing, sucker?", aliases = ["assist"], invoke_without_command = True)
    async def help(self,ctx):

        currentPage = 1
        #for each cog in the bot, we are going to iterate and find out the commands
        for cog in self.bot.cogs:
            commands = self.bot.cogs[cog].get_commands()
            c[cog] = {}
            for command in commands:
                #and append them to the dictionary c
                c[cog][command.name] = command.description

        #So the total pages are equal to the number of cogs, which are the elements in this case
        totalPages = len(c)

        message = await ctx.send(embed= updateEmbed(currentPage, c, totalPages))
        await ctx.send("Knock knock")

        #Here we control the page configuration by adding emotes for reaction that can be detected by bot to change the page.
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        #This is the check function, which is passed to ensure the user is the same as the one who asked for help, and the reaction is among the emojis specified
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

        while True:
            try:
                #We wait for a reaction from the user
                reaction, user = await bot.wait_for("reaction_add", timeout=3000, check=check)

                #Check if the emoji is the forward one and current page is not the last, we go onto the next page
                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    currentPage += 1
                    await message.edit(embed= updateEmbed(currentPage, c, totalPages))
                    await message.remove_reaction(reaction, user)

                #Check if the emoji is the backward one and current page is not the first, we go onto the previous page
                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    currentPage -= 1
                    await message.edit(embed= updateEmbed(currentPage, c, totalPages))
                    await message.remove_reaction(reaction, user)

                #Otherwise
                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError():
                await ctx.send("Reaction time is up. Send a fresh command Please!")

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Misc(bot))