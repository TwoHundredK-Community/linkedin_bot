import asyncio
from datetime import datetime, time
import logging
from typing import Optional, List
from .company_scraper import CompanyScraper
from bot.bot import LinkedInBot

logger = logging.getLogger(__name__)

class LinkedInScheduler:
    def __init__(self, company_url: str, discord_bot: LinkedInBot, channel_id: int):
        if not company_url:
            raise ValueError("company_url cannot be empty")
            
        self.scraper = CompanyScraper(company_url)
        self.discord_bot = discord_bot
        self.channel_id = channel_id
        self.last_check: Optional[datetime] = None
        
    async def check_and_send_updates(self, instant: bool = False) -> List[Post]:
        """
        Check for new LinkedIn posts and send them to Discord
        
        Args:
            instant (bool): If True, ignore the last check time
            
        Returns:
            List[Post]: List of posts that were found and processed
        """
        try:
            scraper = CompanyScraper(self.scraper.company_url)
            posts = await scraper.get_latest_posts(limit=10)
            
            if not posts:
                return []
                
            # Filter out posts we've already seen
            new_posts = []
            for post in posts:
                if instant or self._is_new_post(post):
                    new_posts.append(post)
                    await self._send_to_discord(post)
                    self._update_last_check(post)
                    
            return new_posts
            
        except Exception as e:
            logger.error(f"Error in check_and_send_updates: {e}")
            return []
        
    async def start_scheduler(self, check_time: time = time(hour=9, minute=0)):
        """Start the daily scheduler"""
        logger.info("Scheduler started")
        try:
            while True:
                now = datetime.now()
                target_time = datetime.combine(now.date(), check_time)
                
                # If today's check time has passed, schedule for tomorrow
                if now.time() > check_time:
                    target_time = datetime.combine(now.date(), check_time)
                    target_time = target_time.replace(day=target_time.day + 1)
                    
                # Calculate seconds until next check
                seconds_until_check = (target_time - now).total_seconds()
                
                # Wait until next check time
                await asyncio.sleep(seconds_until_check)
                
                # Perform the check
                await self.check_and_send_updates()
                
        except asyncio.CancelledError:
            logger.info("Scheduler cancelled")
        except Exception as e:
            logger.error(f"Unexpected error in scheduler: {str(e)}") 