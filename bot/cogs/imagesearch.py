import discord
from discord.ext import commands
from pybooru import Danbooru as danbooru
import nekos
from pygelbooru import Gelbooru

data_folder = 'C:/more like shithub/discord-bot-master/data/'

class FileHandler:
    
    async def danbooru_write(self, tag):  
        f = open(data_folder+'danboorudata.txt', 'a')
        if tag is None:
            tag = 'random'
        f.write(tag + "\n")
        f.close()
        await self.update('danbooru')
    
    async def update(self, board):
        file = open(data_folder+board+'data.txt', 'r')
        results = dict()
        lines = file.read().splitlines()
        for line in lines:
            for tag in line.split(" "):
                results[tag] = 0
        for index in lines:
            for tag in index.split(" "):
                results[tag] += 1
        f = open(data_folder+board+'tagfrequency.txt', 'w')
        for x, y in sorted(results.items(), reverse=True, key=lambda x: x[1]):
            f.write(str(y) + ' - ' + x + '\n')
        f.close()
        file.close()

    async def write(self, tag, file):
        f= open(data_folder+file+'data.txt', 'a')
        for x in tag:
            f.write(x + '\n')
        f.close()
        await self.update(file)

class Private:
    danbooru_api_key = 'HE3uUzSG85HGgYtCQLmd5zRF'
    
    gelbooru_api_key = 'ed348ca73176c8db5dd8fd2aeaeedc04fe7f27e4d7482fda5a3b60ca6c2be4ea'
    gelbooru_user_id = '884983'

data = Private()
client = danbooru(site_name='danbooru', api_key=data.danbooru_api_key)
gelbooru = Gelbooru(api_key=data.gelbooru_api_key, user_id=data.gelbooru_user_id)
fh = FileHandler()

class ImageSearch(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('danbooru cog loaded for pictures of ankha for kody')

    @commands.command()
    async def ankha(self, ctx):
        await ctx.send(client.post_list(limit = 1, tags = 'ankha_(animal_crossing)', random = True)[0]['file_url'])
        await fh.danbooru_write('ankha_(animal_crossing)')

    @commands.command()
    async def danbooru(self, ctx, *tag):
        async def tagCon():
            if tag is None:
                return None
            elif len(tag) == 1:
                return tag[0]
            elif len(tag) == 2:
                return tag[0] + " " + tag[1]
            elif len(tag) > 2:
                await tagOverload()

        async def tagOverload():
            await ctx.send('`Only 2 tags can be searched for at a time, random searching`')
            
        t = await tagCon()
        try:
            await fh.danbooru_write(t)
            await ctx.send(client.post_list(limit = 1, tags = t, random = True)[0]['file_url'])
        except KeyError:
            print('\t\t------------FILE_URL ERROR BYPASSED------------')
            danbooru(self,ctx,tag)
        except IndexError:
            await ctx.send('No posts found for tag ' + str(tag) + ' ' + nekos.textcat())

    @commands.command()
    async def gelbooru(self, ctx, *tag):   
        y = list(tag)
        try: 
            await ctx.send(str(await gelbooru.random_post(tags=y)))
            await fh.write(y, 'gelbooru')
        except:
            await ctx.send('error')

    @commands.command(name='nekos.life')
    async def neko(self, ctx, tag='neko'):
        try:
            if tag == 'femboy':
                await ctx.send('https://tenor.com/view/femboy-janitors-sweeping-hooters-bathroom-gif-17512541')
            else:
                await ctx.send(nekos.img(tag))
        except:
            await ctx.send('invalid search ' + nekos.textcat())
        finally:
            await fh.write([tag], 'nekos')

def setup(client):
    client.add_cog(ImageSearch(client))