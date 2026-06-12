import pandas as pd

# Load dataset
data = pd.read_csv("dataset/athlete_data.csv")

# Display dataset
print(data)

# Display first 3 rows
print(data.head(3))

# Show column names
print(data.columns)

# Show athlete names
print(data["name"])

# Average sprint time
print("Average Sprint Time:", data["sprint_time"].mean())