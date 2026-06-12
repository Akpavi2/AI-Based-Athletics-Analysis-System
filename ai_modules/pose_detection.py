# =====================================
# POSE DETECTION MODULE
# =====================================

def detect_pose(athlete_data):
    """
    Basic pose analysis module
    for deployment version.
    """

    balance_score = athlete_data.get(
        "balance_score",
        50
    )

    if balance_score >= 85:

        posture = "Excellent Posture"

    elif balance_score >= 70:

        posture = "Good Posture"

    else:

        posture = "Posture Needs Improvement"

    return {

        "balance_score": balance_score,

        "posture": posture

    }