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
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json



cars = ["Backfire", "Breakout","Gizmo","Hotshot", "Merc","Octane","Paladin","Road Hog","Venom","X-Devil","Aftershock","Esper","Grog","Marauder","Masamune"," Proteus","Ripper","Scarab","Takumi","Triton","Vulcan","Zippy","Animus GP","Breakout Type-S","Centio V17","Cyclone","Diestro","Dominus GT","Endo","Fennec","Imperator DT5","Insidio","Jäger 619","Mantis","Nimbus","Octane ZSR","Peregrine TT","Road Hog XL","Samurai","Sentinel","Takumi RX-T","Twinzer","Tygris","Werewolf","X-Devil Mk2","Komodo","Artemis","Battle Bus","Chikara","Guardian","Harbinger","Maverick","Mudcat","R3MX","Ronin","Tyranno"]

my_secret = os.environ['bottoken']

with open("status.json","r") as statusfile:
   statusjson = json.load(statusfile)
   status = statusjson["status"]
   print(status)


intents = discord.Intents.default()
intents.members = True
bot = discord.ext.commands.Bot(command_prefix="$", intents=intents, help_command=None, activity=discord.Game(status))

myguild = bot.get_guild(774573801802432523)

@bot.event
async def on_command(ctx):
  with open("command_log.txt","a") as log:
    log.write(ctx.author.name + " - $" + str(ctx.command) + " " + str(ctx.kwargs))
    log.write("\n")




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
       return "y".lower() in m.content and m.channel == channel 
    await bot.wait_for('message', check=check)
    role = discord.Object("774586769865703424")
    await member.add_roles(role)
    channel = bot.get_channel(839265539741188157)
    embed=discord.Embed(title="Role added successfully", description="Role Name: Hey i know you", color=0x00ff40)
    embed.add_field(name="Member Name:", value=member.mention, inline=True)
    embed.set_footer(text="Swabbie is cool")
    await channel.send(embed=embed)
    await member.send("You now have access to the Discord")
  
@bot.event
async def on_ready():
  print("Bot Online")
  supchannel = bot.get_channel(786606153864970270)
  await supchannel.purge(limit=100000000)
  await supportticket()


 

@bot.event
async def on_message(message):
  channels = [bot.get_channel(797596782237843468),bot.get_channel(797932900968300596)]
  if message.channel in channels and message.attachments:
    await message.add_reaction("🔥")
    await message.add_reaction("🗑")
  await bot.process_commands(message)


