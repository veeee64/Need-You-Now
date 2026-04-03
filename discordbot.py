from datetime import datetime
from zoneinfo import ZoneInfo
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --------- TIMEZONE ROLES ----------
TIMEZONE_ROLES = {
    1: "HST",
    2: "AKST",
    3: "PST",
    4: "MST",
    5: "CST",
    6: "EST",
    7: "AST",
    8: "BRT",
    9: "GMT",
    10: "CET",
    11: "EET",
    12: "MSK",
    13: "GST",
    14: "IST",
    15: "BST",
    16: "ICT",
    17: "CST-China",
    18: "JST",
    19: "AEST",
    20: "ACST",
    21: "AWST",
    22: "NZST",
    23: "UTC+13",
    24: "UTC+14"
}

# --------- ROLE SETUP ----------
async def setup_roles(guild):
    existing_roles = {role.name: role for role in guild.roles}
    for name in TIMEZONE_ROLES.values():
        if name not in existing_roles:
            try:
                await guild.create_role(name=name)
            except discord.Forbidden:
                print(f"Missing permissions to create role {name} in {guild.name}")

@bot.event
async def on_guild_join(guild):
    await setup_roles(guild)

@bot.event
async def on_ready():
    print(f"Live as {bot.user}")
    for guild in bot.guilds:
        await setup_roles(guild)

# --------- COMMANDS ----------
@bot.command()
async def timezone(ctx, number: int = None):
    if number is None or number not in TIMEZONE_ROLES:
        await ctx.send("Pick a number from 1 to 24.")
        return

    role_name = TIMEZONE_ROLES[number]
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    # Remove old timezone roles
    roles_to_remove = [r for r in ctx.author.roles if r.name in TIMEZONE_ROLES.values()]
    if roles_to_remove:
        await ctx.author.remove_roles(*roles_to_remove)

    await ctx.author.add_roles(role)
    await ctx.send(f"your timezone is {role_name}")

# --------- CALCULATION ----------
def calculate_time_from_role(user_roles):
    tz_role = next((r.name for r in user_roles if r.name in TIMEZONE_ROLES.values()), None)
    if tz_role is None:
        tz_role = "EST"  # fallback default

    now = datetime.now(ZoneInfo(tz_role))
    hour = now.hour % 12
    minute = now.minute
    minutes_after_1 = (hour - 1) * 60 + minute
    quarters = minutes_after_1 // 15

    return f"It's {quarters} quarters after 1, I'm all alone and I need you now. ({tz_role})"

@bot.command()
async def glorp(ctx):
    msg = calculate_time_from_role(ctx.author.roles)
    await ctx.send(msg)

# --------- RUN ----------
token = os.getenv("TOKEN")
if token is None:
    raise Exception("TOKEN not set")

bot.run(token)
