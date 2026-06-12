import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)



import streamlit as st
import matplotlib.pyplot as plt
import cv2
import tempfile
import pandas as pd
import pickle
# from ai_modules.ai_recommendation_engine import generate_recommendations
from ai_modules.ai_engine import get_complete_ai_report
from database.athlete_database import connection, cursor
import hashlib
# from ai_modules.pose_detection import process_video


# =====================================
# PASSWORD HASH FUNCTION
# =====================================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


st.set_page_config(

    page_title="AI Athletics Platform",

    page_icon="🏃",

    layout="wide",

    initial_sidebar_state="expanded"
)
st.title("🏃 AI Athletics Platform")
# =====================================
# LOAD ML MODELS
# =====================================

with open("models/event_model.pkl", "rb") as file:
    event_model = pickle.load(file)

with open("models/category_model.pkl", "rb") as file:
    category_model = pickle.load(file)




# =====================================
# CUSTOM UI DESIGN
# =====================================

st.markdown("""

<style>

.main {

    background-color: #0E1117;

    color: white;
}

.stApp {

    background-color: #0E1117;
}

h1, h2, h3 {

    color: #00FFAA;
}

div.stButton > button {

    background-color: #00AA88;

    color: white;

    border-radius: 10px;

    height: 3em;

    width: 100%;
}

[data-testid="metric-container"] {

    background-color: #1E1E1E;

    border: 1px solid #00FFAA;

    padding: 15px;

    border-radius: 12px;
}

.sidebar .sidebar-content {

    background-color: #111827;
}

</style>

""", unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "data_saved" not in st.session_state:
    st.session_state.data_saved = False

# =====================================
# LOGIN SYSTEM
# =====================================

if not st.session_state.logged_in:

    st.header("Login Portal")

    st.info("Welcome to the AI Athletics Intelligence Platform")
    auth_mode = st.radio(

        "Select Option",

        ["Login", "Signup"]
  )

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    role = st.selectbox(
        "Select Role",
        ["Athlete", "Coach","Admin"]
    )

    # =====================================
# SIGNUP SYSTEM
# =====================================

    if auth_mode == "Signup":

        if st.button("Create Account"):

            if username != "" and password != "":

                try:

                    cursor.execute(

                        """

                        INSERT INTO users (

                            username,
                            password,
                            role

                        )

                        VALUES (?, ?, ?)

                        """,

                        (
                            username,
                            hash_password(password),
                            role
                        )
                    )

                    connection.commit()

                    st.success(
                        "Account Created Successfully"
                    )

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )
            else:

                st.warning(
                    "Please fill all fields"
                )

    # =====================================
    # LOGIN SYSTEM
    # =====================================

    elif auth_mode == "Login":

        if st.button("Login"):

            cursor.execute(

                """

                SELECT * FROM users

                WHERE username = ?

                AND password = ?

                AND role = ?

                """,

                (
                    username,
                    hash_password(password),
                    role
                )
            )

            user = cursor.fetchone()

            if user:

                st.session_state.logged_in = True
                st.session_state.role = role

                st.success(
                    "Login Successful!"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Credentials"
                )   

# =====================================
# AFTER LOGIN
# =====================================

