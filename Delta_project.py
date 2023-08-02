import discord # Подключаем библиотеку
import yt_dlp
import nacl.secret
from discord.ext import commands
from Config import settings_Delta
import ffmpeg

intents = discord.Intents.default() # Подключаем "Разрешения"
intents.message_content = True
intents.members = True
# Задаём префикс и интенты
bot = commands.Bot(command_prefix=settings_Delta['prefix'], intents=intents)

# С помощью декоратора создаём первую команду
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.event
async def on_ready():
    print(f'Бот {bot.user.name} готов к работе!')

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        voice_client = await voice_channel.connect()
        ydl_opts = {'format': 'bestaudio/best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            voice_client.play(discord.FFmpegPCMAudio(source=url2, executable="C:\\ffmpeg\\ffmpeg.exe"))
    else:
        await ctx.send('Вы должны быть подключены к голосовому каналу.')

@bot.command()
async def pause(ctx):
    ctx.voice_client.pause()

@bot.command()
async def resume(ctx):
    ctx.voice_client.resume()

bot.run(settings_Delta['token'])