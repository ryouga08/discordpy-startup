from discord.ext import commands
import datetime
import discord
import os
import traceback
import asyncio

bot = commands.Bot(command_prefix='/')
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
    reaction_member = [">>>"]
    cnt = 2
    while len(reaction_member)-1 <= cnt:
        try:
            reaction, user = await client.wait_for('reaction_add',timeout=0.1,check=check)
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
async def rect(ctx, about = "募集", cnt = 4, settime = 10.0):
    cnt, settime = int(cnt), float(settime)
    reaction_member = [">>>"]
    test = discord.Embed(title=about,colour=0x1e90ff)
    test.add_field(name=f"あと{cnt}人 募集中\n", value=None, inline=True)
    msg = await ctx.send(embed=test)
    #投票の欄
    await msg.add_reaction('⏫')
    await msg.add_reaction('✖')

    def check(reaction, user):
        emoji = str(reaction.emoji)
        if user.bot == True:    # botは無視
            pass
        else:
            return emoji == '⏫' or emoji == '✖'

    while len(reaction_member)-1 <= cnt:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=settime, check=check)
        except asyncio.TimeoutError:
            await ctx.send('残念、人が足りなかったようだ...')
            break
        else:
            print(str(reaction.emoji))
            if str(reaction.emoji) == '⏫':
                reaction_member.append(user.name)
                cnt -= 1
                test = discord.Embed(title=about,colour=0x1e90ff)
                test.add_field(name=f"あと__{cnt}__人 募集中\n", value='\n'.join(reaction_member), inline=True)
                await msg.edit(embed=test)

                if cnt == 0:
                    test = discord.Embed(title=about,colour=0x1e90ff)
                    test.add_field(name=f"あと__{cnt}__人 募集中\n", value='\n'.join(reaction_member), inline=True)
                    await msg.edit(embed=test)
                    finish = discord.Embed(title=about,colour=0x1e90ff)
                    finish.add_field(name="おっと、メンバーがきまったようだ",value='\n'.join(reaction_member), inline=True)
                    await ctx.send(embed=finish)

            elif str(reaction.emoji) == '✖':
                if user.name in reaction_member:
                    reaction_member.remove(user.name)
                    cnt += 1
                    test = discord.Embed(title=about,colour=0x1e90ff)
                    test.add_field(name=f"あと__{cnt}__人 募集中\n", value='\n'.join(reaction_member), inline=True)
                    await msg.edit(embed=test)
                else:
                    pass
        # リアクション消す。メッセージ管理権限がないとForbidden:エラーが出ます。
        await msg.remove_reaction(str(reaction.emoji), user)        

            
bot.run(token)
