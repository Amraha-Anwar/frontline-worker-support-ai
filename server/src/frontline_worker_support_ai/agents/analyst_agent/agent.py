import json
import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Literal, Optional

class CitizenProfile(BaseModel):
    full_name: str
    location: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None



class AnalysisOutputSchema(BaseModel):
    case_id: str
    request_text: str
    request_type: Literal["emergency_medical", "crime_report", "general_support"]
    timestamp: str
    urgency: Literal["urgent", "critical"]
    citizen_profile: CitizenProfile
    needs_more_info: bool = False



def classify_request(request_text: str) -> tuple[str, str]:
    text = request_text.lower()
    if any(word in text for word in ["heart attack", "accident", "injury", "unconscious"]):
        return "emergency_medical", "critical"
    elif any(word in text for word in ["chori", "theft", "robbery", "fight", "murder"]):
        return "crime_report", "urgent"
    else:
        return "general_support", "urgent"



def save_case(data: dict):
    try:
        with open("cases.json", "r", encoding="utf-8") as f:
            all_cases = json.load(f)
    except FileNotFoundError:
        all_cases = []
    all_cases.append(data)
    with open("cases.json", "w", encoding="utf-8") as f:
        json.dump(all_cases, f, indent=2, ensure_ascii=False)



def main():
    print("\n=== Frontline Worker Support AI | Analyst Agent ===")
    print("Hello! I'm here to assist you. Please describe your issue below.\n")
    user_issue = input("You: ")
    request_type, urgency = classify_request(user_issue)
    location = ""

    while not location.strip():
        print("Agent: Can you provide your exact location or address?")
        location = input("You: ").strip()
    contact = ""

    while not contact.strip():
        print("Agent: Please provide your phone number or email so we can contact you.")
        contact = input("You: ").strip()
    email = contact if "@" in contact else None
    phone = contact if "@" not in contact else None
    full_name = input("Agent: Please provide your full name: ").strip()
    
    if not full_name:
        full_name = "Anonymous"
    final_output = AnalysisOutputSchema(
        case_id=str(uuid.uuid4()),
        request_text=user_issue,
        request_type=request_type,
        timestamp=datetime.now().isoformat(),
        urgency=urgency,
        citizen_profile=CitizenProfile(
            full_name=full_name,
            location=location,
            email=email,
            phone=phone,
        ),
        needs_more_info=False,
    )
    save_case(final_output.model_dump())


    print("\n=== Data Collection Complete ===")
    print(json.dumps(final_output.model_dump(), indent=2, ensure_ascii=False))
   

if __name__ == "__main__":
    main()
