import tkinter as tk
from tkinter import simpledialog, messagebox
import yfinance as yf

def get_latest_eps(ticker):
    """Fetches the most recent EPS for the given stock ticker."""
    stock = yf.Ticker(ticker)
    try:
        # Attempt to get EPS from the `info` dictionary
        eps = stock.info.get('trailingEps', None)
        if eps is not None:
            return eps
        raise ValueError("EPS data not available for this ticker.")
    except Exception as e:
        raise ValueError("Failed to fetch EPS data. Please check the ticker symbol.")

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Prompt user for stock ticker
    ticker = simpledialog.askstring("Stock Ticker", "Enter the stock ticker symbol:")
    if not ticker:
        messagebox.showerror("Input Error", "No ticker symbol entered.")
        return

    try:
        # Fetch the most recent EPS
        eps = get_latest_eps(ticker)
        messagebox.showinfo("Most Recent EPS",
                            f"Ticker: {ticker.upper()}\n"
                            f"Most Recent Earnings Per Share (EPS): ${eps:.2f}")
    except ValueError as e:
        messagebox.showerror("Data Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
