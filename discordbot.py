from discord.ext import commands
import datetime
import discord
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()

embed = discord.Embed(title="タイトル",description="A\nB\nC\nD",color=0xff0000)
embed.add_field(name="フィールドの名前",value="フィールドの値")

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
@bot.command()
async def embcheck(ctx):
    msg = await ctx.channel.send(embed=embed)
    await msg.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER A}')
    await msg.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER B}')
    await msg.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER C}')
    await msg.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER D}')
    
@client.event
async def on_message(message):
    """メンバー募集 (.rect@数字)"""
    if message.content.startswith(".rect"):
        mcount = int(message.content[6:len(message.content)])
        text= "あと{}人 募集中\n"
        revmsg = text.format(mcount)
        #friend_list 押した人のList
        frelist = []
        msg = await client.send_message(message.channel, revmsg)

        #投票の欄
        await client.add_reaction(msg, '\u21a9')
        await client.add_reaction(msg, '⏫')
        await client.pin_message(msg)

        #リアクションをチェックする
        while len(frelist) < int(message.content[6:len(message.content)]):
            target_reaction = await client.wait_for_reaction(message=msg)
            #発言したユーザが同一でない場合 真
            if target_reaction.user != msg.author:
                #==============================================================
                #押された絵文字が既存のものの場合 >> 左　del
                if target_reaction.reaction.emoji == '\u21a9':
                    #==========================================================
                    #◀のリアクションに追加があったら反応 frelistにuser.nameがあった場合　真
                    if target_reaction.user.name in frelist:
                        frelist.remove(target_reaction.user.name)
                        mcount += 1
                        #リストから名前削除
                        await client.edit_message(msg, text.format(mcount) +
                                                        '\n'.join(frelist))
                            #メッセージを書き換え

                    else:
                        pass
                #==============================================================
                #押された絵文字が既存のものの場合　>> 右　add
                elif target_reaction.reaction.emoji == '⏫':
                    if target_reaction.user.name in frelist:
                        pass

                    else:
                        frelist.append(target_reaction.user.name)
                        #リストに名前追加
                        mcount = mcount - 1
                        await client.edit_message(msg, text.format(mcount) +
                                                        '\n'.join(frelist))


                elif target_reaction.reaction.emoji == '✖':
                        await client.edit_message(msg, '募集終了\n'+ '\n'.join(frelist))
                        await client.unpin_message(msg)
                        break
                await client.remove_reaction(msg, target_reaction.reaction.emoji, target_reaction.user)
                #ユーザーがつけたリアクションを消す※権限によってはエラー
                #==============================================================
        else:
            await client.edit_message(msg, '募集終了\n'+ '\n'.join(frelist))

    

    

bot.run(token)
