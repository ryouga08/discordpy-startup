from discord.ext import commands
import datetime
import discord
import os
import traceback
import asyncio

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']      
 
@bot.event
async def on_message(message):
    if message.content == "/start"
        channel = message.channel
        await message.channel.send("入力待ち")

        def hello_check(b):
            return b.content == 'こんにちは'

        msg = await client.wait_for('message', check=hello_check, timeout=10.0)
        await message.channel.send(f'{msg.author.mention}、こんにちは！')
    
bot.run(token)
