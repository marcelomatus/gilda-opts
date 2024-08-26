import requests

# The URL to which the request will be sent
url = "http://homeassistant:5012/optimize"

# Load the JSON data from the file
with open("demand_grid.json", "r") as file:
    data = file.read()

# Set the headers
headers = {"Content-Type": "application/json"}

# Make the POST request
response = requests.post(url, headers=headers, data=data)

# Check the response (optional)
print("Response Status Code:", response.status_code)
print("Response Content:", response.content)
