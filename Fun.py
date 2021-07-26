from discord.colour import Color
from os import name
import discord
import asyncio
import random

from discord.ext import commands

predict_dict = {
    "Good": 
    [
        "Yes! It certainly seems so.",
        "Indeed. It is truthful.", 
        "Positive! I see it to be certain.", 
        "Yes! Yes it is very probable.", 
        "I would go with yes for this one."
    ],
    "Bad": 
    [
        "No! That is certainly not true.", 
        "Uh uh, that seems false.",
        "Negative! It seems certain to be false.", 
        "No. No it is improbable.", 
        "I would go with a no for this one."
    ],
    "Neutral":
    [
        "Outlook appears hazy. Try again.",
        "I cannot find a prediction. Try again?",
        "Prediction uncertain."
    ]
}

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        description = "Gives a prediction for a future event! It is said that my predictions come true if your reality coexists with your mental framework.",
        aliases = ["8ball", "soothsay"]
    )
    async def predict(self, ctx, *, question):
        colordict = {"Good": 0x00ff00, "Bad": 0xff0000, "Neutral": discord.Colour.orange()}
        choice = random.choice(["Good", "Bad", "Neutral"])
        answer = random.choice(predict_dict[choice])

        Sendembed = discord.Embed(title= "Prediction", color= colordict[choice])
#        Sendembed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        Sendembed.add_field(name= f"Question: {question}", value = f"Answer: {answer}")
        await ctx.send(embed= Sendembed)

    @commands.command(
        description = "Rolls a dice that is too nice. Give a number to roll out of a total of it, or skip the number to roll from a default of six",
        aliases = ["dice", "die"]
    )
    async def roll(self, ctx, number : int = 6):
        embed1 = discord.Embed(title= "Dice Roll", description= f"Rolled out of {number}", color= discord.Color(0x350cf9))
        embed1.add_field(name= "And your number is!", value= str(random.randint(1, number)))
#        embed1.set_author(name= ctx.author.name, icon_url= ctx.author.avatar_url)
        await ctx.send(embed= embed1)

    @commands.command(
        description = "Predicts an answer from a given number of options. After all it's not always in binary.",
        aliases = ["multiple", "multipredict"]
    )
    async def mcqpredict(self, ctx, *, question):
        await ctx.send("Question recorded, please list the options or say 'done' to end the prompt.")
        def check(message):
            return message.author.id == ctx.author.id

        options = []
        while True:
            try:
                message = await self.bot.wait_for('message', timeout = 60.0, check= check)
            except asyncio.TimeoutError:
                await ctx.send("Timeout! Try the prediction again.")
                break
            else:
                if message.content == "done":
                    if options:
                        break
                    else:
                        await ctx.send("I am not intelligent enough to choose from nothingness. Give me options.")
                else:
                    options.append(message.content)
                    await message.add_reaction("👍")
        answer = random.choice(options)
        embed1 = discord.Embed(title= "Multiple Choice Prediction", description=f"And the answer is {answer}", color= discord.Color(0x350cf9)) 
        for value in options:
            embed1.add_field(name= f"Option {options.index(value) + 1}", value=value)
        await ctx.send(embed=embed1)
                
def setup(bot):
    bot.add_cog(Fun(bot))