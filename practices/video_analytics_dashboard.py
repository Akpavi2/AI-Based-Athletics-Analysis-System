# =====================================
# IMPORT LIBRARIES
# =====================================

import cv2
import mediapipe as mp
import math
import time
import matplotlib.pyplot as plt

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
# VARIABLES
# =====================================

previous_x = None
previous_y = None

previous_speed = 0

previous_time = time.time()

# =====================================
# ANALYTICS STORAGE
# =====================================

speed_values = []

acceleration_values = []

frame_numbers = []

frame_count = 0

# =====================================
# PROCESS VIDEO
# =====================================

frame_number = 0

while cap.isOpened():

    success, frame = cap.read()

    if not success:
        break

    frame_number += 1

    if frame_number % 10!= 0:
        continue

    # =================================
    # RGB CONVERSION
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
    # BODY ANALYSIS
    # =================================

    if results.pose_landmarks:

        landmarks = results.pose_landmarks.landmark

        # =============================
        # LEFT HIP
        # =============================

        hip = landmarks[
            mp_pose.PoseLandmark.LEFT_HIP
        ]

        current_x = hip.x
        current_y = hip.y

        current_time = time.time()

        # =============================
        # SPEED ESTIMATION
        # =============================

        if previous_x is not None:

            distance = math.sqrt(
                (current_x - previous_x) ** 2 +
                (current_y - previous_y) ** 2
            )

            time_difference = (
                current_time - previous_time
            )

            if time_difference > 0:

                # =====================
                # SPEED
                # =====================

                speed = (
                    distance / time_difference
                )

                # =====================
                # ACCELERATION
                # =====================

                acceleration = (
                    speed - previous_speed
                ) / time_difference

                # =====================
                # STORE VALUES
                # =====================

                speed_values.append(speed)

                acceleration_values.append(
                    acceleration
                )

                frame_numbers.append(
                    frame_count
                )

                # =====================
                # DISPLAY METRICS
                # =====================

                cv2.putText(
                    frame,
                    f"Speed: {speed:.2f}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Acceleration: {acceleration:.2f}",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    2
                )

                # =====================
                # ATHLETE STATUS
                # =====================

                if speed > 1.5:

                    status = "Fast Movement"

                elif speed > 0.8:

                    status = "Moderate Movement"

                else:

                    status = "Slow Movement"

                cv2.putText(
                    frame,
                    status,
                    (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2
                )

                previous_speed = speed

        # =============================
        # UPDATE VARIABLES
        # =============================

        previous_x = current_x
        previous_y = current_y

        previous_time = current_time

        # =============================
        # DRAW BODY LANDMARKS
        # =============================

        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    # =================================
    # SHOW VIDEO
    # =================================

    cv2.imshow(
        "Sports Analytics Dashboard",
        frame
    )

    # Exit

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# =====================================
# RELEASE VIDEO
# =====================================

cap.release()

cv2.destroyAllWindows()

# =====================================
# PERFORMANCE GRAPHS
# =====================================

# =====================================
# SPEED GRAPH
# =====================================

plt.figure(figsize=(10, 5))

plt.plot(
    frame_numbers,
    speed_values
)

plt.title("Athlete Speed Analysis")

plt.xlabel("Frames")

plt.ylabel("Speed")

plt.grid(True)

plt.show()

# =====================================
# ACCELERATION GRAPH
# =====================================

plt.figure(figsize=(10, 5))

plt.plot(
    frame_numbers,
    acceleration_values
)

plt.title("Athlete Acceleration Analysis")

plt.xlabel("Frames")

plt.ylabel("Acceleration")

plt.grid(True)

plt.show()

# =====================================
# SUMMARY ANALYTICS
# =====================================

if len(speed_values) > 0:

    average_speed = sum(speed_values) / len(speed_values)

    max_speed = max(speed_values)

    max_acceleration = max(acceleration_values)

    print("\n===== SPORTS ANALYTICS REPORT =====")

    print(
        f"Average Speed: {average_speed:.2f}"
    )

    print(
        f"Maximum Speed: {max_speed:.2f}"
    )

    print(
        f"Maximum Acceleration: {max_acceleration:.2f}"
    )