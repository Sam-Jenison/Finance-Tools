import tkinter as tk
from tkinter import messagebox
import math

def calculate_statistics(probabilities, returns, expected_return):
    # Calculate variance
    variance = sum(p * ((r - expected_return) ** 2) for p, r in zip(probabilities, returns))
    
    # Calculate standard deviation
    standard_deviation = math.sqrt(variance)
    
    # Calculate coefficient of variation (CV)
    if expected_return == 0:
        cv = float('inf')  # Avoid division by zero
    else:
        cv = standard_deviation / expected_return
    
    return variance, standard_deviation, cv

def solve_missing_values(expected_return, variance, standard_deviation, cv, probabilities, returns):
    # Check if expected return is missing
    if expected_return is None:
        if all(p is not None and r is not None for p, r in zip(probabilities, returns)):
            expected_return = sum(p * r for p, r in zip(probabilities, returns))
        else:
            messagebox.showinfo("Missing Data", "Please provide all required data to calculate the expected return.")
            return None, None, None, None
    
    # Calculate variance if missing
    if variance is None:
        if expected_return is not None and all(p is not None and r is not None for p, r in zip(probabilities, returns)):
            variance, standard_deviation, cv = calculate_statistics(probabilities, returns, expected_return)
        else:
            variance, standard_deviation, cv = None, None, None
    
    # Calculate standard deviation if missing
    if standard_deviation is None:
        if variance is not None:
            standard_deviation = math.sqrt(variance)
        else:
            standard_deviation = None
    
    # Calculate CV if missing
    if cv is None:
        if expected_return is not None and standard_deviation is not None:
            cv = standard_deviation / expected_return
        else:
            cv = None
    
    return expected_return, variance, standard_deviation, cv

def calculate_expected_return():
    try:
        n = int(entries_num.get())
        if n <= 0:
            raise ValueError("Number of scenarios must be a positive integer.")
        
        expected_return_input = entries_expected_return.get()
        
        # Parse input values
        expected_return = float(expected_return_input) if expected_return_input else None
        
        probabilities = []
        returns = []
        
        missing_prob_index = None
        missing_ret_index = None
        
        for i in range(n):
            prob = entries_probabilities[i].get()
            ret = entries_returns[i].get()
            
            if prob == "":
                missing_prob_index = i
                probabilities.append(None)
            else:
                prob = float(prob)
                if prob < 0 or prob > 1:
                    raise ValueError("Probability must be between 0 and 1.")
                probabilities.append(prob)
            
            if ret == "":
                missing_ret_index = i
                returns.append(None)
            else:
                ret = float(ret)
                returns.append(ret)
        
        # Solve for missing values
        expected_return, variance, standard_deviation, cv = solve_missing_values(
            expected_return, None, None, None, probabilities, returns
        )
        
        if expected_return is None:
            return
        
        if missing_prob_index is not None:
            missing_ret = returns[missing_prob_index]
            if missing_ret is not None:
                missing_prob = expected_return / missing_ret
                if 0 <= missing_prob <= 1:
                    probabilities[missing_prob_index] = missing_prob
                else:
                    raise ValueError("Calculated probability out of range (0 to 1).")
        
        if missing_ret_index is not None:
            missing_prob = probabilities[missing_ret_index]
            if missing_prob is not None:
                missing_ret = expected_return / missing_prob
                returns[missing_ret_index] = missing_ret
        
        # Calculate statistics
        variance, standard_deviation, cv = calculate_statistics(probabilities, returns, expected_return)
        
        # Display the results
        result_label.config(text=f"Expected Return: {expected_return:.4f}")
        result_formula_label.config(text="Expected Return Formula: Σ [P * R]")
        variance_label.config(text=f"Variance = Σ [P * (R - ER)²]: {variance:.4f}" if variance is not None else "Variance = Σ [P * (R - ER)²]: NA")
        std_dev_label.config(text=f"Standard Deviation = √Variance: {standard_deviation:.4f}" if standard_deviation is not None else "Standard Deviation = √Variance: NA")
        cv_label.config(text=f"Coefficient of Variation (CV) = Std Dev / ER: {cv:.4f}" if cv is not None else "Coefficient of Variation (CV) = Std Dev / ER: NA")
        
        # Update the entries
        for i, prob in enumerate(probabilities):
            if prob is not None:
                entries_probabilities[i].delete(0, tk.END)
                entries_probabilities[i].insert(0, f"{prob:.4f}")
        
        for i, ret in enumerate(returns):
            if ret is not None:
                entries_returns[i].delete(0, tk.END)
                entries_returns[i].insert(0, f"{ret:.4f}")
    
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def create_entries(n):
    for widget in entry_frame.winfo_children():
        widget.destroy()
    
    global entries_probabilities, entries_returns
    entries_probabilities = []
    entries_returns = []
    
    for i in range(n):
        tk.Label(entry_frame, text=f"Scenario {i+1} Return:").grid(row=i, column=0, padx=5, pady=5)
        ret_entry = tk.Entry(entry_frame)
        ret_entry.grid(row=i, column=1, padx=5, pady=5)
        entries_returns.append(ret_entry)
        
        tk.Label(entry_frame, text=f"Scenario {i+1} Probability:").grid(row=i, column=2, padx=5, pady=5)
        prob_entry = tk.Entry(entry_frame)
        prob_entry.grid(row=i, column=3, padx=5, pady=5)
        entries_probabilities.append(prob_entry)

    # Clear previous results
    result_label.config(text="Expected Return: ")
    result_formula_label.config(text="Expected Return Formula: ")
    variance_label.config(text="Variance = Σ [P * (R - ER)²]: ")
    std_dev_label.config(text="Standard Deviation = √Variance: ")
    cv_label.config(text="Coefficient of Variation (CV) = Std Dev / ER: ")

root = tk.Tk()
root.title("Expected Return Calculator")

# Number of scenarios
tk.Label(root, text="Number of Scenarios:").pack(pady=5)
entries_num = tk.Entry(root)
entries_num.pack(pady=5)

# Expected Return
tk.Label(root, text="Expected Return (Leave empty to calculate):").pack(pady=5)
entries_expected_return = tk.Entry(root)
entries_expected_return.pack(pady=5)

# Button to create input fields
tk.Button(root, text="Create Fields", command=lambda: create_entries(int(entries_num.get()))).pack(pady=5)

# Frame to hold return and probability entries
entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

# Button to calculate expected return and statistics
tk.Button(root, text="Calculate", command=calculate_expected_return).pack(pady=5)

# Labels to display results
result_label = tk.Label(root, text="Expected Return: ")
result_label.pack(pady=5)

result_formula_label = tk.Label(root, text="Expected Return Formula: Σ [P * R]")
result_formula_label.pack(pady=5)

variance_label = tk.Label(root, text="Variance = Σ [P * (R - ER)²]: ")
variance_label.pack(pady=5)

std_dev_label = tk.Label(root, text="Standard Deviation = √Variance: ")
std_dev_label.pack(pady=5)

cv_label = tk.Label(root, text="Coefficient of Variation (CV) = Std Dev / ER: ")
cv_label.pack(pady=5)

root.mainloop()
