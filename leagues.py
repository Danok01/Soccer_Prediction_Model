import requests
import json
import csv


def get_api(url):
    list= []
    
    headers = {
        "x-rapidapi-key": "2813f45597msh5899e05f16ab51ap19ba1fjsna2ce013c7e99",
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    # print(data)
    leagues= data["response"]["leagues"]

    for lig in leagues:
        listed = {
        "id": lig["id"],
        "name": lig["name"],
        "logo": lig["logo"]
        }
        list.append(listed)
    return list

def parse_to_json(data, filename):
    # Save matches to a JSON file
    with open(filename, 'w', encoding="utf-8") as f:
       json.dump(data, f, indent=4)

def json_to_csv():
    with open("leagues", 'r') as f:
        data = json.load(f)
        # Get field names from the first data object
        fields = data[0].keys()

    with open("league2.csv", 'w', newline='') as fp:
        writer = csv.DictWriter(fp, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-leagues"
    file_name = "leagues"

    api_connect= get_api(url)
    if api_connect:
        parse_to_json(api_connect, file_name)
        json_to_csv()