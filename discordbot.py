from datetime import datetime, timedelta
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- ROLE SETUP ----------

TIMEZONE_ROLES = {
    1: "HST",   # Hawaii
    2: "AKST",  # Alaska
    3: "PST",   # Pacific
    4: "MST",   # Mountain
    5: "CST",   # Central
    6: "EST",   # Eastern
    7: "AST",   # Atlantic
    8: "BRT",   # Brazil
    9: "GMT",   # UK
    10: "CET",  # Central Europe
    11: "EET",  # Eastern Europe
    12: "MSK",  # Moscow
    13: "GST",  # Gulf
    14: "IST",  # India
    15: "BST",  # Bangladesh
    16: "ICT",  # Thailand
    17: "CST-China", # China
    18: "JST",  # Japan
    19: "AEST", # Australia East
    20: "ACST", # Australia Central
    21: "AWST", # Australia West
    22: "NZST", # New Zealand
    23: "UTC+13",
    24: "UTC+14"
}

async def setup_roles(guild):
    existing_roles = {role.name: role for role in guild.roles}

    for name in TIMEZONE_ROLES.values():
        if name not in existing_roles:
            await guild.create_role(name=name)

# Run when bot joins a server
@bot.event
async def on_guild_join(guild):
    await setup_roles(guild)

# Also run on startup (for already joined servers)
@bot.event
async def on_ready():
    print(f"Live as {bot.user}")
    for guild in bot.guilds:
        await setup_roles(guild)

# ---------- COMMAND ----------

@bot.command()
async def timezone(ctx, number: int = None):
    if number is None:
        await ctx.send("Use it like this: !timezone 1-24")
        return

    if number not in TIMEZONE_ROLES:
        await ctx.send("Pick a number from 1 to 24.")
        return

    role_name = TIMEZONE_ROLES[number]
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role is None:
        await ctx.send("Timezone roles aren't set up yet.")
        return

    roles_to_remove = [r for r in ctx.author.roles if r.name in TIMEZONE_ROLES.values()]
    if roles_to_remove:
        await ctx.author.remove_roles(*roles_to_remove)

    await ctx.author.add_roles(role)

    await ctx.send(f"your timezone is {role_name}")
    
# ---------- RUN ----------

token = os.getenv("TOKEN")

if token is None:
    raise Exception("TOKEN not set")

bot.run(token)
