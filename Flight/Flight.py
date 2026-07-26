import discord
from discord.ext import commands

from .database import load, save, ensure_storage


class FlightPlugin(commands.Cog):

    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot
        ensure_storage()


    # ==========================
    # MAIN FLIGHT COMMAND
    # ==========================

    @commands.group(
        name="flight",
        invoke_without_command=True
    )
    async def flight(self, ctx):

        config = load("config")

        airline = config.get(
            "airline",
            "Regional Express Australia"
        )

        embed = discord.Embed(
            title=f"✈️ {airline} Flight System",
            description=(
                "**Available Commands**\n\n"

                "✈️ `.flight setup`\n"
                "Creates the flight system channels\n\n"

                "🛫 `.flight create`\n"
                "Create a new flight RSVP\n\n"

                "📋 `.flight presets`\n"
                "Manage flight presets\n\n"

                "⚙️ `.flight config`\n"
                "Configure the flight system\n\n"

                "🔒 `.flight end`\n"
                "End an active flight"
            ),
            color=config.get(
                "color",
                0x1E90FF
            )
        )

        if config.get("logo"):
            embed.set_thumbnail(
                url=config["logo"]
            )

        await ctx.send(embed=embed)



    # ==========================
    # SETUP
    # ==========================

    @flight.command()
    @commands.has_permissions(administrator=True)
    async def setup(
        self,
        ctx,
        *,
        category: discord.CategoryChannel = None
    ):

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

            "airline":
                "Regional Express Australia",

            "color":
                0x1E90FF,

            "logo":
                None
        }


        save(
            "config",
            config
        )


        embed = discord.Embed(

            title="✅ Flight System Setup Complete",

            description=(
                f"📢 Flight Channel:\n"
                f"{flight_channel.mention}\n\n"

                f"📋 Logs:\n"
                f"{log_channel.mention}\n\n"

                f"Category:\n"
                f"{category.name}"
            ),

            color=config["color"]

        )


        await ctx.send(embed=embed)



    # ==========================
    # CONFIG COMMAND GROUP
    # ==========================

    @flight.group(
        name="config",
        invoke_without_command=True
    )
    async def config(
        self,
        ctx
    ):

        data = load("config")


        embed = discord.Embed(
            title="⚙️ Flight Configuration",
            color=data.get(
                "color",
                0x1E90FF
            )
        )


        if not data:

            embed.description = (
                "Flight system has not been setup."
            )

            await ctx.send(embed=embed)
            return



        fields = {

            "Airline":
                data.get("airline"),

            "Flight Channel":
                f"<#{data.get('flight_channel')}>",

            "Log Channel":
                f"<#{data.get('flight_log_channel')}>",

            "Category":
                f"<#{data.get('category')}>",

            "Colour":
                hex(
                    data.get(
                        "color",
                        0x1E90FF
                    )
                ),

            "Logo":
                data.get("logo")
                or "None"

        }


        for name,value in fields.items():

            embed.add_field(
                name=name,
                value=str(value),
                inline=False
            )


        await ctx.send(embed=embed)



    # ==========================
    # AIRLINE
    # ==========================

    @config.command()
    @commands.has_permissions(administrator=True)
    async def airline(
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



    # ==========================
    # CHANNEL
    # ==========================

    @config.command()
    @commands.has_permissions(administrator=True)
    async def channel(
        self,
        ctx,
        channel: discord.TextChannel
    ):

        data = load("config")

        data["flight_channel"] = channel.id

        save(
            "config",
            data
        )


        await ctx.send(
            f"✅ Flight channel set to {channel.mention}"
        )



    # ==========================
    # LOG CHANNEL
    # ==========================

    @config.command()
    @commands.has_permissions(administrator=True)
    async def logs(
        self,
        ctx,
        channel: discord.TextChannel
    ):

        data = load("config")

        data["flight_log_channel"] = channel.id

        save(
            "config",
            data
        )


        await ctx.send(
            f"✅ Log channel set to {channel.mention}"
        )



    # ==========================
    # CATEGORY
    # ==========================

    @config.command()
    @commands.has_permissions(administrator=True)
    async def category(
        self,
        ctx,
        category: discord.CategoryChannel
    ):

        data = load("config")

        data["category"] = category.id

        save(
            "config",
            data
        )


        await ctx.send(
            f"✅ Category set to **{category.name}**"
        )



    # ==========================
    # COLOR
    # ==========================

    @config.command()
    @commands.has_permissions(administrator=True)
    async def color(
        self,
        ctx,
        colour
    ):

        try:

            colour = colour.replace(
                "#",
                ""
            )

            value = int(
                colour,
                16
            )


            data = load("config")

            data["color"] = value

            save(
                "config",
                data
            )


            await ctx.send(
                "✅ Colour updated."
            )


        except:

            await ctx.send(
                "❌ Invalid colour format."
            )



    # ==========================
    # LOGO
    # ==========================

    @config.command()
    @commands.has_permissions(administrator=True)
    async def logo(
        self,
        ctx,
        url
    ):

        data = load("config")

        data["logo"] = url

        save(
            "config",
            data
        )


        await ctx.send(
            "✅ Logo updated."
        )



    # ==========================
    # ERRORS
    # ==========================

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
                "❌ Administrator permissions required."
            )



async def setup(bot):

    await bot.add_cog(
        FlightPlugin(bot)
    )
