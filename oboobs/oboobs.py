import discord
from redbot.core import commands
from redbot.core import checks, Config
# Sys
import asyncio
import aiohttp
import time
import random
import os
import sys
import datetime

DEFAULT = {"nsfw_channels": ["133251234164375552"], "invert" : False, "nsfw_msg": True, "last_update": 0,  "ama_boobs": 12250, "ama_ass": 5991}# Red's testing chan. nsfw content off by default.

#API info:
#example: "/boobs/10/20/rank/" - get 20 boobs elements, start from 10th ordered by rank; noise: "/noise/{count=1; sql limit}/",
#example: "/noise/50/" - get 50 random noise elements; model search: "/boobs/model/{model; sql ilike}/",
#example: "/boobs/model/something/" - get all boobs elements, where model name contains "something", ordered by id; author search: "/boobs/author/{author; sql ilike}/",
#example: "/boobs/author/something/" - get all boobs elements, where author name contains "something", ordered by id; get boobs by id: "/boobs/get/{id=0}/",
#example: "/boobs/get/6202/" - get boobs element with id 6202; get boobs count: "/boobs/count/"; get noise count: "/noise/count/"; vote for boobs: "/boobs/vote/{id=0}/{operation=plus;[plus,minus]}/",
#example: "/boobs/vote/6202/minus/" - negative vote for boobs with id 6202; vote for noise: "/noise/vote/{id=0}/{operation=plus;[plus,minus]}/",
#example: "/noise/vote/57/minus/" - negative vote for noise with id 57;

#example: "/butts/10/20/rank/" - get 20 butts elements, start from 10th ordered by rank; noise: "/noise/{count=1; sql limit}/",
#example: "/noise/50/" - get 50 random noise elements; model search: "/butts/model/{model; sql ilike}/",
#example: "/butts/model/something/" - get all butts elements, where model name contains "something", ordered by id; author search: "/butts/author/{author; sql ilike}/",
#example: "/butts/author/something/" - get all butts elements, where author name contains "something", ordered by id; get butts by id: "/butts/get/{id=0}/",
#example: "/butts/get/6202/" - get butts element with id 6202; get butts count: "/butts/count/"; get noise count: "/noise/count/"; vote for butts: "/butts/vote/{id=0}/{operation=plus;[plus,minus]}/",
#example: "/butts/vote/6202/minus/" - negative vote for butts with id 6202; vote for noise: "/noise/vote/{id=0}/{operation=plus;[plus,minus]}/",
#example: "/noise/vote/57/minus/" - negative vote for noise with id 57;

#Credits:
#Alexhel(pushed oBoobs to v3.0.0rc1), 

BaseCog = getattr(commands, "Cog", object)

