## =====================================
# ADVANCED AI INSIGHTS
# =====================================

def generate_ai_insights(
    athlete_data,
    sprint_score,
    endurance_score,
    jump_score
):

    risk_alerts = []

    recommendations = []

    # =================================
    # SIMULATED RECOVERY DATA
    # =================================

    fatigue_level = 82

    training_hours = 6

    sleep_hours = 5

    heart_rate = 102

    performance_change = -12

    # =================================
    # FATIGUE ANALYSIS
    # =================================

    if fatigue_level >= 80:

        risk_alerts.append(
            "High fatigue detected"
        )

        recommendations.append(
            "Recovery session required"
        )

        recommendations.append(
            "Reduce training intensity"
        )

    # =================================
    # OVERTRAINING ANALYSIS
    # =================================

    if training_hours >= 5 and sleep_hours < 6:

        risk_alerts.append(
            "Possible training overload"
        )

        recommendations.append(
            "Increase recovery sleep"
        )

        recommendations.append(
            "Add light recovery workouts"
        )

    # =================================
    # HEART RATE ANALYSIS
    # =================================

    if heart_rate >= 100:

        risk_alerts.append(
            "Elevated heart rate detected"
        )

        recommendations.append(
            "Monitor cardiovascular recovery"
        )

    # =================================
    # PERFORMANCE DECLINE
    # =================================

    if performance_change <= -10:

        risk_alerts.append(
            "Performance decline detected"
        )

        recommendations.append(
            "Review current training plan"
        )

    # =================================
    # LOW ENDURANCE
    # =================================

    if endurance_score < 65:

        risk_alerts.append(
            "Low endurance capacity"
        )

        recommendations.append(
            "Add aerobic conditioning"
        )

    # =================================
    # INJURY RISK SCORE
    # =================================

    injury_risk_score = 0

    if fatigue_level >= 80:
        injury_risk_score += 30

    if training_hours >= 5:
        injury_risk_score += 25

    if sleep_hours < 6:
        injury_risk_score += 20

    if performance_change <= -10:
        injury_risk_score += 25

    # =================================
    # RISK STATUS
    # =================================

    if injury_risk_score >= 70:

        injury_status = "HIGH RISK"

    elif injury_risk_score >= 40:

        injury_status = "MODERATE RISK"

    else:

        injury_status = "LOW RISK"

    # =================================
    # PERFORMANCE STATUS
    # =================================

    average_score = (

        sprint_score +

        endurance_score +

        jump_score

    ) / 3

    if average_score >= 85:

        performance_status = "Elite Performance"

    elif average_score >= 70:

        performance_status = "Advanced Performance"

    else:

        performance_status = "Performance Needs Improvement"

    # =================================
    # RETURN INSIGHTS
    # =================================

    return {

        "risk_alerts": risk_alerts,

        "recommendations": recommendations,

        "injury_risk_score": injury_risk_score,

        "injury_status": injury_status,

        "average_score": round(
            average_score,
            2
        ),

        "performance_status": performance_status
    }