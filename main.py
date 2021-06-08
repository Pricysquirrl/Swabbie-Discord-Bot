import os
import discord
from discord.ext import commands
from math import floor
import math
from keep_alive import keep_alive
import random
import requests 
from bs4 import BeautifulSoup 
import asyncio

page = requests.get("https://rl.insider.gg/en/xbox")
soup = BeautifulSoup(page.content, 'html.parser')


cars = ["Backfire", "Breakout","Gizmo","Hotshot", "Merc","Octane","Paladin","Road Hog","Venom","X-Devil","Aftershock","Esper","Grog","Marauder","Masamune"," Proteus","Ripper","Scarab","Takumi","Triton","Vulcan","Zippy","Animus GP","Breakout Type-S","Centio V17","Cyclone","Diestro","Dominus GT","Endo","Fennec","Imperator DT5","Insidio","Jäger 619","Mantis","Nimbus","Octane ZSR","Peregrine TT","Road Hog XL","Samurai","Sentinel","Takumi RX-T","Twinzer","Tygris","Werewolf","X-Devil Mk2","Komodo","Artemis","Battle Bus","Chikara","Guardian","Harbinger","Maverick","Mudcat","R3MX","Ronin","Tyranno"]

my_secret = os.environ['bottoken']

rank = "unranked"
highelo = 0
nextrank = "unranked"
arg = "0"
rankcalc = "You are in {}\nYou are about {} games away from {}.\n*I am not always correct*".format(rank, math.floor((highelo - int(arg)) / 8 + 1), nextrank)

intents = discord.Intents.default()
intents.members = True
bot = discord.ext.commands.Bot(command_prefix="$", intents=intents, help_command=None)

@bot.event
async def on_member_join(member):
    await member.send(
        "Welcome to This is Roket Leg, **{}**!\nRight now you won't be able to send or see any messages, but you will be verified shortly once Pricysquirrl is online. If you have nothing better to do, go to the #features channel to see what there is to do.\nThanks! - Swabbie"
        .format(member.name))
    channel = bot.get_channel(839265539741188157)
    await channel.send("**{} has just joined** \nDo you know them? (y/n)".format(
        member.mention))
    print("someone joined")

    def check(m):
       return "y" in m.content and m.channel == channel 
    msg = await bot.wait_for('message', check=check)
    role = discord.Object("774586769865703424")
    await member.add_roles(role)
    channel = bot.get_channel(839265539741188157)
    embed=discord.Embed(title="Role added successfully", description="Role Name: Hey i know you", color=0x00ff40)
    embed.add_field(name="Member Name:", value=member.mention, inline=True)
    embed.set_footer(text="Swabbie is cool")
    await channel.send(embed=embed)
  



@bot.event
async def on_message(message):
  channels = [bot.get_channel(797596782237843468),bot.get_channel(797932900968300596)]
  if message.channel in channels and message.attachments:
    await message.add_reaction("🔥")
    await message.add_reaction("🗑")
  await bot.process_commands(message)

@bot.command()
async def trendingitems(ctx):
  embed=discord.Embed(title="Trending Items on Rl.Insider", description="(In order)")
  trending_items = soup.find(id="trendingItems")
  for link in trending_items.find_all('a'):
    link_items = link.get('href').replace('/en/xbox/', '')
    acclink_items = link.get('href')
    accacclink_items = "https://rl.insider.gg" + acclink_items 
    split_items = link_items.split('/')
    if len(split_items) == 2:
        item = split_items[0]
        colour = split_items[1]
        sblue = 'sblue'
        if sblue == colour:
          colour = "sky blue"
        fgreen = 'fgreen'
        if fgreen == colour:
          colour = "forest green"
        sienna = 'sienna'
        if sienna == colour:
          colour = "burnt sienna"
        fgreen = 'fgreen'
        underscore = "_"
        if underscore in item:
          item = item.replace("_"," ")
        if underscore in colour:
          colour = colour.replace("_"," ")
        embed.add_field(name=colour + " " + item, value=accacclink_items, inline=False)
    elif len(split_items) == 1:
        item = split_items[0]
        underscore = "_"
        if underscore in item:
          item = item.replace("_"," ")
        embed.add_field(name=item, value= accacclink_items, inline=False)
   
  await ctx.send(embed=embed)

@bot.command()
async def rlgarage(ctx, arg):
 page = requests.get("https://rocket-league.com/player/"+arg)
 if page.status_code == 404:
   embedtree=discord.Embed(title="{}'s RLGarage Account not Found".format(arg), description="https://rocket-league.com/404",color=0xff0000)
   embedtree.add_field(name="Did you spell ```{}``` right?".format(arg), value="Double check!",inline=False)
   await ctx.send(embed=embedtree)
 elif page.status_code == 200:
