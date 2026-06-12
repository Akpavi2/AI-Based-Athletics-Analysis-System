# =====================================
# AI FEEDBACK REPORT SYSTEM
# =====================================

def generate_feedback_report(
    athlete_data,
    sprint_score,
    endurance_score,
    jump_score
):

    strengths = []
    weaknesses = []
    recommendations = []

    # =================================
    # SPRINT ANALYSIS
    # =================================

    if sprint_score >= 85:

        strengths.append(
            "Excellent sprint speed"
        )

    else:

        weaknesses.append(
            "Sprint performance needs improvement"
        )

        recommendations.append(
            "Add sprint interval training"
        )

    # =================================
    # ENDURANCE ANALYSIS
    # =================================

    if endurance_score >= 85:

        strengths.append(
            "Strong endurance capacity"
        )

    else:

        weaknesses.append(
            "Moderate endurance"
        )

        recommendations.append(
            "Increase aerobic sessions"
        )

        recommendations.append(
            "Add recovery cardio training"
        )

    # =================================
    # JUMP ANALYSIS
    # =================================

    if jump_score >= 85:

        strengths.append(
            "Strong jumping ability"
        )

    else:

        weaknesses.append(
            "Explosive power needs improvement"
        )

        recommendations.append(
            "Add plyometric exercises"
        )

    # =================================
    # OVERALL SCORE
    # =================================

    overall_score = (
        sprint_score +
        endurance_score +
        jump_score
    ) / 3

    # =================================
    # STATUS
    # =================================

    if overall_score >= 90:

        status = "Elite Athletic Performance"

    elif overall_score >= 75:

        status = "Advanced Athletic Level"

    elif overall_score >= 60:

        status = "Intermediate Athletic Development"

    else:

        status = "Beginner Development Stage"

    # =================================
    # RETURN REPORT
    # =================================

    return {

        "strengths": strengths,

        "weaknesses": weaknesses,

        "recommendations": recommendations,

        "overall_score": round(
            overall_score,
            2
        ),

        "status": status
    }