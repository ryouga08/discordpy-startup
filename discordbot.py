from discord.ext import commands
import datetime
import discord
import os
import traceback

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
    await msg.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER A}')
    await msg.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER B}')
    await msg.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER C}')
    await msg.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER D}')
    name = await ctx.target_reaction.user()
    await ctx.send(name)
   

bot.run(token)
