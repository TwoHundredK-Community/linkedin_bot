import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

class TestCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="ping", description="Test the bot's response time")
    async def ping(self, interaction: discord.Interaction):
        """Simple command to test bot responsiveness"""
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! 🏓 Latency: {latency}ms")
    
    @app_commands.command(name="echo", description="Echo back a message")
    @app_commands.describe(message="The message to echo back")
    async def echo(self, interaction: discord.Interaction, message: str):
        """Echo the user's message back to them"""
        await interaction.response.send_message(f"Echo: {message}")
    
    @app_commands.command(name="info", description="Get information about the bot")
    async def info(self, interaction: discord.Interaction):
        """Display bot information"""
        embed = discord.Embed(
            title="LinkedIn Discord Bot",
            description="A bot that syncs LinkedIn content to Discord",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Features",
            value="• Company post sync\n• Job alerts\n• Trending topics",
            inline=False
        )
        embed.add_field(
            name="Status",
            value="🟢 Online",
            inline=True
        )
        embed.add_field(
            name="Latency",
            value=f"{round(self.bot.latency * 1000)}ms",
            inline=True
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(TestCommands(bot)) 