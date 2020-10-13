from discord.ext import commands
import datetime
import discord
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

embed = discord.Embed(title="タイトル",description="中身",color=0xff0000)
embed.add_field(name="フィールドの名前",value="フィールドの値")
emoji = '\N{THUMBS UP SIGN}'

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
    await ctx.channel.send(embed=embed)
    await ctx.client.add_reaction(emoji)
   


bot.run(token)
