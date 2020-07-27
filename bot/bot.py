import discord
from discord.ext import commands
from discord.utils import get
import config
import urllib.request

print('Starting up')
client = commands.Bot(command_prefix = config.PREFIX)

@client.event
async def on_ready():
    print("Bot is ready.")

@client.command()
async def ping(ctx):
    await ctx.send(f"Faatinin kopegiyim tsk. ping = {client.latency*1000}ms")

@client.command()
async def about(ctx):
    await ctx.send(config.ABOUT)

@client.command()
async def test(ctx, *, question):
    await ctx.send(f"question = {question}")

@client.command()
@commands.is_owner()
async def reload(ctx):
    await ctx.send(f"Reloading...")

@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice_client = get(client.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_connected():
        await voice_client.move_to(channel)
    else:
        voice_client = await channel.connect()

@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice_client = get(client.voice_clients, guild=ctx.guild)

    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()


@client.command()
async def play(ctx, url):
    await join(ctx)
    voice_client = get(client.voice_clients, guild=ctx.guild)
    with open("sound.mp3", 'wb') as sound:
        print("Downloading")
        response = urllib.request.urlopen(url)
        data = response.read()
        sound.write(data)
        print("Download complete, playing.")
    voice_client.play(discord.FFmpegPCMAudio("sound.mp3"))

@client.event
async def on_message(message):
    # Groovy id
    if (message.author.id == config.MUSIC_BOT_ID):
        print(message.embeds[0].description)

    await client.process_commands(message)


client.run(config.TOKEN)
