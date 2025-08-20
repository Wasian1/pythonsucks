import discord
from discord.ext import commands
import wavelink

class SpotifyBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, query):
        # Check if the Spotify client is initialized
        if not hasattr(self.bot, 'spotify'):
            await ctx.send("Spotify client is not yet initialized. Please wait and try again.")
            return

        # Search for the track on Spotify
        results = self.bot.spotify.search(q=query, limit=1, type='track')

        # Extract the first track from the search results
        track = results['tracks']['items'][0]

        # Get the track URL
        track_url = track['external_urls']['spotify']

        # Send the track URL in the Discord channel
        await ctx.send(f'Now playing: {track_url}')

async def setup(bot):
  await bot.add_cog(SpotifyBot(bot))