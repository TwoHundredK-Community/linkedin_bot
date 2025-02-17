import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID', 0))
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID', 0))
LINKEDIN_COMPANY_URL = os.getenv('LINKEDIN_COMPANY_URL')

# Command prefix
COMMAND_PREFIX = "!"

# Validate required environment variables
if not all([BOT_TOKEN, GUILD_ID, DISCORD_CHANNEL_ID, LINKEDIN_COMPANY_URL]):
    raise ValueError(
        "Missing required environment variables. "
        "Please check your .env file contains: "
        "DISCORD_TOKEN, DISCORD_GUILD_ID, DISCORD_CHANNEL_ID, LINKEDIN_COMPANY_URL"
    ) 