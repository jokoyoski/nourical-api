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

class HealthCondition(str, Enum):
    PREGNANCY = "pregnancy"
    DIABETES = "diabetes"
    HIGH_BLOOD_PRESSURE = "high_blood_pressure"
    HIGH_CHOLESTEROL = "high_cholesterol"
    CANCER = "cancer"
    HEART_DISEASE = "heart_disease"
    KIDNEY_DISEASE = "kidney_disease"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    NON_BINARY = "non_binary"

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
                "description": "Desk job, minimal exercise",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779475488/desk_mzqrrh.png"
            },
            {
                "value": ActivityLevel.LIGHTLY_ACTIVE.value,
                "label": "Lightly Active",
                "description": "Light exercise 1-3x/week",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779475488/walk_agcrgc.png"
            },
            {
                "value": ActivityLevel.MODERATELY_ACTIVE.value,
                "label": "Moderately Active",
                "description": "Exercise 3-5x/week",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779475488/swim_sgegny.png"
            },
            {
                "value": ActivityLevel.VERY_ACTIVE.value,
                "label": "Very Active",
                "description": "Intense exercise 6-7x/week",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779475488/power_ld5imv.png"
            },
            {
                "value": ActivityLevel.EXTREMELY_ACTIVE.value,
                "label": "Extremely Active",
                "description": "Physical job + training",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779475488/power_ld5imv.png"
            }
        ]
        return activity_levels
    
    @staticmethod
    def get_regions():
        regions = [
            {
                "value": Region.EUROPE.value,
                "label": "Europe",
                "continent": "Europe",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779475661/globe_lt1evx.png"
            },
            {
                "value": Region.NORTH_AMERICA.value,
                "label": "North America",
                "continent": "America",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779475661/globe_lt1evx.png"
            },
            {
                "value": Region.LATIN_AMERICA.value,
                "label": "Latin America",
                "continent": "America",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779475661/globe_lt1evx.png"
            },
            {
                "value": Region.SOUTH_AMERICA.value,
                "label": "South America",
                "continent": "America",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779475661/globe_lt1evx.png"
            },
            {
                "value": Region.EAST_AFRICA.value,
                "label": "East Africa",
                "continent": "Africa",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779475661/globe_lt1evx.png"
            },
            {
                "value": Region.SOUTHERN_AFRICA.value,
                "label": "Southern Africa",
                "continent": "Africa",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779475661/globe_lt1evx.png"
            },
            {
                "value": Region.WEST_AFRICA.value,
                "label": "West Africa",
                "continent": "Africa",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779475661/globe_lt1evx.png"
            },
            {
                "value": Region.NORTH_AFRICA.value,
                "label": "North Africa",
                "continent": "Africa",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779475661/globe_lt1evx.png"
            },
            {
                "value": Region.ASIA.value,
                "label": "Asia",
                "continent": "Asia",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779475661/globe_lt1evx.png"
            },
            {
                "value": Region.OCEANIA.value,
                "label": "Oceania",
                "continent": "Oceania",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779475661/globe_lt1evx.png"
            }
        ]
        return regions
    
    @staticmethod
    def get_health_conditions():
        health_conditions = [
            {
                "value": HealthCondition.PREGNANCY.value,
                "label": "Pregnancy",
                "description": "Trimester aware",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779476154/pregnant_iimxbp.png"
            },
            {
                "value": HealthCondition.DIABETES.value,
                "label": "Diabetes",
                "description": "Blood sugar control",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779476240/diabets_drpcsm.png"
            },
            {
                "value": HealthCondition.HIGH_BLOOD_PRESSURE.value,
                "label": "High blood pressure",
                "description": "Sodium management",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779476332/bllof_qpk29m.png"
            },
            {
                "value": HealthCondition.HIGH_CHOLESTEROL.value,
                "label": "High cholesterol",
                "description": "Heart healthy fast",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779476152/high_cholestrol_xtlolb.png"
            },
            {
                "value": HealthCondition.CANCER.value,
                "label": "Cancer",
                "description": "During or post treatment",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779476151/cancer_wzehba.png"
            },
            {
                "value": HealthCondition.HEART_DISEASE.value,
                "label": "Heart Disease",
                "description": "Trimester aware",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779476152/heart_pyvnmh.png"
            },
            {
                "value": HealthCondition.KIDNEY_DISEASE.value,
                "label": "Kidney Disease",
                "description": "Kidney health management",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779476153/kidney_od2enp.png"
            },
            {
                "value": HealthCondition.OTHER.value,
                "label": "Other",
                "description": "Other health condition",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779476153/other_mgle0c.png"
            },
            {
                "value": HealthCondition.PREFER_NOT_TO_SAY.value,
                "label": "Prefer Not To Say",
                "description": "Decline to specify",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779476154/prefer_not_say_k9dd3x.png"
            }
        ]
        return health_conditions
    
    @staticmethod
    def get_genders():
        genders = [
            {
                "value": Gender.MALE.value,
                "label": "Male",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779476594/image_ijtcrz.png"
            },
            {
                "value": Gender.FEMALE.value,
                "label": "Female",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779476592/female_ev0usr.png"
            },
            {
                "value": Gender.OTHER.value,
                "label": "Other",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779476597/prfer_bovb2c.png"
            },
            {
                "value": Gender.NON_BINARY.value,
                "label": "Non Binary",
                "icon": "https://res.cloudinary.com/jokoyoski/image/upload/v1779476595/non_binary_tj6agb.png"
            }
        ]
        return genders
