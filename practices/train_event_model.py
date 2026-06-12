# =====================================
# IMPORT LIBRARIES
# =====================================

import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import accuracy_score

# =====================================
# LOAD DATASET
# =====================================

df = pd.read_csv("dataset/athlete_data.csv")

print("\nDATASET LOADED SUCCESSFULLY")

print(df.head())

# =====================================
# FEATURES (INPUTS)
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
# LABELS (OUTPUT)
# =====================================

y = df["event"]

print("\nFEATURES")
print(X.head())

print("\nLABELS")
print(y.head())

# =====================================
# TRAIN TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTRAINING DATA SIZE")
print(len(X_train))

print("\nTESTING DATA SIZE")
print(len(X_test))

# =====================================
# CREATE MODEL
# =====================================

model = DecisionTreeClassifier()

# =====================================
# TRAIN MODEL
# =====================================

model.fit(X_train, y_train)

print("\nMODEL TRAINED SUCCESSFULLY")

# =====================================
# MAKE PREDICTIONS
# =====================================

predictions = model.predict(X_test)

print("\nMODEL PREDICTIONS")
print(predictions)

# =====================================
# CHECK ACCURACY
# =====================================

accuracy = accuracy_score(y_test, predictions)

print("\nMODEL ACCURACY")

print(round(accuracy * 100, 2), "%")

# =====================================
# NEW ATHLETE PREDICTION
# =====================================

new_athlete = pd.DataFrame([[
    19,     # age
    178,    # height
    70,     # weight
    22.1,   # BMI
    94,     # sprint_score
    72,     # endurance_score
    90,     # jump_score
    86.8    # overall_score
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

print("\nNEW ATHLETE PREDICTION")

print("Predicted Event:", prediction[0])