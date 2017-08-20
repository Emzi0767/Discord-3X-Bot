from bot3x import is_authorized
from curious.commands import command
from curious.commands.plugin import Plugin
from curious.commands.context import Context
from curious.dataclasses.channel import Channel


class Bot3XCommands(Plugin):
    def __init__(self, bot):
        self._bot = bot

    @property
    def module_name(self):
        return "Core"

    @command(name="enable", description="Enables the 3X greeter in specified channel", invokation_checks=[is_authorized], aliases=["on"])
    async def _enable(self, ctx: Context, chn: Channel):
        """
        Enables the 3X greeter
        """
        gsts = ctx.bot.guild_settings
        if str(ctx.guild.id) not in gsts:
            gsts[str(ctx.guild.id)] = {"enabled": True, "welcome": "Greetings, **{}**!", "farewell": "Bye, **{}**!", "channel": chn.id}

        gst = gsts[str(ctx.guild.id)]
        gst["enabled"] = True

        ctx.bot.save_settings()

        await ctx.channel.send("👌")

    @command(name="disable", description="Disables the 3X greeter", invokation_checks=[is_authorized], aliases=["off"])
    async def _disable(self, ctx: Context):
        """
        Disables the 3X greeter
        """
        gsts = ctx.bot.guild_settings
        if str(ctx.guild.id) not in gsts:
            gsts[str(ctx.guild.id)] = {"enabled": False, "welcome": "Greetings, **{}**!", "farewell": "Bye, **{}**!", "channel": None}

        gst = gsts[str(ctx.guild.id)]
        gst["enabled"] = False

        ctx.bot.save_settings()

        await ctx.channel.send("👌")

    @command(name="welcome", description="Changes the 3X welcome message", invokation_checks=[is_authorized])
    async def _welcome(self, ctx: Context, *, msg: str):
        """
        Changes the 3X welcome message
        """
        gsts = ctx.bot.guild_settings
        if str(ctx.guild.id) not in gsts:
            gsts[str(ctx.guild.id)] = {"enabled": False, "welcome": "Greetings, **{}**!", "farewell": "Bye, **{}**!", "channel": None}

        gst = gsts[str(ctx.guild.id)]
        gst["welcome"] = msg

        ctx.bot.save_settings()

        await ctx.channel.send("👌")

    @command(name="farewell", description="Changes the 3X farewell message", invokation_checks=[is_authorized])
    async def _farewell(self, ctx: Context, *, msg: str):
        """
        Changes the 3X farewell message
        """
        gsts = ctx.bot.guild_settings
        if str(ctx.guild.id) not in gsts:
            gsts[str(ctx.guild.id)] = {"enabled": False, "welcome": "Greetings, **{}**!", "farewell": "Bye, **{}**!", "channel": None}

        gst = gsts[str(ctx.guild.id)]
        gst["farewell"] = msg

        ctx.bot.save_settings()

        await ctx.channel.send("👌")
