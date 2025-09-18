
import requests
import matplotlib.pyplot as plt
import os
import json

# --- Configuration ---
CITY =  input("Enter the your city") # You can change this to any city you want to check

# --- File Paths ---
# Get the absolute path of the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(SCRIPT_DIR, "weather_plot.png")
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")

def get_api_key():
    """
    Reads the API key from the config.json file.
    """
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: Configuration file not found at {CONFIG_PATH}")
        print("Please create a 'config.json' file in the same directory with your API key.")
        return None

    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
            api_key = config.get("Default")
            if not api_key or api_key == "your_api_key_here":
                print("Please add your OpenWeatherMap API key to the 'config.json' file.")
                return None
            return api_key
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading configuration file: {e}")
        return None

def get_weather_data(city, api_key):
    """
    Fetches 5-day weather forecast data from the OpenWeatherMap API.
    """
    if not api_key:
        return None

    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # Use "imperial" for Fahrenheit
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def plot_weather_data(data, city):
    """
    Creates and saves a line plot of temperature and humidity over time.
    """
    if not data:
        print("No data to plot.")
        return

    # Extract timestamps, temperatures, and humidity from the data
    timestamps = [item['dt_txt'] for item in data['list']]
    temperatures = [item['main']['temp'] for item in data['list']]
    humidity = [item['main']['humidity'] for item in data['list']]

    # Create the plot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot Temperature
    color = 'tab:red'
    ax1.set_xlabel('Date and Time')
    ax1.set_ylabel('Temperature (°C)', color=color)
    ax1.plot(timestamps, temperatures, color=color, marker='o', linestyle='-', label='Temperature')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.tick_params(axis='x', rotation=45)

    # Create a second y-axis for Humidity
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Humidity (%)', color=color)
    ax2.plot(timestamps, humidity, color=color, marker='x', linestyle='--', label='Humidity')
    ax2.tick_params(axis='y', labelcolor=color)

    # Add title and grid
    plt.title(f'5-Day Weather Forecast for {city}')
    fig.tight_layout()  # Adjust layout to make room for rotated x-axis labels
    plt.grid(True)

    # Save the plot
    try:
        plt.savefig(IMAGE_PATH)
        print(f"Visualization saved to {IMAGE_PATH}")
    except Exception as e:
        print(f"Error saving plot: {e}")

    plt.show()

def main():
    """
    Main function to run the script.
    """
    api_key = get_api_key()
    if api_key:
        weather_data = get_weather_data(CITY, api_key)
        if weather_data:
            plot_weather_data(weather_data, CITY)

if __name__ == "__main__":
    main()
