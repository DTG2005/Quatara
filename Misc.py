from logging import error
import discord
from discord import embeds
from discord.errors import HTTPException, InteractionResponded
from discord.ext import commands
import asyncio

class ForwardButton(discord.ui.Button):
    def __init__(self, currentpage, c, totalpages):
        super().__init__(style= discord.ButtonStyle.blurple, label= "Forward", row= 0)
        self.currentpage = currentpage
        self.c = c
        self.totalpages = totalpages

    async def callback(self, interaction : discord.Interaction):
        if self.currentpage != self.totalpages:
            self.currentpage +=1
            await interaction.response.edit_message(embed = updateEmbed(self.currentpage, self.c, self.totalpages))
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
            await interaction.response.edit_message(embed = updateEmbed(self.currentpage, self.c, self.totalpages))
            for component in self.view.children:
                component.currentpage = self.currentpage

            
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
    
    class helpView(discord.ui.View):
        def __init__(self, currentpage, c, totalpages):
            super().__init__()
            self.currentpage = currentpage
            self.c = c
            self.totalpages = totalpages
            self.add_item(BackwardButton(self.currentpage, self.c, self.totalpages))
            self.add_item(ForwardButton(self.currentpage, self.c, self.totalpages))

            

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
        await ctx.send(embed= updateEmbed(currentPage, c, totalPages), view=self.helpView(currentPage, c, totalPages))

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Misc(bot))