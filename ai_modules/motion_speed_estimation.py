# =====================================
# MOTION SPEED ESTIMATION
# =====================================

def estimate_speed(athlete_data):

    sprint_score = athlete_data.get(
        "sprint_score",
        0
    )

    if sprint_score >= 90:

        speed = "Excellent Speed"

    elif sprint_score >= 75:

        speed = "Good Speed"

    else:

        speed = "Needs Speed Improvement"

    return speed