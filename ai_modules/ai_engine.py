# =====================================
# AI ENGINE (MASTER BRAIN SYSTEM)
# =====================================

# Core AI Modules
from ai_modules.ai_recommendation_engine import generate_recommendations
from ai_modules.training_plan_generator import generate_training_plan
from ai_modules.ai_feedback_report_system import generate_feedback_report
from ai_modules.advanced_ai_insights import generate_ai_insights

# Performance Modules
from ai_modules.athlete_progress_tracker import get_progress_analysis
from ai_modules.goal_tracking_system import track_goals

# Biomechanics / CV Modules
from ai_modules.pose_detection import detect_pose
from ai_modules.running_form_analysis import analyze_running_form
from ai_modules.stride_analysis import analyze_stride
from ai_modules.knee_angle_tracking import track_knee_angle
from ai_modules.motion_speed_estimation import estimate_speed
# from ai_modules.video_analysis import analyze_video


# =====================================
# MASTER AI CONTROLLER FUNCTION
# =====================================

def get_complete_ai_report(
    athlete_data,
    sprint_score,
    endurance_score,
    jump_score,
    video_path=None

):
    """
    MASTER FUNCTION
    This connects ALL AI systems into one output
    """

    # ==============================
    # 1. CORE RECOMMENDATIONS
    # ==============================

    recommendations = generate_recommendations(
        sprint_score,
        endurance_score,
        jump_score
    )

    # ==============================
    # 2. TRAINING PLAN
    # ==============================

    training_plan = generate_training_plan(
        sprint_score,
        endurance_score,
        jump_score
    )

    # ==============================
    # 3. AI FEEDBACK REPORT
    # ==============================

    feedback_report = generate_feedback_report(
        athlete_data,
        sprint_score,
        endurance_score,
        jump_score
    )

    # ==============================
    # 4. ADVANCED INSIGHTS
    # ==============================

    insights = generate_ai_insights(
        athlete_data,
        sprint_score,
        endurance_score,
        jump_score
    )

    # ==============================
    # 5. PROGRESS ANALYSIS
    # ==============================

    progress = get_progress_analysis(
        athlete_data
    )

    # ==============================
    # 6. GOAL TRACKING
    # ==============================

    goals = track_goals(
        sprint_score,
        endurance_score,
        jump_score
    )

    # ==============================
    # 7. BIOMECHANICS ANALYSIS (CV)
    # ==============================

    if video_path:

        biomechanics = {

            "pose": detect_pose(video_path),

            "running_form": analyze_running_form(video_path),

            "stride": analyze_stride(video_path),

            "knee_angle": track_knee_angle(video_path),

            "speed": estimate_speed(video_path)

        }
    else:

        biomechanics = {
            "message": "No video uploaded"
        }

    # ==============================
    # FINAL OUTPUT PACKAGE
    # ==============================

    

    return {
        "recommendations": recommendations,
        "training_plan": training_plan,
        "feedback_report": feedback_report,
        "insights": insights,
        "progress": progress,
        "goals": goals,
        "biomechanics": biomechanics
    }