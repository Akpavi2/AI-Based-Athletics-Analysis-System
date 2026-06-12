# =====================================
# IMPORT LIBRARIES
# =====================================

import sqlite3

import pandas as pd

# =====================================
# CONNECT DATABASE
# =====================================

connection = sqlite3.connect(
    "athletics_database.db"
)

# =====================================
# LOAD DATABASE TABLE
# =====================================

query = "SELECT * FROM athletes"

df = pd.read_sql_query(
    query,
    connection
)

# =====================================
# SHOW DATABASE
# =====================================

print("\n===== ATHLETE DATABASE =====")

print(df)

# =====================================
# OVERALL PERFORMANCE RANKING
# =====================================

overall_ranking = df.sort_values(
    by="overall_score",
    ascending=False
)

print("\n===== OVERALL RANKINGS =====")

print(
    overall_ranking[
        [
            "name",
            "overall_score"
        ]
    ]
)

# =====================================
# SPRINT RANKING
# =====================================

sprint_ranking = df.sort_values(
    by="sprint_score",
    ascending=False
)

print("\n===== SPRINT RANKINGS =====")

print(
    sprint_ranking[
        [
            "name",
            "sprint_score"
        ]
    ]
)

# =====================================
# ENDURANCE RANKING
# =====================================

endurance_ranking = df.sort_values(
    by="endurance_score",
    ascending=False
)

print("\n===== ENDURANCE RANKINGS =====")

print(
    endurance_ranking[
        [
            "name",
            "endurance_score"
        ]
    ]
)

# =====================================
# JUMP RANKING
# =====================================

jump_ranking = df.sort_values(
    by="jump_score",
    ascending=False
)

print("\n===== JUMP RANKINGS =====")

print(
    jump_ranking[
        [
            "name",
            "jump_score"
        ]
    ]
)

# =====================================
# EVENT-WISE FILTERING
# =====================================

event_name = "100m"

event_athletes = df[
    df["event"] == event_name
]

event_athletes = event_athletes.sort_values(
    by="overall_score",
    ascending=False
)

print(f"\n===== {event_name} ATHLETES =====")

print(
    event_athletes[
        [
            "name",
            "overall_score"
        ]
    ]
)

# =====================================
# TOP ATHLETE
# =====================================

top_athlete = overall_ranking.iloc[0]

print("\n===== TOP ATHLETE =====")

print(
    f"{top_athlete['name']} "
    f"→ "
    f"{top_athlete['overall_score']}"
)

# =====================================
# CLOSE DATABASE
# =====================================

connection.close()

print("\nDatabase Closed")