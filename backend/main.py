import asyncio
from bot.bot import LinkedInBot
from core.linkedin.scheduler import LinkedInScheduler
from bot.config import DISCORD_CHANNEL_ID, LINKEDIN_COMPANY_URL

async def main():
    bot = LinkedInBot()
    
    async def start_linkedin_monitoring():
        scheduler = LinkedInScheduler(
            company_url=LINKEDIN_COMPANY_URL,
            discord_bot=bot,
            channel_id=int(DISCORD_CHANNEL_ID)
        )
        await scheduler.start_scheduler()
    
    bot.loop.create_task(start_linkedin_monitoring())
    await bot.start(bot.token)

if __name__ == "__main__":
    asyncio.run(main()) 