#good test acc: Doddleboddle (3 accs linked
   xboxusername = "Not linked"
   xboxaccount = ""
   steamusername = "Not linked"
   steamaccount = ""
   epicgamesusername = "Not linked"
   playstationusername = "Not linked"
   playstationaccount = ""
   discordusername = "Not linked"
   discordaccount = ""
   nintendousername = "Not linked"
   redditusername = "Not linked"
   redditaccount = ""
   soup = BeautifulSoup(page.content, 'html.parser')
   try:
     embed=discord.Embed(title="{}'s RLGarage Account".format(arg), description="https://rocket-league.com/player/"+arg +"\nMost recent trade post:")
     hasitems = soup.find("div",class_="rlg-trade__itemshas")
     wantsitems = soup.find("div",class_="rlg-trade__itemswants")
     haslst=[]
     wantslst=[]
     for i in hasitems.find_all("a"):
       haslst.append(i.get_text(strip=True,separator=" "))
     embed.add_field(name="**Has:**", value="\n".join(haslst),inline=True)
     for s in wantsitems.find_all("a"):
       wantslst.append(s.get_text(strip=True,separator=" "))
     embed.add_field(name="**Wants:**", value="\n".join(wantslst), inline=True)
   except:
       embed=discord.Embed(title="{}'s RLGarage Account".format(arg), description="https://rocket-league.com/player/"+arg)
       embed.add_field(name="No recent trades found",value = "Trade supposed to be here? - Click refresh")
   profilelinks = soup.find(class_="rlg-hero__platforms")
   for linked in profilelinks.find_all("a"):
       acclinks = linked.get('href')
       if "account.xbox" in acclinks:
         xboxaccount = acclinks.replace(" ","%20")
       if "steamcommunity" in acclinks:
         steamaccount = acclinks.replace(" ","%20")
       if "my.playstation" in acclinks:
         playstationaccount = acclinks.replace(" ","%20")
       if "discordapp" in acclinks:
         discordaccount = acclinks.replace(" ","%20")
       if "reddit.com" in acclinks:
         redditaccount = acclinks.replace(" ","%20")
   embed.add_field(name="Message {}".format(arg), value="[Message here](https://rocket-league.com/chat/{})".format(arg)
,inline=False)
   platforms = soup.find("div",class_="rlg-hero__platforms")
   for b in platforms.find_all(class_="rlg-network__main"):
     accname = b.get_text(strip=True,separator="")
     if "Xbox" in accname:
       xboxusername = accname.replace("Xbox","")
     if "Steam" in accname:
       steamusername = accname.replace("Steam","")
     if "Epic Games" in accname:
       epicgamesusername = accname.replace("Epic Games","")
     if "PlayStation" in accname:
       playstationusername = accname.replace("PlayStation","")
     if "Discord" in accname:
       discordusername = accname.replace("Discord","")
     if "Nintendo Switch" in accname:
       nintendousername = accname.replace("Nintendo Switch","")
     if "Reddit" in accname:
       redditusername = accname.replace("Reddit","")
   embed.add_field(name="Linked Platforms", value="Xbox: [{}]({})\nSteam: [{}]({}) \nEpic Games: {}\nPlayStation: [{}]({})\nNintendo Switch: {}\nDiscord: [{}]({})\nReddit: [{}]({})".format(xboxusername,xboxaccount,steamusername,steamaccount,epicgamesusername, playstationusername, playstationaccount,nintendousername,discordusername, discordaccount,redditusername,redditaccount),inline=False)
   msg = await ctx.send(embed=embed)
   await msg.add_reaction("🔄")
   try:
     await bot.wait_for(
     "reaction_add",
      timeout=1000.0, 
      check=lambda reaction, user: user == ctx.author and reaction.emoji == "🔄" and reaction.message == msg,
        )
   except asyncio.TimeoutError:
      try:
        await msg.remove_reaction("🔄", bot.user)
      except discord.NotFound:
            pass
   else:
      await msg.delete()
      await rlgarage(ctx, arg=arg)
    

@bot.command()
async def randomcar(ctx):
    msg = await ctx.send("{}, your chosen car is **the {}**".format(ctx.author.mention, random.choice(cars)))
    await msg.add_reaction("🔄")
    try:
        await bot.wait_for(
            "reaction_add",
            timeout=200.0, 
            check=lambda reaction, user: user == ctx.author and reaction.emoji == "🔄" and reaction.message == msg,
        )
    except asyncio.TimeoutError:
        try:
            await msg.remove_reaction("🔄", bot.user)
        except discord.NotFound:
            pass
    else:
        await msg.delete()
        await randomcar(ctx)
      

@bot.command()
async def help(ctx):
 embed=discord.Embed(title="My command prefix is $", description="**What I can do:**")
 embed.set_author(name="Swabbie Bot Commands")
 embed.add_field(name="$rankdistribution", value="Shows what percentile you are in out of the Rocket League playerbase", inline=False)
 embed.add_field(name="$ovo [mmr]  (in development)", value="Tells you what rank you are in 1v1s and how many wins you need to get to the next rank.  Especially useful for when you are unranked.  Use the command rl.rank [platform] [username] to see your mmr", inline=False)
 embed.add_field(name="$randomcar", value="Chooses a random car (excluding paid dlcs) for you to use!", inline=False)
 embed.add_field(name="$trendingitems", value="Shows the most trending items in order on RL.Insider", inline=False)
 embed.add_field(name="$rlgarage [username]", value="Gives you a link to their profile, their most recent trade post, link to message them and linked platforms", inline=False)
 await ctx.send(embed=embed)
 await ctx.message.delete()

