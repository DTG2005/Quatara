from os import name
import discord
import asyncio
import random
from PIL import Image, ImageDraw, ImageOps
from io import BytesIO

from discord.ext import commands
def crop_to_circle(im):
    size = (145, 145)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output

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

    @commands.hybrid_command(
        description = "Gives a prediction for a future event! Yes they are always true. *sighs*",
        aliases = ["8ball", "soothsay"]
    )
    async def predict(self, ctx, *, question):
        colordict = {"Good": 0x00ff00, "Bad": 0xff0000, "Neutral": discord.Colour.orange()}
        choice = random.choice(["Good", "Bad", "Neutral"])
        answer = random.choice(predict_dict[choice])

        Sendembed = discord.Embed(title= "Prediction", color= colordict[choice])
        Sendembed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar.url)
        Sendembed.add_field(name= f"Question: {question}", value = f"Answer: {answer}")
        await ctx.send(embed= Sendembed)

    @commands.hybrid_command(
        description = "Rolls a dice. Give a number to roll a total of it, or skip the number to roll a default of six",
        aliases = ["dice", "die"]
    )
    async def roll(self, ctx, number : int = 6):
        embed1 = discord.Embed(title= "Dice Roll", description= f"Rolled out of {number}", color= discord.Color(0x350cf9))
        embed1.add_field(name= "And your number is!", value= str(random.randint(1, number)))
        embed1.set_author(name= ctx.author.name, icon_url= ctx.author.avatar.url)
        await ctx.send(embed= embed1)

    @commands.hybrid_command(
        description = "Predicts an answer from a given number of options. After all it's not always in binary.",
        aliases = ["multiple", "multipredict"]
    )
    async def mcqpredict(self, ctx, *, question):
        await ctx.send("Question recorded, please list the options or say 'done' to end the prompt.")
        def check(message):
            return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id

        options = []
        while True:
            try:
                message = await self.bot.wait_for('message', timeout = 20.0, check= check)
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

    @commands.hybrid_command(
        description = "Yeets a disgrace off into the void. YEEEEEEEEEEEEEEEEEEET!!!",
        aliases = ["YEEEET"]
    )
    async def yeetimg(self, ctx, user: discord.Member):
        asset = None
        try:
            asset = user.avatar.with_size(128)
        except Exception as e:
            await ctx.send(e)
            await ctx.send("I need a second person to yeet, dummy. Try again cautiously or I'll yeet you.")
        data = BytesIO(await asset.read())
        asset2 = ctx.author.avatar.with_size(128)
        data2 = BytesIO(await asset2.read())
        pfp2 = Image.open(data2)

        YEET = Image.open("Images/Yeet.jpg")
        pfp = Image.open(data)
        YEET.paste(pfp.resize((60, 60)), (180, 46))
        YEET.paste(pfp2.resize((60,60)), (229, 117))
        YEET.paste(pfp.resize((60, 60)), (129, 343))
        YEET.paste(pfp2.resize((60,60)), (69, 322))
        YEET.paste(pfp.resize((60, 60)), (240, 288))
        YEET.paste(pfp2.resize((60,60)), (396, 364))

        YEET.save("Images/Profiles/profile2.jpg")
        await ctx.send(file= discord.File("Images/Profiles/profile2.jpg"))
                
async def setup(bot):
    await bot.add_cog(Fun(bot))