@bot.command()
async def tictactoe(ctx):
  embed=discord.Embed(title="Welcome to TicTacToe", description="A multiplayer game built by [Pricysquirrl#1641](https://discord.com/channels/@me/876492093248389120)", color=0x00ffb7)
  embed.add_field(name="Tag a friend to start", value="(@ them)", inline=True)
  embed.add_field(name="How to play TicTacToe", value="[Watch Here](https://www.youtube.com/watch?v=USEjXNCTvcc)", inline=True)
  embed.add_field(name="How to play", value="When it is your go, pick a number 1-9 corresponding to a spot on the grid.", inline=False)
  embed.set_footer(text="Play TicTacToe on Discord with friends!")
  await ctx.send(embed=embed)

  async def get_opponent():
    def check_opponent(input):
      return input.author == ctx.author and bool(input.mentions)
    try:
      msg = await bot.wait_for("message", check=check_opponent, timeout=120)
    except:
      await ctx.send("Game idle.  Ending...")
      return False
    else:
      if len(msg.mentions) > 1:
        await ctx.send("Choose 1 opponent please!")
        await get_opponent()
      else:
        global opponent_id, opponent_name,opponent_object
        opponent_id = msg.mentions[0].id
        opponent_name = msg.mentions[0].name
        opponent_object = msg.mentions[0]
        await ctx.send(f"An invite has been sent to {opponent_name}\nOr if they are here, they can just type ``join``")
        invite=discord.Embed(title=f"{ctx.author.name} has Challenged you to a TicTacToe Game", description=f"Type  ``join``  in [this channel]({msg.jump_url}) to accept the invitation")
        invite.set_footer(text="$tictactoe: Play TicTacToe on Discord with friends!")
        await opponent_object.send(embed=invite)
        def check_opponent_confirm(opp):
         return opp.author.id == opponent_id and opp.content == "join"
        try:
          await bot.wait_for("message", check=check_opponent_confirm, timeout=120)
        except:
          await ctx.send(f"{opponent_name} has not joined.  Game ending...")
          return False
        else:
          await ctx.send("Invite accepted.  Game starting...")
          time.sleep(2)
          global opponent_check_complete
          opponent_check_complete = True
  
  await get_opponent()
  

  global board,moves,game_on,current_player,other_player, emoji_moves,other_player_name,current_player_name,move_counter,tie,afk
  board = ["1️⃣","2️⃣","3️⃣","4️⃣","️5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
  moves = ["1","2","3","4","5","6","7","8","9"]
  emoji_moves = ["1️⃣","2️⃣","3️⃣","4️⃣","️5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
  game_on = True
  current_player = ctx.author.id
  current_player_name = ctx.author.name
  other_player = opponent_id
  other_player_name = opponent_name
  move_counter = 0
  tie = False
  afk = False



  def switch_move():
    global current_player,other_player,current_player_name,other_player_name
    if current_player == ctx.author.id:
      current_player = opponent_id
      current_player_name = opponent_name
      other_player = ctx.author.id
      other_player_name = ctx.author.name
    elif current_player == opponent_id:
      current_player = ctx.author.id
      current_player_name = ctx.author.name
      other_player = opponent_id
      other_player_name = opponent_name


  async def handle_move():
    global game_on,moves,emoji_moves
    await ctx.send("<@!{}>, it is your go!".format(current_player))
    async def contain_move():
      global game_on,move_counter,afk
      def check_move(move):
        return move.author.id == current_player and move.content in moves
      try:
        playermove = await bot.wait_for("message", check=check_move, timeout=45)
      except:
        await ctx.send("<@!{}> has made no move.  <@!{}> wins!".format(current_player,other_player))
        game_on = False
        afk = True
        return False
      else:
        if current_player == ctx.author.id:
          symbol = "🟢"
          if board[int(playermove.content)-1] in emoji_moves:
            board[int(playermove.content)-1] = symbol
            move_counter += 1
            await display_board()
            return
          else:
            await ctx.send("That place is already taken, try another")
            await contain_move()
        elif current_player == opponent_id:
          symbol = "❌"
          if board[int(playermove.content)-1] in emoji_moves:
           board[int(playermove.content)-1] = symbol
           move_counter += 1
           await display_board()
           return
          else:
            await ctx.send("That place is already taken, try another")
            await contain_move()
    await contain_move()
        
  async def display_starting_board():
    embed=discord.Embed(title="TicTacToe Game in Progress", description=f"{ctx.author.name} VS {opponent_name}", color=0x00ffb7)
    embed.add_field(name="Board", value=f"{board[0]}  |  {board[1]}  |  {board[2]} \n----+----+----\n{board[3]}  |  {board[4]}  |  {board[5]}\n----+----+----\n{board[6]}  |  {board[7]}  |  {board[8]}", inline=True)
    embed.add_field(name="Current player", value=f" <@!{current_player}>\n\n**Next Go**\n<@!{other_player}>", inline=True)
    embed.set_footer(text="$tictactoe: Play TicTacToe on Discord with friends!")
    await ctx.send(embed=embed)


  async def display_board():
    embed=discord.Embed(title="TicTacToe Game in Progress", description=f"{ctx.author.name} VS {opponent_name}", color=0x00ffb7)
    embed.add_field(name="Board", value=f"{board[0]}  |  {board[1]}  |  {board[2]} \n----+----+----\n{board[3]}  |  {board[4]}  |  {board[5]}\n----+----+----\n{board[6]}  |  {board[7]}  |  {board[8]}", inline=True)
    embed.add_field(name="Current player", value=f" <@!{other_player}>\n\n**Next Go**\n<@!{current_player}>", inline=True)
    embed.set_footer(text="$tictactoe: Play TicTacToe on Discord with friends!")
    await ctx.send(embed=embed)
 
  def check_for_win():
    global game_on, move_counter,tie
    if board[0] == board[1] == board[2]:
      game_on = False
      return True
    elif board[3] == board[4] == board[5]:
      game_on = False
      return True
    elif board[7] == board[4] == board[8]:
      game_on = False
      return True
    elif board[0] == board[3] == board[6]:
      game_on = False
      return True
    elif board[1] == board[4] == board[7]:
      game_on = False
      return True
    elif board[2] == board[5] == board[8]:
      game_on = False
      return True
    elif board[0] == board[4] == board[8]:
      game_on = False
      return True
    elif board[2] == board[4] == board[6]:
      game_on = False
      return True
    elif move_counter == 9:
      game_on = False
      tie = True
    else:
      return False
    

    


  async def play_game():
    global other_player,tie,afk
    await display_starting_board()
    while game_on:
       await handle_move()
       check_for_win()
       switch_move()
    else:
      if tie:
          embed=discord.Embed(title="Draw!", description="TicTacToe Game Over", color=0x00ffb7)
          embed.add_field(name="Play Again?", value="Use $tictactoe", inline=True)
          embed.set_footer(text="Play TicTacToe on Discord with friends!")
          await ctx.send(embed=embed)
          return
      elif afk:
        embed=discord.Embed(title=f"{current_player_name} wins!", description="TicTacToe Game Over", color=0x00ffb7)
        embed.add_field(name="Play Again?", value="Use $tictactoe", inline=True)
        embed.set_footer(text="Play TicTacToe on Discord with friends!")
        await ctx.send(embed=embed)
        return
      else:
        embed=discord.Embed(title=f"{other_player_name} wins!", description="TicTacToe Game Over", color=0x00ffb7)
        embed.add_field(name="Play Again?", value="Use $tictactoe", inline=True)
        embed.set_footer(text="Play TicTacToe on Discord with friends!")
        await ctx.send(embed=embed)
        return

  try:
    if opponent_check_complete == True:
      await play_game()
    else:
      return
  except:
    return
  


      





    

  





@bot.command()
async def trendingitems(ctx, chosenplatform=None):
  if chosenplatform is None:
   embeddive = discord.Embed(title="Please choose a platform",description="Valid platforms are ```psn``````xbox``````switch``````pc```",color=0xff0000)
   await ctx.send(embed=embeddive)
  elif chosenplatform.lower() not in ("psn", "xbox", "switch", "pc"):
   embeddoor=discord.Embed(title="{} is not a valid platform".format(chosenplatform.lower()), description="Valid platforms are ```psn``````xbox``````switch``````pc```",color=0xff0000)
   await ctx.send(embed=embeddoor)
  else:
    page = requests.get("https://rl.insider.gg/en/{}".format(chosenplatform.lower()))
    soup = BeautifulSoup(page.content, 'html.parser')
    embed=discord.Embed(title="Trending Items on Rl.Insider [{}]".format(chosenplatform), description="(In order)")
    trending_items = soup.find(id="trendingItems")
    for link in trending_items.find_all('a'):
      link_items = link.get('href').replace('/en/{}/'.format(chosenplatform.lower()), '')
      acclink_items = link.get('href')
      accacclink_items = "https://rl.insider.gg" + acclink_items 
      split_items = link_items.split('/')
      if len(split_items) == 2:
          item = split_items[0]
          colour = split_items[1]
          if 'sblue' == colour:
            colour = "sky blue"
          if 'fgreen' == colour:
            colour = "forest green"
          if 'sienna' == colour:
            colour = "burnt sienna"
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
async def rlg(ctx,*, arg):
 accounts = []
 page = requests.get("https://rocket-league.com/player/"+arg)
 if page.status_code == 404:
   embedtree=discord.Embed(title="{}'s RLGarage Account not Found".format(arg), description="https://rocket-league.com/404",color=0xff0000)
   embedtree.add_field(name="Did you spell ```{}``` right?".format(arg), value="Double check!",inline=False)
   await ctx.send(embed=embedtree)
 elif page.status_code == 200:
#good test acc: Doddleboddle (3 accs linked)
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
   profilelinks = soup.find(class_="rlg-user__networks")
   for linked in profilelinks.find_all("a"):
       acclinks = linked.get('href')
       if "account.xbox" in acclinks:
         xboxaccount = acclinks.replace(" ","%20")
       if "steamcommunity" in acclinks:
         steamaccount = acclinks.replace(" ","%20")
       if "discordapp" in acclinks:
         discordaccount = acclinks.replace(" ","%20")
       if "reddit.com" in acclinks:
         redditaccount = acclinks.replace(" ","%20")
   embed.add_field(name="Message {}".format(arg), value="[Message here](https://rocket-league.com/chat/{})".format(arg)
,inline=False)
   platforms = soup.find("div",class_="rlg-user__networks")
   for b in platforms.find_all(class_="rlg-network__main"):
     accname = b.get_text(strip=True,separator="")
     if "Xbox" in accname:
       xboxusername = accname.replace("Xbox","")
       accounts.append("Xbox: [{}]({})".format(xboxusername, xboxaccount))
     if "Steam" in accname:
       steamusername = accname.replace("Steam","")
       accounts.append("Steam: [{}]({})".format(steamusername, steamaccount))
     if "Epic Games" in accname:
       epicgamesusername = accname.replace("Epic Games","")
       accounts.append("Epic Games: {}".format(epicgamesusername))
     if "PlayStation" in accname:
       playstationusername = accname.replace("PlayStation","")
       accounts.append("Playstation: {}".format(playstationusername))
     if "Discord" in accname:
       discordusername = accname.replace("Discord","")
       accounts.append("Discord: [{}]({})".format(discordusername, discordaccount))
     if "Nintendo Switch" in accname:
       nintendousername = accname.replace("Nintendo Switch","")
       accounts.append("Nintendo Switch: {}".format(nintendousername))
     if "Reddit" in accname:
       redditusername = accname.replace("Reddit","")
       accounts.append("Reddit: [{}]({})".format(redditusername, redditaccount))
   embed.add_field(name="Linked Platforms", value="\n".join(accounts),inline=False)
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
      await rlg(ctx, arg=arg)
    
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
async def xbox(ctx, *, gamertag=None):
  if gamertag is None:
    await ctx.send("You forgot to add a gamertag!")
    return
  elif "account.xbox" in gamertag:
    query = gamertag
  else:
    query = "https://account.xbox.com/en-gb/profile?gamertag="+gamertag.replace("#","")
  findingmsg = await ctx.send("Finding account...\n(This may take a few seconds)")
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome("/usr/bin/chromedriver",options=chrome_options)
  driver.get(query)
  email = os.environ['email']
  passw = os.environ['passw']
  driver.find_element_by_id("i0116").send_keys(email)
  driver.find_element_by_id("idSIButton9").click()
  WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "i0118"))).send_keys(passw)
  driver.find_element_by_id("idSIButton9").click()
  if "login.live.com/ppsecure/post.srf" in driver.current_url:
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#idBtn_Back"))).click()
  else:
    pass
  try:
    if "profile?" in driver.current_url:
      gamerscore = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".c-action-trigger.c-glyph.glyph-gamerscore"))).text
      gamertagtext = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".c-heading-3"))).text
      pfp = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".c-image.f-round"))).get_attribute("src")
      try:
        badgesimg = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'badges')]/img"))).get_attribute("alt")
      except:
        pass
      WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".item-value-data")))
      ff = []
      followers_els = driver.find_elements_by_css_selector(".item-value-data")
      for el in followers_els:
          ff.append(el.text)
      followers = ff[0]
      friends = ff[1]
      WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@id,'right-side')]/p")))
      
      irlname = ""
      statusName = []
      status_name = driver.find_elements_by_xpath("//div[contains(@id,'right-side')]/p")

      statusName = []

      for r in status_name:
        statusName.append(r.text)
      if len(statusName) > 1:
        status  = statusName[1]
        irlname = statusName[0]
      else:
        status  = statusName[0]
      try:
        if "year(s) with Xbox Live" in badgesimg:
          accountage = badgesimg.split(" ")[0]
        else:
          accountage = "<1"
      except:
        accountage = "<1"
        
      await findingmsg.delete()
      xboxembed=discord.Embed(title="{}'s Xbox Account".format(gamertagtext), url = query, description=str(irlname) + "\n" + str(status))
      xboxembed.add_field(name="Info",value="**Followers:** {}\n**Friends:** {} \n**Gamerscore:** {} \n**Xbox Live Account Age:** {}".format(followers, friends, gamerscore, accountage))
      xboxembed.set_thumbnail(url=pfp)
      xboxembedsent = await ctx.send(embed=xboxembed)
      driver.quit()
      await xboxembedsent.add_reaction("🔄")
      try:
        await bot.wait_for(
        "reaction_add",
          timeout=1000.0, 
          check=lambda reaction, user: user == ctx.author and reaction.emoji == "🔄" and reaction.message == xboxembedsent,
            )
      except asyncio.TimeoutError:
          try:
            await xboxembedsent.remove_reaction("🔄", bot.user)
          except discord.NotFound:
                pass
      else:
          await xboxembedsent.delete()
          await xbox(ctx, gamertag=gamertag)
  except:
    pass

  
