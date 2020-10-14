from discord.ext import commands
import datetime
import discord
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']
rea = discord.Reaction()

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
        
    def check(reaction, user):
        emoji = str(reaction.emoji)
        if user.bot == True:    # botは無視
            pass
        else:
            return emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER A}'
    
    reaction, user = await client.wait_for('reaction_add', check=check)
    print(str(reaction.emoji))
        if str(reaction.emoji) == '\N{REGIONAL INDICATOR SYMBOL LETTER A}':
            reaction_member.append(user.name)
            emded = discord.Embed(title="title",description="A\nB\nC\nD",colour=0xff0000)
            embed.add_field(name = "name",value = "value")
            await msg.edit(embed=embed)   
    
@bot.event
async def on_message(message):
    # 送信者がbotである場合は弾く
    if message.author.bot:
        return 
    # メッセージの本文が 鳴いて だった場合
    if message.content == "hello":
        # メッセージが送られてきたチャンネルに送る
        await message.channel.send("hello")
        

        

            
bot.run(token)
