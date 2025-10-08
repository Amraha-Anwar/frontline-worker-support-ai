from agents import Agent
from .instructions import INSTRUCTIONS

civic_agent = Agent(
    name="Civic Agent", 
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini"
)
