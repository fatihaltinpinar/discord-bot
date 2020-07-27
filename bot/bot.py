import discord
from discord.ext import commands
from discord.utils import get
import config
import urllib.request
from bot.database import Database
import re
import csv

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
async def invite_link(ctx):
    await ctx.message.author.send(("Invite Link: " + config.INVITE_LINK))

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
    if (message.author.id == config.MUSIC_BOT_ID and message.embeds[0].title == "Now playing"):
        description = message.embeds[0].description
        print("Adding: ", description)
        video_title = re.search("\[(.*?)\]", description).group(1)
        video_link = re.search("\((http[s]?://(.*?))\)", description).group(1)
        member_id = re.search("\[<@(.*)>\]", description).group(1)
        guild_id = message.guild.id
        db.add_play_request(video_title, video_link, member_id, guild_id)
    await client.process_commands(message)


@client.command()
async def list(ctx):
    # member_ids = db.get_member_ids(ctx.guild.id)
    # member_names = {}
    # for id in member_ids:
    #     member_names[id] = client.get_user(id).name
    request_list = db.get_request_list(ctx.guild.id)

    with open('temp.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(("Video Title", "Video URL","Play Count"))
        writer.writerows(request_list)

    with open('temp.csv', 'r', newline='', encoding='utf-8') as file:
        await ctx.send(file=(discord.File(file, filename="request_list.csv")))


print('Starting up')
db = Database(config.DBFILE)
db.create_tables()
client.run(config.TOKEN)
