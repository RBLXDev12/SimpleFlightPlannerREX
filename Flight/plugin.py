import discord
from discord.ext import commands

from .database import load, save, ensure_storage



class FlightPlugin(commands.Cog):

    __version__ = "1.0.0"


    def __init__(self, bot):

        self.bot = bot

        ensure_storage()



    # ==============================
    # MAIN FLIGHT GROUP
    # ==============================


    @commands.group(
        name="flight",
        invoke_without_command=True
    )
    async def flight(self, ctx):

        await ctx.send(
            "✈️ Flight System\n\n"
            "Commands:\n"
            ".flight setup\n"
            ".flight config\n"
            ".flight presets"
        )



    # ==============================
    # SETUP COMMAND
    # ==============================


    @flight.command()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx, category: discord.CategoryChannel=None):

        config = load("config")


        if config.get("flight_channel"):

            await ctx.send(
                "⚠️ Flight system is already setup."
            )

            return



        if category is None:

            category = await ctx.guild.create_category(
                "✈️ Flight System"
            )



        flight_channel = await ctx.guild.create_text_channel(
            "flight-announcements",
            category=category
        )


        log_channel = await ctx.guild.create_text_channel(
            "flight-logs",
            category=category
        )



        config = {

            "category": category.id,

            "flight_channel": flight_channel.id,

            "flight_log_channel": log_channel.id,

            "airline": "Regional Express Australia",

            "color": 0x1E90FF,

            "logo": None

        }


        save(
            "config",
            config
        )



        embed = discord.Embed(

            title="✈️ Flight System Setup",

            description=
            f"Flight Channel: {flight_channel.mention}\n"
            f"Logs: {log_channel.mention}",

            color=config["color"]

        )


        await ctx.send(
            embed=embed
        )



    # ==============================
    # CONFIG COMMAND
    # ==============================


    @flight.group(
        name="config",
        invoke_without_command=True
    )
    async def config(self, ctx):

        data = load("config")


        embed = discord.Embed(

            title="✈️ Flight Configuration",

            color=data.get(
                "color",
                0x1E90FF
            )

        )


        for key,value in data.items():

            embed.add_field(

                name=key,

                value=str(value),

                inline=False

            )


        await ctx.send(
            embed=embed
        )



    @config.command(
        name="airline"
    )
    @commands.has_permissions(administrator=True)
    async def config_airline(
        self,
        ctx,
        *,
        name
    ):

        data = load("config")


        data["airline"] = name


        save(
            "config",
            data
        )


        await ctx.send(
            f"✅ Airline changed to **{name}**"
        )



    @config.command(
        name="color"
    )
    @commands.has_permissions(administrator=True)
    async def config_color(
        self,
        ctx,
        colour
    ):


        data = load("config")


        try:

            if colour.startswith("#"):

                colour = colour.replace("#","")


            data["color"] = int(
                colour,
                16
            )


            save(
                "config",
                data
            )


            await ctx.send(
                "✅ Colour updated."
            )


        except:

            await ctx.send(
                "❌ Invalid colour."
            )



    # ==============================
    # ERROR HANDLING
    # ==============================


    @setup.error
    async def setup_error(
        self,
        ctx,
        error
    ):

        if isinstance(
            error,
            commands.MissingPermissions
        ):

            await ctx.send(
                "❌ Administrator permission required."
            )



async def setup(bot):

    await bot.add_cog(
        FlightPlugin(bot)
    )