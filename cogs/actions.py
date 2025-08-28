from discord.ext import commands
import discord
import random
import requests
from os import getcwd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

class Actions(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def identify_yourself(self, ctx):
    bot_name = self.bot.user.name
    await ctx.send(f"My name is {bot_name}. Onion Haseo")
    await ctx.send("https://i.imgur.com/2vF1I4F.gif")



  @commands.command()
  async def slap(self, ctx, user: discord.Member):
    randomgifs = [
        "https://i.imgur.com/8KfHd8m.gif",
        "https://media3.giphy.com/media/Ur8qw9UJEhNuw/giphy.gif?cid=ecf05e47p42pm7lj9kcaxb0u208emw4j0p6erodp0ng4k3eh&rid=giphy.gif&ct=g",
        "https://i.imgur.com/ZDiDDdc.gif",
        "https://media4.giphy.com/media/xUO4t2gkWBxDi/giphy.gif?cid=ecf05e47aekbuiexi28gfnltl98ka4mej1gmv8rtyxotnwlc&rid=giphy.gif&ct=g",
        "https://media1.giphy.com/media/m6etefcEsTANa/giphy.gif?cid=ecf05e47n6zud179239u2xbsqqr1tf6cf0e50hbezre83q6n&rid=giphy.gif&ct=g",
        "https://media4.giphy.com/media/9U5J7JpaYBr68/giphy.gif?cid=ecf05e47szk9lbpb9c28cskz6ayvvjl8bv1cxe6382gkjjqr&rid=giphy.gif&ct=g",
        "https://media0.giphy.com/media/Zau0yrl17uzdK/giphy.gif?cid=ecf05e47z5mtms641bmud1zl2q8fko6c0uli7k75avvfiwc9&rid=giphy.gif&ct=g",
        "https://media3.giphy.com/media/lX03hULhgCYQ8/giphy.gif?cid=ecf05e47n6zud179239u2xbsqqr1tf6cf0e50hbezre83q6n&rid=giphy.gif&ct=g",
        "https://media1.giphy.com/media/s5zXKfeXaa6ZO/giphy.gif?cid=ecf05e47eec3gdrsr1gxjg8exywvjsxkuddov5t5dy3p9a2n&rid=giphy.gif&ct=g",
        "https://c.tenor.com/qvvKGZhH0ysAAAAC/anime-girl.gif"]

    embed = discord.Embed(
        title = "",
        description = f"{ctx.author.mention} has slapped {user.mention}",
        color = ctx.author.color
    )

    randomgif = random.choice(randomgifs)
    embed.set_image(url = randomgif)
    await ctx.channel.send(embed = embed)


  @commands.command()
  async def bite(self, ctx, user: discord.Member):
    randombite = ["https://media3.giphy.com/media/l0Iy0QdzD3AA6bgIg/giphy.gif?cid=ecf05e475t1bu4m75y5uuyi5broc4ae2n88ytaffyn8nmgnq&rid=giphy.gif&ct=g",
                "https://media3.giphy.com/media/69159EHgBoG08/giphy.gif?cid=ecf05e475t1bu4m75y5uuyi5broc4ae2n88ytaffyn8nmgnq&rid=giphy.gif&ct=g",
                "https://media2.giphy.com/media/CacB5USV4xLUbtcr2q/giphy.gif?cid=ecf05e47jhouvrj8eivbuhlxi0daez0t2kbinmuxjwwbuo6o&rid=giphy.gif&ct=g",                     
"https://loginportal.funnyjunk.com/thumbnails/comments/Nice+i+love+megaabsol+and+just+got+my+hands+on+_e5d6b07dce1878e9442184bfcf0b8aa3.gif",
 "https://c.tenor.com/p9AJkXcmJucAAAAd/nom-tik-tok.gif",  
      "https://c.tenor.com/nkNsOraAx4AAAAAC/anime-bite.gif",
      "https://c.tenor.com/4g4c7CE1jkIAAAAd/eat-eats.gif"
               ]
    embed =discord.Embed(title = "",
                      description =f"{ctx.author.mention} has bitten {user.mention}",
                      color = ctx.author.color)

    randombites = random.choice(randombite)
    embed.set_image(url = randombites)
    await ctx.channel.send(embed = embed)

  @commands.command()
  async def youtubecomment(self, ctx, *, args):
        # Split the input string by spaces to extract avatar, username, and comment
        # Assuming the input format is "<avatar_url> <username> <comment>"
        avatar_var, username_var, comment_var = args.split(maxsplit=2)

        URL = f'https://some-random-api.ml/canvas/youtube-comment?avatar={avatar_var}&username={username_var}&comment={comment_var}'
        await ctx.channel.send(URL)

  @commands.command()
  async def lyrics(self, ctx, title, *, artist):


    await ctx.send(f"Okay, searching for {title} by {artist}...")

    def lyricsapi():
      musicapi = requests.get(f"https://api.lyrics.ovh/v1/{artist}/{title}")
      if  musicapi.status_code == 200:
        songinfo = musicapi.json()
        print(songinfo)
        return(songinfo)
      else:
        musicapi = f"Received bad status code {musicapi.status_code}."
        print(musicapi)

    song_lyrics = lyricsapi()
    lyrics = song_lyrics.get("lyrics")
    lyrics1 = lyrics[:len(lyrics)//2]
    lyrics2 = lyrics[len(lyrics)//2:]
    await ctx.send(f"Here are the lyrics for {title} by {artist}\n")

    await ctx.send(f"Enjoy! \n \n \n{lyrics1}")
    await ctx.send(lyrics2)


  #@commands.command()
  #async def gas(self, ctx, zip_code):
    #time.sleep(1)
    #await ctx.send("Searching for ~hot singles~ gas prices in your area...")

    #self.chrome_options = Options()
    #self.chrome_options.add_argument("--disable-extensions")
    #self.chrome_options.add_argument("--disable-gpu")
    #self.chrome_options.add_argument('--no-sandbox')
    #self.chrome_options.add_argument('--disable-dev-shm-usage')
    #self.chrome_options.add_argument('--headless')
    #self.driver = webdriver.Chrome(options=self.chrome_options)

    #self.driver.get(f"https://www.gasbuddy.com/home?search={zip_code}&fuel=1&maxAge=8&method=all")

    #location_xpath = self.driver.find_elements(By.XPATH, './/h3[@class="header__header3___1b1oq header__header___1zII0 header__midnight___1tdCQ header__snug___lRSNK StationDisplay-module__stationNameHeader___1A2q8"]')
    #for location_names in location_xpath:
      #location_names1= location_names.get_attribute('innerText')
      #print(location_names1)




  @commands.command()
  async def gas(self, ctx, zip_code):
    time.sleep(1)
    await ctx.send("Searching for ~~hot singles~~ gas prices in your area...")

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}

    URL = f"https://www.gasbuddy.com/home?search={zip_code}&fuel=1&maxAge=8&method=all"

    gas_page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(gas_page.content, 'html.parser')


    location_names = soup.find_all('h3', class_='header__header3___1b1oq header__header___1zII0 header__midnight___1tdCQ header__snug___lRSNK StationDisplay-module__stationNameHeader___1A2q8')
    location_names_list = [location.get_text(strip=True) for location in location_names]
    print(location_names_list)

    address_names = soup.find_all(class_='StationDisplay-module__address___2_c7v')
    address_names_list = [address.get_text(strip=True) for address in address_names]
    print(address_names_list)

    prices = soup.find_all('span', class_='text__xl___2MXGo text__left___1iOw3 StationDisplayPrice-module__price___3rARL')
    prices_list = [price.get_text(strip = True) for price in prices]
    print(prices_list)


    stats_name = soup.find('h2', class_='header__header2___1p5Ig header__header___1zII0 PriceTrends-module__regionHeader___pULcn')
    if stats_name:
      current_stats_name = stats_name.get_text(strip=True)
    else:
      current_stats_name = "Unknown Region"
    print(current_stats_name)

    lowest_avg = soup.find_all('span', class_='text__lg___1S7OO text__bold___1C6Z_ text__left___1iOw3 PriceTrends-module__priceHeader___fB9X9')
    current_lowest_avg = [stat.get_text(strip=True) for stat in lowest_avg]


    current_lowest = current_lowest_avg[0]
    current_average = current_lowest_avg[1]

    print(current_lowest)
    print(current_average)

    await ctx.send(f"{len(location_names_list)} locations found")   
    time.sleep(1)
    for i in range(len(location_names_list)):
      await ctx.send(f"{i+1}. \n Station Brand: {location_names_list[i]}, Address: {address_names_list[i]}, Price: **{prices_list[i]}**")
      time.sleep(1)
    time.sleep(1)
    await ctx.send(f"Current {current_stats_name}: \n\nLowest Price: **{current_lowest}** \n\n Average Price: **{current_average}**")



  @commands.command()
  async def victory(self, ctx):
    time.sleep(3)
    memories_list = ["https://cdn.discordapp.com/attachments/115908075143168002/115930341448876039/309528_271349949541873_5223004_n.jpg", "https://media.discordapp.net/attachments/115908075143168002/116018254748581888/Capture2.JPG", "https://cdn.discordapp.com/attachments/115908075143168002/117865749015429123/383498_458366140922707_496343925_n.jpg", "https://media.discordapp.net/attachments/115908075143168002/118353857389658116/IMG_1448288158716236900641.jpg?width=254&height=452", "https://media.discordapp.net/attachments/115908075143168002/118894885230084096/q7qCrxA.jpg", "https://media.discordapp.net/attachments/115908075143168002/118895434382049283/1439883158486.jpg?width=339&height=452", "https://media.discordapp.net/attachments/115908075143168002/118898833622040577/Joseph.gif", "https://media.discordapp.net/attachments/115908075143168002/118903202413412353/IMG_20130901_163922_815.jpg?width=254&height=452", "https://media.discordapp.net/attachments/115908075143168002/118904160245514241/41a1gz1g21L._SL500_AA280_.jpg", "https://media.discordapp.net/attachments/115908075143168002/177376490508386305/1462079311760.png", "https://media.discordapp.net/attachments/115908075143168002/177491256241291265/20160504_114623.jpg?width=254&height=452", "https://media.discordapp.net/attachments/120291502592098304/177542885275598850/13177136_1703510633238043_69623708732713682_n.png?width=378&height=452", "https://media.discordapp.net/attachments/155598979755671553/177689047097933825/Shinoa_Hiragi_4.jpg?width=657&height=452", "https://media.discordapp.net/attachments/120291502592098304/177828533505097729/13129128_229521757418333_1203523202_n.png?width=452&height=452", "https://media.discordapp.net/attachments/115908075143168002/177883814691864577/Meowning.jpg?width=804&height=452", "https://media.discordapp.net/attachments/115908075143168002/178223731703939073/a756187f-3a0b-42a4-90b4-4d364560af9a2107918101.jpg?width=254&height=452", "https://cdn.discordapp.com/attachments/155598979755671553/178744150550642690/Honkers_Emoji_Face.jpg", "https://media.discordapp.net/attachments/155598979755671553/178773712592568321/1462692098098.jpg", "https://cdn.discordapp.com/attachments/155598979755671553/178989436271460353/1462724792431.jpg", "https://cdn.discordapp.com/attachments/115908075143168002/179739501185335297/unknown.png", "https://media.discordapp.net/attachments/155598979755671553/180507949179994114/1457761694391.jpg?width=200&height=452", "https://cdn.discordapp.com/attachments/115908075143168002/248471862168780800/20161116_083625-1.jpg", "https://media.discordapp.net/attachments/115908075143168002/257972009106014208/tumblr_oi2hzfkesf1tkyvlbo1_500.png", "https://media.discordapp.net/attachments/115908075143168002/273985929247588352/20170125_182202.jpg?width=339&height=452", "https://media.discordapp.net/attachments/115908075143168002/276763978003251200/unknown.png", "https://media.discordapp.net/attachments/115908075143168002/283786034615943168/image.jpg?width=602&height=452", "https://media.discordapp.net/attachments/115908075143168002/299247967909707776/unknown.png", "https://cdn.discordapp.com/attachments/115908075143168002/300502358851584020/Screenshot_20170408-222820.png", "https://media.discordapp.net/attachments/115908075143168002/301468805627117568/20170411_142432.jpg?width=252&height=452", "https://cdn.discordapp.com/attachments/115908075143168002/304722273670135809/18090572_1443002182416738_2010546348_o.jpg", "https://cdn.discordapp.com/attachments/115908075143168002/304810872059068417/0642112001419278232_filepicker.png", "https://cdn.discordapp.com/attachments/115908075143168002/306577393814994954/candies1.png", "https://cdn.discordapp.com/attachments/115908075143168002/307771662923726849/IMG_20170428_121303523.jpg", "https://media.discordapp.net/attachments/115908075143168002/308765842693423125/unknown.png", "https://media.discordapp.net/attachments/115908075143168002/311660563984023553/2016-03-10_66483602.JPG?width=804&height=452", "https://media.discordapp.net/attachments/115908075143168002/311975474563776512/Snapchat-1015540537.jpg?width=254&height=452", "https://media.discordapp.net/attachments/115908075143168002/312075801635848193/Screenshot_5215.png?width=804&height=452", "https://media.discordapp.net/attachments/115908075143168002/314481815253549056/image.jpg?width=339&height=452", "https://media.discordapp.net/attachments/115908075143168002/316609992931147777/image.jpg?width=339&height=452", "https://cdn.discordapp.com/attachments/115908075143168002/318513899915968512/image.jpg", "https://cdn.discordapp.com/attachments/115908075143168002/318976243347488768/420084_612268225458689_1101111176_n.png", "https://media.discordapp.net/attachments/115908075143168002/318980046704607233/39e.jpg", "https://media.discordapp.net/attachments/115908075143168002/322179933176594433/20170607_180752.jpg?width=602&height=452", "https://media.discordapp.net/attachments/115908075143168002/322833334688284692/unknown.png?width=519&height=452", "https://cdn.discordapp.com/attachments/156066774692003850/325794959091564544/1490914369232.gif", "https://cdn.discordapp.com/attachments/115908075143168002/326179691964792832/gXBlywbpqra7pcAAAAAElFTkSuQmCC.png", "https://media.discordapp.net/attachments/115908075143168002/326181159157628929/IcGy0AAAAASUVORK5CYII.png?width=870&height=435", "https://cdn.discordapp.com/attachments/115908075143168002/329411280450486272/Snapchat-1199028793.jpg", "https://media.discordapp.net/attachments/115908075143168002/335915929856901122/IMG_20170715_152117.jpg?width=339&height=452", "https://media.discordapp.net/attachments/115908075143168002/477348288039747594/38814094_828316800672037_1971162153733849088_n.png?width=809&height=452", "https://media.discordapp.net/attachments/115908075143168002/478844080986783765/C94-Cosplay-Extra-1-26.jpg?width=339&height=452", "https://cdn.discordapp.com/attachments/115908075143168002/480875776820903949/655E8D45-BE38-4D58-AA8B-2B3285003DED.jpg", "https://media.discordapp.net/attachments/115908075143168002/480875780973264898/06207C17-9F4B-472F-AA2A-9C41FFE0A39F.jpg?width=339&height=452", "https://media.discordapp.net/attachments/115908075143168002/482375231084691457/unknown.png", "https://media.discordapp.net/attachments/115908075143168002/489598449118085136/unknown.png", "https://media.discordapp.net/attachments/115908075143168002/501860937024667668/12705607_10206721662934301_543742203573935271_n.jpg?width=804&height=452", "https://media.discordapp.net/attachments/115908075143168002/508666293814296589/image0.jpg?width=432&height=452", "https://media.discordapp.net/attachments/115908075143168002/513044437325053978/image1.jpg?width=339&height=452", "https://cdn.discordapp.com/attachments/115908075143168002/544418372771774464/SPOILER_flat750x1000075t.u2.jpg", "https://media.discordapp.net/attachments/115908075143168002/548408972491751444/20190222_003518.jpg?width=254&height=451", "https://tenor.com/view/angry-fist-arthur-gif-5794225", "https://media.discordapp.net/attachments/115908075143168002/505639051337138176/20181025_141005.jpg?width=219&height=452", "https://cdn.discordapp.com/attachments/115908075143168002/713582910677975087/81INGqNlqGL.png", "https://media.discordapp.net/attachments/115908075143168002/710328989905846383/carbs_3.jpg?width=339&height=452", "https://media.discordapp.net/attachments/115908075143168002/710289785989759022/unknown.png", "https://media.discordapp.net/attachments/115908075143168002/708752046748205166/unknown.png?width=780&height=452", "https://media.discordapp.net/attachments/115908075143168002/701319771035271248/unknown.png?width=804&height=452", "https://media.discordapp.net/attachments/115908075143168002/701318376739438652/unknown.png?width=804&height=452", "https://media.discordapp.net/attachments/115908075143168002/701270593634435122/latest.png", "https://media.discordapp.net/attachments/115908075143168002/698281623820435576/lol.JPG?width=870&height=425", "https://media.discordapp.net/attachments/115908075143168002/697607427906076742/image0.png?width=804&height=452", "https://cdn.discordapp.com/attachments/115908075143168002/695121893312823376/TCC_MHMP.png", "https://media.discordapp.net/attachments/115908075143168002/690404576192495636/ETgHVKQXsAYyG1M.png?width=452&height=452", "https://media.discordapp.net/attachments/115908075143168002/690351942316327302/unknown.png?width=436&height=452", "https://media.discordapp.net/attachments/115908075143168002/677418064639426560/yXXUWLvh.jpg?width=452&height=452", "https://media.discordapp.net/attachments/115908075143168002/675211252212957194/ilived.jpg?width=452&height=452", "https://media.discordapp.net/attachments/115908075143168002/671288412413624320/FB_IMG_1580118235188.jpg?width=448&height=452", "https://media.discordapp.net/attachments/115908075143168002/670468395594022942/20200124_191956.jpg?width=214&height=452", "https://media.discordapp.net/attachments/115908075143168002/663219130723467264/unknown.png?width=603&height=452", "https://media.discordapp.net/attachments/115908075143168002/661409486074019911/unknown.png", "https://media.discordapp.net/attachments/115908075143168002/645480216726208532/20191116_193410.jpg?width=339&height=452", "https://media.discordapp.net/attachments/115908075143168002/637500051081527319/20191025_191803.jpg?width=870&height=412", "https://media.discordapp.net/attachments/115908075143168002/630495616371261460/image0.jpg?width=602&height=452", "https://media.discordapp.net/attachments/115908075143168002/628026372069130260/image0.jpg?width=602&height=452", "https://media.discordapp.net/attachments/115908075143168002/625459243658641419/image2.jpg?width=602&height=452", "https://media.discordapp.net/attachments/115908075143168002/625459243113512961/image0.jpg?width=220&height=452", "https://media.discordapp.net/attachments/115908075143168002/623344451133243422/20190916_192810.jpg?width=433&height=452", "https://media.discordapp.net/attachments/115908075143168002/623300537567150110/20190916_163212.jpg", "https://cdn.discordapp.com/attachments/115908075143168002/591063301086248973/SPOILER_1560990544663.png", "https://media.discordapp.net/attachments/115908075143168002/583783792955752464/47e90w2jde131.png?width=479&height=452", "https://media.discordapp.net/attachments/115908075143168002/577916020124287012/IMG_20190502_195717_108.jpg?width=452&height=452", "https://media.discordapp.net/attachments/115908075143168002/577905744746250273/FB_IMG_1557847153355.jpg?width=770&height=452", "https://media.discordapp.net/attachments/115908075143168002/576485757276127262/Snapchat-1772734517.jpg?width=235&height=452", "https://media.discordapp.net/attachments/115908075143168002/576482300175581215/image0.png?width=254&height=452", "https://media.discordapp.net/attachments/115908075143168002/574443289306988554/Screenshot_20190410-215059_Slow_motion_editor.jpg?width=214&height=452", "https://media.discordapp.net/attachments/115908075143168002/571578464772161536/unknown.png?width=602&height=452", "https://media.discordapp.net/attachments/115908075143168002/571015153123065856/20190425_124957.jpg?width=337&height=452", "https://66.media.tumblr.com/fe8d1be1ccfb88482d5e2fdc9b8b3bdf/tumblr_pq16tcY17G1vgdf7so1_1280.jpg", "https://media.discordapp.net/attachments/115908075143168002/566102390265348097/unknown.png?width=804&height=452", "https://media.discordapp.net/attachments/115908075143168002/565405798629376001/FB_IMG_1554873638530.jpg?width=452&height=452", "https://cdn.discordapp.com/attachments/115908075143168002/562371284294434826/games.gif", "https://cdn.discordapp.com/attachments/115908075143168002/556666789086625862/tumblr_pmm0ep4Gsv1u5q5o1o1_1280.jpg", "https://media.discordapp.net/attachments/115908075143168002/546246519041294337/20190216_012801.jpg?width=337&height=452", "https://media.discordapp.net/attachments/115908075143168002/544030089055305728/20190209220934_1.jpg?width=804&height=452", "https://media.discordapp.net/attachments/115908075143168002/544006684033679363/original_result.png?width=452&height=452", "https://media.discordapp.net/attachments/115908075143168002/536426846095409177/tumblr_nvionl2udH1uqab09o1_500.jpg?width=452&height=452", "https://media.discordapp.net/attachments/115908075143168002/530232846695006208/unknown.png", "https://media.discordapp.net/attachments/115908075143168002/526139671588372481/image0.jpg", "https://media.discordapp.net/attachments/115908075143168002/518097483101110290/image0.jpg?width=602&height=452", "https://media.discordapp.net/attachments/922005982819778570/959635253327167518/E8BAC828-9023-4431-B86F-475D70ECE6C5.jpg?width=339&height=452", "https://cdn.discordapp.com/attachments/922005982819778570/959635253578842182/AF7B78FB-80CA-407D-B86D-E47D29DE0726.jpg", "https://cdn.discordapp.com/attachments/922005982819778570/959635319198732348/5667FE15-345F-4217-A982-AE545797A2E8.jpg", "https://cdn.discordapp.com/attachments/922005982819778570/959635319454568509/0C9EB111-4E08-4227-A785-C4DEC7E97186.jpg", "https://cdn.discordapp.com/attachments/922005982819778570/959635842543026186/189EDA07-D0F7-47E9-8E30-6720AF59837F.jpg", "https://cdn.discordapp.com/attachments/922005982819778570/959635844292038686/553BC8EC-B280-4AF4-9DFE-8C70EDED4E62.jpg", "https://media.discordapp.net/attachments/922005982819778570/959635855616647208/899BF3B7-07DF-4B9F-A377-A62AFF6FC357.png?width=254&height=452", "https://cdn.discordapp.com/attachments/922005982819778570/959636015314792518/46F74C27-7C10-42DC-ABF1-4A156B72314C.jpg", "https://cdn.discordapp.com/attachments/922005982819778570/959636031517384764/43683BE4-1EC8-48A5-910C-D8C1A1C5F0A7.jpg", "https://cdn.discordapp.com/attachments/922005982819778570/959636035279654932/3ED391CB-1685-451C-B645-EB0612B2C30E.jpg", "https://cdn.discordapp.com/attachments/922005982819778570/959636043500507147/B2A4DBDE-7896-409F-BA0F-E3CE4F6013CF.jpg", "https://cdn.discordapp.com/attachments/922005982819778570/959636044188368996/E511FD5A-C8B2-4EB3-8FB5-306A5CE5FD7F.jpg", "https://cdn.discordapp.com/attachments/922005982819778570/959635909081456690/37157979-2A17-4932-AB14-6C885B0FB969.jpg"]
    select_memory = random.choice(memories_list)
    embed = discord.Embed(title = "Tripping Down Memory Lane :notes: ", description = " <:sip:820505650337284147> Happy April Fools Day! <:sip:820505650337284147> ", color =ctx.author.color)
    embed.set_image(url = select_memory)
    await ctx.channel.send(embed = embed)

  intents = discord.Intents.default()
  intents.reactions = True
  intents.members = True

  @commands.command(pass_context=True)
  async def reaction_role_msg(self, ctx):
    channel = self.bot.get_channel(922005982819778570)
    msg = "React to the emojis below for your role !"
    message_capture = await channel.send(msg)
    reactions = ['🤠', '🔥']
    for emoji in reactions: 
        await message_capture.add_reaction(emoji)



async def setup(bot):
  await bot.add_cog(Actions(bot))