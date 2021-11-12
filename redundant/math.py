import discord
from discord.ext import commands
import math

class Math(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('math cog loaded B)')

    # Commands
    @commands.command()
    async def pythag(self, ctx, dat): # 3,4
       try:
            datas = dat.split(',')
            maths = math.sqrt(pow(int(datas[0]), 2) + pow(int(datas[1]), 2))
       except:
           await ctx.send('Invalid input. (Valid entry is \"int,int\"; ex. \"3,4\")')

       await ctx.send(maths)

    @commands.command()
    async def selfdiv(self, ctx, x):
        v = True
        y = int(x)
        while y > 0:
            z = y % 10
            if (y % z) != 0:
                v = False
            y = int(y / 10)
        await ctx.send(v)


def setup(client):
    client.add_cog(Math(client))