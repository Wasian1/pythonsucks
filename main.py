import asyncio
from threading import Thread
import sys
import os
from dotenv import load_dotenv
import datetime
from typing import cast

import discord
from discord.ext import commands, tasks
from zoneinfo import ZoneInfo
import tzdata
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import wavelink
import logging
import aiohttp

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "settings.env"))

LAVALINK_PASSWORD = os.getenv("LAVALINK_PASSWORD")

target_message_id = 1068981877425315982

def format_duration(duration: int) -> str:
    """Convert milliseconds to MM:SS or HH:MM:SS format."""
    seconds = duration // 1000
    h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
    if h > 0:
        return f"{h:02}:{m:02}:{s:02}"
    return f"{m:02}:{s:02}"

class Bot(commands.Bot):
    def __init__(self) -> None:
        intents: discord.Intents = discord.Intents.all()
        intents.message_content = True
        def get_prefix(bot, message):

          prefixes = ['$', '!', ':^)']

          if not message.guild:
            return ':^'

          return commands.when_mentioned_or(*prefixes)(bot, message)
        self.initial_extensions = ['cogs.actions', 'cogs.games', 'cogs.bot_messages', 'cogs.music_player']

        # Initialize the Spotify client here
        self.spotify_client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                                                                          client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'))
        self.spotify = spotipy.Spotify(client_credentials_manager=self.spotify_client_credentials_manager)

        
        

        discord.utils.setup_logging(level=logging.INFO)
        super().__init__(command_prefix=get_prefix,description = 'Hebi Kyoko が　来た！！！', intents=intents)

    async def setup_hook(self) -> None:
      # Load extensions
      for extension in self.initial_extensions:
        try:
            await self.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}: {e}')

      # Start birthday task
      birthday_test_1.start()

      # Start Lavalink connection in background
      await self.connect_lavalink()
    async def wait_for_lavalink():
      url = "http://lavalink:2333"
      while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as resp:
                    if resp.status == 401:  # Lavalink responds with 401 when ready
                        print("Lavalink is ready!")
                        return
        except Exception:
            pass
        print("Waiting for Lavalink...")
        await asyncio.sleep(2)

    async def connect_lavalink(self):
      while True:
        try:
            print("Trying to connect Lavalink...")
            nodes = [wavelink.Node(uri="http://lavalink:2333", password="Doughnuts12")]
            await wavelink.Pool.connect(nodes=nodes, client=self, cache_capacity=None)
            print("Lavalink connected successfully!")
            return
        except Exception as e:
            print(f"Failed to connect Lavalink: {e}")
            await asyncio.sleep(5)

    async def on_ready(self) -> None:
        logging.info(f"Logged in: {self.user} | {self.user.id}")

    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
        logging.info(f"Wavelink Node connected: {payload.node!r} | Resumed: {payload.resumed}")

    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload) -> None:
        player: wavelink.Player | None = payload.player
        if not player:
            # Handle edge cases...
            return

        original: wavelink.Playable | None = payload.original
        track: wavelink.Playable = payload.track

        embed: discord.Embed = discord.Embed(title="Now Playing")
        embed.description = f"**{track.title}** by `{track.author}`"

        if track.artwork:
            embed.set_image(url=track.artwork)

        if original and original.recommended:
            embed.description += f"\n\n`This track was recommended via {track.source}`"

        if track.album.name:
            embed.add_field(name="Album", value=track.album.name)

        await player.home.send(embed=embed)


bot: Bot = Bot()



@bot.command(name='restart')
async def restart(ctx):
    await ctx.send("Restarting bot...")
    await bot.close()  # Gracefully closes connections
    # Docker will restart the container if restart: always is set

@bot.command()
async def join(ctx, *, channel_name: str = None):
    """Kyoko will join you in voice chat"""
  # Check if a channel name was provided
    if channel_name is None:
        await ctx.send("Please specify a voice channel to join.")
        return

    # Get the voice channel by name
    channel = discord.utils.get(ctx.guild.voice_channels, name=channel_name)

    # Check if the channel exists
    if channel is None:
        await ctx.send(f"Voice channel '{channel_name}' not found.")
        return

    # Connect to the voice channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client is not None:
        await voice_client.move_to(channel)
    else:
        await channel.connect()

    await ctx.send(f"Joined {channel.name}")

