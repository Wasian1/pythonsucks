import discord
from discord.ext import commands
import random
import time
import requests
import pandas as pd
import os
import re 
import json
import async_cse
from bs4 import BeautifulSoup
import asyncio
import nest_asyncio
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

GCS_DEVELOPER_KEY = os.environ.get("GOOGLE_KEY")

class Games(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.google = async_cse.Search(GCS_DEVELOPER_KEY)
    nest_asyncio.apply()



  @commands.command()
  async def animequotegame(self, ctx):

    def anime_quote_api():
      #making a GET request to the endpoint.
      resp = requests.get("https://some-random-api.ml/animu/quote")
      #checking if resp has a healthy status code.
      if 300 > resp.status_code >= 200:
        content = resp.json() #returns a dictionary of {sentence: value , character: value, anime: value}
      else: 
        content = f"Received bad status code of {resp.status_code}"
      return content 




    await ctx.send("1. Guess the Anime\n2. Guess the Character")
    def check(quote_choice):
      return quote_choice.author == ctx.author and quote_choice.channel == ctx.channel and \
    int(quote_choice.content)in [1, 2, 3]

    correct_answers = 0
    questions_answered = 0
    streak = 0
    question_number = 1

    quote_choice = await self.bot.wait_for("message", check=check)
    if int(quote_choice.content) == 1:
      await ctx.send("Okay, initializing Quote Game: Guess the Anime")
      time.sleep (2)
      await ctx.send("How many questions would you like to answer?")
      number_of_questions = await self.bot.wait_for("message")   
      i = 0

      while int(number_of_questions.content) > i:
        anime_quote_dict = anime_quote_api()
        anime_quote_dict_sentence = anime_quote_dict.get("sentence")
        anime_quote_dict_character = anime_quote_dict.get("character")
        anime_quote_dict_anime = anime_quote_dict.get("anime")

        time.sleep(2)

        await ctx.send(f"Quote Number {question_number}: {anime_quote_dict_sentence}")
        quote_answer1 = await self.bot.wait_for("message")
        if quote_answer1.content.lower() == anime_quote_dict_anime.lower():
          correct_answers += 1
          streak += 1
          questions_answered += 1
          question_number += 1
          time.sleep(2)
          await ctx.send(f"Nice job! You have answered {correct_answers} questions correctly. You are on a {streak} question streak")

          await ctx.send("https://media1.giphy.com/media/QyWBTLDn9WHt0FXGJS/giphy.gif?cid=ecf05e47fgxtclg97gv5xj53luccwl0bl7g0rci0kelmg5ui&rid=giphy.gif&ct=g") 
          i += 1
          time.sleep(2)

          if int(number_of_questions.content) > i:
            await ctx.send("Next question...")
          else:
            pass
          time.sleep(1)

        else:
          correct_answers += 0
          streak = 0
          questions_answered += 1
          question_number += 1

          await ctx.send(f"Zannen, wrong answer. The correct answer is {anime_quote_dict_anime}. You have answered {correct_answers} correctly. Your question streak has been reset")
          time.sleep(2)

          await ctx.send("https://media4.giphy.com/media/KzJxl2IjVyBRz2l492/giphy.gif?cid=ecf05e47tyc9h23x6ra9vez9hzg8sls99zpmwxrdlypccvvq&rid=giphy.gif&ct=g")
          time.sleep(1)
          i += 1

          if int(number_of_questions.content) > i:
            await ctx.send("Next question...")
          else: 
            pass
          time.sleep(1)


    elif int(quote_choice.content) == 2:
      await ctx.send("Okay, initializing Quote Game: Guess the Character")
      time.sleep (1)
      await ctx.send("How many questions would you like to answer?")
      number_of_questions = await self.bot.wait_for("message")
      i = 0
      await ctx.send("Okay...generating quiz...")

      while int(number_of_questions.content) > i:
        anime_quote_dict = anime_quote_api()
        anime_quote_dict_sentence = anime_quote_dict.get("sentence")
        anime_quote_dict_character = anime_quote_dict.get("character")
        anime_quote_dict_anime = anime_quote_dict.get("anime")

        time.sleep(2)
        await ctx.send(f"Quote Number {question_number}: {anime_quote_dict_sentence}")
        time.sleep(2)

        quote_answer1 = await self.bot.wait_for("message")
        if quote_answer1.content.lower() == anime_quote_dict_character.lower():
          correct_answers += 1
          streak += 1
          questions_answered += 1
          question_number += 1
          time.sleep(2)

          await ctx.send(f"Nice job! You have answered {correct_answers} questions correctly. You are on a {streak} question streak")
          time.sleep(2)
          await ctx.send("https://media1.giphy.com/media/QyWBTLDn9WHt0FXGJS/giphy.gif?  cid=ecf05e47fgxtclg97gv5xj53luccwl0bl7g0rci0kelmg5ui&rid=giphy.gif&ct=g")
          i += 1

          if int(number_of_questions.content) > i:
            await ctx.send("Next question...")
          else:
            pass

          time.sleep(2)
        else:
          correct_answers += 0
          streak = 0
          questions_answered += 1
          question_number += 1
          time.sleep(2)

          await ctx.send(f"Zannen, wrong answer. The correct answer is {anime_quote_dict_character}. You have answered {correct_answers} correctly. Your question streak has been reset")
          time.sleep(2)
          await ctx.send("https://media4.giphy.com/media/KzJxl2IjVyBRz2l492/giphy.gif?cid=ecf05e47tyc9h23x6ra9vez9hzg8sls99zpmwxrdlypccvvq&rid=giphy.gif&ct=g")
          i += 1

          if int(number_of_questions.content) > i:
            await ctx.send("Next question...")
          else:
            pass
            time.sleep(1)

    if correct_answers >= questions_answered / 2:
        time.sleep(2)
        await ctx.send("Calculating Totals...")
        time.sleep(3)
        await ctx.send(f"Thanks for playing! Your final score was {correct_answers}. Your final streak was {streak} questions. You went at least 50/50!")
        await ctx.send("https://media2.giphy.com/media/5AnqfqyWRtG2Q/giphy.gif?cid=ecf05e47jp8ha2b9t6fdxrahs54xy8s9fg01si43xa69aif7&rid=giphy.gif&ct=g")
    elif correct_answers < questions_answered / 2:
        time.sleep(2)
        await ctx.send("Calculating Totals...")
        time.sleep(3)
        await ctx.send(f"Thanks for playing! Your final score was {correct_answers}. Your final streak was {streak}. You didn't make 50/50 this time but you can always try again.")
        await ctx.send("https://media1.giphy.com/media/nYYtQdLqwwlTe3ccKh/giphy.gif?cid=ecf05e47qyjzxekys80llt1ivkj5n2845iq0pmgavptd7655&rid=giphy.gif&ct=g")








  @commands.command()
  async def kpopgames(self, ctx):
    await ctx.send("What game would you like to play? (1, 2 or 3)")
    def check(game_choice):
      return game_choice.author == ctx.author and game_choice.channel == ctx.channel and int(game_choice.content) in [1, 2, 3]

    game_choice = await self.bot.wait_for("message", check=check)

    if int(game_choice.content) == 1:
      await ctx.send("Okay, initializing K-Pop Quiz Game")

      time.sleep(1)

      question_type_list = ["Group by Group Member", "Group Member Birthplace", "Group Member Country", "Group by Fanclub Name", "Fanclub Name by Group", "Company by Group Name"]
      correct_answers = 0
      incorrect_answers = 0

      def question_randomizer(self):
        return self.random.choice(question_type_list)

      await ctx.send("How many questions would you like to answer?")
      number_of_questions = await self.bot.wait_for("message")
      i = 0
      while int(number_of_questions.content) > i:

        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_colwidth', 30)
        pd.set_option('display.expand_frame_repr', False)

        kpop_data_idols = pd.read_csv('data/kpop_merged.csv')

        random_kpop_question = question_randomizer()

        #if random_kpop_question = "Group by Group Member":
          #await ctx.send(f"Question {}: )



    elif int(game_choice.content) == 2:
      await ctx.send("Okay, initializing Idol of the Day")
      await ctx.send("Would you like a male or female idol? Please input 'M' for Male or 'F' for female")
      time.sleep(1)

      idol_response = await self.bot.wait_for("message")

      if idol_response.content.lower() == "m":

        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_colwidth', 30)
        pd.set_option('display.expand_frame_repr', False)

        # Load CSV
        kpop_group_data = pd.read_csv(
            'kpop_data/kpop_full_idol_list.csv',
            index_col=False,
            encoding="utf-8-sig",
            quotechar='"',
            skipinitialspace=True
        )

        # Clean column names (remove BOM, whitespace, etc.)
        kpop_group_data.columns = [c.replace('\ufeff','').strip() for c in kpop_group_data.columns]

        # Send the actual column names to Discord for debugging
        await ctx.send(f"Columns after cleaning: {kpop_group_data.columns.tolist()}")

        # Make sure Gender column exists
        if 'Gender' not in kpop_group_data.columns:
            await ctx.send("Error: CSV does not contain a 'Gender' column.")
            return

        # Strip whitespace inside 'Gender' values too
        kpop_group_data['Gender'] = kpop_group_data['Gender'].astype(str).str.strip()

        boy_real_names = kpop_group_data.loc[kpop_group_data['Gender'] == 'Male', 'Full Name']
        boy_real_names_list = list(boy_real_names)
        boy_real_names_random = random.choice(boy_real_names_list)

        boy_name = kpop_group_data.loc[(kpop_group_data['Gender'] == 'Male') & (kpop_group_data['Full Name'] == f"{boy_real_names_random}"), 'Full Name']

        random_boy_group = kpop_group_data.loc[(kpop_group_data['Gender'] == 'Male') & (kpop_group_data['Full Name'] == f"{boy_real_names_random}"), 'Group']

        random_boy_hometown = kpop_group_data.loc[(kpop_group_data['Gender'] == 'Male') & (kpop_group_data['Full Name'] == f"{boy_real_names_random}"), 'Birthplace']

        random_boy_country = kpop_group_data.loc[(kpop_group_data['Gender'] == 'Male') & (kpop_group_data['Full Name'] == f"{boy_real_names_random}"), 'Country']

        random_boy_birthday = kpop_group_data.loc[(kpop_group_data['Gender'] == 'Male') & (kpop_group_data['Full Name'] == f"{boy_real_names_random}"), 'Date of Birth']

        random_boy_stage_name = kpop_group_data.loc[(kpop_group_data['Gender'] == 'Male') & (kpop_group_data['Full Name'] == f"{boy_real_names_random}"), 'Stage Name']

        random_boy_group1 = random_boy_group.to_string(index=False)
        random_boy_hometown1 = random_boy_hometown.to_string(index=False)
        if random_boy_hometown1 == 'NaN':
          random_boy_hometown1 = ""
        else:
          random_boy_hometown1
        random_boy_country1 = random_boy_country.to_string(index=False)
        random_boy_birthday1 = random_boy_birthday.to_string(index=False)
        random_boy_stage_name1 = random_boy_stage_name.to_string(index=False)
        random_boy_name = boy_name.to_string(index=False)

        # Log info for debugging
        logger.info("Random idol selected:")
        logger.info("Stage Name: %s", random_boy_stage_name1)
        logger.info("Full Name: %s", random_boy_name)
        logger.info("Group: %s", random_boy_group1)
        logger.info("Birthplace: %s", random_boy_hometown1)
        logger.info("Country: %s", random_boy_country1)
        logger.info("Date of Birth: %s", random_boy_birthday1)

        async def google_image_search():
          global male_idol_resp
          male_idol_resp = (await self.google.search(f"{random_boy_name} {random_boy_group1} kpop", image_search=True))[0]
          print(male_idol_resp.title)
          print(male_idol_resp.description)
          print(male_idol_resp.image_url)
          print(male_idol_resp.url)
          return male_idol_resp.image_url
        await google_image_search()

        await ctx.send(f"Your idol of the day is {random_boy_stage_name1} !")
        embed = discord.Embed(
                title=f"{random_boy_stage_name1}",
                description=f" Full Name: {boy_real_names_random} \n\n Group: {random_boy_group1} \n\n Hometown: {random_boy_hometown1} {random_boy_country1} \n\n Birthday: {random_boy_birthday1}",
                color=discord.Color.blurple()
            )
        embed.set_image(url=male_idol_resp.image_url)
        await ctx.send(embed=embed)


      elif idol_response.content.lower() == "f":

        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_colwidth', 30)
        pd.set_option('display.expand_frame_repr', False)

        kpop_group_data = pd.read_csv('kpop_full_idol_list.csv')
        girl_real_names = kpop_group_data.loc[kpop_group_data['Gender'] == 'Female', 'Full Name']
        girl_real_names_list = list(girl_real_names)
        girl_real_names_random = random.choice(girl_real_names_list)


        girl_name = kpop_group_data.loc[(kpop_group_data['Gender'] == "Female") & (kpop_group_data['Full Name'] == f"{girl_real_names_random}"), 'Stage Name']

        random_girl_group = kpop_group_data.loc[(kpop_group_data['Gender'] == 'Female') & (kpop_group_data['Full Name'] == f"{girl_real_names_random}"), 'Group']

        random_girl_hometown = kpop_group_data.loc[(kpop_group_data['Gender'] == 'Female') & (kpop_group_data['Full Name'] == f"{girl_real_names_random}"), 'Birthplace']

        random_girl_birthday = kpop_group_data.loc[(kpop_group_data['Gender']== 'Female') & (kpop_group_data['Full Name'] == f"{girl_real_names_random}"), 'Date of Birth']

        random_girl_country = kpop_group_data.loc[(kpop_group_data['Gender'] == 'Female') & (kpop_group_data['Full Name'] == f"{girl_real_names_random}"), 'Country']

        girl_name1 = girl_name.to_string(index=False)
        random_girl_group1 = random_girl_group.to_string(index=False)
        random_girl_hometown1 = random_girl_hometown.to_string(index=False)
        if random_girl_hometown1 == 'NaN':
          random_girl_hometown1 = ""
        else:
          random_girl_hometown1
        random_girl_birthday1 = random_girl_birthday.to_string(index=False)
        random_girl_country1 = random_girl_country.to_string(index=False)

        print(girl_name1)
        print(random_girl_group1)
        print(random_girl_hometown1)
        print(random_girl_birthday1)
        print(random_girl_country1)


      #async def google_image_search(self,ctx):
        #global female_idol_response

        female_idol_response = (await self.google.search(f"{girl_name1} {random_girl_group1} kpop", image_search = True))[0]
        print(female_idol_response.image_url)
        await ctx.send(f"Your idol of the day is {girl_name1} !")
        embed = discord.Embed(
          title = f"{girl_name1}",
          description = f" Full Name: {girl_real_names_random} \n\n Group: {random_girl_group1} \n\n Hometown: {random_girl_hometown1} {random_girl_country1} \n\n Birthday: {random_girl_birthday1}",
          color=discord.Color.green()
        )
        embed.set_image(url = female_idol_response.image_url)
        await ctx.send(embed = embed)


    else:
      time.sleep(1)
      await ctx.send("Okay, initializing jay y pee")
      time.sleep(2)
      embed = discord.Embed(title = "You asked for this", description = f"{ctx.author.mention}, \
                          are you not entertained?",
                         color = ctx.author.color)
      booty_picture = "https://i.pinimg.com/736x/02/15/08/021508d895cbd424d77e9bb52a4d9f05.jpg"
      embed.set_image(url = booty_picture)
      await ctx.channel.send(embed = embed)

  @commands.command()
  async def givewaifu(self, ctx):
      await ctx.send("1. SFW\n2. NSFW\n3. Suprise me")

      def check(message):
          return message.author == ctx.author and message.channel == ctx.channel

      try:
          waifu_response = await self.bot.wait_for("message", check=check,   timeout=30)
      except asyncio.TimeoutError:
          await ctx.send("You took too long to respond.")
          return
      
      type = None
      category = None

      if waifu_response.content.lower() == "nsfw" or str(waifu_response.content) == "2":
          await ctx.send("Naughty, Naughty :^)")
          time.sleep(1)
          type = "nsfw"
          category_list = ['waifu','neko','trap','blowjob']
          category = str(random.choice(category_list))
      elif waifu_response.content.lower() == "sfw" or str(waifu_response.content.strip()) == "1":
          type = "sfw"
          category_list = ['waifu', 'neko', 'shinobu', 'megumin', 'bully', 'cuddle', 
                           'cry', 'hug', 'awoo', 'kiss', 'lick', 'pat', 'smug', 'bonk', 
                           'yeet', 'blush', 'smile', 'wave', 'highfive', 'handhold', 
                           'nom', 'bite', 'glomp', 'slap', 'kill', 'kick', 'happy', 
                           'wink', 'poke', 'dance', 'cringe']
          category = str(random.choice(category_list))
      else:
          type = "suprise"
  
    
      print(self.collectwaifu(type, category))
      print(type, category)
      
      if type == "sfw":
        waifu_url = self.collectwaifu(type, category).get('url')
        embed = discord.Embed(title = "?owo?", description = " <:meguminface1:1219071971573371092> <:meguminface1:1219071971573371092> <:meguminface1:1219071971573371092> ", color =0x2ecc71)
        embed.set_image(url = waifu_url)
        await ctx.send(embed = embed)
        time.sleep(1)
        await ctx.send("Brought to you by our sponsors:")
        await ctx.send("<:HoloRay:1219075732018298920> <:HoloRay:1219075732018298920> <:HoloRay:1219075732018298920><:HoloRay:1219075732018298920><:HoloRay:1219075732018298920>")
      elif type == "nsfw":
        waifu_url = self.collectwaifu(type, category).get('url')
        embed = discord.Embed(title = "Oh you nasty", description = " <:ScoobySmug:523335348659421185> <:ScoobySmug:523335348659421185> <:ScoobySmug:523335348659421185> ", color =0x2ecc71)
        embed.set_image(url = waifu_url)
        await ctx.send(embed = embed)
        time.sleep(1)
        await ctx.send("Brought to you by our sponsor CockCrank")
        await ctx.send("<:CockCrank:1219020492053155951> <:CockCrank:1219020492053155951> <:CockCrank:1219020492053155951><:CockCrank:1219020492053155951><:CockCrank:1219020492053155951>")
      elif type != "sfw" or type != "nsfw":
        await ctx.send("I heard you're into suprises")
        time.sleep(1)
        await ctx.send("So we got you something special")
        time.sleep(1)
        embed = discord.Embed(title = "Just for you!", description = " <:ScoobySmug:523335348659421185> <:ScoobySmug:523335348659421185> <:ScoobySmug:523335348659421185> ", color =0x2ecc71)
        embed.set_image(url = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnA5ZWt6M2FkMnJsdmxiMnJzbWxibGF2MjF3OTZ0ZXBybHo4NDY0NCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/ZE5DmCqNMr3yDXq1Zu/giphy.gif")
        await ctx.send(embed = embed)
        time.sleep(4)
        await ctx.send("Brought to you by our sponsor")
        time.sleep(3)
        await ctx.send(file=discord.File('.//April//matt.jpg'))

  def collectwaifu(self, waifu_type, waifu_category):
    
    resp = requests.get(f"https://api.waifu.pics/{waifu_type}/{waifu_category}")
    if resp.status_code == 200:
        content = resp.json()
    else:
        content = f"Received bad status code of {resp.status_code}"
    return content

async def setup(bot):
  await bot.add_cog(Games(bot))