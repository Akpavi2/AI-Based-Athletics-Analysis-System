# =====================================
# STRIDE ANALYSIS MODULE
# =====================================

import cv2
import mediapipe as mp

# =====================================
# INITIALIZE MEDIAPIPE
# =====================================

mp_pose = mp.solutions.pose

pose = mp_pose.Pose()

# =====================================
# STRIDE ANALYSIS FUNCTION
# =====================================

def analyze_stride(video_path):

    cap = cv2.VideoCapture(video_path)

    previous_left_ankle_x = None

    stride_movements = []

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            break

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = pose.process(rgb_frame)

        if results.pose_landmarks:

            landmarks = results.pose_landmarks.landmark

            left_ankle = landmarks[
                mp_pose.PoseLandmark.LEFT_ANKLE
            ]

            left_ankle_x = left_ankle.x

            if previous_left_ankle_x is not None:

                stride_distance = abs(
                    left_ankle_x -
                    previous_left_ankle_x
                )

                stride_movements.append(
                    stride_distance
                )

            previous_left_ankle_x = left_ankle_x

    cap.release()

    # =====================================
    # FINAL ANALYSIS
    # =====================================

    if len(stride_movements) == 0:

        return {
            "average_stride": 0,
            "stride_quality": "No Data"
        }

    average_stride = sum(
        stride_movements
    ) / len(stride_movements)

    if average_stride > 0.02:

        quality = "Good Stride Length"

    else:

        quality = "Short Stride"

    return {

        "average_stride": round(
            average_stride,
            4
        ),

        "stride_quality": quality
    }