@bot.command()
async def playitloud(ctx: commands.Context, *, query: str) -> None:
    """Play a song with the given query."""
    if not ctx.guild:
        return

    player: wavelink.Player
    player = cast(wavelink.Player, ctx.voice_client)  # type: ignore
    

    if not player:
        try:
            player = await ctx.author.voice.channel.connect(cls=wavelink.Player)  # type: ignore
        except AttributeError:
            await ctx.send("Please join a voice channel first before using this command.")
            return
        except discord.ClientException:
            await ctx.send("I was unable to join this voice channel. Please try again.")
            return

    # Turn on AutoPlay to enabled mode.
    # enabled = AutoPlay will play songs for us and fetch recommendations...
    # partial = AutoPlay will play songs for us, but WILL NOT fetch recommendations...
    # disabled = AutoPlay will do nothing...
    player.autoplay = wavelink.AutoPlayMode.enabled

    # Lock the player to this channel...
    if not hasattr(player, "home"):
        player.home = ctx.channel
    elif player.home != ctx.channel:
        await ctx.send(f"You can only play songs in {player.home.mention}, as the player has already started there.")
        return

    # This will handle fetching Tracks and Playlists...
    # Seed the doc strings for more information on this method...
    # If spotify is enabled via LavaSrc, this will automatically fetch Spotify tracks if you pass a URL...
    # Defaults to YouTube for non URL based queries...
    tracks: wavelink.Search = await wavelink.Playable.search(query)
    if not tracks:
        await ctx.send(f"{ctx.author.mention} - Could not find any tracks with that query. Please try again.")
        return

    if isinstance(tracks, wavelink.Playlist):
        # tracks is a playlist...
        added: int = await player.queue.put_wait(tracks)
        await ctx.send(f"Added the playlist **`{tracks.name}`** ({added} songs) to the queue.")
    else:
        track: wavelink.Playable = tracks[0]
        await player.queue.put_wait(track)
        embed = discord.Embed(
                              title="🎶 Track Added to Queue",
                              description=f"**{track.title}** by **{track.author}**",
                              color=discord.Color.blurple()
                              )
        embed.set_footer(text=f"Added by {ctx.author.display_name} • Duration: {format_duration(track.length)}")

        await ctx.send(embed=embed)

    if not player.playing:
        # Play now since we aren't playing anything...
        await player.play(player.queue.get(), volume=30)

    # Optionally delete the invokers message...
    try:
        await ctx.message.delete()
    except discord.HTTPException:
        pass


@bot.command()
async def remote_play(ctx, target_channel_name: str, *, query: str):
  
  if not ctx.guild:
    return

  # Check if the target channel name is enclosed in double quotes
  if target_channel_name.startswith('"') and target_channel_name.endswith('"'):
      target_channel_name = target_channel_name[1:-1]  # Remove the quotes

  player: wavelink.Player
  player = cast(wavelink.Player, ctx.voice_client)  # type: ignore

  # Get the target voice channel by name
  target_channel = discord.utils.get(ctx.guild.voice_channels, name=target_channel_name)

  if not target_channel:
    await ctx.send(f"Voice channel '{target_channel_name}' not found.")
    return

  if not player:
    try:
        player = await target_channel.connect(cls=wavelink.Player)  # type: ignore
    except AttributeError:
        await ctx.send("Please join a voice channel first before using this command.")
        return
    except discord.ClientException:
        await ctx.send("I was unable to join this voice channel. Please try again.")
        return

  # Turn on AutoPlay to enabled mode.
  # enabled = AutoPlay will play songs for us and fetch recommendations...
  # partial = AutoPlay will play songs for us, but WILL NOT fetch recommendations...
  # disabled = AutoPlay will do nothing...
  player.autoplay = wavelink.AutoPlayMode.enabled

  # Lock the player to this channel...
  if not hasattr(player, "home"):
    player.home = ctx.channel
  elif player.home != ctx.channel:
    await ctx.send(f"You can only play songs in {player.home.mention}, as the player has already started there.")
    return

  # This will handle fetching Tracks and Playlists...
  # Seed the doc strings for more information on this method...
  # If spotify is enabled via LavaSrc, this will automatically fetch Spotify tracks if you pass a URL...
  # Defaults to YouTube for non URL based queries...
  tracks: wavelink.Search = await wavelink.Playable.search(query)
  if not tracks:
    await ctx.send(f"{ctx.author.mention} - Could not find any tracks with that query. Please try again.")
    return

  if isinstance(tracks, wavelink.Playlist):
    # tracks is a playlist...
    added: int = await player.queue.put_wait(tracks)
    await ctx.send(f"Added the playlist **`{tracks.name}`** ({added} songs) to the queue.")
  else:
    track: wavelink.Playable = tracks[0]
    await player.queue.put_wait(track)
    await ctx.send(f"Added **`{track}`** to the queue.")

  if not player.playing:
    # Play now since we aren't playing anything...
    await player.play(player.queue.get(), volume=30)

  # Optionally delete the invokers message...
  try:
    await ctx.message.delete()
  except discord.HTTPException:
    pass

