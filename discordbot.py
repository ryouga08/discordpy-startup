from discord.ext import commands
import datetime
import discord
import os
import traceback
import asyncio

bot = commands.Bot(command_prefix='/')
client = discord.Client()
token = os.environ['DISCORD_BOT_TOKEN']

@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
@bot.command()
async def embcheck(ctx):
    embed = discord.Embed(title="タイトル",description="A\nB\nC\nD",color=0xff0000)
    embed.add_field(name="フィールドの名前",value="フィールドの値")
    msg = await ctx.channel.send(embed=embed)
    for reaction in ['\N{REGIONAL INDICATOR SYMBOL LETTER A}', '\N{REGIONAL INDICATOR SYMBOL LETTER B}', '\N{REGIONAL INDICATOR SYMBOL LETTER C}','\N{REGIONAL INDICATOR SYMBOL LETTER D}']:
        await msg.add_reaction(reaction)
        
    def check(reaction, user):
        emoji = str(reaction.emoji)
        if user.bot == True:    # botは無視
            pass
        else:
            return emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER A}'
    reaction_member = []
    cnt = 2
    while len(reaction_member)-1 <= cnt:
        try:
            reaction, user = await client.wait_for('reaction_add',timeout=60.0,check=check)
        except asyncio.TimeoutError:
            await ctx.send('time over')
            break
        else:
            # print(str(reaction.emoji))
            if str(reaction.emoji) == '\N{REGIONAL INDICATOR SYMBOL LETTER A}':
                reaction_member.append(user.name)
                cnt -= 1
                await msg.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER E}')                  
 
@bot.command()
async def length(ctx):
    await ctx.send("入力待ち")
    def check(msg):
        return msg.author == message.author
    wait_message = await client.wait_for("message",check=check)
    await ctx.send(wait_message.content)
    await ctx.send("end")
   
@bot.event
async def on_message(message):
    if message.content.startswith('$greet'):
        channel = message.channel
        await channel.send('Say hello!')

        def check(m):
            return m.content == 'hello' and m.channel == channel

        msg = await client.wait_for('message', check=check)
        await channel.send('Hello {.author}!'.format(msg))
            
bot.run(token)
