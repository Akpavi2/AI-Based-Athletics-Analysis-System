# =====================================
# IMPORT LIBRARIES
# =====================================

import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# =====================================
# LOAD DATASET
# =====================================

df = pd.read_csv("dataset/athlete_data.csv")

print("DATASET LOADED")

# =====================================
# FEATURES
# =====================================

X = df[[
    "age",
    "height",
    "weight",
    "BMI",
    "sprint_score",
    "endurance_score",
    "jump_score",
    "overall_score"
]]

# =====================================
# EVENT PREDICTION MODEL
# =====================================

y_event = df["event"]

X_train_event, X_test_event, y_train_event, y_test_event = train_test_split(
    X,
    y_event,
    test_size=0.2,
    random_state=42
)

event_model = RandomForestClassifier()

event_model.fit(X_train_event, y_train_event)

print("\nEVENT MODEL TRAINED")

# =====================================
# CATEGORY PREDICTION MODEL
# =====================================

y_category = df["category"]

X_train_cat, X_test_cat, y_train_cat, y_test_cat = train_test_split(
    X,
    y_category,
    test_size=0.2,
    random_state=42
)

category_model = RandomForestClassifier()

category_model.fit(X_train_cat, y_train_cat)

print("CATEGORY MODEL TRAINED")

# =====================================
# SAVE EVENT MODEL
# =====================================

with open("models/event_model.pkl", "wb") as file:

    pickle.dump(event_model, file)

print("\nEVENT MODEL SAVED")

# =====================================
# SAVE CATEGORY MODEL
# =====================================

with open("models/category_model.pkl", "wb") as file:

    pickle.dump(category_model, file)

print("CATEGORY MODEL SAVED")

# =====================================
# LOAD MODELS AGAIN
# =====================================

with open("models/event_model.pkl", "rb") as file:

    loaded_event_model = pickle.load(file)

with open("models/category_model.pkl", "rb") as file:

    loaded_category_model = pickle.load(file)

print("\nMODELS LOADED SUCCESSFULLY")

# =====================================
# NEW ATHLETE DATA
# =====================================

new_athlete = [[
    20,
    178,
    70,
    22.1,
    92,
    75,
    88,
    85.5
]]

# =====================================
# PREDICT EVENT
# =====================================

event_prediction = loaded_event_model.predict(new_athlete)

print("\nPREDICTED EVENT")
print(event_prediction[0])

# =====================================
# PREDICT CATEGORY
# =====================================

category_prediction = loaded_category_model.predict(new_athlete)

print("\nPREDICTED CATEGORY")
print(category_prediction[0])