import discord
from discord import app_commands
from bot.config import BOT_TOKEN, GUILD_ID

class LinkedInBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        
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

    async def send_linkedin_update(self, channel_id: int, content: str, url: str):
        """Send LinkedIn post update to specified Discord channel"""
        channel = self.get_channel(channel_id)
        if not channel:
            return
        
        embed = discord.Embed(
            title="New LinkedIn Post",
            description=content[:2000] if content else "No content available",
            color=discord.Color.blue(),
            url=url
        )
        embed.set_footer(text="Posted via LinkedIn")
        
        await channel.send(embed=embed)

def run_bot():
    bot = LinkedInBot()
    bot.run(BOT_TOKEN)

if __name__ == "__main__":
    run_bot() 
