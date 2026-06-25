## =====================================
# IMPORT LIBRARIES
# =====================================

import cv2
import mediapipe as mp
import math

# =====================================
# INITIALIZE MEDIAPIPE
# =====================================

mp_pose = mp.solutions.pose

pose = mp_pose.Pose()

# =====================================
# ANGLE CALCULATION FUNCTION
# =====================================

def calculate_angle(a, b, c):

    ax, ay = a
    bx, by = b
    cx, cy = c

    angle = math.degrees(

        math.atan2(
            cy - by,
            cx - bx
        )

        -

        math.atan2(
            ay - by,
            ax - bx
        )
    )

    angle = abs(angle)

    if angle > 180:

        angle = 360 - angle

    return angle


# =====================================
# KNEE ANGLE TRACKING FUNCTION
# =====================================

def track_knee_angle(video_path):

    cap = cv2.VideoCapture(video_path)

    knee_angles = []

    with mp_pose.Pose(

        static_image_mode=False,

        min_detection_confidence=0.5,

        min_tracking_confidence=0.5

    ) as pose:

        frame_number = 0

        while cap.isOpened():

            success, frame = cap.read()

            if not success:
                break

            frame_number += 1

            if frame_number % 10 != 0:
                continue

            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            results = pose.process(
                rgb_frame
            )

            if results.pose_landmarks:

                landmarks = (
                    results.pose_landmarks.landmark
                )

                hip = landmarks[
                    mp_pose.PoseLandmark.LEFT_HIP
                ]

                knee = landmarks[
                    mp_pose.PoseLandmark.LEFT_KNEE
                ]

                ankle = landmarks[
                    mp_pose.PoseLandmark.LEFT_ANKLE
                ]

                hip_point = (
                    hip.x,
                    hip.y
                )

                knee_point = (
                    knee.x,
                    knee.y
                )

                ankle_point = (
                    ankle.x,
                    ankle.y
                )

                knee_angle = calculate_angle(

                    hip_point,

                    knee_point,

                    ankle_point
                )

                knee_angles.append(
                    knee_angle
                )

    cap.release()

    # =====================================
    # NO DATA
    # =====================================

    if len(knee_angles) == 0:

        return {

            "average_knee_angle": 0,

            "efficiency": "No Data"

        }

    average_knee_angle = (

        sum(knee_angles)

        / len(knee_angles)

    )

    # =====================================
    # EFFICIENCY ANALYSIS
    # =====================================

    if average_knee_angle > 160:

        efficiency = "Good Extension"

    elif average_knee_angle > 120:

        efficiency = "Moderate Bend"

    else:

        efficiency = (
            "Low Running Efficiency"
        )

    return {

        "average_knee_angle": round(
            average_knee_angle,
            2
        ),

        "efficiency": efficiency

    }