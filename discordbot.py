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
    1: ("HST", "Pacific/Honolulu"),
    2: ("AKST", "America/Anchorage"),
    3: ("PST", "America/Los_Angeles"),
    4: ("MST", "America/Denver"),
    5: ("CST", "America/Chicago"),
    6: ("EST", "America/New_York"),
    7: ("AST", "America/Halifax"),
    8: ("BRT", "America/Sao_Paulo"),
    9: ("GMT", "Etc/GMT"),
    10: ("CET", "Europe/Paris"),
    11: ("EET", "Europe/Athens"),
    12: ("MSK", "Europe/Moscow"),
    13: ("GST", "Asia/Dubai"),
    14: ("IST", "Asia/Kolkata"),
    15: ("BST", "Asia/Dhaka"),
    16: ("ICT", "Asia/Bangkok"),
    17: ("CST-China", "Asia/Shanghai"),
    18: ("JST", "Asia/Tokyo"),
    19: ("AEST", "Australia/Sydney"),
    20: ("ACST", "Australia/Adelaide"),
    21: ("AWST", "Australia/Perth"),
    22: ("NZST", "Pacific/Auckland"),
    23: ("UTC+13", "Pacific/Enderbury"),
    24: ("UTC+14", "Pacific/Kiritimati")
}

# --------- ROLE SETUP ----------
async def setup_roles(guild):
    existing_roles = {role.name: role for role in guild.roles}
    for _, (role_name, tz) in TIMEZONE_ROLES.items():
        if role_name not in [r.name for r in guild.roles]:
            try:
                await guild.create_role(name=role_name)
            except discord.Forbidden:
                print(f"Missing permissions to create role {role_name} in {guild.name}")

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

    role_name, tz_iana = TIMEZONE_ROLES[number]

    # Look for the role properly
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role is None:
        # If it wasn’t found, try creating it on the fly
        try:
            role = await ctx.guild.create_role(name=role_name)
        except discord.Forbidden:
            await ctx.send(f"I don’t have permission to create the role {role_name}!")
            return

    # Remove any old timezone roles
    old_roles = [r for r in ctx.author.roles if r.name in [n for n, _ in TIMEZONE_ROLES.values()]]
    if old_roles:
        await ctx.author.remove_roles(*old_roles)

    # Add the new role
    await ctx.author.add_roles(role)
    await ctx.send(f"your timezone is {role_name}")
# --------- CALCULATION ----------
def calculate_time_from_role(user_roles):
    tz_role_tuple = next(
        ((name, tz) for _, (name, tz) in TIMEZONE_ROLES.items() if name in [r.name for r in user_roles]),
        None
    )
    
    if tz_role_tuple is None:
        tz_name, tz_iana = "EST", "America/New_York"  # fallback
    else:
        tz_name, tz_iana = tz_role_tuple

    now = datetime.now(ZoneInfo(tz_iana))
    hour = now.hour % 12
    minute = now.minute
    minutes_after_1 = (hour - 1) * 60 + minute
    quarters = minutes_after_1 // 15

    return f"It's {quarters} quarters after 1, I'm all alone and I need you now. ({tz_name})"

@bot.command()
async def glorp(ctx):
    msg = calculate_time_from_role(ctx.author.roles)
    await ctx.send(msg)

# --------- RUN ----------
token = os.getenv("TOKEN")
if token is None:
    raise Exception("TOKEN not set")

bot.run(token)