async def delete(ctx: commands.Context, query) -> None:
  """Deletes a song from the queue by queue index"""
  player: wavelink.Player
  player = cast(wavelink.Player, ctx.voice_client)
  query_index = int(query)  # Convert query to an integer
  if query_index == 1:
    query_index = 0
  removed_item = player.queue[query_index]
  player.queue.remove(removed_item)


@bot.command()
async def queuecount(ctx: commands.Context) -> None:
  """"Shows the current queue count"""""
  player: wavelink.Player
  player = cast(wavelink.Player, ctx.voice_client)
  queue_len = str(len(player.queue))
  if queue_len == "0":
    await ctx.send ("No additional songs currently in queue!")
  else:
    await ctx.send (queue_len)

@bot.command()
async def viewqueue(ctx: commands.Context) -> None:
  """"Shows songs in queue"""""
  player: wavelink.Player
  player = cast(wavelink.Player, ctx.voice_client)
  for item in player.queue:
    
    await ctx.send (str(item))


@bot.command()
async def skip(ctx: commands.Context) -> None:
    """Skip the current song."""
    player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
    if not player:
        return

    await player.skip(force=True)
    await ctx.message.add_reaction("\u2705")


@bot.command()
async def nightcore(ctx: commands.Context) -> None:
    """Set the filter to a nightcore style."""
    player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
    if not player:
        return

    filters: wavelink.Filters = player.filters
    filters.timescale.set(pitch=1.2, speed=1.2, rate=1)
    await player.set_filters(filters)

    await ctx.message.add_reaction("\u2705")


@bot.command(name="toggle", aliases=["pause", "resume"])
async def pause_resume(ctx: commands.Context) -> None:
    """Pause or Resume the Player depending on its current state."""
    player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
    if not player:
        return

    await player.pause(not player.paused)
    await ctx.message.add_reaction("\u2705")


@bot.command()
async def volume(ctx: commands.Context, value: int) -> None:
    """Change the volume of the player."""
    player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
    if not player:
        return

    await player.set_volume(value)
    await ctx.message.add_reaction("\u2705")


@bot.command(aliases=["dc"])
async def disconnect(ctx: commands.Context) -> None:
    """Disconnect the Player."""
    player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
    if not player:
        return

    await player.disconnect()
    await ctx.message.add_reaction("\u2705")


  #for guild in bot.guilds:
    #for channel in guild.text_channels :
      #if str(channel) == "dev-workshop" :
        #await channel.send("**Your overlord has entered the chat**")
        #GreenText = "*```yaml\nAll Hail Snek Kyoko```*"
        #await channel.send(GreenText)
        #await channel.send(file=discord.File('toshino-kyoko-snake.gif'))

  #await bot.change_presence(activity=discord.Game(name = 'Snek Kyoko reporting for duty', type =1, url='https://www.twitch.tv/pandanpaisen'))
  #print(f'Sucessfully logged in and booted...!')

@bot.event
async def on_wavelink_track_end(payload: wavelink.TrackEndEventPayload):
    print(f"Track ended: {payload.track.title}")

@bot.event
async def on_wavelink_track_exception(payload: wavelink.TrackExceptionEventPayload):
    print(f"Track error: {payload.track.title}, Exception: {payload.exception}")

@bot.event
async def on_wavelink_track_stuck(payload: wavelink.TrackStuckEventPayload):
    print(f"Track stuck: {payload.track.title}, Threshold: {payload.threshold_ms}ms")

@bot.command()
async def redonodes(ctx: commands.Context) -> None:
  """Change the volume of the player."""
  guild = ctx.guild
  player = wavelink.NodePool.get_node().get_player(guild)
  await wavelink.NodePool.get_node().disconnect()
  await wavelink.NodePool.connect(client=bot, nodes= [wavelink.Node(uri=f"ws://lava-v4.ajieblogs.eu.org:80", password="https://dsc.gg/ajidevserver")])
  print("Is playing:", player.is_playing)
  print("Is connected:", player.is_connected)
  print("Current track:", player.current)
  print("Queue size:", player.queue.count)

