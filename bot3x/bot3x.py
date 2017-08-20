import datetime
import json
import traceback
import sys
import curio
import curious.core.client
import bot3x
from curious.core.event import event, EventContext
from curious.commands.context import Context
from curious.dataclasses.presence import Game
from curious.dataclasses.member import Member
from concurrent.futures._base import CancelledError


def is_authorized(ctx: Context):
    gld = ctx.guild
    if gld is None:
        return False

    usr: Member = ctx.author
    if usr.id == 181875147148361728:
        return True

    rls = usr.roles
    has = False
    for xrl in rls:
        if xrl.id == 214796473689178133:
            has = True
            break

    if not has:
        return False

    return True


class Bot3X(curious.core.client.Client):
    def __init__(self, **kwargs):
        super().__init__(command_prefix="3x:")
        self.guild_settings = kwargs.get("guild_settings", {})
        self._status_task = None

    def save_settings(self):
        gst = json.dumps(self.guild_settings)
        with open("gconf.json", "w", encoding="utf-8") as f:
            f.write(gst)

    async def status3x(self):
        try:
            lop = datetime.datetime(2015, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
            bot3x.log("3X Game initialized", tag="3X GAME")

            while True:
                cop = datetime.datetime.now(datetime.timezone.utc)
                tdelta = cop - lop

                if tdelta.seconds >= 1200:
                    lop = cop
                    await self.change_status(game=Game(name="Hello, sir!"))

                await curio.sleep(0.1)

        except CancelledError:
            pass

        except Exception as e:
            bot3x.logex(e, tag="3X GAME")

        finally:
            bot3x.log("3X Game closed", tag="3X GAME")

    # Error handling
    @event("error")
    async def on_error(self, event, *args, **kwargs):
        exinfo = sys.exc_info()
        exfmts = [s.replace("\\n", "") for s in traceback.format_exception(*exinfo)]
        bot3x.log(*exfmts, tag="3X ERR")

    # Bot preparation
    @event("ready")
    async def on_ready(self, ctx: EventContext):
        bot3x.log("Logged in as {}".format(self.user.name), tag="INSTANCE")
        self._status_task = await curio.spawn(self.status3x, daemon=True)

    # Guild init
    @event("guild_streamed")
    @event("guild_available")
    @event("guild_create")
    async def on_guild_available(self, ctx: EventContext, guild):
        bot3x.log("Guild available: {}".format(guild.name), tag="3X CORE")

    @event("guild_unavailable")
    @event("guild_delete")
    async def on_guild_unavailable(self, guild):
        bot3x.log("Guild unavailable: {}".format(guild.name), tag="3X CORE")

    # Greetings
    @event("member_join")
    async def on_member_join(self, ctx: EventContext, member: Member):
        gld = member.guild
        if gld is None:
            return

        if str(gld.id) not in self.guild_settings:
            return

        gst = self.guild_settings[str(gld.id)]
        if not gst["enabled"] or not gst["channel"]:
            return

        for xch in gld.channels:
            if xch.id == gst["channel"]:
                chn = xch
                break
        if chn is None:
            return

        try:
            await chn.send(gst["welcome"].format(member.name))

        except Exception as e:
            bot3x.logex(e, tag="GREETER-W")

    @event("member_leave")
    async def on_member_remove(self, ctx: EventContext, member: Member):
        gld = member.guild
        if gld is None:
            return

        if str(gld.id) not in self.guild_settings:
            return

        gst = self.guild_settings[str(gld.id)]
        if not gst["enabled"] or not gst["channel"]:
            return

        for xch in gld.channels:
            if xch.id == gst["channel"]:
                chn = xch
                break
        if chn is None:
            return

        try:
            await chn.send(gst["farewell"].format(member.user.username))

        except Exception as e:
            bot3x.logex(e, tag="GREETER-L")