@bot.command()
async def help(ctx):
 embed=discord.Embed(title="My command prefix is $", description="**What I can do:**")
 embed.set_author(name="Swabbie Bot Commands")
 embed.add_field(name="$rankdistribution [season]", value="Shows what percentile you are in out of the Rocket League playerbase", inline=False)
 embed.add_field(name="$ovo [mmr]  (in development)", value="Tells you what rank you are in 1v1s and how many wins you need to get to the next rank.  Especially useful for when you are unranked.  Use the command rl.rank [platform] [username] to see your mmr", inline=False)
 embed.add_field(name="$randomcar", value="Chooses a random car (excluding paid dlcs) for you to use!", inline=False)
 embed.add_field(name="$trendingitems", value="Shows the most trending items in order on RL.Insider", inline=False)
 embed.add_field(name="$rlg [username]", value="Gives you a link to their profile, their most recent trade post, link to message them and linked platforms", inline=False)
 embed.add_field(name="$banmessage [message]", value="Creates a custom ban message with a funny message of your choice", inline=False)
 embed.add_field(name="$xbox [gamertag]", value="Displays information about about an xbox account", inline=False)
 embed.add_field(name="$tictactoe", value="Play TicTacToe on Discord with friends!", inline=False)
 await ctx.send(embed=embed)
 await ctx.message.delete()

