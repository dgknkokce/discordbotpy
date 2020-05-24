import discord
import os
import youtube_dl
import shutil
from discord.ext import commands
from discord.utils import get

TOKEN = "NzExMzMzNzcxNjg0NjEwMTcw.XsCBqQ.nwT1IDpasb1zjWRhHIzmfrQmc9k"
BOT_PREFIX = "."

bot = commands.Bot(command_prefix=BOT_PREFIX)


@bot.event
async def on_ready():
    print("Bot is ready.")



@bot.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        await channel.connect()
        print(f"Deli Bot has connected to {channel}")

    await ctx.send(f"Deli Bot is here!")



@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Deli Bot has left {channel}")
        await ctx.send(f"I'm leaving... Just for now :)")
    else:
        print(f"Deli Bot is not leaving")
        await ctx.send(f"I'm still here!")




@bot.event
async def on_member_join(member):
    print(f"{member} has joined the server.")


@bot.event
async def on_member_remove(member):
    print(f"{member} has left the server.")



#shows ping.
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")




#clears last 5 messages. ıt clears the command message too so added 1
@bot.command()
async def clear(ctx, amount=6):
    await ctx.channel.purge(limit=amount)





@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Unbanned {member.mention}")



@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return 




@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")


@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")

# travels all files in cog folder ends with ".py"
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")




@bot.command()
async def play(ctx, url: str):

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.realpath("Queue")
            length = len(os.listdir(DIR))
            still_in_queue = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Song still in queue: {still_in_queue}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, "song.mp3")

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song.")



    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing.")
        return

    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue folder.")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")


    await ctx.send("Getting everything ready now.")
    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now.\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    try:
        new_name = name.rsplit("-", 2)
        await ctx.send(f"Playing {new_name[0]}")
    except:
        await ctx.send(f"Playing song.")
    print("playing.\n")


@bot.command(aliases=["pau","p"])
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused.")
        voice.pouse()
        await ctx.send("Music paused.")
    else:
        print("Music not playing, failed pause.")
        await ctx.send("Music not playing, failed pause.")



@bot.command(aliases=["res", "r"])
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music.")
        voice.resume()
        await ctx.send("Resumed music.")
    else:
        print("Music is not paused.")
        await ctx.send("Music is not paused.")



@bot.command(aliases=["s"])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    queues.clear()

    queue_infile = os.path.isdir("./Queue")
    if queue_infile is True:
        shutil.rmtree("./Queue")

    if voice and voice.is_playing():
        print("Music stopped.")
        voice.stop()
        await ctx.send("Music stopped.")
    else:
        print("No music playing, failed to stop")
        await ctx.send("No music playing, failed to stop.")


queues = {}

@bot.command(aliases=["q"])
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")

    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "outtmpl": queue_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now.\n")
        ydl.download([url])
    await ctx.send("Adding song " + str(q_num) + " to the queue.")
    print("Song added to queue.\n")


@bot.command(aliases=["n"])
async def next(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)



    if voice and voice.is_playing():
        print("Playing next song.")
        voice.stop()
        await ctx.send("Next song.")
    else:
        print("No music playing, failed to play next song")
        await ctx.send("No music playing failed.")


# handles all commands.
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("There is no such command in here.")

# handles specific command(in here it's clear).
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify an amount of messages to delete.")





bot.run(TOKEN)
