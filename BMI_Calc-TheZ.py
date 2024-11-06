# TheZ's BMI Calculator

import customtkinter as ctk
from tkinter import messagebox
import math # Ignore this line

ctk.set_appearance_mode("Dark") # Main theme mode
ctk.set_default_color_theme("dark-blue")


MIN_WEIGHT_KG, MAX_WEIGHT_KG = 20, 300  
MIN_HEIGHT_M, MAX_HEIGHT_M = 0.5, 2.5   
MIN_AGE, MAX_AGE = 2, 120               


def obf_calc(weight: float, height_m: float) -> float:
    return round(weight / (height_m ** 2), 2)


def obf_body_fat_percentage(bmi: float, age: int, gender: str) -> float:
    if gender == "Male":
        body_fat = (1.20 * bmi) + (0.23 * age) - 16.2
    elif gender == "Female":
        body_fat = (1.20 * bmi) + (0.23 * age) - 5.4
    else:
        body_fat = (1.20 * bmi) + (0.23 * age) - 10
    return round(body_fat, 2)

# BMR Calculation using Mifflin-St Jeor Equation
def calculate_bmr(weight: float, height_cm: float, age: int, gender: str) -> float:
    if gender == "Male":
        return round(10 * weight + 6.25 * height_cm - 5 * age + 5, 2)
    elif gender == "Female":
        return round(10 * weight + 6.25 * height_cm - 5 * age - 161, 2)
    else:
        return round(10 * weight + 6.25 * height_cm - 5 * age - 78, 2)

# Macro Nutrient Recommendation based on BMR
def macro_nutrient_recommendation(bmr: float) -> str:
    protein = round(bmr * 0.3 / 4)
    carbs = round(bmr * 0.5 / 4)
    fats = round(bmr * 0.2 / 9)
    return f"Recommended Daily Intake:\nProtein: {protein}g, Carbs: {carbs}g, Fats: {fats}g"


def validate_inputs(weight: float, height_m: float, age: int) -> bool:
    if not (MIN_WEIGHT_KG <= weight <= MAX_WEIGHT_KG):
        weight_entry.configure(fg_color="red")
        return False
    if not (MIN_HEIGHT_M <= height_m <= MAX_HEIGHT_M):
        height_entry.configure(fg_color="red")
        return False
    if not (MIN_AGE <= age <= MAX_AGE):
        age_entry.configure(fg_color="red")
        return False
    return True



def reset_entry_colors():
    weight_entry.configure(fg_color=("white", "gray14"))
    height_entry.configure(fg_color=("white", "gray14"))
    age_entry.configure(fg_color=("white", "gray14"))


def obf_classify_bmi(obf_bmi: float, obf_age: int, obf_gender: str, obf_bmr: float, body_fat: float) -> str:
    classification = ""
    if obf_age < 2:
        classification = "BMI classification not available for infants"
    elif obf_bmi < 18.5:
        classification = "Underweight - Aim to increase nutrition intake."
    elif 18.5 <= obf_bmi < 24.9:
        classification = "Normal weight - Maintain current lifestyle."
    elif 25 <= obf_bmi < 29.9:
        classification = "Overweight - Consider increased activity."
    else:
        classification = "Obesity - Consult healthcare provider."

    
    if body_fat < 10:
        classification += " Low body fat - Ensure sufficient calorie intake."
    elif body_fat > 30:
        classification += " High body fat - A balanced diet is recommended."

    return classification + f" BMR: {obf_bmr} kcal/day"


def obf_calculate():
    try:
        print(f"Converting weight: {weight_entry.get()}")
        obf_weight = float(weight_entry.get())
        
        print(f"Converting height: {height_entry.get()}")
        obf_height_value = float(height_entry.get())
        
        print(f"Converting age: {age_entry.get()}")
        obf_age = int(age_entry.get())
        
        obf_height_unit = height_unit_var.get()
        obf_gender = gender_var.get()

        obf_height_m = obf_height_value / 100 if obf_height_unit == "cm" else obf_height_value
        obf_height_cm = obf_height_value if obf_height_unit == "cm" else obf_height_value * 100
        
        print(f"Height in meters: {obf_height_m}")
        
        
        print(f"Validating - Weight range: {MIN_WEIGHT_KG} <= {obf_weight} <= {MAX_WEIGHT_KG}")
        print(f"Validating - Height range: {MIN_HEIGHT_M} <= {obf_height_m} <= {MAX_HEIGHT_M}")
        print(f"Validating - Age range: {MIN_AGE} <= {obf_age} <= {MAX_AGE}")

        
        reset_entry_colors()
        if not validate_inputs(obf_weight, obf_height_m, obf_age):
            messagebox.showwarning("Input Error", "Please ensure all inputs are within valid ranges.")
            return
        
        print("Starting calculations...")
        obf_bmi = obf_calc(obf_weight, obf_height_m)
        print(f"BMI calculated: {obf_bmi}")
        obf_bmr = calculate_bmr(obf_weight, obf_height_cm, obf_age, obf_gender)
        print(f"BMR calculated: {obf_bmr}")
        obf_body_fat = obf_body_fat_percentage(obf_bmi, obf_age, obf_gender)
        print(f"Body fat calculated: {obf_body_fat}")
        obf_classification = obf_classify_bmi(obf_bmi, obf_age, obf_gender, obf_bmr, obf_body_fat)
        macro_recommendations = macro_nutrient_recommendation(obf_bmr)

        
        result_label.configure(text=f"BMI: {obf_bmi}")
        classification_label.configure(text=f"Classification: {obf_classification}")
        body_fat_label.configure(text=f"Body Fat %: {obf_body_fat}")
        bmr_label.configure(text=f"BMR: {obf_bmr} kcal/day")
        macro_label.configure(text=macro_recommendations)

    except ValueError as e:
        print(f"Error occurred: {str(e)}") 
        messagebox.showerror("Input Error", "Please enter valid numbers for weight, height, and age.")


