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

st.markdown("""
<style>

/* Main App Background */
.stApp {
    background-color: #0F0F0F;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Headers */
h1, h2, h3 {
    color: #00FF88;
}

/* Cards */
div[data-testid="metric-container"] {
    background-color: #1A1A1A;
    border: 1px solid #0A66FF;
    padding: 15px;
    border-radius: 12px;
}

/* Buttons */
.stButton > button {
    background-color: #0A66FF;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #00FF88;
    color: black;
}

/* Input Fields */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background-color: #1A1A1A;
    color: white;
}

/* Select Boxes */
.stSelectbox div {
    background-color: #1A1A1A;
}

/* Expanders */
.streamlit-expanderHeader {
    background-color: #1A1A1A;
    color: white;
}

/* Success Box */
.stSuccess {
    border-radius: 10px;
}

/* Warning Box */
.stWarning {
    border-radius: 10px;
}

/* Error Box */
.stError {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)
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

    # st.sidebar.success(
    #     f"Logged in as: {st.session_state.role}"
    # )

    # if st.sidebar.button("Logout"):

    st.sidebar.markdown("""
    # 🏃 Athletics AI

    ### Sports Analytics Platform
    """)

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

                st.header(" 🏃Athlete Registration")

                st.session_state.name = st.text_input(
                    "Athlete Name"
                )

                st.session_state.age = st.number_input(
                    "Age",
                    min_value=5,
                    max_value=100
                )

                st.session_state.gender = st.selectbox(
                    "Gender",
                    ["Male", "Female","Other"]
                )

                st.session_state.height = st.number_input(
                    "Height (cm)",
                    min_value=80

                )

                st.session_state.weight = st.number_input(
                    "Weight (kg)",
                    min_value=15
                )

                st.session_state.sprint_time = st.number_input(
                    "Sprint Time (seconds)",
                    min_value=0.0,
                    step=0.1
                )

                st.session_state.endurance = st.number_input(
                    "Endurance Score",
                    min_value=0,
                    max_value=100
                )

                st.session_state.vertical_jump = st.number_input(
                    "Vertical Jump",
                    min_value=0
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


                if profile_photo:
                    st.session_state.profile_photo = profile_photo

                # if st.button("Save Data"):

                #     st.session_state.data_saved = True

                #     st.success("Athlete Data Saved Successfully")
                confirm = st.checkbox(
                    "I confirm the athlete details are correct"
                )


                if st.button("Save Data"):
                    if not confirm:
                        st.error("Please confirm athlete details")
                        st.stop()

                    # =========================
                    # VALIDATION
                    # =========================

                    if st.session_state.name.strip() == "":
                        st.error("Name cannot be empty")
                        st.stop()

                    clean_name = st.session_state.name.replace(" ", "")

                    if len(clean_name) < 2:
                        st.error("Name must contain at least 2 letters")
                        st.stop()

                    if not clean_name.isalpha():
                        st.error("Name should contain only letters")
                        st.stop()
                        

                    if st.session_state.age <= 0:
                        st.error("Invalid age")
                        st.stop()

                    if st.session_state.height < 80:
                        st.error("Please enter a valid height")
                        st.stop()

                    if st.session_state.weight < 15:
                        st.error("Please enter a valid weight")
                        st.stop()

                    if st.session_state.sprint_time <= 0:
                        st.error("Sprint time must be greater than 0")
                        st.stop()    

                    if st.session_state.sprint_time >60:
                        st.error("Sprint time seems unrealistic")
                        st.stop()

                    if len(st.session_state.achievements) > 500:
                        st.error("Achievements text is too long")
                        st.stop()    

                    # =====================================
                    # DUPLICATE ATHLETE CHECK
                    # =====================================

                    cursor.execute("""

                    SELECT COUNT(*)

                    FROM athletes

                    WHERE

                    name = ?
                    AND age = ?
                    

                    """, (

                        st.session_state.name,
                        st.session_state.age,
                        

                    ))

                    existing = cursor.fetchone()[0]

                    if existing > 0:
                        st.warning("Athlete already exists in database")
                        st.stop()

                    # if st.session_state.height < 100:
                    #     st.error("Height seems invalid")
                    #     st.stop()

                    # if st.session_state.weight < 20:
                    #     st.error("Weight seems invalid")
                    #     st.stop()    

                    

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

                        st.subheader("📊 Assessment Results")

                    # First Row

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric(
                                "BMI",
                                round(bmi, 2)
                            )

                        with col2:
                            st.metric(
                                "Sprint Score",
                                sprint_score
                            )

                        with col3:
                            st.metric(
                                "Endurance Score",
                                endurance_score
                            )

                        # Second Row

                        col4, col5 = st.columns(2)

                        with col4:
                            st.metric(
                                "Jump Score",
                                jump_score
                            )

                        with col5:
                            st.metric(
                                "Overall Score",
                                round(overall_score, 2)
                            )

                else:
                    st.warning("Please Register Athlete First")



            # =================================
            # SCORING
            # =================================

            elif talent_menu == "Scoring":

                st.header("📊 Performance Scoring")

                if st.session_state.data_saved:

                    (
                        bmi,
                        sprint_score,
                        endurance_score,
                        jump_score,
                        overall_score
                    ) = calculate_scores()

                    col1, col2, col3, col4, col5 = st.columns(5)

                    with col1:
                        st.metric("BMI", round(bmi, 2))

                    with col2:
                        st.metric("Sprint", sprint_score)

                    with col3:
                        st.metric("Endurance", endurance_score)

                    with col4:
                        st.metric("Jump", jump_score)

                    with col5:
                        st.metric("Overall", round(overall_score, 2))

                    st.divider()

                    st.success(
                        f"Overall Athlete Rating: {round(overall_score, 2)}/100"
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

                    input_data = pd.DataFrame([{
                        "age": st.session_state.age,
                        "height": st.session_state.height,
                        "weight": st.session_state.weight,
                        "BMI": bmi,
                        "sprint_score": sprint_score,
                        "endurance_score": endurance_score,
                        "jump_score": jump_score,
                        "overall_score": overall_score
                    }])

                    # Event Prediction

                    event_prediction = event_model.predict(
                        input_data
                    )

                    # Category Prediction

                    category_prediction = category_model.predict(
                        input_data
                    )

                    st.subheader("🎯 AI Prediction Results")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Predicted Event",
                            event_prediction[0]
                        )

                    with col2:
                        st.metric(
                            "Athlete Category",
                            category_prediction[0]
                        )


                    st.subheader("📋 Athlete Input Summary")

                    summary_df = pd.DataFrame({
                        "Metric": [
                            "BMI",
                            "Sprint Score",
                            "Endurance Score",
                            "Jump Score",
                            "Overall Score"
                        ],
                        "Value": [
                            round(bmi,2),
                            sprint_score,
                            endurance_score,
                            jump_score,
                            round(overall_score,2)
                        ]
                    })

                    st.dataframe(
                        summary_df,
                        width="Stretch"
                    )    

                else:
                    st.warning("Please Register Athlete First")

            # =================================
            # ANALYTICS
            # =================================
            elif talent_menu == "Analytics":
                st.header(" 📊 Performance Analytics")

                if st.session_state.data_saved:


                    (
                        bmi,
                        sprint_score,
                        endurance_score,
                        jump_score,
                        overall_score
                    ) = calculate_scores()


                    # =====================================
                    # ATHLETE SUMMARY CARD
                    # =====================================

                    st.subheader("🏃 Athlete Summary")

                    col1, col2 = st.columns([1,3])

                    with col1:

                        if "profile_photo" in st.session_state and st.session_state.profile_photo:

                            st.image(
                                st.session_state.profile_photo,
                                width=120
                            )

                        else:

                            st.image(
                                "https://cdn-icons-png.flaticon.com/512/149/149071.png",
                                width=120
    )

                    with col2:

                        st.markdown(f"""
                    ### {st.session_state.name}

                    🏃 Event: {st.session_state.specialization}

                    🎂 Age: {st.session_state.age}

                    ⚥ Gender: {st.session_state.gender}

                    📏 Height: {st.session_state.height} cm

                    ⚖ Weight: {st.session_state.weight} kg

                    📊 BMI: {round(bmi,2)}
                    """)

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


                    st.subheader("📈 Performance Breakdown")

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


                    # =====================================
                    # PERFORMANCE TREND
                    # =====================================

                    st.subheader("📉 Performance Trend")

                    trend_df = pd.DataFrame({
                        "Week":[1,2,3,4,5],
                        "Performance":[
                            overall_score-20,
                            overall_score-15,
                            overall_score-10,
                            overall_score-5,
                            overall_score
                        ]
                    })

                    st.line_chart(
                        trend_df.set_index("Week")
                    )



                    # =====================================
                    # ATHLETE ANALYSIS
                    # =====================================

                    st.subheader("🧠 Athlete Analysis")

                    scores_dict = {
                        "Sprint": sprint_score,
                        "Endurance": endurance_score,
                        "Jump": jump_score
                    }

                    best_skill = max(
                        scores_dict,
                        key=scores_dict.get
                    )

                    weak_skill = min(
                        scores_dict,
                        key=scores_dict.get
                    )

                    st.success(
                        f"Best Skill: {best_skill}"
                    )

                    st.warning(
                        f"Needs Improvement: {weak_skill}"
                    )

                    st.info(
                        f"Overall Athlete Rating: {round(overall_score,2)}/100"
                    )
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
                            "Vertical Jump",
                            "Predicted Event",
                            "Recommendation",
                            "Training Plan",
                            "Image"
                        ]
                    )


                    st.subheader("📊 History Summary")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Total Athletes",
                            len(history_df)
                        )

                    with col2:
                        st.metric(
                            "Average Age",
                            round(history_df["Age"].mean(), 1)
                        )

                    with col3:
                        st.metric(
                            "Average Height",
                            round(history_df["Height"].mean(), 1)
                        )    

                

                        
                    st.subheader("📋 Athlete Records")

                    search_name = st.text_input(
                        "🔍 Search Athlete"
                    )

                    if search_name:

                        history_df = history_df[
                            history_df["Name"]
                            .str.contains(
                                search_name,
                                case=False
                            )
                        ]
                                        

                    # =====================================
                    # DISPLAY TABLE
                    # =====================================

                    st.dataframe(

                        history_df,

                        width="stretch"
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

                    (
                        bmi,
                        sprint_score,
                        endurance_score,
                        jump_score,
                        overall_score
                    ) = calculate_scores()

                    # Athlete Profile Card

                    # =====================================
                    # ATHLETE PROFILE CARD
                    # =====================================

                    col1, col2 = st.columns([1, 3])

                    with col1:

                        if athlete[12] != "":

                            st.image(
                                athlete[12],
                                width=150
                            )

                        else:

                            st.image(
                                "https://cdn-icons-png.flaticon.com/512/149/149071.png",
                                width=120
    )
                    with col2:

                        st.markdown(
                            f"""
                    ### {athlete[1]}

                    🏃 Event: {athlete[9]}

                    🎂 Age: {athlete[2]}

                    ⚥ Gender: {athlete[3]}

                    📏 Height: {athlete[4]} cm

                    ⚖️ Weight: {athlete[5]} kg
                    """
                        )

                    st.divider()

                    # =====================================
                    # KPI SECTION
                    # =====================================

                    bmi_height = athlete[4] / 100

                    bmi = athlete[5] / (bmi_height * bmi_height)

                    col1, col2, col3, col4, col5 = st.columns(5)

                    with col1:
                        st.metric(
                            "BMI",
                            round(bmi, 2)
                        )

                    with col2:
                        st.metric(
                            "Sprint",
                            sprint_score
                        )

                    with col3:
                        st.metric(
                            "Endurance",
                            endurance_score
                        )

                    with col4:
                        st.metric(
                            "Jump",
                            jump_score
                        )

                    with col5:
                        st.metric(
                            "Overall",
                            round(overall_score, 2)
                        )

                    st.divider()

                    # =====================================
                    # ACHIEVEMENTS
                    # =====================================

                    st.subheader("🏅 Achievements")

                    st.success(
                        athlete[10]
                    )

                    # =====================================
                    # INJURY HISTORY
                    # =====================================

                    st.subheader("🩺 Injury History")

                    st.warning(
                        athlete[11]
                    )


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
                    st.session_state.video_path = video_path


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

                st.header(" 🤖 AI Performance Recommendations")

                if st.session_state.data_saved:

                    (
                        bmi,
                        sprint_score,
                        endurance_score,
                        jump_score,
                        overall_score
                    ) = calculate_scores()


                    # =====================================
                    # ATHLETE PROFILE CARD
                    # =====================================

                    col1, col2 = st.columns([1, 3])

                    with col1:

                        if "profile_photo" in st.session_state and st.session_state.profile_photo:
                            st.image(
                                st.session_state.profile_photo,
                                width=120
                            )

                    with col2:

                        st.markdown(
                            f"""
                    ### {st.session_state.name}

                    🏃 **{st.session_state.specialization}**

                    📏 **{st.session_state.height} cm**

                    ⚖️ **{st.session_state.weight} kg**
                    """
                        )

                    st.divider()

                    st.header("Athlete Performance Dashboard")

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Sprint", sprint_score)

                    with col2:
                        st.metric("Endurance", endurance_score)

                    with col3:
                        st.metric("Jump", jump_score)

                    with col4:
                        st.metric(
                            "Overall",
                            round(overall_score, 2)
                        )

                    video_path = st.session_state.get(
                        "video_path",
                        None
                    )

                    ai_report = get_complete_ai_report(
                        athlete_data=st.session_state,
                        sprint_score=sprint_score,
                        endurance_score=endurance_score,
                        jump_score=jump_score,
                        video_path=video_path
                    )

                    st.subheader("🎯 AI Recommendations")

                    for rec in ai_report["recommendations"]:
                        st.success(rec)

                    st.subheader("📅 Weekly Training Plan")

                    for day, activities in ai_report["training_plan"].items():

                        with st.expander(day):

                            for activity in activities:

                                st.write("✅", activity)

                    insights = ai_report["insights"]

                    st.subheader(" 🧠 AI Insights")

                    st.success(
                        f"Performance Status: {insights['performance_status']}"
                    )

                    st.warning(
                        f"Injury Status: {insights['injury_status']}"
                    )

                    st.write(
                        f"Injury Risk Score: {insights['injury_risk_score']}"
                    )

                    st.write("⚠ Risk Alerts")

                    for alert in insights["risk_alerts"]:

                        st.error(alert)

                    

                    progress = ai_report["progress"]

                    progress_df = pd.DataFrame({
                        "Week": progress["weeks"],
                        "Sprint": progress["sprint_scores"],
                        "Endurance": progress["endurance_scores"],
                        "Jump": progress["jump_scores"]
                    })

                    st.subheader(" 📈 Performance Progress")

                    st.line_chart(
                        progress_df.set_index("Week")
                    )

                    st.write(
                        f"Improvement Rate: {progress['improvement']}%"
                    )

                    st.write(
                        f"Status: {progress['status']}"
                    )

                    goals = ai_report["goals"]

                    st.subheader("🎯 Goal Tracking")

                    st.write("Sprint Progress")
                    st.progress(goals["sprint_progress"] / 100)

                    st.write("Endurance Progress")
                    st.progress(goals["endurance_progress"] / 100)

                    st.write("Jump Progress")
                    st.progress(goals["jump_progress"] / 100)

                    st.write("Overall Progress")
                    st.progress(goals["overall_progress"] / 100)

                    st.success(
                        goals["motivation"]
                    )

                    
                    bio = ai_report["biomechanics"]
                    # st.write("DEBUG:", bio)

                    st.subheader("🏃 Biomechanics")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Pose Score",
                            bio["pose"]["pose_score"]
                        )

                    with col2:
                        st.metric(
                            "Knee Angle",
                            round(
                                bio["knee_angle"]["average_knee_angle"],
                                1
                            )
                        )

                    with col3:
                        st.metric(
                            "Speed Score",
                            round(
                                bio["speed"]["speed_score"],
                                4
                            )
                        )

                    st.info(
                        f"Posture: {bio['pose']['posture']}"
                    )

                    st.info(
                        f"Stride Quality: {bio['stride']['stride_quality']}"
                    )

                    st.info(
                        f"Running Form: {bio['running_form']['posture']}"
                    )

                    st.info(
                        f"Speed Status: {bio['speed']['speed_status']}"
                    )        

                else:

                    st.warning(
                        "Please Register Athlete First"
                    )
                            # =================================
                            # WORKOUT GUIDANCE
                            # =================================

            elif coach_menu == "Workout Guidance":

                st.header("💪 Workout Guidance")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.info("""
                🏃 Sprint Training

                Duration: 30 min

                Intensity: High
                """)

                with col2:
                    st.info("""
                🏋 Strength Training

                Duration: 45 min

                Intensity: Medium
                """)

                with col3:
                    st.info("""
                🧘 Recovery Session

                Duration: 20 min

                Intensity: Low
                """)

                            # =================================
                            # IMPROVEMENT ANALYSIS
                            # =================================

            elif coach_menu == "Improvement Analysis":

                st.header("📈 Improvement Analysis")

                st.success(
                    "Strength: Sprint Performance"
                )

                st.warning(
                    "Weak Area: Endurance"
                )

                st.info(
                    "Focus Area: Long-distance running and aerobic training"
                )

                            # =================================
                            # MOTIVATION SYSTEM
                            # =================================

            elif coach_menu == "Motivation System":

                st.header("🏅 Motivation System")

                st.success(
                    "Consistency builds champions!"
                )

                st.metric(
                    "Weekly Goal",
                    "5/7 Sessions Completed"
                )

                st.info(
                    "Achievement Badge: Rising Athlete 🚀"
                )

                            # =================================
                            # DIET PLANNER
                            # =================================

            elif coach_menu == "Future Diet Planner":

                st.header("🥗 Diet Planner")

                col1, col2 = st.columns(2)

                with col1:

                    st.success("""
                🍳 Breakfast

                Oats

                Eggs

                Banana
                """)

                    st.success("""
                🍛 Lunch

                Rice

                Chicken

                Vegetables
                """)

                with col2:

                    st.success("""
                🥗 Dinner

                Salad

                Paneer/Fish

                Milk
                """)

                    st.success("""
                💧 Hydration

                3-4 Litres Water
                """)

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
                width="stretch"
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