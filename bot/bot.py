from pathlib import Path

import discord
from discord.ext import commands
# https://www.youtube.com/watch?v=UfnF5nFyoKg&list=PLYeOw6sTSy6ZIfraPiUsJWuxjqoL47U3u&index=4

class MusicBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(command_prefix=self.prefix, case_insensitive=True)#, intents=discord.Intents.all())

    def setup(self):
        print("setup running")

        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f"\tLoaded {cog}")

        print("setup done :3")

    def run(self):
        self.setup()

        with open("C:/more like shithub/discord-bot-master/data/token.0", "r", encoding="utf-8") as f:
            TOKEN = f.read()

        print("running")
        super().run(TOKEN, reconnect=True)
    
    async def shutdown(self):
        print("shutting down D:")
        await super().close()

    async def close(self):
        print("closing on keyboard interrupt")
        await self.shutdown()

    async def on_connect(self):
        print(f"\tconnected to discord (latency: {self.latency*1000:,.0f}ms)")

    async def on_resumed(self):
        print("resumed")

    async def on_disconnect(self):
        print("disconnected")

    #async def on_error(self):
    #    raise
    #
    #async def on_command_error(self, ctx, exc):
    #    raise getattr(exc, "original", exc)
    #
    #async def on_ready(self):
    #    self.client_id = (await self.application_info()).id
    #    print("bot ready >:3")

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or("j ")(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)
