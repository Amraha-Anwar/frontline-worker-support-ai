import asyncio
import json
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel

from agents import (
    function_tool,
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
)
from agents.memory.sqlite_session import SQLiteSession

from frontline_worker_support_ai.agents import guidance_agent
from frontline_worker_support_ai.agents.analyst_agent.instructions import INSTRUCTIONS
from frontline_worker_support_ai.agents.guidance_agent.agent import guidance_agent

# Load environment variables
load_dotenv()

# Set up Gemini client and model
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.0-flash",
)

config = RunConfig(model=model)

# Define the data model for a case
class CaseData(BaseModel):
    case_id: str
    citizen_name: str
    issue_type: str
    urgency: str
    details: str
    location: str
    contact: str
    timestamp: str



# Tool to save user case data
@function_tool
def save_case_tool(case: CaseData) -> str:
    """Save the case information in a JSON file."""
    try:
        with open("cases.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(case.dict())
    with open("cases.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return f"Case saved successfully! Total cases: {len(data)}"



# Create the Analyst Agent
analyst_agent = Agent(
    name="Analyst Agent",
    instructions= INSTRUCTIONS,
    handoffs=[guidance_agent],
    tools=[ save_case_tool],
)

# Main function to start the chat
async def main():
    print("\n=== Frontline Worker Support AI | Analyst Agent ===")
    print("Analyst Agent: Hello! How can I help you today?")

    # Create or connect to SQLite memory database
    session = SQLiteSession(session_id="citizen_chat_001", db_path="chat_memory.db")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit" , "bye" , "goodbye"]:
            print("Conversation ended.")
            break

        # Send input to the agent and keep chat context in session
        result = await Runner.run(
            starting_agent=analyst_agent,
            input=user_input,
            run_config=config,
            session=session,
        )

        print(f"\nAnalyst Agent: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
