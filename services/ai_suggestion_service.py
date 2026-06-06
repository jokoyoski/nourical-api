import json
from urllib.parse import quote
from datetime import date, timedelta
from openai import OpenAI
from config import Config

DAYS_ORDER = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def get_week_start():
    d = date.today()
    return d - timedelta(days=d.weekday())

def day_to_date(day_name):
    week_start = get_week_start()
    offset = DAYS_ORDER.index(day_name.lower())
    return (week_start + timedelta(days=offset)).isoformat()

_client = None

def get_client():
    global _client
    if _client is None:
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured")
        _client = OpenAI(api_key=Config.OPENAI_API_KEY)
    return _client

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def get_avatar_url(food_name):
    encoded = quote(food_name)
    return f"https://ui-avatars.com/api/?name={encoded}&size=300&background=4CAF50&color=fff&rounded=true&bold=true"

def inject_images(meal_plan):
    for day in DAYS:
        if day not in meal_plan:
            continue
        actual_date = day_to_date(day)
        for meal_type, meal_data in meal_plan[day].items():
            meal_time = meal_data.get("time", "00:00")
            meal_data["date"] = actual_date
            meal_data["meal_datetime"] = f"{actual_date}T{meal_time}:00"
            for food in meal_data.get("foods", []):
                name = food.get("name", "food")
                food["image_url"] = get_food_image(name)
                food["date"] = actual_date
                food["meal_datetime"] = f"{actual_date}T{meal_time}:00"
                food.pop("image_keyword", None)
    return meal_plan

def build_prompt(onboarding, meal_times, foods_to_avoid=None):
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

    avoid_str = ", ".join(foods_to_avoid) if foods_to_avoid else "none"

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
- Foods to NEVER include: {avoid_str}

Generate a full 7-day meal plan. For each day ({days_str}), include one food item per meal slot ({meal_slots_str}).

Each food item must include:
- name (string)
- calories (number)
- protein_g (number)
- carbs_g (number)
- fat_g (number)
- description (one short sentence)
- image_keyword (1-2 simple English words best describing the food visually, e.g. "oatmeal", "jollof rice", "grilled chicken", "pancakes")

IMPORTANT rules:
- NEVER include any of the foods listed under "Foods to NEVER include" — not as a main item, ingredient, or side
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


def build_targets_prompt(onboarding):
    return f"""You are a professional nutritionist AI. Based on the user profile below, recommend their ideal daily calorie and macro targets.

User Profile:
- Age: {onboarding.get('age')}
- Gender: {onboarding.get('gender')}
- Weight: {onboarding.get('weight_kg')} kg
- Height: {onboarding.get('height_cm')} cm
- Target Weight: {onboarding.get('target_weight_kg')} kg
- Activity Level: {onboarding.get('activity_level')}
- Main Goal: {onboarding.get('main_goal')}
- Health Conditions: {onboarding.get('health_conditions') or 'none'}
- Dietary Preferences: {onboarding.get('dietary_preferences') or 'none'}
- Region: {onboarding.get('region')}

Return ONLY valid JSON with no extra text:
{{
  "calories": <number>,
  "protein_g": <number>,
  "carbs_g": <number>,
  "fat_g": <number>,
  "reasoning": "<one short paragraph explaining why these targets suit this person>"
}}
"""


def get_food_image(dish_name):
    try:
        import urllib.request as _urllib
        import urllib.parse as _parse
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={_parse.quote(dish_name)}"
        with _urllib.urlopen(url, timeout=4) as resp:
            data = json.loads(resp.read())
        meals = data.get('meals') or []
        if meals:
            return meals[0].get('strMealThumb', '') or get_avatar_url(dish_name)
    except Exception:
        pass
    return get_avatar_url(dish_name)


_cuisine_cache = {}


class AISuggestionService:
    @staticmethod
    def get_cuisines_by_region(region):
        if region in _cuisine_cache:
            return _cuisine_cache[region]

        prompt = f"""You are a food and culture expert. List the most popular and well-known cuisines (cooking styles or food traditions) from the region: "{region}".

Return ONLY valid JSON with no extra text:
{{
  "cuisines": [
    {{
      "value": "<lowercase_slug e.g. nigerian>",
      "label": "<Display Name>",
      "description": "<2-4 iconic dishes, comma separated>",
      "sample_dish": "<one iconic dish name for the image>"
    }}
  ]
}}

Rules:
- Return between 4 and 10 cuisines relevant to that region
- value must be a lowercase slug (underscores allowed, no spaces)
- sample_dish should be the most iconic single dish from that cuisine
"""
        response = get_client().chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a food and culture expert. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        cuisines = data.get("cuisines", [])
        for c in cuisines:
            c["image_url"] = get_food_image(c.pop("sample_dish", c["label"]))
        _cuisine_cache[region] = cuisines
        return cuisines

    @staticmethod
    def get_daily_targets(onboarding):
        prompt = build_targets_prompt(onboarding)
        response = get_client().chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional nutritionist AI. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return {
            'calories': float(data['calories']),
            'protein_g': float(data['protein_g']),
            'carbs_g': float(data['carbs_g']),
            'fat_g': float(data['fat_g']),
            'reasoning': data.get('reasoning', '')
        }

    @staticmethod
    def get_meal_plan(onboarding, meal_times, foods_to_avoid=None):
        prompt = build_prompt(onboarding, meal_times, foods_to_avoid)

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
