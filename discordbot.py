from discord.ext import commands
import datetime
import discord
import os
import traceback
import asyncio

bot = commands.Bot(command_prefix='/')
client = discord.Client()
token = os.environ['DISCORD_BOT_TOKEN']

citycodes = {
    "土浦": '080020',
    "水戸": '080010',
    "札幌": '016010',
    "仙台": '040010',
    "東京": '130010',
    "横浜": '140010',
    "名古屋": '230010',
    "大阪": '270000',
    "広島": '340010',
    "福岡": '400010',
    "鹿児島": '460010',
    "那覇": '471010'
}

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
 
@client.event
async def on_message(message):
  if message.author != client.user:

    reg_res = re.compile(u"Bot君、(.+)の天気は？").search(message.content)
    if reg_res:

      if reg_res.group(1) in citycodes.keys():

        citycode = citycodes[reg_res.group(1)]
        resp = urllib.request.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read()
        resp = json.loads(resp.decode('utf-8'))

        msg = resp['location']['city']
        msg += "の天気は、\n"
        for f in resp['forecasts']:
          msg += f['dateLabel'] + "が" + f['telop'] + "\n"
        msg += "です。"

        await client.send_message(message.channel, message.author.mention + msg)

      else:
        await client.send_message(message.channel, "そこの天気はわかりません...")
            
bot.run(token)
