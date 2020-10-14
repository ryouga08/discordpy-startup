from discord.ext import commands
import datetime
import discord
import os
import traceback
import re

link_regex = re.compile(
            r'^https?://(?:(ptb|canary)\.)?discordapp\.com/channels/'
            r'(?:([0-9]{15,21})|(@me))'
            r'/(?P<channel_id>[0-9]{15,21})/(?P<message_id>[0-9]{15,21})/?$'
        )
client = discord.Client()

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

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
    for reaction in ['\N{REGIONAL INDICATOR SYMBOL LETTER A}', '\N{REGIONAL INDICATOR SYMBOL LETTER B}', '\N{REGIONAL INDICATOR SYMBOL LETTER C}','\N{REGIONAL INDICATOR SYMBOL LETTER D}']:
        await msg.add_reaction(reaction)

@client.event
async def on_message(message):
    # 送信者がbotである場合は弾く
    if message.author.bot:
        return 
    if message.content.startswith("/get_reactions "):
        link = message.content.replace("/get_reactions ", "")
        match = link_regex.match(link)
        channel = client.get_channel(int(match.group("channel_id")))
        target_message = await channel.fetch_message(int(match.group("message_id")))
        reactions = target_message.reactions
        text = "絵文字 : 個数\n"
        for reaction in reactions:
            text += f"{reaction.emoji} : {reaction.count}\n"

        await message.channel.send(text)

bot.run(token)
