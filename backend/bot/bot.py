import discord
from discord.ext import commands
from bot.config import BOT_TOKEN, GUILD_ID

class LinkedInBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        
    async def setup_hook(self):
        # Load test commands cog
        await self.load_extension("bot.cogs.test_commands")
        
        # Sync commands with Discord
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        
    async def on_ready(self):
        print(f"Bot is ready! Logged in as {self.user}")
        print(f"Connected to {len(self.guilds)} guilds")
        
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            return
        raise error

def run_bot():
    bot = LinkedInBot()
    bot.run(BOT_TOKEN)

if __name__ == "__main__":
    run_bot() 
