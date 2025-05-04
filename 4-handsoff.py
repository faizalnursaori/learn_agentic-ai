from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from pydantic import BaseModel, Field
from typing import List
import json

load_dotenv()

@function_tool
def search_hotels():
    hotels = [
        {
            "name": "Park Hyatt Tokyo",
            "address": "Tokyo, Japan",
            "amenities": ["pool", "spa", "gym"],
            "price_per_night": 800,
            "recommendation_reason": "Best value for money",
        },
        {
            "name": "Shinjuku Granbell Hotel",
            "address": "Tokyo, Japan",
            "amenities": ["pool", "spa", "gym"],
            "price_per_night": 900,
            "recommendation_reason": "Excellent location",
        },
        {
            "name": "Hotel Gracery Shinjuku",
            "address": "Tokyo, Japan",
            "amenities": ["pool", "spa", "gym"],
            "price_per_night": 1000,
            "recommendation_reason": "Wonderful view",
        },
    ]

    return json.dumps(hotels)
class HotelRecommendation(BaseModel):
    name: str
    address: str
    amenities: List[str]
    price_per_night: float
    recommendation_reason: str


hotel_agent = Agent(
    name="Hotel Agent",
    instructions="""
    You are a hotel agent that help the user plan perfect trip.

    Use the search_hotels to find hotel options and recommend the best one to the user.

    """,
    model="gpt-4.1-mini",
    output_type=HotelRecommendation,
    tools=[search_hotels]
)

@function_tool
def search_flights():
    flights = [
        {
            "origin": "New York",
            "destination": "Tokyo",
            "departure_date": "2023-08-15",
            "return_date": "2023-08-20",
            "airline": "United Airlines",
            "price": 1000,
            "recommendation_reason": "Best value for money",
        },
        {
            "origin": "New York",
            "destination": "Tokyo",
            "departure_date": "2023-08-15",
            "return_date": "2023-08-20",
            "airline": "United Airlines",
            "price": 1100,
            "recommendation_reason": "Excellent location",
        },
        {
            "origin": "New York",
            "destination": "Tokyo",
            "departure_date": "2023-08-15",
            "return_date": "2023-08-20",
            "airline": "United Airlines",
            "price": 1200,
            "recommendation_reason": "Wonderful view",
        },
    ]

    return json.dumps(flights)

class FlightRecommendation(BaseModel):
    origin: str
    destination: str
    departure_date: str
    return_date: str
    airline: str
    price: float
    recommendation_reason: str

flight_agent = Agent(
    name="Flight Agent",
    instructions="""
    You are a flight agent that help the user plan perfect trip.

    Use the search_flights to find flight options and recommend the best one to the user.

    """,
    model="gpt-4.1-mini",
    output_type=FlightRecommendation,
    tools=[search_flights]
)

class TravelPlan(BaseModel):
    destination: str
    trip_duration: str
    budget: float
    activities: List[str] = Field(description="List of recommendations activities")
    notes: List[str] = Field(description="List of additional recommendations")

travel_agent = Agent(

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

    If the user asks specificially about flight, use the flight agent to help with that
    """,
    model="gpt-4.1-mini",
    output_type=TravelPlan,
    handoffs=[hotel_agent, flight_agent]
)

result = Runner.run_sync(travel_agent, input="Gimme the plan for me to Japan, with budget $10000, find me the best hotels as well as flight recommendation, what should i do, and tell me the weather in Tokyo?")
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
    print(f"- {note}")