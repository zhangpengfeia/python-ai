from fastapi import APIRouter
from agent.tools.api_weather import api_weather
from agent.tools.api_user_location import api_city

router = APIRouter()

@router.get("/weather")
async def get_weather():
    city_info = api_city()
    weather = api_weather(city_info["location_id"])
    return weather

@router.get("/location")
async def get_location():
    city_info = api_city()
    return {
        "city": city_info["city"],
        "region": city_info["city_region"],
        "location_id": city_info["location_id"]
    }