from typing import Any
import requests
import matplotlib.pyplot as plt
import json

api_key = input("Please enter your API key: ")

def send_req(url):
    response = requests.get(url)
    data = response.json()
    return data

def Mayors(api_key):
    url = f"https://api.hypixel.net/resources/skyblock/election?key={api_key}&format=json"
    data = send_req(url)

    if "data" in data:
        election_data = data["data"]
        names = []
        keys = []
        perks_names = []
        perks_descriptions = []
        votes = []

        for candidate in election_data:
            names.append(candidate["name"])
            keys.append(candidate["key"])
            perks_data = candidate["perks"]
            perk_names = [perk["name"] for perk in perks_data]
            perk_descriptions = [perk["description"] for perk in perks_data]
            perks_names.append(", ".join(perk_names))
            perks_descriptions.append(", ".join(perk_descriptions))
            votes.append(candidate["votes"])

        # Create a bar graph for votes
        plt.figure(figsize=(10, 6))
        plt.bar(names, votes)
        plt.xlabel("Candidates")
        plt.ylabel("Votes")
        plt.title("Skyblock Election Votes")

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        # Show the graph
        plt.show()

        # Print candidate names, keys, perks, and votes
        for name, key, perks_name, perks_desc, vote in zip(names, keys, perks_names, perks_descriptions, votes):
            print(f"Candidate: {name}")
            print(f"Key: {key}")
            print(f"Perks: {perks_name}")
            print(f"Perk Descriptions: {perks_desc}")
            print(f"Votes: {vote}")
            print("-" * 30)
    else:
        print("No data found in the API response.")
        # Print the entire API response for debugging
        print(json.dumps(data, indent=4))

# Call the Mayors function with your API key
Mayors(api_key)
