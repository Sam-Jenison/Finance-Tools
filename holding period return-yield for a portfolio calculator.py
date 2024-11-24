import tkinter as tk
from tkinter import ttk

class InvestmentCalculator:
    def __init__(self, root):
        # Set the window size to be larger (4 cm wider and longer)
        root.geometry("700x550")  # Approximate size: (700 pixels wide, 550 pixels tall)
        
        self.root = root
        self.root.title("Investment Calculator")
        
        # Create column headers
        headers = ["Shares", "Starting Price", "Beginning Market Value",
                   "Ending Price", "Ending Market Value", "Holding Period Return",
                   "Holding Period Yield", "Percent Weight", "Weighted HPY"]
        
        for col, header in enumerate(headers):
            label = tk.Label(root, text=header, relief=tk.RAISED)
            label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

        # Create entry fields for up to 10 investments
        self.entries = []
        self.num_investments = 10
        
        for i in range(self.num_investments):
            row_entries = []
            for j in range(len(headers)):
                entry = tk.Entry(root)
                entry.grid(row=i+1, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)
        
        # Button to compute results
        compute_button = tk.Button(root, text="Compute", command=self.compute)
        compute_button.grid(row=self.num_investments+1, column=0, columnspan=9, pady=10)
        
    def compute(self):
        total_market_value_beginning = 0
        total_market_value_ending = 0
        
        for i in range(self.num_investments):
            try:
                shares = float(self.entries[i][0].get())
                start_price = float(self.entries[i][1].get())
                end_price = float(self.entries[i][3].get())
                
                begin_market_value = shares * start_price
                end_market_value = shares * end_price
                hpr = end_market_value / begin_market_value if begin_market_value != 0 else 0
                hpy = hpr - 1
                
                total_market_value_beginning += begin_market_value
                total_market_value_ending += end_market_value
                
                # Update entry fields with calculated values
                self.entries[i][2].delete(0, tk.END)
                self.entries[i][2].insert(0, f"{begin_market_value:.2f}")
                
                self.entries[i][4].delete(0, tk.END)
                self.entries[i][4].insert(0, f"{end_market_value:.2f}")
                
                self.entries[i][5].delete(0, tk.END)
                self.entries[i][5].insert(0, f"{hpr:.2f}")
                
                self.entries[i][6].delete(0, tk.END)
                self.entries[i][6].insert(0, f"{hpy:.2f}")
                
            except ValueError:
                # Clear results if input is invalid
                self.entries[i][2].delete(0, tk.END)
                self.entries[i][4].delete(0, tk.END)
                self.entries[i][5].delete(0, tk.END)
                self.entries[i][6].delete(0, tk.END)
        
        for i in range(self.num_investments):
            try:
                begin_market_value = float(self.entries[i][2].get())
                percent_weight = (begin_market_value / total_market_value_beginning) if total_market_value_beginning != 0 else 0
                weighted_hpy = float(self.entries[i][6].get()) * percent_weight
                
                self.entries[i][7].delete(0, tk.END)
                self.entries[i][7].insert(0, f"{percent_weight:.2%}")
                
                self.entries[i][8].delete(0, tk.END)
                self.entries[i][8].insert(0, f"{weighted_hpy:.2%}")
                
            except ValueError:
                # Clear weight and weighted HPY if input is invalid
                self.entries[i][7].delete(0, tk.END)
                self.entries[i][8].delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = InvestmentCalculator(root)
    root.mainloop()
