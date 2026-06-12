# =====================================
# GOAL TRACKING SYSTEM
# =====================================

def track_goals(
    sprint_score,
    endurance_score,
    jump_score
):

    # =================================
    # TARGET GOALS
    # =================================

    sprint_goal = 95

    endurance_goal = 95

    jump_goal = 95

    workout_streak = 12

    # =================================
    # PROGRESS CALCULATIONS
    # =================================

    sprint_progress = (
        sprint_score /
        sprint_goal
    ) * 100

    endurance_progress = (
        endurance_score /
        endurance_goal
    ) * 100

    jump_progress = (
        jump_score /
        jump_goal
    ) * 100

    # =================================
    # OVERALL PROGRESS
    # =================================

    overall_progress = (

        sprint_progress +

        endurance_progress +

        jump_progress

    ) / 3

    # =================================
    # MILESTONE STATUS
    # =================================

    if overall_progress >= 90:

        milestone = (
            "Elite Goal Near Completion"
        )

    elif overall_progress >= 75:

        milestone = (
            "Strong Progress Achieved"
        )

    elif overall_progress >= 50:

        milestone = (
            "Good Improvement Stage"
        )

    else:

        milestone = (
            "Initial Development Stage"
        )

    # =================================
    # MOTIVATION MESSAGE
    # =================================

    if workout_streak >= 30:

        motivation = (
            "Outstanding consistency!"
        )

    elif workout_streak >= 15:

        motivation = (
            "Great discipline maintained!"
        )

    elif workout_streak >= 7:

        motivation = (
            "Strong weekly consistency!"
        )

    else:

        motivation = (
            "Keep building your streak!"
        )

    # =================================
    # RETURN DATA
    # =================================

    return {

        "sprint_progress":
            round(
                sprint_progress,
                2
            ),

        "endurance_progress":
            round(
                endurance_progress,
                2
            ),

        "jump_progress":
            round(
                jump_progress,
                2
            ),

        "overall_progress":
            round(
                overall_progress,
                2
            ),

        "milestone":
            milestone,

        "workout_streak":
            workout_streak,

        "motivation":
            motivation
    }