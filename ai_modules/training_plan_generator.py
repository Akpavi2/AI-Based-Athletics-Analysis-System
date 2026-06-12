# =====================================
# TRAINING PLAN GENERATOR
# =====================================

def generate_training_plan(
    sprint_score,
    endurance_score,
    jump_score
):

    training_plan = {}

    # =====================================
    # DETERMINE WEAKNESSES
    # =====================================

    weaknesses = []

    if sprint_score < 75:
        weaknesses.append("Sprint")

    if endurance_score < 75:
        weaknesses.append("Endurance")

    if jump_score < 75:
        weaknesses.append("Jump")

    # =====================================
    # DETERMINE EVENT
    # =====================================

    if sprint_score >= endurance_score:

        event = "100m"

    else:

        event = "800m"

    # =====================================
    # MONDAY
    # =====================================

    monday = []

    if event == "100m":

        monday.append("Sprint Drills")
        monday.append("Acceleration Training")

    else:

        monday.append("Long Distance Running")
        monday.append("Cardio Conditioning")

    if "Endurance" in weaknesses:

        monday.append("Interval Running")

    training_plan["Monday"] = monday

    # =====================================
    # TUESDAY
    # =====================================

    training_plan["Tuesday"] = [

        "Strength Training",
        "Core Exercises",
        "Mobility Work"
    ]

    # =====================================
    # WEDNESDAY
    # =====================================

    training_plan["Wednesday"] = [

        "Recovery Jog",
        "Stretching",
        "Foam Rolling"
    ]

    # =====================================
    # THURSDAY
    # =====================================

    training_plan["Thursday"] = [

        "Explosive Training",
        "Plyometrics",
        "Sprint Technique"
    ]

    # =====================================
    # FRIDAY
    # =====================================

    training_plan["Friday"] = [

        "Gym Training",
        "Lower Body Strength"
    ]

    # =====================================
    # SATURDAY
    # =====================================

    training_plan["Saturday"] = [

        "Performance Session",
        "Event Specific Drills"
    ]

    # =====================================
    # SUNDAY
    # =====================================

    training_plan["Sunday"] = [

        "Rest Day",
        "Recovery Walk"
    ]

    return training_plan