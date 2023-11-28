# Import libraries
import requests
import json
import pandas as pd
from tabulate import tabulate

# Get the user's Hypixel API key as input
api_key = input("Please enter your API key: ")


# Function to send a request to the specified URL and return the JSON data
def send_req(url):
    print("Sending request to Hypixel API...")
    response = requests.get(url)
    # read response as json and then print a table using pandas
    print("Raw dump of response:")
    data = response.json()
    # print(json.dumps(data, indent=4))

    return data


# Function to retrieve and display information about Skyblock election candidates
def Mayors(api_key):
    # Construct the URL for the Hypixel API Skyblock election data
    url = f"https://api.hypixel.net/resources/skyblock/election?key={api_key}&format=json"
    # Send a request to the API and get the JSON data
    data = send_req(url)

    # Check if the API call was successful
    # If it was, create a pandas table from the json data
    if data and "success" in data:
        # Create a table from the data
        candidates = data["mayor"]["election"]["candidates"]
        df = pd.DataFrame(candidates)

        print("\nTable of Skyblock election candidates:")
        print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))

    else:
        print("Failed to retrieve data from Hypixel API. Please check your API key and try again.")


# Call the Mayors function with the user's API key
Mayors(api_key)
