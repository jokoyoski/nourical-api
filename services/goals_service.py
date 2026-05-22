from enum import Enum


class GoalType(str, Enum):
    LOSE_WEIGHT = "lose_weight"
    MAINTAIN_WEIGHT = "maintain_weight"
    GAIN_MUSCLE = "gain_muscle"
    IMPROVE_OVERALL_HEALTH = "improve_overall_health"
    MANAGE_CONDITIONS = "manage_conditions"

class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"
    EXTREMELY_ACTIVE = "extremely_active"

class Region(str, Enum):
    EUROPE = "europe"
    NORTH_AMERICA = "north_america"
    LATIN_AMERICA = "latin_america"
    SOUTH_AMERICA = "south_america"
    EAST_AFRICA = "east_africa"
    SOUTHERN_AFRICA = "southern_africa"
    WEST_AFRICA = "west_africa"
    NORTH_AFRICA = "north_africa"
    ASIA = "asia"
    OCEANIA = "oceania"

class Cuisine(str, Enum):
    NIGERIAN = "nigerian"
    GHANAIAN = "ghanaian"
    SENEGALESE = "senegalese"
    IVORIAN = "ivorian"
    CAMEROONIAN = "cameroonian"

class HealthCondition(str, Enum):
    PREGNANCY = "pregnancy"
    DIABETES = "diabetes"
    HIGH_BLOOD_PRESSURE = "high_blood_pressure"
    HIGH_CHOLESTEROL = "high_cholesterol"
    CANCER = "cancer"
    HEART_DISEASE = "heart_disease"

class GoalsService:
    @staticmethod
    def get_goals():
        goals = [
            {
                "value": GoalType.LOSE_WEIGHT.value,
                "label": "Lose Weight",
                "description": "Reduce body weight through calorie deficit and exercise",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779392575/lose_weight_rtxnav.png"
            },
            {
                "value": GoalType.MAINTAIN_WEIGHT.value,
                "label": "Maintain Weight",
                "description": "Keep current weight stable with balanced nutrition",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779392575/maintain_weight_nusozf.png"
            },
            {
                "value": GoalType.GAIN_MUSCLE.value,
                "label": "Gain Muscle",
                "description": "Build muscle mass through strength training and protein intake",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779392575/gain_muscle_xa6uqz.png"
            },
            {
                "value": GoalType.IMPROVE_OVERALL_HEALTH.value,
                "label": "Improve Overall Health",
                "description": "Enhance general wellness through balanced lifestyle choices",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779392575/improve_overall_health_fp2mtt.png"
            },
            {
                "value": GoalType.MANAGE_CONDITIONS.value,
                "label": "Manage Conditions",
                "description": "Manage specific health conditions through tailored nutrition",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779392575/manage_conditions_yaxlxr.png"
            }
        ]
        return goals
    
    @staticmethod
    def get_activity_levels():
        activity_levels = [
            {
                "value": ActivityLevel.SEDENTARY.value,
                "label": "Sedentary",
                "description": "Desk job, minimal exercise"
            },
            {
                "value": ActivityLevel.LIGHTLY_ACTIVE.value,
                "label": "Lightly Active",
                "description": "Light exercise 1-3x/week"
            },
            {
                "value": ActivityLevel.MODERATELY_ACTIVE.value,
                "label": "Moderately Active",
                "description": "Exercise 3-5x/week"
            },
            {
                "value": ActivityLevel.VERY_ACTIVE.value,
                "label": "Very Active",
                "description": "Intense exercise 6-7x/week"
            },
            {
                "value": ActivityLevel.EXTREMELY_ACTIVE.value,
                "label": "Extremely Active",
                "description": "Physical job + training"
            }
        ]
        return activity_levels
    
    @staticmethod
    def get_regions():
        regions = [
            {
                "value": Region.EUROPE.value,
                "label": "Europe",
                "continent": "Europe"
            },
            {
                "value": Region.NORTH_AMERICA.value,
                "label": "North America",
                "continent": "America"
            },
            {
                "value": Region.LATIN_AMERICA.value,
                "label": "Latin America",
                "continent": "America"
            },
            {
                "value": Region.SOUTH_AMERICA.value,
                "label": "South America",
                "continent": "America"
            },
            {
                "value": Region.EAST_AFRICA.value,
                "label": "East Africa",
                "continent": "Africa"
            },
            {
                "value": Region.SOUTHERN_AFRICA.value,
                "label": "Southern Africa",
                "continent": "Africa"
            },
            {
                "value": Region.WEST_AFRICA.value,
                "label": "West Africa",
                "continent": "Africa"
            },
            {
                "value": Region.NORTH_AFRICA.value,
                "label": "North Africa",
                "continent": "Africa"
            },
            {
                "value": Region.ASIA.value,
                "label": "Asia",
                "continent": "Asia"
            },
            {
                "value": Region.OCEANIA.value,
                "label": "Oceania",
                "continent": "Oceania"
            }
        ]
        return regions
    
    @staticmethod
    def get_cuisines():
        cuisines = [
            {
                "value": Cuisine.NIGERIAN.value,
                "label": "Nigerian",
                "description": "Jollof rice, Beans, Poundo yam"
            },
            {
                "value": Cuisine.GHANAIAN.value,
                "label": "Ghanaian",
                "description": "Fufu, Light soup, waakye, kelewele"
            },
            {
                "value": Cuisine.SENEGALESE.value,
                "label": "Senegalese",
                "description": "Mafe, yasse, Poundo yam"
            },
            {
                "value": Cuisine.IVORIAN.value,
                "label": "Ivorian",
                "description": "Attieke, Aloco"
            },
            {
                "value": Cuisine.CAMEROONIAN.value,
                "label": "Cameroonian",
                "description": "Ndole, eru, koki, suya"
            }
        ]
        return cuisines
    
    @staticmethod
    def get_health_conditions():
        health_conditions = [
            {
                "value": HealthCondition.PREGNANCY.value,
                "label": "Pregnancy",
                "description": "Trimester aware"
            },
            {
                "value": HealthCondition.DIABETES.value,
                "label": "Diabetes",
                "description": "Blood sugar control"
            },
            {
                "value": HealthCondition.HIGH_BLOOD_PRESSURE.value,
                "label": "High blood pressure",
                "description": "Sodium management"
            },
            {
                "value": HealthCondition.HIGH_CHOLESTEROL.value,
                "label": "High cholesterol",
                "description": "Heart healthy fast"
            },
            {
                "value": HealthCondition.CANCER.value,
                "label": "Cancer",
                "description": "During or post treatment"
            },
            {
                "value": HealthCondition.HEART_DISEASE.value,
                "label": "Heart Disease",
                "description": "Trimester aware"
            }
        ]
        return health_conditions
