import tkinter as tk
from tkinter import messagebox


def calculate_bmi():
    try:
        # Get input values
        weight = float(entry_weight.get())
        height = float(entry_height.get()) / 100  # Convert cm to meters

        # BMI Formula: weight(kg) / height^2(m)
        bmi = weight / (height ** 2)
        bmi = round(bmi, 2)

        # Determine status and color
        if bmi < 18.5:
            status = "Underweight"
            color = "#3498db"  # Blue
        elif 18.5 <= bmi < 25:
            status = "Normal weight"
            color = "#2ecc71"  # Green
        elif 25 <= bmi < 30:
            status = "Overweight"
            color = "#f1c40f"  # Yellow
        else:
            status = "Obesity"
            color = "#e74c3c"  # Red

        # Update result labels
        label_result.config(text=f"Your BMI: {bmi}", fg=color)
        label_status.config(text=f"Status: {status}", fg=color)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for height and weight.")
    except ZeroDivisionError:
        messagebox.showerror("Input Error", "Height cannot be zero.")


# Initialize main window
root = tk.Tk()
root.title("Python BMI Calculator")
root.geometry("300x350")

# UI Layout
tk.Label(root, text="BMI Calculator", font=("Arial", 16, "bold"), pady=20).pack()

# Height Input
tk.Label(root, text="Height (cm):").pack()
entry_height = tk.Entry(root)
entry_height.pack(pady=5)

# Weight Input
tk.Label(root, text="Weight (kg):").pack()
entry_weight = tk.Entry(root)
entry_weight.pack(pady=5)

# Calculate Button
btn_calc = tk.Button(root, text="Calculate", command=calculate_bmi, bg="#34495e", fg="white", padx=10)
btn_calc.pack(pady=20)

# Display Results
label_result = tk.Label(root, text="Your BMI: --", font=("Arial", 12))
label_result.pack()

label_status = tk.Label(root, text="Status: --", font=("Arial", 12))
label_status.pack(pady=5)

# Run the application
root.mainloop()