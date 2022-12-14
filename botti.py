import botconfig
import string
from tabnanny import check
import time
from tokenize import String
import discord
from discord.ext import commands
import random
import logging

#Tee tiedosto botconfig, johon lisätään seuraavat tiedot:
TOKEN = botconfig.TOKEN
BOTNAME = botconfig.BOTNAME
RUNNERROLEID = botconfig.RUNNERROLEID
HUNTERROLEID = botconfig.HUNTERROLEID
GUILDID = botconfig.GUILDID
HUNTCHATID = botconfig.HUNTCHATID
RUNNERCHATID = botconfig.RUNNERCHATID


intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)
testi = 0

@bot.event
async def on_ready():
    print(f'{BOTNAME} is ready')



@bot.command()
async def runner(ctx, *args):
    runid = ctx.guild.get_role(RUNNERROLEID)
    huntid = ctx.guild.get_role(HUNTERROLEID)
    kaikki = ctx.guild.members

    await ctx.author.add_roles(runid)
    await ctx.author.remove_roles(huntid)
    await ctx.send(f'Käyttäjän {ctx.author.name} Hunter-rooli poistettu')
    await ctx.send(f'{ctx.author.name} on Runner!')

# Jos halutaan muuttaa loput huntereiksi, lisätään 'all'
    if(len(args) < 1):
        return
    if args[0] == 'all':
        for x in kaikki:
            if x != ctx.author and x.bot is False:
                await x.remove_roles(runid)
                await x.add_roles(huntid)
                await ctx.channel.send(f'{x} on Hunter!')


@bot.command()
async def hunter(ctx, *args):
    runid = ctx.guild.get_role(RUNNERROLEID)
    huntid = ctx.guild.get_role(HUNTERROLEID)
    kaikki = ctx.guild.members

    await ctx.author.add_roles(huntid)
    await ctx.author.remove_roles(runid)
    await ctx.send(f'Käyttäjän {ctx.author.name} Runner-rooli poistettu')
    await ctx.send(f'{ctx.author.name} on Hunter!')

    # Jos halutaan muuttaa loput runnereiksi, lisätään 'all'
    if(len(args) < 1):
        return
    if args[0] == 'all':
        for x in kaikki:
            if x != ctx.author and x.bot is False:
                await x.remove_roles(huntid)
                await x.add_roles(runid)
                await ctx.channel.send(f'{x} on Runner!')


@bot.command()
async def draw(ctx, arg1, arg2: int):
    #BUG Voi arpoa saman tyypin kaksi kertaa
    kaikki = ctx.guild.members
    ihmiset = []
    for member in kaikki:
        if not member.bot:
            ihmiset.append(member)
    
    if arg1 == 'hunter':
        arvottava_rooli = ctx.guild.get_role(HUNTERROLEID)
        vastakkainen_rooli = ctx.guild.get_role(RUNNERROLEID)
    elif arg1 == 'runner':
        arvottava_rooli = ctx.guild.get_role(RUNNERROLEID)
        vastakkainen_rooli = ctx.guild.get_role(HUNTERROLEID)
    elif arg1 == 'names':
        await ctx.send('Arvonnan tulos:')
        i = 0
        while i < arg2:
            randnum = random.randint(0, len(ihmiset)-1)
            await ctx.send(ihmiset[randnum].name)
            return

    else:
        ctx.send('Ilmoita, mikä rooli arvotaan \n Esim: !draw hunter 1')        
    i = 0
    while i < arg2:
        randnum = random.randint(0, len(ihmiset)-1)
        await ihmiset[randnum].add_roles(arvottava_rooli)
        await ihmiset[randnum].add_roles(vastakkainen_rooli)
        await ctx.send(f'Arvottu {arvottava_rooli.name}: {ihmiset[randnum].name}')
        i += 1

    print(randnum)

@bot.command()
async def clear(ctx, *args):
    kaikki = ctx.guild.members
    runid = ctx.guild.get_role(RUNNERROLEID)
    huntid = ctx.guild.get_role(HUNTERROLEID)
    for x in kaikki:
        await x.remove_roles(runid)
    for x in kaikki:
        await x.remove_roles(huntid)

    await ctx.send('Roolit poistettu!')

@bot.command()
async def purgechat(ctx, args):
    if args == 'hunter':
        chatid = HUNTCHATID
    if args == 'runner':
        chatid = RUNNERCHATID

    chat_to_delete = ctx.guild.get_channel(chatid)
    deleted = await chat_to_delete.purge(limit=50)
    await chat_to_delete.send(f'Poistettu {len(deleted)} viestiä kanavalta {chat_to_delete.name}')

@bot.command()
async def timer(ctx, arg):
    if arg == 'start':
        testi = time.time()
        await ctx.send(f'Ajastin käynnistetty {time.ctime()}')
    if arg == 'end':
        endtime = time.time()
        await ctx.send(f'Ajastin pysäytetty. Pelin kesto: {testi-endtime}')


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
print('Debug')
bot.run(TOKEN)




