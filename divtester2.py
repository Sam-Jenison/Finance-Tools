import tkinter as tk
from tkinter import messagebox
import yfinance as yf
from tkcalendar import DateEntry
from datetime import date
from tkinter import ttk
from collections import defaultdict
from ttkthemes import ThemedStyle


def validate_year(date_entry):
    year = date_entry.get_date().year
    if year < 1000 or year > 9999:
        messagebox.showwarning("Invalid Year", "Please enter a four-digit year.")
        date_entry.set_date(None)


def get_stock_info(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        stock_name = info.get('longName', '')
        currency = info.get('currency', '')
        return stock_name, currency
    except Exception as e:
        print(f"Error: {str(e)}")
        messagebox.showwarning("Error", f"Failed to fetch stock information. Please check the console.")
        return '', ''


def calculate_total_dividends(symbol, start_date, end_date, shares):
    try:
        stock = yf.Ticker(symbol)
        dividends = stock.dividends

        # Filter dividends based on date range
        filtered_dividends = dividends.loc[start_date:end_date]

        total_dividends = filtered_dividends.sum() * shares
        return total_dividends
    except Exception as e:
        print(f"Error: {str(e)}")
        messagebox.showwarning("Error", f"Failed to calculate total dividends. Please check the console.")


def calculate_button_click():
    symbol = symbol_entry.get()
    start_date = start_calendar.get_date().strftime("%Y-%m-%d")
    end_date = end_calendar.get_date().strftime("%Y-%m-%d")
    shares = float(shares_entry.get())

    stock_name, currency = get_stock_info(symbol)
    if not stock_name:
        return

    total_dividends = calculate_total_dividends(symbol, start_date, end_date, shares)

    if total_dividends is not None:
        dividends_text = f"Total Dividends:"
        total_sum_label.configure(text=dividends_text)

        # Add data to the table
        ticker = symbol.upper()  # Capitalize the stock ticker
        dividend_total = f"${total_dividends:.3f}"  # Rounded to 3 decimal places with dollar sign
        table.insert("", "end", values=(ticker, stock_name, f"{start_date} - {end_date}", dividend_total, currency,
                                        shares))

        # Update the total dividends sum
        update_total_dividends_sum()


def reset_button_click():
    # Clear input fields and table
    symbol_entry.delete(0, tk.END)
    start_calendar.set_date(date.today())
    end_calendar.set_date(date.today())
    shares_entry.delete(0, tk.END)
    total_sum_label.configure(text="")
    table.delete(*table.get_children())

    # Update the total dividends sum
    update_total_dividends_sum()


def update_total_dividends_sum():
    total_sum = defaultdict(float)
    for item in table.get_children():
        dividend_total = float(table.item(item)["values"][3].replace("$", ""))
        currency = table.item(item)["values"][4]
        total_sum[currency] += dividend_total

    total_dividends_text = "Total Dividends:"
    for currency, total in total_sum.items():
        total_dividends_text += f" {total:.2f} {currency}"
    total_sum_label.configure(text=total_dividends_text)


def show_message_box():
    messagebox.showinfo("Message", "Hello, this is a themed message box!")


window = tk.Tk()
window.title("Dividend Calculator")
window.geometry("1000x750")

# Create a themed style for the window
style = ThemedStyle(window)
style.set_theme("equilux")  # Set the theme to "equilux"

symbol_label = tk.Label(window, text="Stock Symbol:")
symbol_label.pack()
symbol_entry = tk.Entry(window)
symbol_entry.pack()
symbol_entry.focus()

start_label = tk.Label(window, text="Start Date (dd/mm/yyyy):")
start_label.pack()
start_calendar = DateEntry(window, width=12, background='green',
                           foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
start_calendar.pack()
start_calendar.set_date(date.today())
start_calendar.bind("<<DateEntrySelected>>", lambda event: validate_year(start_calendar))

end_label = tk.Label(window, text="End Date (dd/mm/yyyy):")
end_label.pack()
end_calendar = DateEntry(window, width=12, background='green',
                         foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
end_calendar.pack()
end_calendar.set_date(date.today())
end_calendar.bind("<<DateEntrySelected>>", lambda event: validate_year(end_calendar))

shares_label = tk.Label(window, text="Number of Shares:")
shares_label.pack()
shares_entry = tk.Entry(window)
shares_entry.pack()

calculate_button = tk.Button(window, text="Calculate", command=calculate_button_click)
calculate_button.pack()

reset_button = tk.Button(window, text="Reset", command=reset_button_click)
reset_button.pack()

total_sum_label = tk.Label(window, text="")
total_sum_label.pack()

# Create a table to display dividend data
table_frame = ttk.Frame(window)
table_frame.pack(pady=20)

table_columns = ("Stock Ticker", "Stock Name", "Date Range", "Dividend Total", "Currency", "Number of Shares")
table = ttk.Treeview(table_frame, columns=table_columns, show="headings")
table.pack()

for column in table_columns:
    table.heading(column, text=column)
    table.column(column, width=150)

message_box_button = tk.Button(window, text="Show Message Box", command=show_message_box)
message_box_button.pack()

window.mainloop()
