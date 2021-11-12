import discord
from discord.ext import commands, tasks
import nekos


class Main(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('main cog loaded,,,,, nya~')      # Client.discord.Status.online
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name='with cogs'))

    # Commands

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'this took me {round(self.client.latency * 1000)}ms')

    @commands.command(name="googleshowmethisguysballsplease", aliases=["balls", "google", "google,showmethisguy'sballsplease", "googleshowmethisguy'sballsplease", "google,showmethisguysballsplease"])
    async def balls(self, ctx):
        await ctx.send("WOAEEEEEEEY")
        await ctx.send("https://live.staticflickr.com/5256/5404132722_475b82e163_b.jpg")

    @commands.command()
    async def hi(self, ctx):
        await ctx.send('hi :3')

    @commands.command(name='how are you', aliases=['howareyou'])
    async def feeling(self, ctx):
        await ctx.send('good!')


def setup(client):
    client.add_cog(Main(client))
