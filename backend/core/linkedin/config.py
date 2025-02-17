from pydantic_settings import BaseSettings

class LinkedInSettings(BaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET: str
    REDIRECT_URI: str = "http://localhost:8000/linkedin/callback"
    SCOPES: str = "r_organization_social r_organization_admin w_organization_social"
    
    # Optional: Store the access token securely in your database
    ACCESS_TOKEN: str | None = None
    
    class Config:
        env_prefix = "LINKEDIN_" 