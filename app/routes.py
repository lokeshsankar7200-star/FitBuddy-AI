import os
import json

from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from google import genai

load_dotenv()

router = APIRouter()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=API_KEY)


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "FitBuddy backend is working!"
    }


@router.post("/generate-plan")
def generate_plan(data: dict):

    name = data.get("name", "User")
    age = data.get("age", "")
    activity = data.get("activity", "")
    goal = data.get("goal", "")

    prompt = f"""
Create a safe, age-appropriate 7-day general fitness and wellness plan.

User:
Name: {name}
Age: {age}
Activity level: {activity}
Goal: {goal}

Return ONLY valid JSON.

Use exactly this structure:

{{
  "days": [
    {{
      "day": 1,
      "title": "Day 1",
      "activities": [
        "Activity 1",
        "Activity 2"
      ],
      "tip": "Simple wellness tip"
    }}
  ]
}}

Include exactly 7 days.

Keep activities simple and safe.
Include rest or easy-recovery activities where appropriate.
Do not recommend restrictive diets, extreme exercise,
weight-loss targets, or body comparisons.
"""

    try:

        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        text = interaction.output_text.strip()

        plan = json.loads(text)

        return {
            "name": name,
            "age": age,
            "activity": activity,
            "goal": goal,
            "plan": plan
        }

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Gemini returned an invalid plan format."
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini API error: {str(error)}"
        )