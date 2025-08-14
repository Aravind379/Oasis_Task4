import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

# Put your API key here
API_KEY = "8a855ffab7af14b74ad842c9c6f875a2"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    """Fetch weather data for a given city from OpenWeatherMap API."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        messagebox.showerror("Error", f"Failed to fetch data:\n{err}")
        return None

def search_weather():
    """Trigger weather search when user clicks 'Search'."""
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Warning", "Please enter a city name!")
        return

    data = get_weather(city)
    if data and data.get("cod") == 200:
        show_weather(data)
    else:
        messagebox.showerror("Error", "City not found. Please check the spelling.")

def show_weather(data):
    """Update the GUI with weather details and icon."""
    city_name = f"{data['name']}, {data['sys']['country']}"
    temperature = f"{data['main']['temp']}°C"
    condition = data['weather'][0]['description'].capitalize()

    weather_label.config(text=f"{city_name}\n{temperature}\n{condition}")

    icon_code = data['weather'][0]['icon']
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    icon_response = requests.get(icon_url)
    icon_image = Image.open(BytesIO(icon_response.content))
    icon_photo = ImageTk.PhotoImage(icon_image)

    icon_label.config(image=icon_photo)
    icon_label.image = icon_photo  # Keep reference

# ------------------- GUI -------------------
root = tk.Tk()
root.title("Weather App")
root.geometry("300x300")
root.config(bg="lightblue")

city_entry = tk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=10)

search_btn = tk.Button(root, text="Search", font=("Arial", 12), command=search_weather)
search_btn.pack()

weather_label = tk.Label(root, text="", font=("Arial", 14), bg="lightblue")
weather_label.pack(pady=10)

icon_label = tk.Label(root, bg="lightblue")
icon_label.pack()

root.mainloop()
