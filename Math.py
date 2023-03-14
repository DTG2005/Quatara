import discord
import asyncio
import math
from discord.ext import commands

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        description= "Make me add for you, hmph!"
    )
    async def add(self, ctx):
        await ctx.send("I am now capturing the numbers you wish to add. Please write the numbers, and say 'done' when you are finished. Text responses will not be recorded.")
        nums = []
        def check(message):
            return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id
        
        while True:
            try:
                message = await self.bot.wait_for('message', timeout = 20.0, check = check)
            except asyncio.TimeoutError():
                await ctx.send("Timeout! Try again")
            else:
                if message.content == 'done':
                    if nums:
                        break
                    else:
                        await ctx.send("Cannot add nothing, unless you want me to say 0.")
                else:
                    try:
                        nums.append(float(message.content))
                        await message.add_reaction("👍")
                    except ValueError:
                        await message.channel.send("That's a text, dummy. Send NUMBERS. **N U M B E R S**.")
                        continue
        sum = 0
        for i in nums:
            sum += i
        await ctx.send(sum)

    @commands.hybrid_command(
        description="Lets me do the subtraction by myself.",
        aliases = ["minus"]
    )
    async def subtract(self, ctx, minuend : float, subtrahend : float):
        await ctx.send(minuend - subtrahend)

    @commands.hybrid_command(
        description= "Division for dummies!",
    )
    async def divide(self, ctx, dividend: float, divisor: float):
        await ctx.send(dividend / divisor)

    @commands.hybrid_command(
        description="Performs quick division to give you the integer quotient."
    )
    async def quotient(self, ctx, dividend : float, divisor: float):
        await ctx.send(dividend//divisor)

    @commands.hybrid_command(
        description="Performs quick division to give you the remainder."
    )
    async def remainder(self, ctx, dividend : float, divisor: float):
        await ctx.send(dividend%divisor)

    @commands.hybrid_command(
        description="Performs exponentiation.",
        aliases= ['exponent', 'raisedto']
    )
    async def power(self, ctx, base : float, index: float):
        await ctx.send(base**index)

    @commands.hybrid_command(
        description="Sin function. Iykyk.",
    )
    async def sin(self, ctx, radians:float):
        await ctx.send(f"sin {radians} = {math.sin(radians)}")
        
    @commands.hybrid_command(
        description="Cos function. Iykyk.",
    )
    async def cos(self, ctx, radians: float):
        await ctx.send(f"cos {radians} = {math.cos(radians)}")
    
    @commands.hybrid_command(
        description="Tan function. Iykyk.",
    )
    async def tan(self, ctx, radians: float):
        await ctx.send(f"tan {radians} = {math.tan(radians)}")

    @commands.hybrid_command(
        description="Gives you the square root of the number."
    )
    async def sqrt(self, ctx, num: float):
        await ctx.send(math.sqrt(num))

    @commands.hybrid_command(description="Gives you the value of pi, π.")
    async def pi(self, ctx):
        await ctx.send(f"π = {math.pi}")

    
    async def cog_command_error(self, ctx, error):
        if isinstance(error, ValueError):
            await ctx.send("That's a text, dummy. Send NUMBERS. **N U M B E R S**.")


async def setup(bot):
    await bot.add_cog(Math(bot))