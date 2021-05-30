import os
import discord
from discord.ext import commands
from math import floor
import math
from keep_alive import keep_alive
from datetime import date

my_secret = os.environ['bottoken']

today = date.today()
d4 = today.strftime("%b-%d-%Y")

#statements below are not modifying these defaults
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
    embed=discord.Embed(title="ROLE ADDED SUCCESSFULLY", description="Role Name: Hey i know you", color=0x00ff40)
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
async def help(ctx):
 embed=discord.Embed(title="My command prefix is $", description="**What I can do:**")
 embed.set_author(name="Swabbie Bot Commands")
 embed.add_field(name="$rankdistribution", value="Shows what percentile you are in out of the Rocket League playerbase", inline=False)
 embed.add_field(name="$ovo [mmr]  (in development)", value="  Tells you what rank you are in and how many wins you need to get to the next rank.  Especially useful for when you are unranked.  Use the command rl.rank [platform] [username] to see your mmr", inline=True)
 await ctx.send(embed=embed)
 await ctx.message.delete()

@bot.command()
async def rankdistribution(ctx):
 embed=discord.Embed(title="Click on image to view", description="----------------------")
 embed.set_author(name="Rank Distribution (S2)", url="https://www.reddit.com/r/RocketLeague/comments/ms8d7p/season_2_rank_distribution/")
 embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/774631741020176384/832697232453009458/image0.png")
 embed.add_field(name="Subject to change", value="----------------------", inline=False)
 embed.set_footer(text="Swabbie is epic")
 await ctx.send(embed=embed)
 await ctx.message.delete()


@bot.command()
async def ovo (ctx, arg):
 if 0<int(arg)<153:
   #not modifying
   highelo = 153
   rank = "Bronze 1"
   nextrank = "Bronze 2"
   await ctx.send(rankcalc)

@bot.command()
async def contribute (ctx):
 

@commands.has_role("Must feel VERY special")
@bot.command()
async def status(ctx, arg):
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

#only works on repl
bot.run(my_secret)
