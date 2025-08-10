# API Interactions

Working with web APIs

---

## REST API Request

```python output_only live
import requests
import json

print("Random User Generator:\n")
response = requests.get('https://randomuser.me/api/')
data = response.json()

user = data['results'][0]
print(f"Name: {user['name']['title']} {user['name']['first']} {user['name']['last']}")
print(f"Email: {user['email']}")
print(f"Location: {user['location']['city']}, {user['location']['country']}")
print(f"Phone: {user['phone']}")
```

---

## Weather API

```python live
import requests

def get_weather(city):
    api_key = "YOUR_API_KEY"  # Replace with actual key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

# Example usage (remove comment to test)
# weather = get_weather("London")
# print(f"Temperature: {weather['main']['temp']}°C")
# print(f"Weather: {weather['weather'][0]['description']}")

print("Weather API Client Ready!")
print("Uncomment code to test with real API key")
```

---

## JSON Processing

```python output_only live
import json

data = {
    "project": "Slidedown",
    "version": 1.5,
    "features": [
        "Markdown Support",
        "Live Code Execution",
        "Theming System",
        "Output Display"
    ],
    "stats": {
        "slides": 42,
        "users": 1500,
        "rating": 4.8
    }
}

print("JSON Structure:\n")
print(json.dumps(data, indent=2))
```

---

# API Power in Terminal
