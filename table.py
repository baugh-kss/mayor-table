# Import libraries
from typing import Any
import requests
import matplotlib.pyplot as plt
import json
import pandas as pd

# Get the user's Hypixel API key as input
api_key = input("Please enter your API key: ")

# Function to send a request to the specified URL and return the JSON data
def send_req(url):
    print("Sending request to Hypixel API...")
    response = requests.get(url)
    # read response as json and then print a table using pandas
    print("Raw dump of response:")
    data = response.json()
    print(json.dumps(data, indent=4))

    return data

# Function to retrieve and display information about Skyblock election candidates
def Mayors(api_key):
    # Construct the URL for the Hypixel API Skyblock election data
    url = f"https://api.hypixel.net/resources/skyblock/election?key={api_key}&format=json"
    
    # Send a request to the API and get the JSON data
    data = send_req(url)


# Call the Mayors function with the user's API key
Mayors(api_key)
