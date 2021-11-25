import discord
from discord.ext import commands
from pybooru import Danbooru 
import nekos
from pygelbooru import Gelbooru

data_folder = 'C:/more like shithub/discord-bot-master/data/'

class FileHandler:
    
    async def leader_update(self, board):
        with open(f'{data_folder}{board}data.txt', 'r') as file:
            results = dict()
            lines = file.read().splitlines()
            for line in lines: # instantiate the dictionary with all of the tags, value set to 0
                for tag in line.split(" "):
                    results[tag] = 0
            for index in lines: # loop through searches and add 1 to each value's spot in the dictionary
                for tag in index.split(" "):
                    results[tag] += 1
        with open(f'{data_folder}{board}tagfrequency.txt', 'w') as f:
            for x, y in sorted(results.items(), reverse=True, key=lambda x: x[1]):
                f.write(f'{str(y)} - {str(x)}\n')

    async def write(self, tag, file):
        if tag is None:
            tag = 'random'
        with open(f'{data_folder}{file}data.txt', 'a') as f:
            for x in tag:
                f.write(f'{x}\n')
        await self.leader_update(file)

    async def error_log(self, post):
        with open(f'{data_folder}ERRONEOUS_POSTS.txt', 'a') as f:
            f.write(f'{post}\n\n')

class Private:
    danbooru_api_key = 'HE3uUzSG85HGgYtCQLmd5zRF'
    
    gelbooru_api_key = 'ed348ca73176c8db5dd8fd2aeaeedc04fe7f27e4d7482fda5a3b60ca6c2be4ea'
    gelbooru_user_id = '884983'

data = Private()
danbooru = Danbooru(site_name='danbooru', api_key=data.danbooru_api_key)
gelbooru = Gelbooru(api_key=data.gelbooru_api_key, user_id=data.gelbooru_user_id)
fh = FileHandler()

class ImageSearch(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('danbooru cog loaded for pictures of ankha for kody')

    @commands.command(name='danbooru')
    async def danbooru_search(self, ctx, *tag):
        async def tagCon():
            if tag is None:
                return None
            elif len(tag) == 1:
                return tag[0]
            elif len(tag) == 2:
                return f'{tag[0]} {tag[1]}'
            elif len(tag) > 2:
                await tagOverload()

        async def tagOverload():
            await ctx.send('`Only 2 tags can be searched for at a time, random searching`')
            
        t = await tagCon()
        post = danbooru.post_list(limit = 1, tags = t, random = True)[0]
        try:
            await ctx.send(post['file_url'])
            await fh.write(t, 'danbooru')
        except KeyError:
            print('\t\t------------FILE_URL ERROR------------')
            await fh.error_log(post)
        except IndexError:
            await ctx.send(f'No posts found for tag {str(tag)} {nekos.textcat()}')

    @commands.command(name='gelbooru')
    async def gelbooru_search(self, ctx, *tag):   
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
            await ctx.send(f'invalid search {nekos.textcat()}')
        finally:
            await fh.write([tag], 'nekos')


def setup(client):
    client.add_cog(ImageSearch(client))