@bot.command()
async def rankdistribution(ctx, season="2"):
 embed=discord.Embed(title="Click on image to view", description="----------------------")
 if season.lower() == "1":
   embed.set_author(name="Rank Distribution (S1)", url="https://www.reddit.com/r/RocketLeague/comments/kr4weh/season_1_rank_distribution/")
   embed.set_image(url="https://media.discordapp.net/attachments/774631741020176384/796458094355808347/Screenshot_2021-01-06_at_19.18.58.png?width=748&height=1074")
 if season.lower() == "2":
   embed=discord.Embed(title="Click on image to view", description="----------------------")
   embed.set_author(name="Rank Distribution (S2)", url="https://www.reddit.com/r/RocketLeague/comments/ms8d7p/season_2_rank_distribution/")
   embed.set_image(url="https://cdn.discordapp.com/attachments/774631741020176384/832697232453009458/image0.png")
 await ctx.send(embed=embed)

@bot.group()
async def rank(ctx):
 pass

@rank.command()
async def ovo (ctx, elo):
 if 0<int(elo)<153:
   highelo = 153
   rank = "Bronze 1"
   nextrank = "Bronze 2"
   rankcalc = "You are in {}\nYou are about {} games away from {}.\n*I am not always correct*".format(rank, math.floor((highelo - int(elo)) / 8 + 1), nextrank)
   try:
     await ctx.reply(rankcalc)
   except:
     await ctx.send(rankcalc)
 if 153<int(elo)<300:
    highelo = 300
    rank = "Bronze 2"
    nextrank = "Bronze 3"
    rankcalc = "You are in {}\nYou are about {} games away from {}.\n*I am not always correct*".format(rank, math.floor((highelo - int(elo)) / 8 + 1), nextrank)
    try:
      await ctx.reply(rankcalc)
    except:
      await ctx.send(rankcalc)

