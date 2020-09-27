import discord
import random
import time
import asyncio
import wave
import contextlib
from mutagen.mp3 import MP3
from discord.ext import commands

# Discord bot token
TOKEN = 'randomToken'
client = commands.Bot(command_prefix = '.')

# Making sure the discord bot is activated
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="with you :)"))
    print('Bot online.')

# Get the discord bot to join and play the clips in the channel
@client.command(pass_context=True)
async def join(ctx):
    #audio clips
    queue()
    # time that is going to be in between different clips
    listWithtime = [30, 60, 120, 15, 90, 45]
    randomNumber = 0
    originalLengthQueue = len(queue)
    # joining the users voice channel
    userChannel = ctx.message.author.voice
    if userChannel != None:
        channel = userChannel.channel
        vc = await channel.connect()
        # while there are still items in the queue
        for i in range(originalLengthQueue):
            randomNumber = random.randint(1, originalLengthQueue)
            # no repeats in the audio clips played
            while randomNumber not in queue:
                randomNumber = random.randint(1, originalLengthQueue)
            randomNumber = i + 1
            randomListNumber = listWithtime[random.randint(0, len(listWithtime) - 1)]
            # get that clip that is going to be played
            clipToPlay = queue[randomNumber]
            print(clipToPlay)
            vc.play(discord.FFmpegPCMAudio(clipToPlay))
            audio = MP3(clipToPlay)
            # check how long the audio file is so you can wait for that amount of times
            print(audio.info.length)
            queue.pop(randomNumber)
            duration = audio.info.length
            print(randomListNumber)
            await asyncio.sleep(duration + 2)
        await leave(ctx)

# Have the discord bot leave the voice channel
@client.command(pass_context=True)
async def leave(ctx):
    channel = ctx.message.guild.voice_client
    if channel != None:
        await channel.disconnect()

client.run(TOKEN)