def obf_clear():
    weight_entry.delete(0, ctk.END)
    height_entry.delete(0, ctk.END)
    age_entry.delete(0, ctk.END)
    gender_var.set("Select")
    height_unit_var.set("m")
    reset_entry_colors()  
    result_label.configure(text="BMI: ")
    classification_label.configure(text="Classification: ")
    body_fat_label.configure(text="Body Fat %: ")
    bmr_label.configure(text="BMR: ")
    macro_label.configure(text="")


def obf_switch_theme(choice):
    themes = {"retro": "green", "neon": "pink", "city": "dark-blue", "default": "blue"}
    ctk.set_default_color_theme(themes.get(choice, "blue"))


app = ctk.CTk()
app.title("BMI & Health Calculator - TheZ")
app.geometry("700x900")
app.resizable(False, False)
app.iconbitmap("icon.ico")

title_label = ctk.CTkLabel(app, text="BMI & Health Calculator - TheZ", font=("Helvetica", 20, "bold"))
title_label.pack(pady=10)


weight_label = ctk.CTkLabel(app, text="Enter weight (kg):")
weight_label.pack(pady=(10, 5))
weight_entry = ctk.CTkEntry(app, placeholder_text="e.g. 70")
weight_entry.pack(pady=(0, 10))


height_label = ctk.CTkLabel(app, text="Enter height:")
height_label.pack(pady=(10, 5))
height_frame = ctk.CTkFrame(app)
height_frame.pack(pady=(0, 10), padx=10, fill="x")
height_entry = ctk.CTkEntry(height_frame, placeholder_text="e.g. 175, 1.75")
height_entry.pack(side="left", expand=True, fill="x", padx=5)
height_unit_var = ctk.StringVar(value="m")
height_unit_menu = ctk.CTkOptionMenu(height_frame, variable=height_unit_var, values=["m", "cm"])
height_unit_menu.pack(side="right", padx=5)


age_label = ctk.CTkLabel(app, text="Enter age:")
age_label.pack(pady=(10, 5))
age_entry = ctk.CTkEntry(app, placeholder_text="e.g. 25")
age_entry.pack(pady=(0, 10))


gender_label = ctk.CTkLabel(app, text="Select gender:")
gender_label.pack(pady=(10, 5))
gender_var = ctk.StringVar(value="Select")
gender_menu = ctk.CTkOptionMenu(app, variable=gender_var, values=["Male", "Female", "Other"])
gender_menu.pack(pady=(0, 10))


calculate_button = ctk.CTkButton(app, text="Calculate BMI & Metrics", command=obf_calculate)
calculate_button.pack(pady=15)


result_label = ctk.CTkLabel(app, text="BMI: ", font=("Helvetica", 14))
result_label.pack(pady=(10, 5))

classification_label = ctk.CTkLabel(app, text="Classification: ", font=("Helvetica", 14))
classification_label.pack(pady=5)

body_fat_label = ctk.CTkLabel(app, text="Body Fat %: ", font=("Helvetica", 14))
body_fat_label.pack(pady=5)

bmr_label = ctk.CTkLabel(app, text="BMR: ", font=("Helvetica", 14))
bmr_label.pack(pady=5)

macro_label = ctk.CTkLabel(app, text="", font=("Helvetica", 12))
macro_label.pack(pady=(5, 10))


clear_button = ctk.CTkButton(app, text="Clear Fields", command=obf_clear)
clear_button.pack(pady=10)


theme_label = ctk.CTkLabel(app, text="Select Theme: (Doesn't work yet)", font=("Helvetica", 12))
theme_label.pack(pady=(10, 5))
theme_var = ctk.StringVar(value="default")
theme_menu = ctk.CTkOptionMenu(app, variable=theme_var, values=["default", "retro", "neon", "city"], command=obf_switch_theme)
theme_menu.pack(pady=(0, 20))

app.mainloop()