@bot.command()
async def contribute (ctx):
 embed=discord.Embed(title="Issue a pull request to help with some code - anything helps!", description='[Bot Github Link](https://github.com/Pricysquirrl/Swabbie-Discord-Bot)   More updated: [Bot Replit Link](https://replit.com/@Pricysquirrl/Roket-Leg-Discord-Bot#main.py)', color=0x00ff4c)
 embed.set_author(name="Want to Help Contribute to the Code or Have any Suggestions?", url="https://github.com/Pricysquirrl/Swabbie-Discord-Bot")
 embed.add_field(name="About", value='Bad code written in python using discord.py library.\n Github repo may be a bit out of date, so see Replit link above for more recent code, but please use Github for pull requests.\n DM <@766742332204253196> for any questions', inline=False)
 await ctx.send(embed=embed)
 
@commands.has_role("Must feel VERY special")
@bot.command()
async def status(ctx, *, message):
   await bot.change_presence(activity=discord.Game(name=message))
   with open("status.json","w") as statusfile:
     json.dump({"status":message, "author":ctx.author.name}, statusfile)
   await ctx.send("Done! Changed status to **playing {}**".format(message))
   print("Changed status to {}".format(message))
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

async def supportticket():
  embed=discord.Embed(title="Help and Suggestions", description="Need help with the server, bots or people or have a suggestion?", color=0x00ff59)
  embed.add_field(name="How to get help or make a suggestion", value="Open a support ticket with ⛑ below", inline=False)
  supchannel = bot.get_channel(786606153864970270)
  msg = await supchannel.send(embed=embed)
  await msg.add_reaction("⛑")
  def check(reaction, user):
    if user != bot.user and reaction.message.id == msg.id:
     return str(reaction) == '⛑'
  while True:
   reaction, user = await bot.wait_for("reaction_add", check=check)
   global helprole
   helprole = discord.utils.get(user.roles, id=851168291770597376)
   if helprole is None:
     global myguild
     myguild = bot.get_guild(774573801802432523)
     global supportrole
     supportrole = await myguild.create_role(name="{}'s Ticket".format(user.name))
     helprole = discord.Object(851168291770597376)
     await user.add_roles(supportrole)
     await user.add_roles(helprole)
     modrole= discord.utils.get(user.roles, id=774589745664753665)
     overwrites= {
      myguild.default_role: discord.PermissionOverwrite(view_channel=False),
      supportrole: discord.PermissionOverwrite(send_messages=True, read_messages=True, view_channel=True, read_message_history=True),
      modrole: discord.PermissionOverwrite(send_messages=True, read_messages=True, view_channel=True, read_message_history=True)
      
     }
     global newchannel
     newchannel = await myguild.create_text_channel("⛑{}s-support-ticket".format(user.name), overwrites=overwrites)
     await newchannel.send("**This is your support ticket**\nPlease state your problem below\nA mod will be with you shortly")
     supchannel = bot.get_channel(786606153864970270)
     modchannel = bot.get_channel(839265539741188157)
     await modchannel.send("**NEW SUPPORT TICKET**\n<@&774589745664753665>\n<#{}>".format(newchannel.id))
     await reaction.remove(user)
     global ticketuser
     ticketuser = user
   else:
     await user.send("You have a support ticket open already\n<#{}>".format(newchannel.id))
     await reaction.remove(user)

