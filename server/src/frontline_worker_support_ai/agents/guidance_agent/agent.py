from agents import Agent
from .instructions import INSTRUCTIONS
from ..police_agent import police_agent
from ..hospital_agent import hospital_agent
from ..civic_agent import civic_agent

guidance_agent = Agent(
    name="Guidance Agent", 
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    handoffs=[hospital_agent, police_agent, civic_agent],
)
