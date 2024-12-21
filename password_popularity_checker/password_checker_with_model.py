import pickle
import tkinter as tk
from tkinter import PhotoImage, Toplevel
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load the trained model
with open("models/password_popularity_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Helper functions for password analysis
def estimate_password_popularity(password):
    """Estimate how many people use the password based on model features."""
    length = len(password)
    unique_characters = len(set(password))
    contains_numbers = any(char.isdigit() for char in password)
    
    # Prepare features for the model
    features = np.array([[length, unique_characters, int(contains_numbers)]])
    estimated_popularity = model.predict(features)
    
    # Round the result to give an approximate popularity count
    return max(int(estimated_popularity[0]), 0)

def analyze_password_strength(password):
    """Analyze password strength based on length, character types, etc."""
    length = len(password)
    has_numbers = any(char.isdigit() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_special = any(not char.isalnum() for char in password)
    
    # Basic scoring for password strength
    score = 0
    score += 1 if length >= 8 else 0
    score += 1 if has_numbers else 0
    score += 1 if has_upper else 0
    score += 1 if has_special else 0

    if score <= 1:
        strength = "Weak"
    elif score == 2:
        strength = "Moderate"
    else:
        strength = "Strong"

    return strength, score

def calculate_hack_time(password):
    """Estimate time to crack password based on character variety and length."""
    length = len(password)
    char_types = [
        any(char.islower() for char in password),
        any(char.isupper() for char in password),
        any(char.isdigit() for char in password),
        any(not char.isalnum() for char in password)
    ]
    char_space = sum(26 if t else 0 for t in char_types[:2]) + (10 if char_types[2] else 0) + (10 if char_types[3] else 0)
    attempts = char_space ** length

    seconds_to_crack = attempts / 1e6  # Assume 1 million attempts per second
    if seconds_to_crack < 60:
        return f"{seconds_to_crack:.2f} seconds"
    elif seconds_to_crack < 3600:
        return f"{seconds_to_crack / 60:.2f} minutes"
    elif seconds_to_crack < 86400:
        return f"{seconds_to_crack / 3600:.2f} hours"
    else:
        return f"{seconds_to_crack / 86400:.2f} days"

def provide_recommendations(password):
    """Provide password improvement recommendations."""
    recommendations = []
    if len(password) < 8:
        recommendations.append("Increase length to at least 8 characters.")
    if not any(char.isdigit() for char in password):
        recommendations.append("Add at least one numeric character.")
    if not any(char.isupper() for char in password):
        recommendations.append("Include uppercase letters.")
    if not any(not char.isalnum() for char in password):
        recommendations.append("Add special characters like !, @, #, etc.")

    return recommendations if recommendations else ["Your password is strong!"]

def show_password_analytics(password):
    """Show detailed password analytics in a new window."""
    analytics_window = Toplevel(root)
    analytics_window.title("Password Analytics")
    analytics_window.geometry("600x500")
    analytics_window.configure(bg="#2b2b2b")
    
    estimated_popularity = estimate_password_popularity(password)
    strength, score = analyze_password_strength(password)
    recommendations = provide_recommendations(password)
    crack_time = calculate_hack_time(password)
    
    # Display analytics
    tk.Label(analytics_window, text=f"Estimated Popularity: {estimated_popularity}", font=("Arial", 12), 
             fg="white", bg="#2b2b2b").pack(pady=5)
    tk.Label(analytics_window, text=f"Password Strength: {strength}", font=("Arial", 12), 
             fg="white", bg="#2b2b2b").pack(pady=5)
    tk.Label(analytics_window, text=f"Estimated Time to Hack: {crack_time}", font=("Arial", 12), 
             fg="white", bg="#2b2b2b").pack(pady=5)
    tk.Label(analytics_window, text="Recommendations:", font=("Arial", 12, "underline"), 
             fg="#FFD700", bg="#2b2b2b").pack(pady=5)
    
    for rec in recommendations:
        tk.Label(analytics_window, text=rec, font=("Arial", 10), fg="light gray", bg="#2b2b2b").pack()
    
    # Generate Character Distribution Bar Chart
    character_types = ['Length', 'Unique Characters', 'Numbers', 'Uppercase', 'Special']
    values = [
        len(password),
        len(set(password)),
        sum(1 for char in password if char.isdigit()),
        sum(1 for char in password if char.isupper()),
        sum(1 for char in password if not char.isalnum())
    ]

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))

    # Bar Chart
    ax[0].bar(character_types, values, color=['#FF6347', '#4682B4', '#3CB371', '#FFD700', '#FF69B4'])
    ax[0].set_title("Character Distribution")
    ax[0].set_ylabel("Count")
    ax[0].set_xlabel("Character Types")
    ax[0].tick_params(axis='x', rotation=30)

    # Pie Chart
    labels = ["Other Users", "You"]
    sizes = [1000000 - estimated_popularity, estimated_popularity]
    colors = ["#d3d3d3", "#4682B4"]
    ax[1].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax[1].set_title("Popularity of Password")

    # Display the chart in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, analytics_window)
    canvas.get_tk_widget().pack(pady=10)
    canvas.draw()

    # Back Button to Close Analytics Window
    def go_back():
        analytics_window.destroy()

    back_button = tk.Button(analytics_window, text="Back", command=go_back, font=("Arial", 10, "bold"),
                            bg="#5f9ea0", fg="white", activebackground="#4682b4", activeforeground="white")
    back_button.pack(pady=10)
