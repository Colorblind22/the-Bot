import discord
from discord.ext import commands
import nekos


class Nekos(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('nekos cog loaded,,,,, nya~')      # Client.discord.Status.online

    # Commands

    

    @commands.command()
    async def owoify(self, ctx, *text):
        words = str()
        for x in text:
            words += x + " "
        await ctx.send(nekos.owoify(words))

    @commands.command()
    async def cat(self, ctx):
        await ctx.send(nekos.cat())

    @commands.command()
    async def why(self, ctx):
        await ctx.send(nekos.why())

    @commands.command()
    async def fact(self, ctx):
        await ctx.send(nekos.fact())



def setup(client):
    client.add_cog(Nekos(client))
