import discord
from discord.ext import commands
from diffusers import AutoPipelineForText2Image
import torch

class ML(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(description="I grab my paintbrush and paint whatever rubbish you tell me to paint. Credits: Stable Diffusion")
    async def genim(self, ctx : commands.Context, prompt):
        message = await ctx.send("Processing your input and sending the image soon...\nWarning: It may take up to 15 mins, pretty slow ik")
        image = self.bot.pipe(prompt).images[0]
        image.save("output1.png")
        output = discord.File('output1.png')
        embed = discord.Embed(
            color=discord.Color.blurple(),
            title= "Image Generation using Stable Diffusion",
            description=prompt
        )
        embed = embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_image(url='attachments://output1.png')
        await ctx.send(embed=embed, file=output)


async def setup(bot):
    await bot.add_cog(ML(bot))