import discord
from discord.ext import commands
import requests
import nekos

class League(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('league cog loaded :game_controller:')

    # Commands
    @commands.command()
    async def lfarm(self, ctx, *sumName):
        if sumName != None:
            #print(sumName)
            sumNamex = ''
            for x in sumName:
                if x != sumName[-1]:
                    sumNamex += x + " "
                    #print(sumNamex)
                else:
                    sumNamex += x
                   # print(sumNamex)
            try:
                apiKey = 'RGAPI-2d8f508a-f412-4a56-9455-9129fb932ede'
                ret1 = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + sumNamex + "?api_key=" + apiKey)
                accountId = ret1.json()['accountId']
                ret2 = requests.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + accountId + "?endIndex=2&beginIndex=0&api_key=" + apiKey)
                t1 = ret2.json()['matches']
                t2 = t1[0]["gameId"]
                ret3 = requests.get("https://na1.api.riotgames.com/lol/match/v4/matches/" + str(t2) + "?api_key=" + apiKey)
                ret4 = ret3.json()['participantIdentities']
                ret5 = ret4
                for i in ret5:
                    x = i['player']
                    if x['summonerName'] == sumNamex:
                        ret5 = i['participantId']

                ret6 = ret3.json()
                y1 = ret6['participants']
                for z in y1:
                    if z['participantId'] == ret5:
                        stats = z['stats']
                        laneMinsKilled = stats['totalMinionsKilled']
                        jgMinsKilled = stats['neutralMinionsKilled']
                        finalMinsKilled = laneMinsKilled + jgMinsKilled

                await ctx.send('total minions killed by ' + sumNamex + ' in their last game: ' + str(finalMinsKilled))
            except:
                await ctx.send('invalid summoner name ' + nekos.textcat())
        else:
            await ctx.send('enter a summoner name ' + nekos.textcat())

def setup(client):
    client.add_cog(League(client))
