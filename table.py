# Import libraries
import requests
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
        # Strip Mayor Data
        mayor_data = data["mayor"]
        mayor_name = mayor_data["name"]
        mayor_key = mayor_data["key"]
        mayor_perks = pd.json_normalize(mayor_data["perks"])

        # Create a pandas table from extracted mayor data above
        df_mayor = pd.DataFrame(
            {
                "Mayor Name": [mayor_name] * len(mayor_perks),
                "Mayor Key": [mayor_key] * len(mayor_perks),
                "Perk Name": mayor_perks["name"],
                "Perk Description": mayor_perks["description"],
            }
        )

        # Strip Skyblock Election Candidates Data
        candidates_data = data["mayor"]["election"]["candidates"]
        election_candidates = pd.json_normalize(candidates_data)

        # Create a pandas table from extracted Skyblock Election Candidates data
        df_candidates = pd.DataFrame(
            {
                "Candidate Name": election_candidates["name"],
                "Candidate Key": election_candidates["key"],
                "Perk Name": election_candidates["perks"].apply(lambda x: [p["name"] for p in x]),
                "Perk Description": election_candidates["perks"].apply(lambda x: [p["description"] for p in x]),
                "Votes": election_candidates["votes"],
            }
        )

        print("\n Mayor Details:")
        print(tabulate(df_mayor, headers="keys", tablefmt="fancy_grid", showindex=False))

        print("\n Skyblock Election Candidates:")
        print(tabulate(df_candidates, headers="keys", tablefmt="fancy_grid", showindex=False))

        # print("\nTable of Skyblock election candidates:")
        # print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))

    else:
        print("Failed to retrieve data from Hypixel API. Please check your API key and try again.")


# Call the Mayors function with the user's API key
Mayors(api_key)
