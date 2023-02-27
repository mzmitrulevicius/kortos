import csv
import requests
from multiprocessing import Pool

key = '489e99538c30af260cf43fe7f762bdd99f4a31b99958e94c6b5a4e99d5b5e063'
output_file = 'playerAPI.csv'

# make change here if you want more players
startingID = 1
endingID = 500000
num_processes = 8

def get_player_data(player_id):
    api_url = f"https://api.api-tennis.com/tennis/?method=get_players&player_key={player_id}&APIkey={key}"
    response = requests.get(api_url)
    status = response.status_code
    data = response.json()
    print(status)
    if 'result' in data:
        player_key = data['result'][0]['player_key']
        player_name = data['result'][0]['player_name']
        player_dob = data['result'][0]['player_bday']
        player_country = data['result'][0]['player_country']

        if (player_key != None and player_dob != None and status == 200):
            print(player_key, player_name)
            return [player_key, player_name, player_dob, player_country]

def write_data_to_file(data):
    with open(output_file, "a") as f:
        writer = csv.writer(f)
        writer.writerow(data)

if __name__ == '__main__':
    player_ids = list(range(startingID, endingID+1))
    pool = Pool(num_processes)
    results = pool.map(get_player_data, player_ids)
    for result in results:
        if result:
            write_data_to_file(result)
