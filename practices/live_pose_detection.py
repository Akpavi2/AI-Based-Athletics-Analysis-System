# =====================================
# IMPORT LIBRARIES
# =====================================

import cv2
import mediapipe as mp

# =====================================
# INITIALIZE MEDIAPIPE
# =====================================

mp_pose = mp.solutions.pose

pose = mp_pose.Pose()

mp_draw = mp.solutions.drawing_utils

# =====================================
# START WEBCAM
# =====================================

cap = cv2.VideoCapture(0)

# =====================================
# MAIN LOOP
# =====================================

while True:

    success, frame = cap.read()

    if not success:
        break

    # =================================
    # CONVERT BGR TO RGB
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
    # DRAW LANDMARKS
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
        "AI Athlete Pose Detection",
        frame
    )

    # =================================
    # PRESS Q TO EXIT
    # =================================

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# =====================================
# RELEASE RESOURCES
# =====================================

cap.release()

cv2.destroyAllWindows()