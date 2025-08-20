from discord.ext import commands
import re
import discord
import random
import time

class BotMessages(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author == self.bot.user: # To make sure your bot will ignore messages sent by itself
      return
    discord_input = message.content
    print(discord_input)
    Naughty_Words = re.search(r'^(.*(fuck|shit|penis|cunt|wanker|motherfucker|bastard|dick|prick|pussy|bitch|balls|chode|ecchi|nick|anal|cum|jizz|weiner|fuck you|fuck this|fuckin|fucking|fuck u).*)', discord_input)
    April_fools = re.search(r'^(.*(april|fools).*)', discord_input)
    fools_list = ['.//April//SPOILER_matt.jpg', './/April//SPOILER_Window Matt.png', './/April//SPOILER_Banana Dan.png', './/April//SPOILER_Frog Mondo.png', './/April//SPOILER_Frog Matt UpToke.png', './/April//SPOILER_Pan Dan.png', './/April//SPOILER_Frog Sage 10 Karma.png', './/April//SPOILER_Sage Matt Jackpot.png']
    start = re.search(r'^(.*(xcommence festivities).*)', discord_input)

    if Naughty_Words is not None:
      if discord_input == Naughty_Words.string:
        await message.channel.send('Naughty, Naughty ( ͡° ͜ʖ ͡°)')
        await self.bot.process_commands(message)
      else:
        pass

    elif April_fools is not None:
      if discord_input == April_fools.string:
        random_fool = random.choice(fools_list)
        await message.channel.send(file=discord.File(f"{random_fool}")) 
        if random_fool == ".//April//SPOILER_matt.jpg":
          time.sleep(6)
          await message.channel.send("||<https://shorturl.at/jmsEN?>||")
          await message.channel.send("Congratulations! Click the link to claim your prize. If you dare...")
          time.sleep(4)
          await message.channel.send("As Riley would say,")
          await message.channel.send("*```Do it coward. You fucking wont```*")

        elif random_fool == ".//April//SPOILER_Window Matt.png":
          time.sleep(6)
          await message.channel.send("Looks like someone's happy to see you... :weary: :hot_face: :sweat_drops: ")
          time.sleep(2)
          await message.channel.send("<:matt:230169075626541056> <:matt:230169075626541056> <:matt:230169075626541056>")

        elif random_fool == ".//April//SPOILER_Banana Dan.png":
          time.sleep(6)
          await message.channel.send("<:dan:240621343551258624> <:dan:240621343551258624> <:dan:240621343551258624>")
          await message.channel.send("You have 10 seconds...")
          time.sleep(10)

          dumby_input = await self.bot.wait_for("message")
          dumby_search = re.search(r'^(.*(dumby).*)', dumby_input.content)
          try:
            if dumby_input.content == dumby_search.string:
              time.sleep(2)
              await message.channel.send("https://c.tenor.com/7EttrztgjiAAAAAC/palpatine-star-wars.gif")
              await message.channel.send("Good Anakin Good. Now kill him. Kill him *now*")
          except AttributeError:

            time.sleep(3)
            await message.channel.send("https://c.tenor.com/ZgaGF-2SgCMAAAAd/darth-vader-star-wars.gif")
            time.sleep(3)
            await message.channel.send("Bananas incoming")
            time.sleep(2)
            await message.channel.send("https://c.tenor.com/GnX8QWOF0CEAAAAC/banana-lafuddyduddyp2.gif")

        elif random_fool == ".//April//SPOILER_Frog Mondo.png":
          time.sleep(3)
          await message.channel.send("POGDO has arrived!")
          await message.channel.send("<:mondo:230169125928960000> <:mondo:230169125928960000> <:mondo:230169125928960000> <:mondo:230169125928960000> <:mondo:230169125928960000>")

        elif random_fool == ".//April//SPOILER_Frog Matt UpToke.png":
          time.sleep(6)
          await message.channel.send("You have 10 seconds to send 'Uptoke'...")
          time.sleep(10)
          toke_input = await self.bot.wait_for("message")
          toke_search = re.search(r'^(.*(Uptoke).*)', toke_input.content)
          try:
            if toke_input.content == toke_search.string:
              time.sleep(2)
              await message.channel.send("https://c.tenor.com/7EttrztgjiAAAAAC/palpatine-star-wars.gif")
              await message.channel.send("Good Anakin Good. Now smash that like button. Smash that like button *now*")
              time.sleep(2)
              await message.channel.send("https://media0.giphy.com/media/3o75279fBGgbO848ZW/giphy.gif?cid=ecf05e47y48oioe29ws61occakaq6ckhpsmufk0l4liofasv&rid=giphy.gif&ct=g")
          except AttributeError:

            time.sleep(3)
            await message.channel.send("https://c.tenor.com/ZgaGF-2SgCMAAAAd/darth-vader-star-wars.gif")
            time.sleep(3)
            await message.channel.send("Bonk incoming")
            time.sleep(2)
            await message.channel.send("https://media3.giphy.com/media/CGT6ypGJecSk71Wmbw/giphy.gif?cid=ecf05e47x65kafw5roegvfisneoqqene7popjqpb86olwr2p&rid=giphy.gif&ct=g")

        elif random_fool == ".//April//SPOILER_Pan Dan.png":
          time.sleep(5)
          await message.channel.send("<:chinese:400466737151213568> <:chinese:400466737151213568> <:chinese:400466737151213568> <:chinese:400466737151213568> <:chinese:400466737151213568>")
          await message.channel.send("https://c.tenor.com/5a6Ns4KUvlAAAAAC/cute-panda.gif")

        elif random_fool == ".//April//SPOILER_Frog Sage 10 Karma.png":
          time.sleep(5)
          await message.channel.send("<:medicPog:258747552671727616> <:medicPog:258747552671727616> <:medicPog:258747552671727616>")
          await message.channel.send("https://c.tenor.com/mAMHVi4BCUYAAAAC/judges-10.gif")

        elif random_fool == ".//April//SPOILER_Sage Matt Jackpot.png":

          time.sleep(5)
          await message.channel.send("https://c.tenor.com/PIQKtIgW7PQAAAAC/jojo-joseph-jostar.gif")
          await message.channel.send("pogpogpogpogpogpogpogpog")
          await message.channel.send("<:NyanPog:957170859641040907> <:NyanPog:957170859641040907> <:NyanPog:957170859641040907> <:PogOfGreed:721505607781187617> <:PogOfGreed:721505607781187617> <:PogOfGreed:721505607781187617> <:CacoPog:953152686931443773> <:CacoPog:953152686931443773> <:CacoPog:953152686931443773>  ")
          time.sleep(3)

          await message.channel.send("Congratulations!Click the link below to claim your prize!")
          await message.channel.send("<https://shorturl.at/jloMS>")

        await self.bot.process_commands(message)

    elif start is not None:
      if discord_input == start.string:  
        await message.channel.send("**Your overlord has entered the chat**")
        GreenText = "*```yaml\nAll Hail Snek Kyoko```*"
        await message.channel.send(GreenText)
        await message.channel.send(file=discord.File('toshino-kyoko-snake.gif'))
        time.sleep(8)
        await message.channel.send("\n\n\nGoooooood morning Wordle Solvers. Welcome to the first (maybe annual?) Ciul Clal April Fools Meme Gacha Gather. I am your host Gigachad Snek Kyoko. Today you will have the oppotunity to collect 8 rare gacha items never before seen in the wild. You may try your luck with the commands 'april' and 'fools'. If the call has collected all 8 gacha items by 8:00 PM tonight, there will be a special Ciul Clal themed throwback gacha payout. \n Note. Please do not spam the gacha commands. My creator coded me late at night and did not have time for debugging and error handling. Best of luck gamers and may the waifus/husbandos ever be in your favor.")

        time.sleep(8)
        await message.channel.send("https://media4.giphy.com/media/3ohjV4UYiEvJQrBAaY/giphy.gif?cid=ecf05e47kmjx1xmeiqv13ti4l4rdz9xl3phtdwe60wnwyt88&rid=giphy.gif&ct=g")
        time.sleep(8)
        await message.channel.send("https://media3.giphy.com/media/HwmnWJm5PRTDf8Ko8z/giphy.gif?cid=ecf05e47zshaf2rplebg1jzp3cokbve6hvyyc9jcf2uei3ss&rid=giphy.gif&ct=g")

    else: 
      pass




async def setup(bot):
  await bot.add_cog(BotMessages(bot))