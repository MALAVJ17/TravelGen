import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

# Configure your Gemini API key
genai.configure(api_key = os.getenv("GEMINI_API_KEY") )

model = genai.GenerativeModel("gemini-2.0-flash")  # or "gemini-2.0-flash" if available via API

def generate_llm_itinerary(location, days, interests, weather_info, people, currency, budget):
    prompt = (
    f"You are a professional travel planner. Generate a clean, well-formatted {days}-day itinerary for {people} travelers with the budget of {budget}{currency} "
    f"visiting {location}.\n\n"
    
    f"Details:\n"
    f"- Interests: {', '.join(interests)}\n"
    f"- Current weather: {weather_info}\n\n"

    f"Formatting instructions:\n"
    f"- Use headings like Day 1, Day 2, etc., and format them in bold (use HTML: <b>Day 1</b>).\n"
    f"- For each day, list exactly 3 unique and relevant activities.\n"
    f"- Format activities using • followed by the activity name and a short description.\n"
    f"- Do NOT use asterisk (*) or hyphen (-) symbols.\n"
    f"- Avoid repeating activities. Tailor all suggestions based on the interests and weather.\n"
    f"- Ensure the output is clean, readable, and properly structured.\n\n"

    f"Please begin generating the itinerary below:\n"
)



    response = model.generate_content(prompt)
    return response.text
