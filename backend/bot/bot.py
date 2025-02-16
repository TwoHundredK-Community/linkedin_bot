import discord
from discord.ext import commands
from bot.config import BOT_TOKEN

class LinkedInBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        
    async def setup_hook(self):
        # Load cogs
        await self.load_extension("bot.cogs.company_posts")
        await self.load_extension("bot.cogs.job_alerts")
        await self.load_extension("bot.cogs.trend_alerts")
        
    async def on_ready(self):
        print(f"Bot is ready! Logged in as {self.user}")

def run_bot():
    bot = LinkedInBot()
    bot.run(BOT_TOKEN) 