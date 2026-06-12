# =====================================
# IMPORT LIBRARIES
# =====================================

import pandas as pd

# =====================================
# LOAD DATASET
# =====================================

df = pd.read_csv("dataset/athlete_data.csv")

# =====================================
# SHOW DATASET
# =====================================

print("\nFULL DATASET")
print(df)

# =====================================
# BASIC INFORMATION
# =====================================

print("\nDATASET INFO")
print(df.info())

# =====================================
# CHECK MISSING VALUES
# =====================================

print("\nMISSING VALUES")
print(df.isnull().sum())

# =====================================
# CHECK DUPLICATES
# =====================================

print("\nDUPLICATE ROWS")
print(df.duplicated().sum())

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

print("\nFEATURES")
print(X)

# =====================================
# LABELS
# =====================================

y = df["event"]

print("\nLABELS")
print(y)

# =====================================
# DATASET SHAPE
# =====================================

print("\nDATASET SHAPE")
print(df.shape)

# =====================================
# UNIQUE EVENTS
# =====================================

print("\nEVENT TYPES")
print(df["event"].unique())

# =====================================
# CATEGORY TYPES
# =====================================

print("\nCATEGORY TYPES")
print(df["category"].unique())

# =====================================
# SUMMARY STATISTICS
# =====================================

print("\nSUMMARY")
print(df.describe())