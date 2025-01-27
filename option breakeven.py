import tkinter as tk
from tkinter import messagebox

def calculate_break_even():
    try:
        strike_price = float(entry_strike_price.get())
        premium = float(entry_premium.get())

        if var_long_call.get():
            result = strike_price + abs(premium)  # Treat premium as cost for long call
            message = f"Break-even for Long Call: {result:.2f}"
        elif var_short_call.get():
            result = strike_price + abs(premium)  # Treat premium as income for short call
            message = f"Break-even for Short Call: {result:.2f}"
        elif var_long_put.get():
            result = strike_price - abs(premium)  # Treat premium as cost for long put
            message = f"Break-even for Long Put: {result:.2f}"
        elif var_short_put.get():
            result = strike_price - abs(premium)  # Treat premium as income for short put
            message = f"Break-even for Short Put: {result:.2f}"
        else:
            message = "Please select a trade type (Long/Short, Call/Put)."

        messagebox.showinfo("Break-even Result", message)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values for strike price and premium.")

# Create the main application window
root = tk.Tk()
root.title("Options Break-even Calculator")
root.geometry("400x300")

# Strike Price Entry
label_strike_price = tk.Label(root, text="Strike Price:")
label_strike_price.pack(pady=5)
entry_strike_price = tk.Entry(root)
entry_strike_price.pack(pady=5)

# Premium Entry
label_premium = tk.Label(root, text="Premium (absolute value):")
label_premium.pack(pady=5)
entry_premium = tk.Entry(root)
entry_premium.pack(pady=5)

# Checkboxes for Trade Type
var_long_call = tk.BooleanVar()
var_short_call = tk.BooleanVar()
var_long_put = tk.BooleanVar()
var_short_put = tk.BooleanVar()

checkbox_long_call = tk.Checkbutton(root, text="Long Call", variable=var_long_call)
checkbox_long_call.pack(pady=5)
checkbox_short_call = tk.Checkbutton(root, text="Short Call", variable=var_short_call)
checkbox_short_call.pack(pady=5)
checkbox_long_put = tk.Checkbutton(root, text="Long Put", variable=var_long_put)
checkbox_long_put.pack(pady=5)
checkbox_short_put = tk.Checkbutton(root, text="Short Put", variable=var_short_put)
checkbox_short_put.pack(pady=5)

# Calculate Button
button_calculate = tk.Button(root, text="Calculate Break-even", command=calculate_break_even)
button_calculate.pack(pady=20)

# Run the application
root.mainloop()
