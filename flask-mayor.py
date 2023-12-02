from flask import Flask, render_template
from dotenv import load_dotenv
import os
import requests
import pandas as pd
from tabulate import tabulate
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

app = Flask(__name__)

# Get API key from environment variable
api_key = os.getenv("API_KEY")

# Global variable to store the latest data
latest_data = None


# Function to send a request to the specified URL and return the JSON data
def send_req(url):
    print("Sending request to Hypixel API...")
    response = requests.get(url)
    # read response as json and then print a table using pandas
    print("Raw dump of response:")
    data = response.json()
    return data


# Function to retrieve and store the latest information
def update_data():
    global latest_data
    # api_key = "faaaea25-ee25-4e8c-bca3-f2d57dee54b8"   # Replace with your API key
    url = f"https://api.hypixel.net/resources/skyblock/election?key={api_key}&format=json"
    latest_data = send_req(url)


# Schedule the data update every 6 hours
scheduler = BackgroundScheduler()
scheduler.add_job(update_data, trigger="interval", hours=6)
scheduler.start()

# Initial data retrieval
update_data()


# Route to display the data
@app.route('/')
def display_data():
    global latest_data

    if latest_data and "success" in latest_data:
        mayor_data = latest_data["mayor"]
        mayor_name = mayor_data["name"]
        mayor_key = mayor_data["key"]
        mayor_perks = pd.json_normalize(mayor_data["perks"])

        df_mayor = pd.DataFrame(
            {
                "Mayor Name": [mayor_name] * len(mayor_perks),
                "Mayor Key": [mayor_key] * len(mayor_perks),
                "Perk Name": mayor_perks["name"],
                "Perk Description": mayor_perks["description"],
            }
        )

        candidates_data = latest_data["mayor"]["election"]["candidates"]
        election_candidates = pd.json_normalize(candidates_data)

        df_candidates = pd.DataFrame(
            {
                "Candidate Name": election_candidates["name"],
                "Candidate Key": election_candidates["key"],
                "Perk Name": election_candidates["perks"].apply(lambda x: [p["name"] for p in x]),
                "Perk Description": election_candidates["perks"].apply(lambda x: [p["description"] for p in x]),
                "Votes": election_candidates["votes"],
            }
        )

        mayor_table = tabulate(df_mayor, headers="keys", tablefmt="html", showindex=False)
        candidates_table = tabulate(df_candidates, headers="keys", tablefmt="html", showindex=False)

        return f"<h1>Mayor Details:</h1>{mayor_table}<h1>Skyblock Election Candidates:</h1>{candidates_table}"

    else:
        return "Failed to retrieve data from Hypixel API. Please check your API key and try again."


if __name__ == '__main__':
    app.run(debug=True)
