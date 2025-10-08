# from agents import Agent, Runner
# from .instructions import INSTRUCTIONS
# from ..guidance_agent import guidance_agent

from frontline_worker_support_ai.validations.models import AnalysisOutputSchema
from agents import Agent, Runner
from frontline_worker_support_ai.agents.analyst_agent.instructions import INSTRUCTIONS
from frontline_worker_support_ai.agents.guidance_agent import guidance_agent


from dotenv import load_dotenv
load_dotenv()

analyst_agent = Agent(
    name="Analyst Agent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    handoffs=[guidance_agent],
    output_type=AnalysisOutputSchema,
)

user_input = input("Enter your query: ")

result = Runner.run_sync(
    starting_agent=analyst_agent,
    input=user_input
    )

print(result.final_output)