@bot.event
async def on_raw_reaction_add(payload):


  if payload.message_id != target_message_id:
    return

  guild = bot.get_guild(payload.guild_id)

  if payload.emoji.name == '🔥':
    role = discord.utils.get(guild.roles, name = 'Arizona')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '🌞':
    role = discord.utils.get(guild.roles, name = 'Tucson')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '⛏️':
    role = discord.utils.get(guild.roles, name = 'miner')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '<:Bojji:1030520849784123544>':
    role = discord.utils.get(guild.roles, name = 'big child')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '🍀':
    role = discord.utils.get(guild.roles, name = 'ciul')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '<:andyru:262474347397120000>':
    role = discord.utils.get(guild.roles, name = 'boothter')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '🛗':
    role = discord.utils.get(guild.roles, name = 'yogurt gang')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '🌎':
    role = discord.utils.get(guild.roles, name = 'geoparty')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '<:shinoashock:978776558129012766>':
    role = discord.utils.get(guild.roles, name = 'damn connies')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '<:COPIUM:987016365191856229>':
    role = discord.utils.get(guild.roles, name = 'Mudae-bot’s sweet sixteen')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '<:hypers:1063164818112131182>':
    role = discord.utils.get(guild.roles, name = 'weeb music')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '<:unknown:979244464830836736>':
    role = discord.utils.get(guild.roles, name = 'partygoers')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '<:villager:1052970632188534974>':
    role = discord.utils.get(guild.roles, name = 'time traveler')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '♋':
    role = discord.utils.get(guild.roles, name = 'challenjour')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '<:zach:244228213172076544>':
    role = discord.utils.get(guild.roles, name = 'disgoostan')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '🍞':
    role = discord.utils.get(guild.roles, name = 'carbvengers')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '🌁':
    role = discord.utils.get(guild.roles, name = 'California')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '🇺🇳':
    role = discord.utils.get(guild.roles, name = 'International')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '🎰':
    role = discord.utils.get(guild.roles, name = 'Nevada')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '🍭':
    role = discord.utils.get(guild.roles, name = 'sweeties!')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '<:snake_salute:1009501296727961630>':
    role = discord.utils.get(guild.roles, name = 'Military')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '🌇':
    role = discord.utils.get(guild.roles, name = 'Phoenix')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '🤠':
    role = discord.utils.get(guild.roles, name = 'Texas')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '<:hyperthink:312732126543872001>':
    role = discord.utils.get(guild.roles, name = 'South Dakota')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '🍊':
    role = discord.utils.get(guild.roles, name = 'Florida')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '👹':
    role = discord.utils.get(guild.roles, name = '9th Circle, Hell')
    await payload.member.add_roles(role)

  elif payload.emoji.name == '<:eli:230168985826492426>':
    role = discord.utils.get(guild.roles, name = 'picking up girls')
    await payload.member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):

  if payload.message_id != target_message_id:
    return

  guild = bot.get_guild(payload.guild_id)
  member = guild.get_member(payload.user_id)


  if payload.emoji.name == '🔥':
    role = discord.utils.get(guild.roles, name = 'Arizona')
    await member.remove_roles(role)

  elif payload.emoji.name == '🌞':
    role = discord.utils.get(guild.roles, name = 'Tucson')
    await member.remove_roles(role)

  elif payload.emoji.name == '⛏️':
    role = discord.utils.get(guild.roles, name = 'miner')
    await member.remove_roles(role)

  elif payload.emoji.name == '🍀':
    role = discord.utils.get(guild.roles, name = 'ciul')
    await member.remove_roles(role)

  elif payload.emoji.name == '<:Bojji:1030520849784123544>':
    role = discord.utils.get(guild.roles, name = 'big child')
    await member.remove_roles(role)

  elif payload.emoji.name == '<:andyru:262474347397120000>':
    role = discord.utils.get(guild.roles, name = 'boothter')
    await member.remove_roles(role)

  elif payload.emoji.name == '🛗':
    role = discord.utils.get(guild.roles, name = 'yogurt gang')
    await member.remove_roles(role)

  elif payload.emoji.name == '🌎':
    role = discord.utils.get(guild.roles, name = 'geoparty')
    await member.remove_roles(role)

  elif payload.emoji.name == '<:shinoashock:978776558129012766>':
    role = discord.utils.get(guild.roles, name = 'damn connies')
    await member.remove_roles(role)

  elif payload.emoji.name == '<:COPIUM:987016365191856229>':
    role = discord.utils.get(guild.roles, name = 'Mudae-bot’s sweet sixteen')
    await member.remove_roles(role)

  elif payload.emoji.name == '<:hypers:1063164818112131182>':
    role = discord.utils.get(guild.roles, name = 'weeb music')
    await member.remove_roles(role)

  elif payload.emoji.name == '<:unknown:979244464830836736>':
    role = discord.utils.get(guild.roles, name = 'partygoers')
    await member.remove_roles(role)

  elif payload.emoji.name == '<:villager:1052970632188534974>':
    role = discord.utils.get(guild.roles, name = 'time traveler')
    await member.remove_roles(role)

  elif payload.emoji.name == '♋':
    role = discord.utils.get(guild.roles, name = 'challenjour')
    await member.remove_roles(role)

  elif payload.emoji.name == '<:zach:244228213172076544>':
    role = discord.utils.get(guild.roles, name = 'disgoostan')
    await member.remove_roles(role)

  elif payload.emoji.name == '🍞':
    role = discord.utils.get(guild.roles, name = 'carbvengers')
    await member.remove_roles(role)

  elif payload.emoji.name == '🌁':
    role = discord.utils.get(guild.roles, name = 'California')
    await member.remove_roles(role)

  elif payload.emoji.name == '🇺🇳':
    role = discord.utils.get(guild.roles, name = 'International')
    await member.remove_roles(role)

  elif payload.emoji.name == '🎰':
    role = discord.utils.get(guild.roles, name = 'Nevada')
    await member.remove_roles(role)

  elif payload.emoji.name == '🍭':
    role = discord.utils.get(guild.roles, name = 'sweeties!')
    await member.remove_roles(role)

  elif payload.emoji.name == '<:snake_salute:1009501296727961630>':
    role = discord.utils.get(guild.roles, name = 'Military')
    await member.remove_roles(role)

  elif payload.emoji.name == '🌇':
    role = discord.utils.get(guild.roles, name = 'Phoenix')
    await member.remove_roles(role)

  elif payload.emoji.name == '🤠':
    role = discord.utils.get(guild.roles, name = 'Texas')
    await member.remove_roles(role)

  elif payload.emoji.name == '<:hyperthink:312732126543872001>':
    role = discord.utils.get(guild.roles, name = 'South Dakota')
    await member.remove_roles(role)

  elif payload.emoji.name == '🍊':
    role = discord.utils.get(guild.roles, name = 'Florida')
    await member.remove_roles(role)

  elif payload.emoji.name == '👹':
    role = discord.utils.get(guild.roles, name = '9th Circle, Hell')
    await member.remove_roles(role)

  elif payload.emoji.name == '<:eli:230168985826492426>':
    role = discord.utils.get(guild.roles, name = 'picking up girls')
    await member.remove_roles(role)


