import tkinter as tk
from tkinter import ttk
import requests
import win32print

def get_metar_for_icao(icao_code):
    global response
    base_url = f"https://aviationweather.gov/api/data/metar?taf=true&ids={icao_code}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}\nResponse content: {response.text}"
    except Exception as e:
        return f"Error: {e}"

def fetch_metar():
    icao_code = entry.get().strip().upper()
    if not icao_code:
        result_text.set("ICAO code cannot be empty.")
        return
    metar_data = get_metar_for_icao(icao_code)
    result_text.set(metar_data)
    print_to_printer(metar_data)

def print_to_printer(data):
    printer_name = win32print.GetDefaultPrinter()
    hprinter = win32print.OpenPrinter(printer_name)
    try:
        hjob = win32print.StartDocPrinter(hprinter, 1, ("METAR Data", None, "RAW"))
        try:
            win32print.StartPagePrinter(hprinter)
            raw_data = data.encode('utf-8')
            win32print.WritePrinter(hprinter, raw_data)
            win32print.EndPagePrinter(hprinter)
        finally:
            win32print.EndDocPrinter(hprinter)
    finally:
        win32print.ClosePrinter(hprinter)

#gui 
root = tk.Tk()
root.title("METAR Report")

#wigets fixed a
label = ttk.Label(root, text="Enter ICAO code:")
label.pack(pady=10)

entry = ttk.Entry(root, width=40)
entry.pack(pady=10)

fetch_button = ttk.Button(root, text="Fetch METAR", command=fetch_metar)
fetch_button.pack(pady=10)

result_text = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_text, wraplength=400)
result_label.pack(pady=10)

root.mainloop()
