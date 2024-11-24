import tkinter as tk
from tkinter import messagebox
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Function to fetch and plot stock data
def plot_stock_data():
    # Get user inputs from the pop-up
    ticker = ticker_entry.get()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    # Convert start_date to a datetime object and subtract 20 days for WPVF calculation
    try:
        adjusted_start_date = (datetime.strptime(start_date, "%Y-%m-%d") - timedelta(days=20)).strftime("%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
        return

    # Fetch stock data from Yahoo Finance using yfinance (starting 20 days earlier for WPVF)
    try:
        stock_data = yf.download(ticker, start=adjusted_start_date, end=end_date)
        if stock_data.empty:
            raise ValueError("No data available for the given ticker or date range.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve data: {e}")
        return

    # Calculate WPVF (Weighted Price Volume Flow)
    stock_data['Previous Close'] = stock_data['Close'].shift(1)
    stock_data['Price Change'] = stock_data['Close'] - stock_data['Previous Close']
    
    # WPVF calculation with 20-period rolling sum for Volume
    stock_data['WPVF'] = stock_data['Price Change'] * stock_data['Volume'] / stock_data['Volume'].rolling(window=20).sum()
    
    # Fill NaN values (from rolling sum) with 0 to ensure the graph starts at the start date
    stock_data['WPVF'] = stock_data['WPVF'].fillna(0)

    # Trim the data to start from the actual user-specified start date
    stock_data = stock_data.loc[start_date:]

    # Create two subplots: one for closing price and one for WPVF
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Plot Closing Prices in the first subplot
    ax1.set_title(f"{ticker.upper()} Closing Prices")
    ax1.set_ylabel('Closing Price')
    ax1.plot(stock_data.index, stock_data['Close'], color='tab:blue', label='Close Price')
    ax1.grid(True)

    # Plot WPVF in the second subplot
    ax2.set_title(f"{ticker.upper()} WPVF (Weighted Price Volume Flow)")
    ax2.set_ylabel('WPVF')
    ax2.plot(stock_data.index, stock_data['WPVF'], color='tab:red', label='WPVF')
    ax2.grid(True)

    # Set x-axis label for the bottom graph
    ax2.set_xlabel('Date')

    # Adjust layout and show the plot
    fig.tight_layout()
    plt.show()

# Create the Tkinter window for input
root = tk.Tk()
root.title("Stock Data and WPVF Plotter")

# Labels and Entry widgets for ticker and date range
tk.Label(root, text="Stock Ticker:").grid(row=0, column=0, padx=10, pady=10)
ticker_entry = tk.Entry(root)
ticker_entry.grid(row=0, column=1)

tk.Label(root, text="Start Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)
start_date_entry = tk.Entry(root)
start_date_entry.grid(row=1, column=1)

tk.Label(root, text="End Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10)
end_date_entry = tk.Entry(root)
end_date_entry.grid(row=2, column=1)

# Button to plot data
plot_button = tk.Button(root, text="Plot Data", command=plot_stock_data)
plot_button.grid(row=3, columnspan=2, pady=20)

# Run the Tkinter event loop
root.mainloop()
