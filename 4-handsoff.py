from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from pydantic import BaseModel, Field
from typing import List, Optional

load_dotenv()

@function_tool
def search_hotels():
    hotels = [
        {
            "name": "Park Hyatt Tokyo",
            "address": "Tokyo, Japan",
            "amenities": ["pool", "spa", "gym"],
            "price_per_night": 800,
        },
        {
            "name": "Shinjuku Granbell Hotel",
            "address": "Tokyo, Japan",
            "amenities": ["pool", "spa", "gym"],
            "price_per_night": 900,
        },
        {
            "name": "Hotel Gracery Shinjuku",
            "address": "Tokyo, Japan",
            "amenities": ["pool", "spa", "gym"],
            "price_per_night": 1000,
        },
    ]

    return hotels

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
        },
        {
            "origin": "New York",
            "destination": "Tokyo",
            "departure_date": "2023-08-15",
            "return_date": "2023-08-20",
            "airline": "ANA",
            "price": 1100,
        },
        {
            "origin": "New York",
            "destination": "Tokyo",
            "departure_date": "2023-08-15",
            "return_date": "2023-08-20",
            "airline": "JAL",
            "price": 1200,
        },
    ]

    # Kembalikan sebagai list, bukan JSON string
    return flights

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
    notes: List[str] = Field(default_factory=list, description="List of additional recommendations")
    hotel_recommendation: Optional[HotelRecommendation] = Field(None, description="Recommended hotel")
    flight_recommendation: Optional[FlightRecommendation] = Field(None, description="Recommended flight")

@function_tool
def get_weather_info(city: str):
    # Mock weather data - in a real application, this would call a weather API
    weather_data = {
        "Tokyo": {
            "current": "22°C, Partly Cloudy",
            "forecast": "Mild temperatures around 20-25°C expected for the next week with occasional rain"
        }
    }
    return weather_data.get(city, {"current": "No data available", "forecast": "No forecast available"})

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
    - Use the get_weather_info tool to provide weather information if asked

    If the user asks about hotels or flights, note it in your response, but you'll get specific recommendations
    from specialized agents later.
    """,
    model="gpt-4.1-mini",
    output_type=TravelPlan,
    tools=[get_weather_info]
)

# === STEP BY STEP EXECUTION ===

# Step 1: Dapatkan rencana perjalanan umum dari travel agent
travel_result = Runner.run_sync(
    travel_agent, 
    input="Gimme the plan for me to Japan, with budget $10000. What should I do there, and tell me the weather in Tokyo?"
)
travel_plan = travel_result.final_output

# Step 2: Dapatkan rekomendasi hotel
hotel_result = Runner.run_sync(
    hotel_agent,
    input="I'm looking for a hotel in Tokyo, gimme some recommendations."
)
hotel_recommendation = hotel_result.final_output

# Step 3: Dapatkan rekomendasi penerbangan
flight_result = Runner.run_sync(
    flight_agent,
    input="I'm looking for a flight to Tokyo, gimme some recommendations."
)
flight_recommendation = flight_result.final_output

# Step 4: Tambahkan rekomendasi ke rencana perjalanan
travel_plan.hotel_recommendation = hotel_recommendation
travel_plan.flight_recommendation = flight_recommendation

# === OUTPUT ===

print("TRAVEL AND ITENERARIES")
print(f"Destination: {travel_plan.destination}")
print(f"Trip duration: {travel_plan.trip_duration}")
print(f"Budget: ${travel_plan.budget}")

if travel_plan.hotel_recommendation:
    print("\nRecommended Hotel:")
    print(f"- Name: {travel_plan.hotel_recommendation.name}")
    print(f"- Address: {travel_plan.hotel_recommendation.address}")
    print(f"- Price: ${travel_plan.hotel_recommendation.price_per_night} per night")
    print(f"- Reason: {travel_plan.hotel_recommendation.recommendation_reason}")

if travel_plan.flight_recommendation:
    print("\nRecommended Flight:")
    print(f"- Airline: {travel_plan.flight_recommendation.airline}")
    print(f"- Route: {travel_plan.flight_recommendation.origin} to {travel_plan.flight_recommendation.destination}")
    print(f"- Dates: {travel_plan.flight_recommendation.departure_date} to {travel_plan.flight_recommendation.return_date}")
    print(f"- Price: ${travel_plan.flight_recommendation.price}")
    print(f"- Reason: {travel_plan.flight_recommendation.recommendation_reason}")

print("\nList of activities:")
for activity in travel_plan.activities:
    print(f"- {activity}")

print("\nList of notes:")
for note in travel_plan.notes:
    print(f"- {note}")