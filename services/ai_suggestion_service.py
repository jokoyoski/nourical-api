import json
from urllib.parse import quote
from openai import OpenAI
from config import Config

_client = None

def get_client():
    global _client
    if _client is None:
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured")
        _client = OpenAI(api_key=Config.OPENAI_API_KEY)
    return _client

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday"]

def get_avatar_url(food_name):
    encoded = quote(food_name)
    return f"https://ui-avatars.com/api/?name={encoded}&size=300&background=4CAF50&color=fff&rounded=true&bold=true"

def inject_images(meal_plan):
    for day in DAYS:
        if day not in meal_plan:
            continue
        for meal_type, meal_data in meal_plan[day].items():
            for food in meal_data.get("foods", []):
                name = food.get("name", "food")
                food["image_url"] = get_avatar_url(name)
                food.pop("image_keyword", None)
    return meal_plan

def build_prompt(onboarding, meal_times):
    health_conditions = onboarding.get("health_conditions") or "none"
    dietary_preferences = onboarding.get("dietary_preferences") or "none"
    cuisine_preferences = onboarding.get("cuisine_preferences") or "none"
    region = onboarding.get("region") or "global"
    main_goal = onboarding.get("main_goal") or "eat healthy"
    age = onboarding.get("age")
    gender = onboarding.get("gender")
    weight_kg = onboarding.get("weight_kg")
    target_weight_kg = onboarding.get("target_weight_kg")
    activity_level = onboarding.get("activity_level") or "moderate"

    meal_slots = [
        f"{mt['meal_type']} at {mt['time']}"
        for mt in meal_times if mt.get("enabled", True)
    ]
    meal_slots_str = ", ".join(meal_slots) if meal_slots else "breakfast, lunch, dinner"

    days_str = ", ".join(DAYS)

    prompt = f"""You are a professional nutritionist AI. Create a personalised weekly meal plan for this user:

User Profile:
- Age: {age}
- Gender: {gender}
- Weight: {weight_kg} kg
- Target Weight: {target_weight_kg} kg
- Activity Level: {activity_level}
- Main Goal: {main_goal}
- Region: {region}
- Health Conditions: {health_conditions}
- Dietary Preferences: {dietary_preferences}
- Cuisine Preferences: {cuisine_preferences}
- Meal Times: {meal_slots_str}

Generate a Monday to Friday meal plan. For each day ({days_str}), include one food item per meal slot ({meal_slots_str}).

Each food item must include:
- name (string)
- calories (number)
- protein_g (number)
- carbs_g (number)
- fat_g (number)
- description (one short sentence)
- image_keyword (1-2 simple English words best describing the food visually, e.g. "oatmeal", "jollof rice", "grilled chicken", "pancakes")

IMPORTANT rules:
- Respect all health conditions (e.g. diabetes = low sugar, heart disease = low sodium/fat)
- Prefer foods from the user's region and cuisine preferences
- Vary the meals across the week (no repeats)
- Keep calorie targets appropriate for the user's goal

Return ONLY valid JSON in exactly this structure, no extra text:
{{
  "monday": {{
    "breakfast": {{ "time": "07:00", "foods": [{{"name": "...", "calories": 0, "protein_g": 0, "carbs_g": 0, "fat_g": 0, "description": "..."}}] }},
    "lunch": {{ "time": "12:00", "foods": [...] }},
    "dinner": {{ "time": "19:00", "foods": [...] }}
  }},
  "tuesday": {{ ... }},
  "wednesday": {{ ... }},
  "thursday": {{ ... }},
  "friday": {{ ... }}
}}

Replace times with the user's actual meal times: {meal_slots_str}
"""
    return prompt


class AISuggestionService:
    @staticmethod
    def get_meal_plan(onboarding, meal_times):
        prompt = build_prompt(onboarding, meal_times)

        response = get_client().chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional nutritionist AI. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        meal_plan = json.loads(content)
        meal_plan = inject_images(meal_plan)
        return meal_plan
