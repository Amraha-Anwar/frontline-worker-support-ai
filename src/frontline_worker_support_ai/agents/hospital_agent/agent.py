from agents import Agent
from .instructions import INSTRUCTIONS

hospital_agent = Agent(
    name="Hospital Agent", 
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini"
)
