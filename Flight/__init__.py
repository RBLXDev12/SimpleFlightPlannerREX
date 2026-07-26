from .Flight import FlightPlugin


async def setup(bot):
    await bot.add_cog(FlightPlugin(bot))
