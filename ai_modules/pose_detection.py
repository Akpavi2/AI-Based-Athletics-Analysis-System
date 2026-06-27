# =====================================
# IMPORT LIBRARIES
# =====================================

import cv2


#
# =====================================
# POSE DETECTION FUNCTION
# =====================================

def detect_pose(video_path):
    import mediapipe as mp
    mp_pose = mp.solutions.pose


    # =================================
    # CREATE NEW POSE OBJECT
    # =================================

    pose = mp_pose.Pose(

        static_image_mode=False,

        min_detection_confidence=0.5,

        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(video_path)

    total_frames = 0

    detected_frames = 0

    frame_number = 0

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            break

        frame_number += 1

        if frame_number % 10 != 0:
            continue

        total_frames += 1

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = pose.process(
            rgb_frame
        )

        if results.pose_landmarks:

            detected_frames += 1

    cap.release()

    pose.close()

    # =================================
    # DETECTION SCORE
    # =================================

    if total_frames == 0:

        return {

            "pose_detected": False,

            "pose_score": 0,

            "posture": "No Video Data"
        }

    pose_score = round(

        (detected_frames / total_frames)
        * 100,

        2
    )

    # =================================
    # POSTURE STATUS
    # =================================

    if pose_score >= 90:

        posture = "Excellent Pose Tracking"

    elif pose_score >= 70:

        posture = "Good Pose Tracking"

    else:

        posture = "Poor Pose Tracking"

    return {

        "pose_detected": True,

        "pose_score": pose_score,

        "detected_frames": detected_frames,

        "total_frames": total_frames,

        "posture": posture
    }