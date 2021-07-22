import discord
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
def setup(bot):
    bot.add_cog(Fun(bot))