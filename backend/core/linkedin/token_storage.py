import json
import os
from pathlib import Path
from cryptography.fernet import Fernet
import base64
from typing import Optional

class TokenStorage:
    def __init__(self):
        self.storage_dir = Path("backend/core/linkedin/storage")
        self.storage_file = self.storage_dir / "tokens.enc"
        self.key_file = self.storage_dir / "key.secret"
        self._ensure_storage_exists()
        self._init_encryption()

    def _ensure_storage_exists(self):
        """Ensure storage directory exists"""
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _init_encryption(self):
        """Initialize or load encryption key"""
        if not self.key_file.exists():
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
        else:
            key = self.key_file.read_bytes()
        self.cipher = Fernet(key)

    def save_token(self, company_urlname: str, access_token: str):
        """Save encrypted access token for a company"""
        tokens = self.load_all_tokens()
        tokens[company_urlname] = access_token
        
        # Encrypt and save
        encrypted_data = self.cipher.encrypt(json.dumps(tokens).encode())
        self.storage_file.write_bytes(encrypted_data)

    def get_token(self, company_urlname: str) -> Optional[str]:
        """Get access token for a company"""
        tokens = self.load_all_tokens()
        return tokens.get(company_urlname)

    def load_all_tokens(self) -> dict:
        """Load all stored tokens"""
        if not self.storage_file.exists():
            return {}
            
        try:
            encrypted_data = self.storage_file.read_bytes()
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data)
        except Exception as e:
            print(f"Error loading tokens: {e}")
            return {} 