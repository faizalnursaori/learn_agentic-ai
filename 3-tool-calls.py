from dotenv import load_dotenv
from agents import Agent, Runner,function_tool
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

@function_tool
def get_weather(city: str) -> str:
    weathers = {
        "Tokyo": "Sunny",
        "New York": "Cloudy",
        "Paris": "Rainy",
        "London": "Sunny",
        "Berlin": "Sunny"
    }

    if city in weathers:
        return weathers[city]
    else:
        return "Unknown"
    
@function_tool
def get_recommended_hotels(city: str)-> List[str]:
    hotel_database = {
        "Tokyo": ["Park Hyatt Tokyo", "Shinjuku Granbell Hotel", "Hotel Gracery Shinjuku"],
        "New York": ["The Plaza", "Hotel Pennsylvania", "Arlo SoHo"],
        "Paris": ["Le Meurice", "Hôtel Lutetia", "Pullman Paris Tour Eiffel"]
    }

    return hotel_database.get(city, ["No hotel data available for this city."])

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
    - Hotel Recommendation
    """,
    model="gpt-4.1-mini",
    output_type=TravelPlan,
    tools=[get_weather, get_recommended_hotels]
)

result = Runner.run_sync(agent, input="Gimme the plan for me to Japan, with budget $10000, what should i do, and tell me the weather in Tokyo?")
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