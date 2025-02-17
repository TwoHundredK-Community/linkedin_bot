from dataclasses import dataclass
from datetime import datetime

@dataclass
class Post:
    content: str
    timestamp: datetime
    url: str
    source: str = "LinkedIn" 