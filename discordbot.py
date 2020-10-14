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
@commands.Cog.listener()
async def on_raw_reaction_add(self, payload):
    if payload.member.bot: # BOTアカウントは無視する
        return

    if payload.channel_id != 123456789123: # 特定のチャンネル以外でリアクションした場合は無視する
        return

    if payload.emoji.name == "👍": # 特定の絵文字
       await payload.member.add_roles(payload.member.guild.get_role(123456789123)) # ロールID
            

bot.run(token)
