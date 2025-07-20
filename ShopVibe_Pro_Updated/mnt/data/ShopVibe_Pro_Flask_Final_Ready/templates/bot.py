import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# تحميل التوكن من .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# إعداد الصلاحيات
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

# أمر اختبار
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# أمر للإيقاف من طرف المالك فقط
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("🛑 Shutting down...")
    await bot.close()

bot.run(TOKEN)
