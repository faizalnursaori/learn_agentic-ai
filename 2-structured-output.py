from dotenv import load_dotenv
from agents import Agent, Runner
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

class TravelPlan(BaseModel):
    destination: str
    trip_duration: str
    budget: float
    activities: List[str] = Field(description="List of recommendations activities")
    notes: List[str] = Field(description="List of additional recommendations")

agent = Agent(
    name="Travel Planner",
    instructions="""
    You are a comprehensive travel planner that help the user plan perfect trip
    You can always create personalized travel itenerary based on user interest

    Be a fun and helpful when assisting the user

    Consider to have :
    - Local attraction and activities
    - Budget considerations
    - Travel Duration
    """,
    model="gpt-4.1-mini",
    output_type=TravelPlan
)

result = Runner.run_sync(agent, input="Gimme the plan for me to Japan, with budget $10000, what should i do?")
travel_plan = result.final_output

print("TRAVEL AND ITENERARIES")
print(f"Destination{travel_plan.destination}")
print(f"Trip duration {travel_plan.trip_duration}")
print(f"Budget {travel_plan.budget}")
print("List of activities")
for activity in travel_plan.activities:
    print(f"- {activity}")

print("List of notes")
for note in travel_plan.notes:
    print(note)