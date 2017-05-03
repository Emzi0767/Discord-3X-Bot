import json
import curio
import bot3xlauncher
import bot3x


def main():
    bot3x.log("3X version {} booting".format(bot3x.__version__), tag="3X LDR")

    bot3x.log("Loading config", tag="3X LDR")
    with open("config.json", "r") as f:
        cts = f.read()
        tkd = json.loads(cts)

    args = {"token": tkd["token"], "shard_count": int(tkd["shard_count"])}

    try:
        with open("gconf.json", "r", encoding="utf-8") as f:
            gconf = json.loads(f.read())
        args["guild_settings"] = gconf

    except:
        pass

    bot3x.log("Launching 3X", tag="3X LDR")

    bot3x.log("Running", tag="3X LDR")

    try:
        lchr = bot3xlauncher.Bot3XLauncher(curio.Kernel())
        lchr.run(**args)

    except KeyboardInterrupt:
        pass

    finally:
        bot3x.log("Shutting down", tag="3X LDR")

    bot3x.log("Shutdown finalized", tag="3X LDR")


if __name__ == "__main__":
    main()
