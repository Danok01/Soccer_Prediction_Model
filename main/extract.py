import logging
import json
import csv
import requests
from dotenv import load_dotenv
import os
import psycopg2

logger = logging.getLogger(__name__)


# def fetch_data():
#     URL = "https://api.sportmonks.com/v3/football/teams/search/Liverpool?api_token=v1gIsBbk1MEz32PJ65QZoRZip8MmE4DSPKpmTNlaOogX4hnCy0UZsOjlz0cx&include=statistics;players;"
#     logger.info("fetching player stats from API...")

#     response = requests.get(URL)
#     status = response.raise_for_status()
#     logger.info("API response recieved")
#     print(status)
#     return response.json()

# fetch_data()

import requests
# import pandas as pd

# url = "https://fbrapi.com//team-match-stats"
# params = {
#     "team_id": "92e7e919",
#     "league_id": "9",
#     "season_id": "2024-2025"
# }
# headers = {"X-API-Key": "gwKWr8bzFsYeIjQcb94RgKDSgWuDSLNhbTYtv1jCMA0"}

# response = requests.get(url, params=params, headers=headers)
# response.raise_for_status()
# URL = "https://api.sportmonks.com/v3/football/fixtures/between/2025-08-17/2025-08-18/591?api_token=v1gIsBbk1MEz32PJ65QZoRZip8MmE4DSPKpmTNlaOogX4hnCy0UZsOjlz0cx" #include=participants;league;scores;events.player;statistics.type;sidelined.sideline.player;sidelined.sideline.type;"
# #  "https://api.sportmonks.com/v3/football/teams/search/Liverpool?api_token=v1gIsBbk1MEz32PJ65QZoRZip8MmE4DSPKpmTNlaOogX4hnCy0UZsOjlz0cx"
# response = requests.get(URL)
# # response.raise_for_status()
# # print(f"success: {status}")
# print(response.json())

import requests

def get_api(url):
    list= []
    querystring = {"leagueid":"3"}

    headers = {
        "x-rapidapi-key": "2813f45597msh5899e05f16ab51ap19ba1fjsna2ce013c7e99",
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    print(data)
    # matches= data["response"]["matches"]

    # for match in matches:
    #     listed = {
    #     "utcTime": match["status"]["utcTime"],
    #     "scoreStr": match["status"]["scoreStr"],
    #     "home": match["home"]["name"],
    #     "away": match["away"]["name"],
    #     "finished": match["status"]["finished"]
    #     }
    #     list.append(listed)
    return data


def parse_to_json(data, filename):
    # Save matches to a JSON file
    with open(filename, 'w', encoding="utf-8") as f:
       json.dump(data, f, indent=4)

def json_to_csv():
    with open("gotten", 'r') as f:
        data = json.load(f)
        # Get field names from the first data object
        fields = data[0].keys()

    with open("league2.csv", 'w', newline='') as fp:
        writer = csv.DictWriter(fp, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
        

if __name__ == "__main__":
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-matches-by-league"
    # url = "https://media.api-sports.io/football/leagues"
    file_name = "league2"

    api_connect= get_api(url)
    if api_connect:
        parse_to_json(api_connect, file_name)
        json_to_csv()




# print(matches)