@bot.command()
async def close(ctx):
  if ctx.channel.id == newchannel.id:
    await ctx.channel.delete()
    await supportrole.delete(reason=None)
    await ticketuser.remove_roles(helprole)

@bot.command()
async def banmessage(ctx, *, reason):
  img = Image.open('banmessage.png')
  I1 = ImageDraw.Draw(img)
  with open("ARIALN.TTF"):
   myFont = ImageFont.truetype('ARIALN.TTF', 22)
  modifiedimage = "banmessage2.png"
  try:
   modifiedimage.delete()
  except:
   pass
  if len(reason) <= 55 and len(reason) >= 1:
     I1.text((49, 264), reason, font=myFont, fill =(230, 230, 230))
     img.show()
     img.save("banmessage2.png")
     with open("banmessage2.png", "rb") as accfile:
       msg = await ctx.send(file=discord.File(accfile))
       await msg.add_reaction("📥")
       def check(reaction, user):
         if user != bot.user and reaction.message.id == msg.id and reaction.emoji == '📥':
           return str(reaction) == '📥'
       while True:
         reaction, user = await bot.wait_for("reaction_add", check=check)
         accfile.seek(0)
         await user.send(file=discord.File(accfile, "Ban_Message"))
  elif len(reason) > 55:
     overreason = reason[:52] + "..."
     I1.text((49, 264), overreason, font=myFont, fill =(230, 230, 230))
     img.show()
     img.save("banmessage2.png")
     with open("banmessage2.png", "rb") as accfile:
       msg = await ctx.send(file=discord.File(accfile))
       await msg.add_reaction("📥")
       def check(reaction, user):
         if user != bot.user and reaction.message.id == msg.id and reaction.emoji == '📥':
           return str(reaction) == '📥'
       while True:
          reaction, user = await bot.wait_for("reaction_add", check=check)
          accfile.seek(0)
          await user.send(file=discord.File(accfile, "Ban_Message"))
   
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
