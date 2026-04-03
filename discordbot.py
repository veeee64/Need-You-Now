from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import discord
from discord.ext import commands
import os

#discord bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def calculate():
    now = datetime.now(ZoneInfo("America/New_York"))

    hour = now.hour % 12
    minute = now.minute
    minutes_after_1 = (hour - 1) * 60 + minute
    quarters = minutes_after_1 // 15

    return f"It's {quarters} quarters after 1, I'm all alone and I need you now."

@bot.event
async def on_ready():   
    print(f"Live")

@bot.command()
async def glorp(ctx):
    result = calculate()
    await ctx.send(result)

bot.run(os.getenv("TOKEN"))