else:

    # =================================
    # SIDEBAR
    # =================================
    st.sidebar.title("🏃 Sports AI Menu")

    st.sidebar.success(
        f"Logged in as: {st.session_state.role}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.role = ""
        st.session_state.data_saved = False

        st.rerun()

    # =================================
    # SCORE CALCULATION FUNCTION
    # =================================

    def calculate_scores():

        height = st.session_state.height
        weight = st.session_state.weight
        sprint_time = st.session_state.sprint_time
        endurance = st.session_state.endurance
        vertical_jump = st.session_state.vertical_jump

        # BMI

        if height == 0:
            bmi = 0
        else:
            bmi = weight / ((height / 100) ** 2)

        # Sprint Score

        if sprint_time <= 11:
            sprint_score = 95

        elif sprint_time <= 12:
            sprint_score = 85

        elif sprint_time <= 13:
            sprint_score = 70

        else:
            sprint_score = 50

        # Endurance Score

        if endurance >= 90:
            endurance_score = 95

        elif endurance >= 75:
            endurance_score = 80

        elif endurance >= 60:
            endurance_score = 65

        else:
            endurance_score = 50

        # Jump Score

        if vertical_jump >= 60:
            jump_score = 95

        elif vertical_jump >= 50:
            jump_score = 80

        elif vertical_jump >= 40:
            jump_score = 65

        else:
            jump_score = 50

        # Overall Score

        overall_score = (
            sprint_score * 0.4 +
            endurance_score * 0.3 +
            jump_score * 0.3
        )

        return (
            bmi,
            sprint_score,
            endurance_score,
            jump_score,
            overall_score
        )

    # =================================
    # ATHLETE DASHBOARD
    # =================================

    if st.session_state.role == "Athlete":
        st.subheader("Athlete Dashboard")

        athlete_menu = st.sidebar.selectbox(
            "Athlete Modules",
            [
                "Talent ID System",
                "AI Coach System"
            ]
        )

        # =================================
        # TALENT IDENTIFICATION SYSTEM
        # =================================

        if athlete_menu == "Talent ID System":

            talent_menu = st.sidebar.radio(
                "Talent ID Features",
                [
                    "Registration",
                    "Assessment",
                    "Scoring",
                    "Prediction",
                    "Analytics",
                    "Athlete History",
                    "Profile Dashboard",
                    "Video AI"
                ]
            )

            # =================================
            # REGISTRATION
            # =================================

            if talent_menu == "Registration":

                st.header("Athlete Registration")

                st.session_state.name = st.text_input(
                    "Athlete Name"
                )

                st.session_state.age = st.number_input(
                    "Age",
                    min_value=10,
                    max_value=40
                )

                st.session_state.gender = st.selectbox(
                    "Gender",
                    ["Male", "Female"]
                )

                st.session_state.height = st.number_input(
                    "Height (cm)",
                    min_value=1
                )

                st.session_state.weight = st.number_input(
                    "Weight (kg)",
                    min_value=1
                )

                st.session_state.sprint_time = st.number_input(
                    "Sprint Time"
                )

                st.session_state.endurance = st.number_input(
                    "Endurance Score"
                )

                st.session_state.vertical_jump = st.number_input(
                    "Vertical Jump"
                )

                st.session_state.specialization = st.selectbox(

                    "Specialization",

                    [
                        "100m",
                        "200m",
                        "400m",
                        "800m",
                        "Long Jump",
                        "High Jump"
                    ]
                )

                st.session_state.achievements = st.text_area(
                    "Achievements"
                )

                st.session_state.injury_history = st.text_area(
                    "Injury History"
                )

                profile_photo = st.file_uploader(
                    "Upload Profile Photo",
                    type=["jpg", "png", "jpeg"]
                )

                # if st.button("Save Data"):

                #     st.session_state.data_saved = True

                #     st.success("Athlete Data Saved Successfully")
                if st.button("Save Data"):

    # =====================================
    # SAVE ATHLETE DATA TO DATABASE
    # =====================================

                    cursor.execute("""

                    INSERT INTO athletes (

                        name,
                        age,
                        gender,
                        height,
                        weight,
                        sprint_time,
                        endurance,
                        vertical_jump,
                        specialization,
                        achievements,
                        injury_history,
                        profile_photo           

                    )

                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

                    """, (

                        st.session_state.name,
                        st.session_state.age,
                        st.session_state.gender,
                        st.session_state.height,
                        st.session_state.weight,
                        st.session_state.sprint_time,
                        st.session_state.endurance,
                        st.session_state.vertical_jump,
                        st.session_state.specialization,
                        st.session_state.achievements,
                        st.session_state.injury_history,
                        str(profile_photo.name) if profile_photo else ""

                    ))

                    connection.commit()

                    st.session_state.data_saved = True

                    st.success("Athlete Data Saved Successfully")

            # =================================
            # ASSESSMENT
            # =================================

            elif talent_menu == "Assessment":

                st.header("Fitness Assessment")

                if st.session_state.data_saved:

                    if st.button("Run Assessment"):

                        (
                            bmi,
                            sprint_score,
                            endurance_score,
                            jump_score,
                            overall_score
                        ) = calculate_scores()

                        st.write("BMI:", round(bmi, 2))
                        st.write("Sprint Score:", sprint_score)
                        st.write("Endurance Score:", endurance_score)
                        st.write("Jump Score:", jump_score)
                        st.write(
                            "Overall Score:",
                            round(overall_score, 2)
                        )

                else:
                    st.warning("Please Register Athlete First")

            # =================================
            # SCORING
            # =================================

            elif talent_menu == "Scoring":

                st.header("Performance Scoring")

                if st.session_state.data_saved:

                    (
                        bmi,
                        sprint_score,
                        endurance_score,
                        jump_score,
                        overall_score
                    ) = calculate_scores()

                    st.metric(
                        "Overall Athlete Score",
                        round(overall_score, 2)
                    )

                else:
                    st.warning("Please Register Athlete First")

            # =================================
            # PREDICTION
            # =================================

            elif talent_menu == "Prediction":

                st.header("AI Event Prediction")

                if st.session_state.data_saved:

                    (
                        bmi,
                        sprint_score,
                        endurance_score,
                        jump_score,
                        overall_score
                    ) = calculate_scores()

                    input_data = [[
                        st.session_state.age,
                        st.session_state.height,
                        st.session_state.weight,
                        bmi,
                        sprint_score,
                        endurance_score,
                        jump_score,
                        overall_score
                    ]]

                    # Event Prediction

                    event_prediction = event_model.predict(
                        input_data
                    )

                    st.success(
                        f"Predicted Event: {event_prediction[0]}"
                    )

                    # Category Prediction

                    category_prediction = category_model.predict(
                        input_data
                    )

                    st.success(
                        f"Predicted Category: {category_prediction[0]}"
                    )

                else:
                    st.warning("Please Register Athlete First")

            # =================================
            # ANALYTICS
            # =================================
            elif talent_menu == "Analytics":
                st.header("Performance Analytics")

                if st.session_state.data_saved:


                    (
                        bmi,
                        sprint_score,
                        endurance_score,
                        jump_score,
                        overall_score
                    ) = calculate_scores()

            # =====================================
            # METRICS
            # =====================================

                    col1, col2, col3, col4 = st.columns(4)

                    col1.metric(
                        "Sprint",
                        sprint_score
                    )

                    col2.metric(
                        "Endurance",
                        endurance_score
                    )

                    col3.metric(
                        "Jump",
                        jump_score
                    )

                    col4.metric(
                        "Overall",
                        round(overall_score, 2)
                    )

                    # =====================================
                    # BAR CHART
                    # =====================================

                    scores = [

                        sprint_score,
                        endurance_score,
                        jump_score
                    ]

                    labels = [

                        "Sprint",
                        "Endurance",
                        "Jump"
                    ]

                    fig, ax = plt.subplots(
                        figsize=(7, 4)
                    )

                    ax.bar(
                        labels,
                        scores
                    )

                    ax.set_title(
                        "Athlete Performance Metrics"
                    )

                    ax.set_ylabel(
                        "Scores"
                    )

                    st.pyplot(fig)
                else:

                    st.warning("Please Register Athlete First")

            # =================================
# ATHLETE HISTORY
# =================================

            elif talent_menu == "Athlete History":

                st.header("Athlete Performance History")

                # =====================================
                # LOAD DATABASE RECORDS
                # =====================================

                cursor.execute(
                    "SELECT * FROM athletes"
                )

                records = cursor.fetchall()

                # =====================================
                # CHECK DATA EXISTS
                # =====================================

                if len(records) > 0:

                    # =====================================
                    # CREATE DATAFRAME
                    # =====================================

                    history_df = pd.DataFrame(

                        records,

                        columns=[

                            "ID",
                            "Name",
                            "Age",
                            "Gender",
                            "Height",
                            "Weight",
                            "Sprint Time",
                            "Endurance",
                            "Vertical Jump"
                        ]
                    )

                    # =====================================
                    # DISPLAY TABLE
                    # =====================================

                    st.dataframe(

                        history_df,

                        use_container_width=True
                    )

                    st.success(
                        "Athlete history loaded successfully"
                    )

                else:

                    st.warning(
                        "No athlete records found"
                    )   

            # =================================
            # PROFILE DASHBOARD
            # =================================

            elif talent_menu == "Profile Dashboard":

                st.header("Athlete Profile Dashboard")

                cursor.execute(

                    """

                    SELECT *

                    FROM athletes

                    ORDER BY id DESC

                    LIMIT 1

                    """
                )

                athlete = cursor.fetchone()

                if athlete:

                    st.subheader("Profile Information")

                    st.write(f"Name: {athlete[1]}")
                    st.write(f"Age: {athlete[2]}")
                    st.write(f"Gender: {athlete[3]}")
                    st.write(f"Height: {athlete[4]} cm")
                    st.write(f"Weight: {athlete[5]} kg")

                    st.subheader("Athletic Information")

                    st.write(f"Sprint Time: {athlete[6]}")
                    st.write(f"Endurance: {athlete[7]}")
                    st.write(f"Vertical Jump: {athlete[8]}")

                    st.subheader("Specialization")

                    st.success(athlete[9])

                    st.subheader("Achievements")

                    st.info(athlete[10])

                    st.subheader("Injury History")

                    st.warning(athlete[11])

                    st.subheader("Profile Photo")

                    if athlete[12] != "":

                        st.write(athlete[12])

                    else:

                        st.write("No profile photo uploaded")

                else:

                    st.warning("No athlete profile found")             

            # =================================
            # VIDEO AI
            # =================================

            elif talent_menu == "Video AI":

                st.header("AI Video Analysis")

                uploaded_video = st.file_uploader(
                    "Upload Running Video",
                    type=["mp4", "avi", "mov"]
                )

                if uploaded_video is not None:

                    st.video(uploaded_video)
                    st.info("Video uploaded successfully")


                    # =====================================
                    # CREATE VIDEO PATH
                    # =====================================

                    video_path = os.path.join(

                        "uploaded_videos",

                        uploaded_video.name
                    )

                    # =====================================
                    # SAVE VIDEO
                    # =====================================

                    with open(video_path, "wb") as f:

                        f.write(uploaded_video.getbuffer())

                    st.success(
                        "Video Saved Successfully"
                    )

                    # =====================================
                    # OPEN VIDEO USING OPENCV
                    # =====================================

                    cap = cv2.VideoCapture(
                        video_path
                    )

                    frame_count = 0

                    while cap.isOpened():

                        ret, frame = cap.read()

                        if not ret:
                            break

                        frame_count += 1

                    cap.release()

                    st.success(
                        f"Frames Processed: {frame_count}"
                    )

        # =================================
        # AI COACH SYSTEM
        # =================================

        elif athlete_menu == "AI Coach System":

            coach_menu = st.sidebar.radio(
                "AI Coach Features",
                [
                    "Recommendations",
                    "Workout Guidance",
                    "Improvement Analysis",
                    "Motivation System",
                    "Future Diet Planner"
                ]
            )

            # =================================
            # RECOMMENDATIONS
            # =================================

            if coach_menu == "Recommendations":

                st.header("Dynamic AI Recommendations")

                if st.session_state.data_saved:

                    (
                        bmi,
                        sprint_score,
                        endurance_score,
                        jump_score,
                        overall_score
                    ) = calculate_scores()

                    ai_report = get_complete_ai_report(
                        athlete_data=st.session_state,
                        sprint_score=sprint_score,
                        endurance_score=endurance_score,
                        jump_score=jump_score
                    )

                    st.subheader("AI Recommendations")

                    for r in ai_report["recommendations"]:
                            st.write("•", r)

                    st.subheader("Training Plan")
                    st.write(ai_report["training_plan"])

                    st.subheader("Insights")
                    st.write(ai_report["insights"])

                    st.subheader("Progress")
                    st.write(ai_report["progress"])

                    st.subheader("Goals")
                    st.write(ai_report["goals"])

                    st.subheader("Biomechanics")
                    st.write(ai_report["biomechanics"])

                    

                else:

                    st.warning(
                        "Please Register Athlete First"
                    )
                            # =================================
                            # WORKOUT GUIDANCE
                            # =================================

            elif coach_menu == "Workout Guidance":

                st.header("Workout Guidance")

                st.write("Morning Sprint Training")
                st.write("Strength Training")
                st.write("Recovery Session")

                            # =================================
                            # IMPROVEMENT ANALYSIS
                            # =================================

            elif coach_menu == "Improvement Analysis":

                st.header("Improvement Analysis")

                st.write("Weak Area: Endurance")
                st.write("Suggested: Long-distance runs")

                            # =================================
                            # MOTIVATION SYSTEM
                            # =================================

            elif coach_menu == "Motivation System":

                st.header("Motivation System")

                st.success(
                    "Consistency builds champions!"
                )

                            # =================================
                            # DIET PLANNER
                            # =================================

            elif coach_menu == "Future Diet Planner":

                st.header("Diet Planner")

                st.write("High Protein Diet")
                st.write("Hydration Tracking")
                st.write("Balanced Carbohydrates")

    # =====================================
    # COACH DASHBOARD
    # =====================================

    elif st.session_state.role == "Coach":

        coach_dashboard_menu = st.sidebar.radio(
            "Coach Modules",
            [
                "Athlete Review & Monitoring",
                "Rankings & Analysis"
            ]
        )

        # =================================
        # ATHLETE REVIEW
        # =================================

        if coach_dashboard_menu == "Athlete Review & Monitoring":

            st.header("Coach Performance Dashboard")

            data = {

                "Athlete": [
                    "Akanksha",
                    "Rahul",
                    "Neha",
                    "Aryan"
                ],

                "Sprint Score": [
                    91,
                    78,
                    88,
                    72
                ],

                "Endurance Score": [
                    85,
                    92,
                    81,
                    75
                ],

                "Jump Score": [
                    89,
                    70,
                    93,
                    76
                ],

                "Overall Score": [
                    91,
                    84,
                    88,
                    79
                ]
            }

            df = pd.DataFrame(data)

            st.dataframe(
                df,
                use_container_width=True
            )

            st.subheader("Overall Athlete Rankings")

            st.bar_chart(
                df.set_index("Athlete")[
                    "Overall Score"
                ]
            )

            top_athlete = df.sort_values(
                by="Overall Score",
                ascending=False
            ).iloc[0]

            st.success(
                f"Top Athlete: "
                f"{top_athlete['Athlete']} "
                f"({top_athlete['Overall Score']})"
            )

        # =================================
        # RANKINGS
        # =================================

        elif coach_dashboard_menu == "Rankings & Analysis":

            st.header("Athlete Rankings")

            data = {
                "Athlete": ["A", "B", "C"],
                "Score": [85, 92, 78]
            }

            df = pd.DataFrame(data)

            df = df.sort_values(
                by="Score",
                ascending=False
            )

            st.dataframe(df)

            st.bar_chart(
                df.set_index("Athlete")
            )
    # =====================================
# ADMIN DASHBOARD
# =====================================

    elif st.session_state.role == "Admin":

        st.header("Admin Dashboard")

        st.success(
            "Welcome Admin"
        )

        st.subheader("Platform Controls")

        st.write("• Manage Users")
        st.write("• Monitor Database")
        st.write("• Manage AI Models")        