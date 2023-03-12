import discord
from discord.ext import commands

class Conversions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        description= "Converts C to F."
    )
    async def tempc2f(self, ctx, temp: float):
        await ctx.send(f"Temperature in F is {9 * temp/5 + 32}")

    @commands.hybrid_command(
        description= "Converts F to C."
    )
    async def tempf2c(self, ctx, temp : float):
        await ctx.send(f"Temperature in C is {(temp-32)/9 * 5}")

    @commands.hybrid_command(
        description= "Converts kilogram to pounds."
    )
    async def wtkgtolb(self, ctx, mass : float):
        await ctx.send(f"{mass * 2.205} lb")

    @commands.hybrid_command(
        description= "Converts kilogram to pounds."
    )
    async def wtlbtokg(self, ctx, mass : float):
        await ctx.send(f"{mass / 2.205} kg")

    @commands.hybrid_command(
        description="Converts inches into centimeters."
    )
    async def lenintocm(self, ctx, length : float):
        await ctx.send(f"{length * 2.5} cm")

    @commands.hybrid_command(
        description="Converts centimeters into inches."
    )
    async def lencmtoin(self, ctx, length : float):
        await ctx.send(f"{length / 2.5} in")

    @commands.hybrid_command(
        description="Converts feet into cm."
    )
    async def lenintocm(self, ctx, length : float):
        await ctx.send(f"{length * 2.5} cm")

    @commands.hybrid_command(
        description="Converts metres into yards."
    )
    async def lenmtoy(self, ctx, length : float):
        await ctx.send(f"{length*1.094} yards")

    @commands.hybrid_command(
        description="Converts yards into metres."
    )
    async def lenytom(self, ctx, length : float):
        await ctx.send(f"{length / 1.094} m")

    @commands.hybrid_command(
        description="Converts miles into kilometers."
    )
    async def lenmiltokm(self, ctx, length : float):
        await ctx.send(f"{1.609 * length} km")
    
    @commands.hybrid_command(
        description= "Converts kilometers into miles."
    )
    async def lenkmtomil(self, ctx, length : float):
        await ctx.send(f"{length / 1.609} mil")

    @commands.hybrid_command(
        description="Converts gallons into liters"
    )
    async def volgalltolit(self, ctx, volume : float):
        await ctx.send(f"{3.785 * volume} L")
    
    @commands.hybrid_command(
        description="Converts liters into gallons"
    )
    async def vollittogall(self, ctx, volume : float):
        await ctx.send(f"{3.785 * volume} gallons")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, ValueError):
            await ctx.send("That's a text, dummy. Send NUMBERS for measurements. **N U M B E R S**.")
    
async def setup(bot):
    await bot.add_cog(Conversions(bot))