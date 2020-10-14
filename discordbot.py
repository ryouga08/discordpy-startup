from discord.ext import commands
import datetime
import discord
import os
import traceback

client = discord.Client() #インスタンス化

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

embed = discord.Embed(title="タイトル",description="A\nB\nC\nD",color=0xff0000)
embed.add_field(name="フィールドの名前",value="フィールドの値")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
@bot.command()
async def embcheck(ctx):
    msg = await ctx.channel.send(embed=embed)
    for reaction in ['\N{REGIONAL INDICATOR SYMBOL LETTER A}', '\N{REGIONAL INDICATOR SYMBOL LETTER B}', '\N{REGIONAL INDICATOR SYMBOL LETTER C}','\N{REGIONAL INDICATOR SYMBOL LETTER D}']:
        await msg.add_reaction(reaction)

@client.event 
async def on_raw_reaction_add(payload):
    if payload.emoji.name == "👍": 
        await payload.channel.send("hi")
        
@client.event
async def on_message(msg):
    if msg.content == "/hello":
        await msg.channel.send("hello")
       
            
bot.run(token)
