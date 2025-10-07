from agents import Agent
from .instructions import INSTRUCTIONS

police_agent = Agent(
    name="Police Agent", 
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini"
)
