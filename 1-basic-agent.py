from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model="gpt-4.1-mini"
)

result = Runner.run_sync(agent, input="In this AI Era is programmer still relevant?")
print(result.final_output)