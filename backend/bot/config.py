import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID', 0))
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID', 0))

# Command prefix
COMMAND_PREFIX = "!"

# Validate required environment variables
if not all([BOT_TOKEN, GUILD_ID, CHANNEL_ID]):
    raise ValueError(
        "Missing required environment variables. "
        "Please check your .env file contains: "
        "DISCORD_TOKEN, DISCORD_GUILD_ID, DISCORD_CHANNEL_ID"
    ) 