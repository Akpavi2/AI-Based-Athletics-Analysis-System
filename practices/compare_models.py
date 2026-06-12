# =====================================
# IMPORT LIBRARIES
# =====================================

import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier

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

y = df["event"]

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
# DECISION TREE MODEL
# =====================================

decision_model = DecisionTreeClassifier()

decision_model.fit(X_train, y_train)

decision_predictions = decision_model.predict(X_test)

decision_accuracy = accuracy_score(
    y_test,
    decision_predictions
)

print("\nDECISION TREE ACCURACY")

print(round(decision_accuracy * 100, 2), "%")

# =====================================
# RANDOM FOREST MODEL
# =====================================

random_model = RandomForestClassifier()

random_model.fit(X_train, y_train)

random_predictions = random_model.predict(X_test)

random_accuracy = accuracy_score(
    y_test,
    random_predictions
)

print("\nRANDOM FOREST ACCURACY")

print(round(random_accuracy * 100, 2), "%")

# =====================================
# CONFUSION MATRIX
# =====================================

matrix = confusion_matrix(
    y_test,
    random_predictions
)

print("\nCONFUSION MATRIX")

print(matrix)

# =====================================
# MODEL COMPARISON
# =====================================

print("\nMODEL COMPARISON")

if random_accuracy > decision_accuracy:

    print("Random Forest Performs Better")

elif decision_accuracy > random_accuracy:

    print("Decision Tree Performs Better")

else:

    print("Both Models Perform Same")

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

prediction = random_model.predict(new_athlete)

print("\nNEW ATHLETE PREDICTION")

print("Predicted Event:", prediction[0])