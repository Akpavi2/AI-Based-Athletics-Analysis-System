# =====================================
# IMPORT LIBRARIES
# =====================================

import cv2
import mediapipe as mp
import math

# =====================================
# SPEED ESTIMATION FUNCTION
# =====================================

def estimate_speed(video_path):

    mp_pose = mp.solutions.pose

    previous_x = None

    movement_values = []

    cap = cv2.VideoCapture(video_path)

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

                hip = results.pose_landmarks.landmark[
                    mp_pose.PoseLandmark.LEFT_HIP
                ]

                current_x = hip.x

                if previous_x is not None:

                    movement = abs(
                        current_x - previous_x
                    )

                    movement_values.append(
                        movement
                    )

                previous_x = current_x

    cap.release()

    # =================================
    # NO DATA
    # =================================

    if len(movement_values) == 0:

        return {
            "speed_score": 0,
            "speed_status": "No Data"
        }

    average_speed = sum(
        movement_values
    ) / len(movement_values)

    # =================================
    # SPEED CLASSIFICATION
    # =================================

    if average_speed > 0.015:

        status = "Excellent Speed"

    elif average_speed > 0.008:

        status = "Good Speed"

    else:

        status = "Needs Speed Improvement"

    return {

        "speed_score": round(
            average_speed,
            4
        ),

        "speed_status": status
    }