class OboobsC(BaseCog):
    """The oboobs/obutts.ru NSFW pictures of nature cog.
    https://github.com/Canule/Mash-Cogs
    """

    def __init__(self, bot):
        self.bot = bot
        self.settings = Config.get_conf(self, identifier=69)
        default_global = {
            "ama_ass": 0,
            "ama_boobs": 0,
            "last_update": 0,
            "post_delay": 0,
            "post_channel": None
        }
        default_guild = {
            "invert": False,
            "nsfw_channels" : [],
            "nsfw_msg": True
        }
        self.settings.register_guild(**default_guild)
        self.settings.register_global(**default_global)
        
        self.poster = asyncio.create_task(self.postboobs())

    def __unload(self):
        self.poster.cancel()

    async def get(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                rep = await response.json()
                return rep

    @checks.is_owner()
    @commands.group(name="oboobs", pass_context=True)
    async def _oboobs(self, ctx):
        """The oboobs/obutts.ru pictures of nature cog."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help()
            return

    @_oboobs.command()
    async def postrate(self, ctx, delay: int):
        """
        Sets the posting rate for oboobs
        """
        try:
            await self.settings.post_delay.set(delay)
            await ctx.send(f"Delay has been set to: {delay}")
        except (KeyError, AttributeError,  ValueError):
            await ctx.send("There was a problem setting the delay! Please check your input and try again.")

    @_oboobs.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        """
        Sets the channel to post the filth into
        """
        try:
            await self.settings.post_channel.set(channel.id)
            await ctx.send(f"Channel set to {channel.name}")
        except (KeyError, AttributeError, ValueError):
            await ctx.send("There was a problem setting the channel! Please chekc the input and try again")

    async def postboobs(self):
        """
        Posts the filth with a delay
        """
        channel = await self.settings.post_channel()
        current = "Boob"


        while 1:
            await asyncio.sleep(await self.settings.post_delay())

            post_channel = self.bot.get_channel(channel)
            if current is "boob":
                try:
                    rdm = random.randint(0, await self.settings.ama_boobs())
                    search = ("http://api.oboobs.ru/boobs/{}".format(rdm))
                    result = await self.get(search)
                    tmp = random.choice(result)
                    print(result)
                    boob = "http://media.oboobs.ru/{}".format(tmp["preview"])
                except Exception as e:
                    await post_channel.send("Error getting results.\n{}".format(e))
                    return
                
                emb = discord.Embed(title="Boobs")
                emb.set_image(url=boob)
                await post_channel.send(embed=emb)
                current = "ass"
            else:
                try:
                    rdm = random.randint(0, await self.settings.ama_ass())
                    search = ("http://api.obutts.ru/butts/{}".format(rdm))
                    result = await self.get(search)
                    tmp = random.choice(result)
                    ass = "http://media.obutts.ru/{}".format(tmp["preview"])
                except Exception as e:
                    await post_channel.send("Error getting results.\n{}".format(e))
                    return

                emb = discord.Embed(title="Ass")
                emb.set_image(url=ass)
                await post_channel.send(embed=emb)
                current = "boob"



    # Boobs
    @checks.is_owner()
    @commands.command(no_pm=True)
    async def boobs(self, ctx):
        """Shows some boobs."""
        try:
            rdm = random.randint(0, await self.settings.ama_boobs())
            search = ("http://api.oboobs.ru/boobs/{}".format(rdm))
            result = await self.get(search)
            tmp = random.choice(result)
            print(result)
            boob = "http://media.oboobs.ru/{}".format(tmp["preview"])
        except Exception as e:
             await ctx.send("Error getting results.\n{}".format(e))
             return
        if ctx.channel.is_nsfw():
            emb = discord.Embed(title="Boobs")
            emb.set_image(url=boob)
            await ctx.send(embed=emb)

    # Ass
    @checks.is_owner()
    @commands.command(pass_context=True, no_pm=False)
    async def ass(self, ctx):
        """Shows some ass."""
        try:
            rdm = random.randint(0, await self.settings.ama_ass())
            search = ("http://api.obutts.ru/butts/{}".format(rdm))
            result = await self.get(search)
            tmp = random.choice(result)
            ass = "http://media.obutts.ru/{}".format(tmp["preview"])
        except Exception as e:
            await ctx.send("Error getting results.\n{}".format(e))
            return
        if ctx.channel.is_nsfw():
            emb = discord.Embed(title="Ass")
            emb.set_image(url=ass)
            await ctx.send(embed=emb)


    @checks.admin_or_permissions(administrator=True)
    @_oboobs.command(pass_context=True, no_pm=True)
    async def nsfw(self, ctx):
        """Toggle oboobs nswf for this channel on/off.
        Admin/owner restricted."""
        nsfwChan = False
        # Reset nsfw.
        chans = await self.settings.guild(ctx.guild).nsfw_channels()
        for a in chans:
            if a == ctx.message.channel.id:
                nsfwChan = True
                chans.remove(a)
                await self.settings.guild(ctx.guild).nsfw_channels.set(chans)
                await ctx.send("nsfw ON")
                break
        # Set nsfw.
        if not nsfwChan:
            if ctx.message.channel not in chans:
                chans.append(ctx.message.channel.id)
                await self.settings.guild(ctx.guild).nsfw_channels.set(chans)
                await ctx.send("nsfw OFF")
        
    @checks.admin_or_permissions(administrator=True)
    @_oboobs.command(pass_context=True, no_pm=True)
    async def invert(self, ctx):
        """Invert nsfw blacklist to whitelist
        Admin/owner restricted."""
        if not await self.settings.guild(ctx.guild).invert():
            await self.settings.guild(ctx.guild).invert.set(True)
            await ctx.send("The nsfw list for all servers is now: inverted.")
        elif await self.settings.guild(ctx.guild).invert():
            await self.settings.guild(ctx.guild).invert.set(False)
            await ctx.send("The nsfw list for this server is now: default(blacklist)")

    @checks.is_owner()
    @_oboobs.command(hidden=True)
    async def update(self, ctx):
        await ctx.send("Starting update ...")
        await self.boob_knowlegde()
        await ctx.send("Looks done !")

    async def boob_knowlegde(self):
        #KISS
        last_update = await self.settings.last_update()
        now = round(time.time())
        interval = 86400*2
        if now >= last_update+interval:
            await self.settings.last_update.set(now)
        else:
            return
            
        async def search(url, curr):
            search = ("{}{}".format(url, curr))
            return await self.get(search)

        # Upadate boobs len
        print("Updating amount of boobs...")
        curr_boobs = await self.settings.ama_boobs()
        url = "http://api.oboobs.ru/boobs/"
        done = False
        reachable = curr_boobs
        step = 50
        while not done:
            q = reachable+step
            print("Searching for boobs:", q)
            res = await search(url, q)
            if res != []:
                reachable = q
                res_dc = await search(url, q+1)
                if res_dc == []:
                    await self.settings.ama_boobs.set(reachable)
                    done = True
                    break
                else:
                    await asyncio.sleep(1) # Trying to be a bit gentle for the api.
                    continue
            elif res == []:
                step = round(step/2)
                '''
                if step <= 1:
                    await self.settings.ama_boobs.set(curr_boobs)
                    done = True
                    '''
            await asyncio.sleep(1)
        print("Total amount of boobs:", await self.settings.ama_boobs())

        # Upadate ass len
        print("Updating amount of ass...")
        curr_ass = await self.settings.ama_ass()
        url = "http://api.obutts.ru/butts/"
        done = False
        reachable = curr_ass
        step = 50
        while not done:
            q = reachable+step
            print("Searching for ass:", q)
            res = await search(url, q)
            if res != []:
                reachable = q
                res_dc = await search(url, q+1)
                if res_dc == []:
                    await self.settings.ama_ass.set(reachable)
                    done = True 
                    break
                else:
                    await asyncio.sleep(1)
                    continue
            elif res == []:
                step = round(step/2)
                """
                if step <= 1:
                    #await self.settings.ama_ass.set(curr_ass)
                    done = True
                    """
            await asyncio.sleep(1)
            '''
        if await self.settings.ama_ass() == 0:
            await self.settings.ama_ass.set(5500)
            '''
        print("Total amount of ass:", await self.settings.ama_ass())
