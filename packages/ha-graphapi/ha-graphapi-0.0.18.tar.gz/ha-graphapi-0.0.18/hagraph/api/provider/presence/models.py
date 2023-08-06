from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

class PresenceResponse(BaseModel):
    id: str
    availability: str
    activity: str
