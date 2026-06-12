# =====================================
# ATHLETE PROGRESS TRACKER
# =====================================

def get_progress_analysis(
    athlete_data
):

    # =================================
    # SAMPLE HISTORY
    # =================================

    sprint_scores = [70, 74, 78, 82, 86]

    endurance_scores = [65, 68, 72, 76, 80]

    jump_scores = [60, 63, 67, 71, 75]

    weeks = [

        "Week 1",

        "Week 2",

        "Week 3",

        "Week 4",

        "Week 5"
    ]

    # =================================
    # IMPROVEMENT CALCULATION
    # =================================

    previous_sprint = sprint_scores[-2]

    current_sprint = sprint_scores[-1]

    improvement = (

        (
            current_sprint -
            previous_sprint
        )

        / previous_sprint

    ) * 100

    # =================================
    # STATUS
    # =================================

    if improvement > 10:

        status = "Excellent Improvement"

    elif improvement > 5:

        status = "Good Progress"

    else:

        status = "Needs More Training"

    # =================================
    # RETURN DATA
    # =================================

    return {

        "weeks": weeks,

        "sprint_scores": sprint_scores,

        "endurance_scores": endurance_scores,

        "jump_scores": jump_scores,

        "improvement": round(
            improvement,
            2
        ),

        "status": status
    }