@tasks.loop(seconds = 60)
async def birthday_test_1():
  az_channel = bot.get_channel(132220236425330688)
  print(f"Got channel {az_channel}")

  az_timezone = ZoneInfo('US/Arizona')
  replit_time = datetime.datetime.now(datetime.timezone.utc)
  timechange = replit_time.astimezone(az_timezone)
  current_az_time = timechange.strftime("%H:%M")
  current_az_month = timechange.strftime("%m")
  current_az_day = timechange.strftime("%d")

  print(current_az_time)
  print(current_az_month)
  print(current_az_day)


  curmonth = str(current_az_month)
  curday = str(current_az_day)
  birthdate = curmonth + " " + curday
  birthday_send_time = "07:00"
  print(birthdate)


  bot_birthday   = "9 11"
  nick_c_birthday= "01 10"
  zach_birthday  = "01 11"  
  may_birthday   = "01 19"
  andrew_birthday= "02 13"
  mason_birthday = "03 01"
  eli_birthday   = "03 07"
  eve_birthday   = "03 29"
  chris_birthday = "04 16"
  caleb_birthday = "04 20"
  razor_birthday = "05 15"
  nic_m_birthday = "05 08"
  kevin_birthday = "06 22"
  brand_birthday = "06 25"
  lexi_birthday  = "07 09"
  devin_birthday = "07 13"
  coil_birthday  = "07 23"
  cole_birthday  = "07 27"
  gabe_birthday  = "08 23"
  riley_birthday = "08 25"
  ariel_birthday = "09 10"
  matt_birthday  = "10 20"
  brend_birthday = "10 21"
  noelle_birthday= "11 12"
  joe_birthday   = "11 17"
  emily_birthday = "12 01"
  calvin_birthday= "12 17"
  dan_birthday   = "12 28"
  mondo_birthday = "12 29"

  embed = discord.Embed(title = ":notes: Happy Birthday Snek Kyoko!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  embed.set_image(url = "https://media1.tenor.com/m/m-hf9vntiC4AAAAC/batendo-bolo-bolo.gif")

  nick_c_embed = discord.Embed(title = ":notes: Happy Birthday Nick!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  nick_c_embed.set_image(url = "http://www.quickmeme.com/img/69/693df9aac9be353d959a1b7e6927c6d59f264fe455d44870d84da8380982bf09.jpg")

  zach_embed = discord.Embed(title = ":notes: Happy Birthday Zach!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  zach_embed.set_image(url = "https://media.tenor.com/bZlB4r5tjGUAAAAC/gintamabirthday.gif")

  may_embed = discord.Embed(title = ":notes: Happy Birthday May!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  may_embed.set_image(url = "https://media.tenor.com/VYOOSgFkg0wAAAAC/gintama-anime.gif")

  andrew_embed = discord.Embed(title = ":notes: Happy Birthday Andrew!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  andrew_embed.set_image(url = "https://media.tenor.com/8z1Mz9dgthoAAAAC/ascendance-of-a-bookworm-myne.gif")

  mason_embed = discord.Embed(title = ":notes: Happy Birthday Mason!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  mason_embed.set_image(url = "https://media.tenor.com/dh15zxLi_dAAAAAC/why-you.gif")

  eli_embed = discord.Embed(title = ":notes: Happy Birthday Eli!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  eli_embed.set_image(url = "https://cdn.discordapp.com/attachments/198137809540743168/392730837789179904/DRYCCymUEAAT0go.png")

  eve_embed = discord.Embed(title = ":notes: Happy Birthday Eve!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  eve_embed.set_image(url = "https://media.tenor.com/NA9r1jS4emsAAAAM/berd-flamingo-berd.gif")

  chris_embed = discord.Embed(title = ":notes: Happy Birthday Chris!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  chris_embed.set_image(url = "https://media.tenor.com/xzs9iQyoGaYAAAAC/happy-hockey.gif")

  caleb_embed = discord.Embed(title = ":notes: Happy Birthday Caleb!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  caleb_embed.set_image(url = "https://media.tenor.com/3nHe-FtREicAAAAd/trey-lucus.gif")

  razor_embed = discord.Embed(title = ":notes: Happy Birthday Razor!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  razor_embed.set_image(url = "https://media.tenor.com/J6fI9AxF_ckAAAAd/second-life-metaverse.gif")

  nicm_embed = discord.Embed(title = ":notes: Happy Birthday Nic!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  nicm_embed.set_image(url = "https://media.tenor.com/vLNtmQzuTf0AAAAS/congratulations-brother.gif")

  kevin_embed = discord.Embed(title = ":notes: Happy Birthday Kevin!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  kevin_embed.set_image(url = "https://live.staticflickr.com/65535/51070607158_82e8b152ab_z.jpg")

  brandon_embed = discord.Embed(title = ":notes: Happy Birthday Brandon!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  brandon_embed.set_image(url = "https://media.tenor.com/NKg3Nx-aLzsAAAAC/tower-of-god-funny.gif")

  lexi_embed = discord.Embed(title = ":notes: Happy Birthday Lexi!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  lexi_embed.set_image(url = "https://media.tenor.com/0W0v33ReD7gAAAAC/happy-birthday-kitten.gif")

  devin_embed = discord.Embed(title = ":notes: Happy Birthday Devin!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  devin_embed.set_image(url = "https://media.tenor.com/pNpke5vztHMAAAAC/pit-lady.gif")

  coil_embed = discord.Embed(title = ":notes: Happy Birthday Cole!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  coil_embed.set_image(url = "https://media.tenor.com/m2rhKuj2UEwAAAAC/vaporeon-pokemon.gif")

  cole_embed = discord.Embed(title = ":notes: Happy Birthday Cole!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  cole_embed.set_image(url = "https://media.tenor.com/upP2pV1SsO4AAAAd/resident-evil-village-resident-evil.gif")

  gabe_embed = discord.Embed(title = ":notes: Happy Birthday Gabe (High school)!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  gabe_embed.set_image(url = "https://media.tenor.com/zenjhCdEDtkAAAAC/pokemon-happy.gif")

  riley_embed = discord.Embed(title = ":notes: Happy Birthday Riley!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  riley_embed.set_image(url = "https://cdn.donmai.us/original/95/a0/__nakagawa_natsuki_hibike_euphonium_drawn_by_yamaguchi_satoshi__95a02159feae65e1eb8838b1a7705ecc.jpg")

  ariel_embed = discord.Embed(title = ":notes: Happy Birthday Ari!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  ariel_embed.set_image(url = "https://media.tenor.com/cls9W0cOBiwAAAAC/ouran-ohshc.gif")

  matt_embed = discord.Embed(title = ":notes: Happy Birthday Matt!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  matt_embed.set_image(url = "https://media.tenor.com/XTeOkCxEkP0AAAAd/anime-ranking-of-kings.gif")

  brenden_embed = discord.Embed(title = ":notes: Happy Birthday Brenden!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  brenden_embed.set_image(url = "https://media.tenor.com/FeUvOGQfgccAAAAC/rela-rela-oomfie.gif")

  noelle_embed = discord.Embed(title = ":notes: Happy Birthday Noelle!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  noelle_embed.set_image(url = "https://media.tenor.com/DX3el8xW6lAAAAAC/happy-birthday-birthday-cake.gif")

  joe_embed = discord.Embed(title = ":notes: Happy Birthday Joe!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  joe_embed.set_image(url = "https://media.tenor.com/XXFsGNN7cLwAAAAC/chie-persona.gif")

  emily_embed = discord.Embed(title = ":notes: Happy Birthday Emily!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  emily_embed.set_image(url = "https://media.tenor.com/tWm5_ALi7AIAAAAd/hoppy-birthday-happy-birthday.gif")

  calvin_embed = discord.Embed(title = ":notes: Happy Birthday Calvin!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  calvin_embed.set_image(url = "https://media.tenor.com/T31vVm4cgGAAAAAC/lake-tree.gif")

  dan_embed = discord.Embed(title = ":notes: Happy Birthday Dan!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  dan_embed.set_image(url = "https://media.tenor.com/-3Mtu0HCiokAAAAC/birthday-bts.gif")

  mondo_embed = discord.Embed(title = ":notes: Happy Birthday Mondo!!! :notes: ", description = " <:sip:820505650337284147>  お誕生日おめでとう <:sip:820505650337284147> ", color =0x2ecc71)
  mondo_embed.set_image(url = "https://cdn.discordapp.com/attachments/166301810317983744/346861223050215424/image.jpg")

  if current_az_time == birthday_send_time:

    if birthdate == nick_c_birthday:
      await az_channel.send(embed = nick_c_embed)
      await az_channel.send("<@185638282099425281> 🔥🔥🔥<:hypers:1063164818112131182><:hypers:1063164818112131182><:hypers:1063164818112131182>🔥🔥🔥")
    elif birthdate == bot_birthday:
      await az_channel.send(embed = embed)
      await az_channel.send("<@921659541073051659> 🔥🔥🔥<:PythonBot:1219021028764815432><:PythonBot:1219021028764815432>️<:PythonBot:1219021028764815432>🔥🔥🔥")
    elif birthdate == zach_birthday:
      await az_channel.send(embed = zach_embed)
      await az_channel.send("<@137301812741931008> <:zach:244228213172076544><:zach:244228213172076544><:zach:244228213172076544><:zach:244228213172076544><:zach:244228213172076544>")
    elif birthdate  == may_birthday:
      await az_channel.send(embed = may_embed)
      await az_channel.send("<@141197293360513024> :sheep::sheep::sheep:<:pog:979009312783495190><:pog:979009312783495190>")
    elif birthdate == andrew_birthday:
      await az_channel.send(embed = andrew_embed)
      await az_channel.send("<@115918075370405888> <:andrew:230168932353310720><:andyru:262474347397120000><:andrew:230168932353310720><:andyru:262474347397120000>")
    elif birthdate == mason_birthday:
      await az_channel.send(embed = mason_embed)
      await az_channel.send("<@321731874340864000> <:mason:322280884570947587><:mason:322280884570947587><:mason:322280884570947587><:mason:322280884570947587><:mason:322280884570947587>")
    elif birthdate == eli_birthday:
      await az_channel.send(embed = eli_embed)
      await az_channel.send("<:eli:230168985826492426><:eli:230168985826492426><:eli:230168985826492426>")
    elif birthdate == eve_birthday:
      await az_channel.send(embed = eve_embed)
      await az_channel.send("<@279132667298054145> :tada: :tada: :tada: :tada: :tada:")
    elif birthdate == chris_birthday:
      await az_channel.send(embed = chris_embed)
      await az_channel.send("<@115993234265604096> <:chris:319226266387611648><:chris:319226266387611648><:chris:319226266387611648><:chris:319226266387611648><:chris:319226266387611648>")
    elif birthdate == caleb_birthday:
      await az_channel.send(embed = caleb_embed)
      await az_channel.send("<@121884732546875392> <:PogOfGreed:721505607781187617><:PogOfGreed:721505607781187617><:PogOfGreed:721505607781187617><:NyanPog:957170859641040907><:NyanPog:957170859641040907>")
    elif birthdate == razor_birthday:
      await az_channel.send(embed = razor_embed)
      await az_channel.send("<@122173449123790848> ☠️❤️☠️❤️☠️❤️ :walW::walW:")
    elif birthdate == nic_m_birthday:
      await az_channel.send(embed = nicm_embed)
      await az_channel.send("<@115927815794327554> <:nic:230169190856785920><:nic:230169190856785920><:nic:230169190856785920><:nic:230169190856785920><:nic:230169190856785920>")
    elif birthdate == kevin_birthday:
      await az_channel.send(embed = kevin_embed)
      await az_channel.send("<@115906785537163271> <:kevin:230169044311867392><:kevin:230169044311867392><:kevin:230169044311867392><:kevin:230169044311867392><:kevin:230169044311867392>")
    elif birthdate == brand_birthday:
      await az_channel.send(embed = brandon_embed)
      await az_channel.send("<@187637949008052224> <:brandon:308848163861692426><:brandon:308848163861692426><:brandon:308848163861692426><:brandon:308848163861692426><:brandon:308848163861692426>")
    elif birthdate == lexi_birthday:
      await az_channel.send(embed = lexi_embed)
      await az_channel.send("<@115952162621751304> <:NyanPog:957170859641040907> :partying_face: :tada: :partying_face: ")
    elif birthdate == devin_birthday:
      await az_channel.send(embed = devin_embed)
      await az_channel.send("<@116009569045446657> <:smugDev:571579678465196032><:smugDev:571579678465196032><:smugDev:571579678465196032><:smugDev:571579678465196032><:smugDev:571579678465196032>")
    elif birthdate == coil_birthday:
      await az_channel.send(embed = coil_embed)
      await az_channel.send("<@163085358987345920> <:letsgo:350747133017718796><:letsgo:350747133017718796><:letsgo:350747133017718796><:POGGIES:987016376805904424><:POGGIES:987016376805904424>")
    elif birthdate == cole_birthday:
      await az_channel.send(embed = cole_embed)
      await az_channel.send("<@116104884335542278> <:NyanPog:957170859641040907><:cole:230168965597495297> <:colethink:332739327421317131><:NyanPog:957170859641040907>" )
    elif birthdate == gabe_birthday:
      await az_channel.send(embed = gabe_embed)
      await az_channel.send("<@132395062330916864> :partying_face::partying_face::partying_face:")
    elif birthdate == riley_birthday:
      await az_channel.send(embed = riley_embed)
      await az_channel.send("<@115949042906693639> <:RileyU:571579238914850819> <:rileyJap:314659045262753793><:rileyDrunk:705647960058363904><:riley:230169248738181121>")
    elif birthdate == ariel_birthday:
      await az_channel.send(embed = ariel_embed)
      await az_channel.send("<@621529418967547952> <:Bocchi61:1053107792296288276> <:JigglyAngy:1054138457385082972><:Bojji:1030520849784123544>")
    elif birthdate == matt_birthday:
      await az_channel.send(embed = matt_embed)
      await az_channel.send("<@113008229411241984> <:Bojji:1030520849784123544><:Bojji:1030520849784123544><:POGGIES:987016376805904424> <:villager:1052970632188534974> <:matt:230169075626541056> <:matt:230169075626541056>")
    elif birthdate == brend_birthday:
      await az_channel.send(embed = brenden_embed)
      await az_channel.send("<@115931730854150145> <:brenden:230159979519279104> <:brenden:230159979519279104> <:hypers:1063164818112131182> <:hypers:1063164818112131182> <:brenden:230159979519279104> <:brenden:230159979519279104>")
    elif birthdate == noelle_birthday:
      await az_channel.send(embed = noelle_embed)
      await az_channel.send("<@219286041553534976> :dog: :cat: :goat: :partying_face: ")
    elif birthdate == joe_birthday:
      await az_channel.send(embed = joe_embed)
      await az_channel.send("<@115964667637006336> <:joe:230169017699008523> <:joe:230169017699008523> <:pepeok:230538899359793152> <:CacoPog:953152686931443773>")
    elif birthdate == emily_birthday:
      await az_channel.send(embed = emily_embed)
      await az_channel.send("<@168060375730880514> :bird: :birthday: :bird: :baby_chick: :parrot: :baby_chick: ")
    elif birthdate == calvin_birthday:
      await az_channel.send(embed = calvin_embed)
      await az_channel.send("<@116011732190756868> <:cal:230168950045016064><:calBalls:677780098497118218> <:cal:230168950045016064>:birthday:  ")
    elif birthdate == dan_birthday:
      await az_channel.send(embed = dan_embed)
      await az_channel.send("<@147600171360845824> <:dan:240621343551258624>:hand_with_index_finger_and_thumb_crossed: :fingers_crossed: <:shinoashock:978776558129012766> <:hyperthink:312732126543872001> <:shinoashock:978776558129012766>")
    elif birthdate == mondo_birthday:
      await az_channel.send(embed = mondo_embed)
      await az_channel.send("<@115908537783287809> <:mondo:230169125928960000> <:howdy:413174711325949952> <:mondo:230169125928960000> <:howdy:413174711325949952> <:pog:979009312783495190>")
    else:
        print("Error")



@birthday_test_1.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")


async def main() -> None:
    async with bot:
        await bot.start(os.getenv('TOKEN'))


asyncio.run(main())
#bot.run(os.getenv('TOKEN'))