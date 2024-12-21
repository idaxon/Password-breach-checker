import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Sample synthetic password data (length, unique_characters, contains_numbers, frequency)
data = [
    (6, 2, 1, 80000),  # e.g., "123456"
    (8, 6, 0, 45000),  # e.g., "password"
    (9, 4, 1, 50000),  # e.g., "123456789"
    (5, 5, 0, 20000),  # e.g., "abcde"
    (6, 3, 1, 30000),  # e.g., "qwerty"
    (8, 8, 1, 10000),  # e.g., "iloveyou"
    (4, 1, 1, 90000),  # e.g., "1111"
    (7, 6, 1, 5000),   # e.g., "sunshine"
    (9, 7, 0, 6000),   # e.g., "letmein"
    (10, 8, 1, 3000),  # e.g., "password1"
]

# Convert data to feature matrix X and target vector y
X = np.array([(length, unique_chars, contains_numbers) for length, unique_chars, contains_numbers, _ in data])
y = np.array([freq for _, _, _, freq in data])

#  linear regression model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# Save trained model
with open("models/password_popularity_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

print("Model trained and saved as password_popularity_model.pkl")
