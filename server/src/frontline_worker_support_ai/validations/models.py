
from pydantic import BaseModel, Field
from typing import Literal
import uuid
from datetime import datetime

class CitizenProfileSchema(BaseModel):
    full_name: str
    location: str
    email: str

class AnalysisOutputSchema(BaseModel):
    case_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_text: str
    request_type: str
    timestamp: str
    urgency: Literal["urgent", "critical"]
    citizen_profile: CitizenProfileSchema

    