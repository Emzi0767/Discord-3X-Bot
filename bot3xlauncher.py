import argparse
import json
import bot3x


class Bot3XLauncher:
    def __init__(self, kernel):
        self.kernel = kernel

    @property
    def kernel(self):
        return self._kernel

    @kernel.setter
    def kernel(self, value):
        self._kernel = value

    def run(self, **kwargs):
        kernel = self.kernel

        # core bot config
        bot3x_totalshards = kwargs.get("shard_count", None)
        bot3x_token = kwargs.get("token", None)
        bot3x_guild_settings = kwargs.get("guild_settings", {})

        # init pam
        bot3x.log("Initializing 3X", tag="3X BOT")
        bot3x_config = {"token": bot3x_token, "guild_settings": bot3x_guild_settings}

        bot3x_bot = bot3x.Bot3X(**bot3x_config)
        bot3x_bot.remove_command("help")

        kernel.run(bot3x.Bot3XCommands.setup(bot3x_bot))

        try:
            bot3x.log("3X booting", tag="3X BOT")

            bot3x_bot.run(bot3x_token, bot3x_totalshards)

        except KeyboardInterrupt:
            pass

        finally:
            bot3x.log("3X dying", tag="3X BOT")

            kernel.run(None, shutdown=True)

            bot3x.log("3X died", tag="3X BOT")


def initialize_3x(**kwargs):
    args = kwargs

    try:
        with open("gconf.json", "r", encoding="utf-8") as f:
            gconf = json.loads(f.read())
        args["guild_settings"] = gconf

    except:
        pass

    core = Bot3XLauncher()
    core.run(**args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--shard", type=int, dest="shard_id", help="Shard ID to connect with", default=0)
    parser.add_argument("-c", "--shard-count", type=int, dest="shard_count", help="Total shard count", default=1)
    parser.add_argument("-t", "--token", type=str, dest="token", help="Bot's token", default=None)

    args = parser.parse_args()
    args = vars(args)

    initialize_3x(**args)
