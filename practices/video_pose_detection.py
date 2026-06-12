# =====================================
# IMPORT LIBRARIES
# =====================================

import cv2
import mediapipe as mp

# =====================================
# INITIALIZE MEDIAPIPE
# =====================================

mp_pose = mp.solutions.pose

mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose()

# =====================================
# LOAD VIDEO
# =====================================

video_path = "videos/running.mp4"

cap = cv2.VideoCapture(video_path)

# =====================================
# CHECK VIDEO
# =====================================

if not cap.isOpened():

    print("Error Opening Video")

# =====================================
# PROCESS VIDEO
# =====================================

while cap.isOpened():

    success, frame = cap.read()

    # If video ends

    if not success:
        break

    # =================================
    # CONVERT BGR → RGB
    # =================================

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # =================================
    # POSE DETECTION
    # =================================

    results = pose.process(rgb_frame)

    # =================================
    # DRAW BODY LANDMARKS
    # =================================

    if results.pose_landmarks:

        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    # =================================
    # SHOW VIDEO
    # =================================

    cv2.imshow(
        "Athlete Pose Detection",
        frame
    )

    # Press Q to Exit

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# =====================================
# RELEASE RESOURCES
# =====================================

cap.release()

cv2.destroyAllWindows()