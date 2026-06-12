# # =====================================
# # ATHLETE PROFILE
# # =====================================

# athlete_name = "Rahul"

# event = "100m"

# weakness = "Acceleration"

# # =====================================
# # TRAINING PLAN STORAGE
# # =====================================

# training_plan = {}

# # =====================================
# # SPRINTER PLAN
# # =====================================

# if event == "100m":

#     training_plan = {

#         "Monday": [
#             "Sprint Drills",
#             "Explosive Starts",
#             "Core Training"
#         ],

#         "Tuesday": [
#             "Resistance Sprinting",
#             "Recovery Stretching"
#         ],

#         "Wednesday": [
#             "Speed Endurance",
#             "Leg Strength Training"
#         ],

#         "Thursday": [
#             "Hill Sprints",
#             "Mobility Training"
#         ],

#         "Friday": [
#             "Reaction Time Drills",
#             "Acceleration Practice"
#         ],

#         "Saturday": [
#             "Light Recovery Run",
#             "Flexibility Training"
#         ],

#         "Sunday": [
#             "Rest Day"
#         ]
#     }

# # =====================================
# # ENDURANCE RUNNER PLAN
# # =====================================

# elif event == "800m":

#     training_plan = {

#         "Monday": [
#             "Long-distance Running",
#             "Breathing Exercises"
#         ],

#         "Tuesday": [
#             "Interval Running",
#             "Core Training"
#         ],

#         "Wednesday": [
#             "Tempo Run",
#             "Recovery Stretching"
#         ],

#         "Thursday": [
#             "Cardio Endurance",
#             "Leg Stability Work"
#         ],

#         "Friday": [
#             "Aerobic Conditioning",
#             "Mobility Exercises"
#         ],

#         "Saturday": [
#             "Light Jogging",
#             "Yoga Recovery"
#         ],

#         "Sunday": [
#             "Rest Day"
#         ]
#     }

# # =====================================
# # LONG JUMP PLAN
# # =====================================

# elif event == "Long Jump":

#     training_plan = {

#         "Monday": [
#             "Plyometric Jumps",
#             "Sprint Warmup"
#         ],

#         "Tuesday": [
#             "Explosive Power Drills",
#             "Core Stability"
#         ],

#         "Wednesday": [
#             "Jump Technique Practice",
#             "Landing Drills"
#         ],

#         "Thursday": [
#             "Acceleration Training",
#             "Leg Strength"
#         ],

#         "Friday": [
#             "Bounding Exercises",
#             "Mobility Work"
#         ],

#         "Saturday": [
#             "Recovery Session"
#         ],

#         "Sunday": [
#             "Rest Day"
#         ]
#     }

# # =====================================
# # GENERAL ATHLETE PLAN
# # =====================================

# else:

#     training_plan = {

#         "Monday": [
#             "General Conditioning"
#         ],

#         "Tuesday": [
#             "Mobility Exercises"
#         ],

#         "Wednesday": [
#             "Strength Training"
#         ],

#         "Thursday": [
#             "Cardio Session"
#         ],

#         "Friday": [
#             "Technique Training"
#         ],

#         "Saturday": [
#             "Recovery Work"
#         ],

#         "Sunday": [
#             "Rest Day"
#         ]
#     }

# # =====================================
# # DISPLAY PLAN
# # =====================================

# print("\n===== AI TRAINING PLAN =====")

# print(f"\nAthlete: {athlete_name}")

# print(f"Event: {event}")

# print(f"Weakness Focus: {weakness}")

# # =====================================
# # WEEKLY PLAN
# # =====================================

# for day, exercises in training_plan.items():

#     print(f"\n{day.upper()}")

#     for exercise in exercises:

#         print(f"• {exercise}")

# =====================================
# AI RECOMMENDATION ENGINE
# =====================================

def generate_recommendations(

    sprint_score,
    endurance_score,
    jump_score

):

    recommendations = []

    # =====================================
    # SPRINT ANALYSIS
    # =====================================

    if sprint_score < 80:

        recommendations.append(
            "Improve sprint intervals"
        )

        recommendations.append(
            "Add resistance sprint training"
        )

    # =====================================
    # ENDURANCE ANALYSIS
    # =====================================

    if endurance_score < 80:

        recommendations.append(
            "Increase long-distance running"
        )

        recommendations.append(
            "Add stamina workouts"
        )

    # =====================================
    # JUMP ANALYSIS
    # =====================================

    if jump_score < 80:

        recommendations.append(
            "Add plyometric exercises"
        )

        recommendations.append(
            "Improve lower body strength"
        )

    # =====================================
    # IF PERFORMANCE IS GOOD
    # =====================================

    if len(recommendations) == 0:

        recommendations.append(
            "Excellent overall athletic performance"
        )

    return recommendations