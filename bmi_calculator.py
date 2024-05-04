import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class BMI_Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("BMI Calculator")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.label_weight = tk.Label(self.frame, text="Weight (kg):")
        self.label_weight.grid(row=0, column=0, padx=10, pady=5)
        self.entry_weight = tk.Entry(self.frame)
        self.entry_weight.grid(row=0, column=1, padx=10, pady=5)

        self.label_height = tk.Label(self.frame, text="Height (m):")
        self.label_height.grid(row=1, column=0, padx=10, pady=5)
        self.entry_height = tk.Entry(self.frame)
        self.entry_height.grid(row=1, column=1, padx=10, pady=5)

        self.calculate_button = tk.Button(self.frame, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        self.clear_button = tk.Button(self.frame, text="Clear", command=self.clear_entries)
        self.clear_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.frame_result = tk.Frame(self.master)
        self.frame_result.pack(pady=10)

        self.label_result = tk.Label(self.frame_result, text="")
        self.label_result.pack()

    def calculate_bmi(self):
        weight = float(self.entry_weight.get())
        height = float(self.entry_height.get())
        bmi = weight / (height ** 2)
        bmi_category = self.get_bmi_category(bmi)
        self.display_result(bmi, bmi_category)

        # Save data to a file
        with open("bmi_data.txt", "a") as file:
            file.write(f"Weight: {weight} kg, Height: {height} m, BMI: {bmi}, Category: {bmi_category}\n")

    def get_bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def display_result(self, bmi, category):
        self.label_result.config(text=f"Your BMI is: {bmi:.2f} ({category})")

    def clear_entries(self):
        self.entry_weight.delete(0, tk.END)
        self.entry_height.delete(0, tk.END)
        self.label_result.config(text="")

def plot_bmi_data():
    weights = []
    heights = []
    with open("bmi_data.txt", "r") as file:
        for line in file:
            weight = float(line.split(",")[0].split(":")[1].strip(" kg"))
            height = float(line.split(",")[1].split(":")[1].strip(" m"))
            weights.append(weight)
            heights.append(height)

    plt.scatter(weights, heights)
    plt.xlabel('Weight (kg)')
    plt.ylabel('Height (m)')
    plt.title('BMI Data')
    plt.show()

def main():
    root = tk.Tk()
    app = BMI_Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