@bot.command()
async def rankdistribution(ctx, arg):
 if arg == "s1":
   embed=discord.Embed(title="Click on image to view", description="----------------------")
   embed.set_author(name="Rank Distribution (S1)", url="https://www.reddit.com/r/RocketLeague/comments/ms8d7p/season_2_rank_distribution/")
   embed.set_image(url="https://cdn.discordapp.com/attachments/774631741020176384/832697232453009458/image0.png")
 if arg == "s2":
   embed=discord.Embed(title="Click on image to view", description="----------------------")
   embed.set_author(name="Rank Distribution (S2)", url="https://www.reddit.com/r/RocketLeague/comments/ms8d7p/season_2_rank_distribution/")
   embed.set_image(url="https://cdn.discordapp.com/attachments/774631741020176384/832697232453009458/image0.png")
 await ctx.send(embed=embed)
 await ctx.message.delete()

@bot.group()
async def rank(ctx):
 pass

@rank.command()
async def ovo (ctx, arg):
 if 0<int(arg)<153:
   highelo = 153
   rank = "Bronze 1"
   nextrank = "Bronze 2"
   await ctx.reply(rankcalc)

@bot.command()
async def contribute (ctx):
 embed=discord.Embed(title=r"Issue a pull request to help with some code - anything helps!", description='[Bot Github Link](https://github.com/Pricysquirrl/Swabbie-Discord-Bot)   More updated: [Bot Replit Link](https://replit.com/@Pricysquirrl/Roket-Leg-Discord-Bot#main.py)', color=0x00ff4c)
 embed.set_author(name="Want to Help Contribute to the Code or Have any Suggestions?", url="https://github.com/Pricysquirrl/Swabbie-Discord-Bot")
 embed.add_field(name="About", value='Bad code written in python using discord.py library.\n Github repo may be a bit out of date, so see Replit link above for more recent code, but please use Github for pull requests.\n DM <@766742332204253196> for any questions', inline=False)
 await ctx.send(embed=embed)
 
@commands.has_role("Must feel VERY special")
@bot.command()
async def status(ctx, *, arg):
   await bot.change_presence(activity=discord.Game(name=arg))
   await ctx.send("Done! Changed status to **playing {}**".format(arg))
   print("Changed status")
   await ctx.message.delete()

@commands.has_role("Must feel VERY special")
@bot.command()
async def modhelp(ctx):
 embed=discord.Embed(title="My command prefix is $", description="**What I can do:**")
 embed.set_author(name="Swabbie Bot Mod Commands")
 embed.add_field(name="$message [message]", value="Send a message from Swabbie", inline=False)
 embed.add_field(name="$embed [title] / [description])", value="Send an embed from Swabbie", inline=False)
 embed.add_field(name="$status [status]", value="Change Swabbie's status (must be one word)", inline=False)
 await ctx.send(embed=embed)
 await ctx.message.delete()

@commands.has_role("Must feel VERY special")
@bot.command()
async def supportticket(ctx):
  embed=discord.Embed(title="Help and Suggestions", description="Need help with the server, bots or people or have a suggestion?", color=0x00ff59)
  embed.add_field(name="How to get help or make a suggestion", value="Open a support ticket with ⛑ below", inline=False)
  msg = await ctx.send(embed=embed)
  await msg.add_reaction("⛑")
  try:
    await ctx.message.delete()
  except:
    pass
  def check(reaction, user):
    helprole = discord.Object("851168291770597376")
    if user != bot.user and helprole not in user.roles:
     return str(reaction) == '⛑'
  while True:
   reaction, user = await bot.wait_for("reaction_add", check=check)
   channel = await ctx.guild.create_text_channel("⛑{}s-support-ticket".format(user.name))
   await channel.send("**This is your support ticket**\nPlease state your problem below\nA mod will be with you shortly")
   modchannel = bot.get_channel(839265539741188157)
   await modchannel.send("**NEW SUPPORT TICKET**\n<@&774589745664753665>\n<#{}>".format(channel.id))
   supportrole = await ctx.guild.create_role(name="{}'s Ticket".format(user.name))
   role = supportrole
   helprole = discord.Object("851168291770597376")
   await user.add_roles(role)
   await user.add_roles(helprole)
   await reaction.remove(user)



@commands.has_role("Must feel VERY special")
@bot.command()
async def embed(ctx, *, content: str):
    title, description= content.split('/')
    embed = discord.Embed(title=title, description=description, color=0x00ff40)
    await ctx.send(embed=embed)
    await ctx.message.delete()

@commands.has_role("Must feel VERY special")
@bot.command()
async def message (ctx, * ,arg):
 await ctx.send(arg)
 await ctx.message.delete()


keep_alive()

bot.run(my_secret)
