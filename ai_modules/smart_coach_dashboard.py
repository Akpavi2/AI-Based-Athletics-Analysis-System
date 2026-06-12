# =====================================
# IMPORT LIBRARIES
# =====================================

import pandas as pd

import matplotlib.pyplot as plt

# =====================================
# MULTIPLE ATHLETE DATA
# =====================================

data = {

    "Athlete": [
        "Akanksha",
        "Rahul",
        "Priya",
        "Aman",
        "Sneha"
    ],

    "Sprint Score": [
        92,
        75,
        88,
        68,
        95
    ],

    "Endurance Score": [
        70,
        90,
        82,
        60,
        78
    ],

    "Jump Score": [
        85,
        72,
        91,
        65,
        89
    ],

    "Overall Score": [
        82,
        79,
        87,
        64,
        90
    ],

    "Predicted Event": [
        "100m",
        "800m",
        "Long Jump",
        "400m",
        "100m"
    ]
}

# =====================================
# CREATE DATAFRAME
# =====================================

df = pd.DataFrame(data)

# =====================================
# DISPLAY DATA
# =====================================

print("\n===== ATHLETE DATABASE =====")

print(df)

# =====================================
# ATHLETE RANKING SYSTEM
# =====================================

ranked_df = df.sort_values(
    by="Overall Score",
    ascending=False
)

print("\n===== ATHLETE RANKINGS =====")

print(ranked_df)

# =====================================
# TOP ATHLETE
# =====================================

top_athlete = ranked_df.iloc[0]

print("\n===== TOP ATHLETE =====")

print(
    f"{top_athlete['Athlete']} "
    f"({top_athlete['Overall Score']})"
)

# =====================================
# WEAK ATHLETES DETECTION
# =====================================

weak_athletes = df[
    df["Overall Score"] < 70
]

print("\n===== ATHLETES NEEDING IMPROVEMENT =====")

print(weak_athletes)

# =====================================
# EVENT FILTERING
# =====================================

sprinters = df[
    df["Predicted Event"] == "100m"
]

print("\n===== 100m ATHLETES =====")

print(sprinters)

# =====================================
# VISUALIZATION
# =====================================

plt.figure(figsize=(10, 5))

plt.bar(
    df["Athlete"],
    df["Overall Score"]
)

plt.title(
    "Athlete Performance Comparison"
)

plt.xlabel("Athletes")

plt.ylabel("Overall Score")

plt.grid(True)

plt.show()