import requests
import json

def get_weather(city: str) -> str:
    """
    Query real weather information by calling the wttr.in API.
    """
    # API endpoint, we request JSON format data
    url = f"https://wttr.in/{city}?format=j1"
    
    try:
        # Make network request
        response = requests.get(url)
        # Check if response status code is 200 (success)
        response.raise_for_status() 
        # Parse returned JSON data
        data = response.json()
        
        # Extract current weather conditions
        current_condition = data['current_condition'][0]
        weather_desc = current_condition['weatherDesc'][0]['value']
        temp_c = current_condition['temp_C']
        
        # Format as natural language and return
        return f"{city} current weather: {weather_desc}, temperature {temp_c}°C"
        
    except requests.exceptions.RequestException as e:
        # Handle network errors
        return f"Error: Network problem encountered while querying weather - {e}"
    except (KeyError, IndexError) as e:
        # Handle data parsing errors
        return f"Error: Failed to parse weather data, possibly invalid city name - {e}"