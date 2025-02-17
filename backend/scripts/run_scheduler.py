import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(backend_dir)

# Load environment variables
env_path = Path(backend_dir) / '.env'
load_dotenv(env_path)

from core.linkedin.scheduler import LinkedInScheduler
from core.linkedin.token_storage import TokenStorage
from bot.bot import LinkedInBot
from bot.config import LINKEDIN_COMPANY_URL, DISCORD_CHANNEL_ID

async def run_check_and_send_updates():
    try:
        # Initialize the TokenStorage
        token_storage = TokenStorage()
        
        # Get company name from URL
        company_urlname = LINKEDIN_COMPANY_URL.rstrip('/').split('/')[-1]
        
        # Check if we have a valid token
        token = token_storage.get_token(company_urlname)
        if not token:
            print(f"No LinkedIn token found for company: {company_urlname}")
            print("Please authenticate first by:")
            print("1. Start the FastAPI server")
            print(f"2. Visit /linkedin/auth?company_url={LINKEDIN_COMPANY_URL}")
            print("3. Complete the OAuth flow")
            return

        # Initialize the LinkedInBot
        discord_bot = LinkedInBot()
        
        # Initialize the LinkedInScheduler with env values
        scheduler = LinkedInScheduler(
            company_url=LINKEDIN_COMPANY_URL,
            discord_bot=discord_bot,
            channel_id=DISCORD_CHANNEL_ID
        )

        print(f"Starting LinkedIn post check for company: {company_urlname}")
        # Call the function with the instant flag set to True
        posts = await scheduler.check_and_send_updates(instant=True)
        print(f"Found {len(posts)} posts")
        
    except Exception as e:
        print(f"Error running scheduler: {e}")
    finally:
        # Cleanup
        if 'discord_bot' in locals():
            await discord_bot.close()

if __name__ == '__main__':
    asyncio.run(run_check_and_send_updates())