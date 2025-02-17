from typing import List, Optional
from datetime import datetime
import aiohttp
import asyncio
from core.models.post import Post
from core.linkedin.config import LinkedInSettings
import logging
from urllib.parse import quote
from base64 import b64encode
import json
from core.linkedin.token_storage import TokenStorage

logger = logging.getLogger(__name__)

class CompanyScraper:
    def __init__(self, company_url: str):
        if not company_url:
            raise ValueError("company_url cannot be empty")
        if not company_url.startswith("https://www.linkedin.com/company/"):
            raise ValueError("Invalid LinkedIn company URL format")
            
        self.company_url = company_url.rstrip('/')
        self.company_urlname = company_url.split('/')[-1]
        self.settings = LinkedInSettings()
        self.base_url = "https://api.linkedin.com/v2"
        self.token_storage = TokenStorage()
        
    async def get_auth_url(self) -> str:
        """Generate LinkedIn OAuth URL"""
        params = {
            'response_type': 'code',
            'client_id': self.settings.CLIENT_ID,
            'redirect_uri': self.settings.REDIRECT_URI,
            'scope': self.settings.SCOPES,
            'state': b64encode(json.dumps({'company': self.company_urlname}).encode()).decode()
        }
        
        return f"https://www.linkedin.com/oauth/v2/authorization?" + "&".join(f"{k}={quote(v)}" for k, v in params.items())
        
    async def exchange_code_for_token(self, code: str) -> str:
        """Exchange authorization code for access token"""
        async with aiohttp.ClientSession() as session:
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': self.settings.CLIENT_ID,
                'client_secret': self.settings.CLIENT_SECRET,
                'redirect_uri': self.settings.REDIRECT_URI
            }
            
            async with session.post('https://www.linkedin.com/oauth/v2/accessToken', data=data) as response:
                if response.status != 200:
                    raise Exception(f"Failed to get access token: {await response.text()}")
                    
                result = await response.json()
                return result['access_token']

    async def _get_company_urn(self) -> str:
        """Get company URN using organization lookup"""
        async with aiohttp.ClientSession() as session:
            headers = self._get_auth_headers()
            
            endpoint = f"{self.base_url}/organizations?q=vanityName&vanityName={quote(self.company_urlname)}"
            
            async with session.get(endpoint, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['elements'][0]['id']
                raise Exception(f"Failed to get company URN: {await response.text()}")

    def _get_auth_headers(self) -> dict:
        """Get headers with authentication"""
        # Try to get token from storage first
        access_token = self.token_storage.get_token(self.company_urlname)
        if not access_token:
            access_token = self.settings.ACCESS_TOKEN
            
        if not access_token:
            raise ValueError("Access token not found. Please authenticate first.")
            
        return {
            "Authorization": f"Bearer {access_token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "LinkedIn-Version": "202304"
        }

    async def get_latest_posts(self, limit: int = 10) -> List[Post]:
        """Fetch latest posts using LinkedIn Organization API"""
        try:
            company_urn = await self._get_company_urn()
            
            async with aiohttp.ClientSession() as session:
                headers = self._get_auth_headers()
                
                # Using organization posts endpoint
                endpoint = (
                    f"{self.base_url}/ugcPosts?"
                    f"q=author&author=urn:li:organization:{company_urn}&"
                    f"count={limit}&sortBy=CREATED"
                )
                
                async with session.get(endpoint, headers=headers) as response:
                    if response.status != 200:
                        logger.error(f"API request failed: {await response.text()}")
                        return []
                        
                    data = await response.json()
                    return [self._parse_post(item) for item in data.get('elements', [])]
                    
        except Exception as e:
            logger.error(f"Error fetching LinkedIn posts: {str(e)}")
            return []

    def _parse_post(self, post_data: dict) -> Post:
        """Parse LinkedIn post data into Post model"""
        content = post_data.get('specificContent', {}).get('com.linkedin.ugc.ShareContent', {}).get('text', '')
        post_id = post_data.get('id', '').split(':')[-1]
        post_url = f"https://www.linkedin.com/feed/update/{post_id}"
        created_time = datetime.fromtimestamp(post_data.get('created', {}).get('time', 0) / 1000)
        
        return Post(
            content=content,
            timestamp=created_time,
            url=post_url,
            source="LinkedIn"
        )

    async def get_company_info(self) -> dict:
        """
        Get company information using LinkedIn API
        
        Returns:
            dict: Company information including name, description, etc.
        """
        try:
            company_urn = await self._get_company_urn()
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.settings.ACCESS_TOKEN}",
                    "X-Restli-Protocol-Version": "2.0.0"
                }
                
                endpoint = f"{self.base_url}/organizations/{company_urn}"
                
                async with session.get(endpoint, headers=headers) as response:
                    if response.status != 200:
                        logger.error(f"API request failed: {await response.text()}")
                        return {}
                        
                    data = await response.json()
                    
                    return {
                        'name': data.get('localizedName', ''),
                        'description': data.get('localizedDescription', ''),
                        'followers': data.get('followingInfo', {}).get('followerCount', 0)
                    }
                    
        except Exception as e:
            logger.error(f"Error fetching company info: {str(e)}")
            return {} 