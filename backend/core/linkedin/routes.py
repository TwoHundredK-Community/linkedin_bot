from fastapi import APIRouter, HTTPException
from core.linkedin.company_scraper import CompanyScraper
from core.linkedin.token_storage import TokenStorage
import json
from base64 import b64decode

router = APIRouter()
token_storage = TokenStorage()

@router.get("/linkedin/auth")
async def linkedin_auth(company_url: str):
    scraper = CompanyScraper(company_url)
    auth_url = await scraper.get_auth_url()
    return {"auth_url": auth_url}

@router.get("/linkedin/callback")
async def linkedin_callback(code: str, state: str):
    try:
        state_data = json.loads(b64decode(state))
        company_urlname = state_data['company']
        company_url = f"https://www.linkedin.com/company/{company_urlname}"
        
        scraper = CompanyScraper(company_url)
        access_token = await scraper.exchange_code_for_token(code)
        
        # Store the access token
        token_storage.save_token(company_urlname, access_token)
        
        return {"message": "Authentication successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/linkedin/token/{company_urlname}")
async def get_token(company_urlname: str):
    """Get stored token for a company (protected endpoint)"""
    token = token_storage.get_token(company_urlname)
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    return {"token": token} 