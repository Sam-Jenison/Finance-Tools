import yfinance as yf
import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox

def fetch_closing_prices(ticker, start_date, end_date, interval='1d', monthly=False):
    """
    Fetch closing prices for a given ticker, start date, end date, and interval.
    
    :param ticker: Stock or index ticker symbol
    :param start_date: Start date in 'YYYY-MM-DD' format
    :param end_date: End date in 'YYYY-MM-DD' format
    :param interval: Data interval ('1d' for daily, '1mo' for monthly)
    :param monthly: If True, return the last trading day of each month
    :return: DataFrame containing the closing prices
    """
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date, interval=interval)
    
    # Remove timezone information from datetime index
    if data.index.tz is not None:
        data.index = data.index.tz_localize(None)
    
    # If monthly, get the last trading day of each month
    if monthly:
        data = data.resample('M').last()  # Resample to monthly and get the last entry (last trading day)
    
    return data['Close']

def save_to_excel(ticker, data, interval):
    """
    Save the closing prices to an Excel file.
    
    :param ticker: Stock or index ticker symbol
    :param data: DataFrame containing closing prices
    :param interval: Data interval ('daily' or 'monthly')
    """
    with pd.ExcelWriter(f'{ticker}_{interval}_closing_prices.xlsx', engine='openpyxl') as writer:
        data.to_excel(writer, sheet_name=f'{interval.capitalize()} Closing Prices')

def fetch_and_save_data():
    """
    Fetch and save data based on user input from a GUI.
    """
    ticker = simpledialog.askstring("Input", "Enter the ticker symbol:")
    if not ticker:
        messagebox.showerror("Input Error", "Ticker symbol cannot be empty.")
        return

    start_date = simpledialog.askstring("Input", "Enter the start date (YYYY-MM-DD):")
    end_date = simpledialog.askstring("Input", "Enter the end date (YYYY-MM-DD):")
    
    if not start_date or not end_date:
        messagebox.showerror("Input Error", "Start date and end date cannot be empty.")
        return
    
    interval = var_interval.get()
    
    if interval not in ['daily', 'monthly']:
        messagebox.showerror("Input Error", "Invalid interval selected.")
        return

    try:
        if interval == 'daily':
            closing_prices = fetch_closing_prices(ticker, start_date, end_date, interval='1d')
        elif interval == 'monthly':
            closing_prices = fetch_closing_prices(ticker, start_date, end_date, interval='1d', monthly=True)
        
        save_to_excel(ticker, closing_prices, interval)
        messagebox.showinfo("Success", f"Data saved to {ticker}_{interval}_closing_prices.xlsx")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_gui():
    """
    Create and display the GUI for user input.
    """
    global var_interval
    root = tk.Tk()
    root.title("Stock Data Fetcher")
    
    tk.Label(root, text="Select the interval for closing prices:").pack(pady=10)
    
    var_interval = tk.StringVar(value='daily')
    tk.OptionMenu(root, var_interval, 'daily', 'monthly').pack(pady=5)
    
    tk.Button(root, text="Submit", command=fetch_and_save_data).pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
