# =====================================
# IMPORT LIBRARIES
# =====================================

import cv2
import mediapipe as mp

# =====================================
# INITIALIZE MEDIAPIPE
# =====================================

mp_pose = mp.solutions.pose

# =====================================
# RUNNING FORM ANALYSIS
# =====================================

def analyze_running_form(video_path):

    pose = mp_pose.Pose(
        static_image_mode=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(video_path)

    frame_count = 0

    posture_scores = []
    balance_scores = []

    frame_number = 0

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            break

        frame_number += 1

        if frame_number % 10 != 0:
            continue

        # process every 10th frame
        if frame_count % 10 != 0:
            continue

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = pose.process(rgb_frame)

        if results.pose_landmarks:

            landmarks = results.pose_landmarks.landmark

            left_shoulder = landmarks[
                mp_pose.PoseLandmark.LEFT_SHOULDER
            ]

            right_shoulder = landmarks[
                mp_pose.PoseLandmark.RIGHT_SHOULDER
            ]

            left_hip = landmarks[
                mp_pose.PoseLandmark.LEFT_HIP
            ]

            right_hip = landmarks[
                mp_pose.PoseLandmark.RIGHT_HIP
            ]

            shoulder_level = abs(
                left_shoulder.y -
                right_shoulder.y
            )

            hip_level = abs(
                left_hip.y -
                right_hip.y
            )

            posture_scores.append(
                shoulder_level
            )

            balance_scores.append(
                hip_level
            )

    cap.release()

    pose.close()

    if len(posture_scores) == 0:

        return {
            "posture": "No Data",
            "arm_drive": "No Data",
            "balance": "No Data"
        }

    avg_posture = sum(
        posture_scores
    ) / len(posture_scores)

    avg_balance = sum(
        balance_scores
    ) / len(balance_scores)

    # =====================================
    # POSTURE
    # =====================================

    if avg_posture < 0.03:
        posture = "Excellent Posture"
    elif avg_posture < 0.06:
        posture = "Good Posture"
    else:
        posture = "Needs Improvement"

    # =====================================
    # BALANCE
    # =====================================

    if avg_balance < 0.03:
        balance = "Balanced Running"
    elif avg_balance < 0.06:
        balance = "Moderately Stable"
    else:
        balance = "Unstable Running"

    # =====================================
    # ARM DRIVE
    # =====================================

    if avg_posture < 0.03:
        arm_drive = "Strong Arm Drive"
    elif avg_posture < 0.06:
        arm_drive = "Average Arm Drive"
    else:
        arm_drive = "Needs Improvement"

    return {

        "posture": posture,

        "arm_drive": arm_drive,

        "balance": balance,

        "posture_score": round(
            avg_posture,
            4
        ),

        "balance_score": round(
            avg_balance,
            4
        )
    }