# =====================================
# IMPORT LIBRARIES
# =====================================

import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

from sklearn.metrics import confusion_matrix

# =====================================
# LOAD DATASET
# =====================================

df = pd.read_csv("dataset/athlete_data.csv")

print("\nDATASET LOADED")

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
# LABELS
# =====================================

y = df["category"]

print("\nCATEGORY LABELS")
print(y.unique())

# =====================================
# TRAIN TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =====================================
# CREATE MODEL
# =====================================

model = RandomForestClassifier()

# =====================================
# TRAIN MODEL
# =====================================

model.fit(X_train, y_train)

print("\nCATEGORY MODEL TRAINED")

# =====================================
# PREDICTIONS
# =====================================

predictions = model.predict(X_test)

print("\nPREDICTIONS")
print(predictions)

# =====================================
# ACCURACY
# =====================================

accuracy = accuracy_score(y_test, predictions)

print("\nMODEL ACCURACY")

print(round(accuracy * 100, 2), "%")

# =====================================
# CONFUSION MATRIX
# =====================================

matrix = confusion_matrix(
    y_test,
    predictions
)

print("\nCONFUSION MATRIX")

print(matrix)

# =====================================
# NEW ATHLETE PREDICTION
# =====================================

new_athlete = pd.DataFrame([[
    19,
    178,
    70,
    22.1,
    94,
    72,
    90,
    86.8
]], columns=[
    "age",
    "height",
    "weight",
    "BMI",
    "sprint_score",
    "endurance_score",
    "jump_score",
    "overall_score"
])

prediction = model.predict(new_athlete)

print("\nNEW ATHLETE CATEGORY")

print("Predicted Category:", prediction[0])