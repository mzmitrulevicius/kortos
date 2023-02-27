import csv
import requests
from multiprocessing import Pool

playerDict = {}
playerMatches = []
api_key = "489e99538c30af260cf43fe7f762bdd99f4a31b99958e94c6b5a4e99d5b5e063"
output_file_name = "matchPlayed.csv"
url_file = "url.txt"
reader = csv.reader(open("playerAPI.csv", "r"))
for index, row in enumerate(reader):
    if index != 0:
        key, name, dob, country = row
        playerDict[int(key)] = [name, dob, country]

for player1 in list(playerDict.keys())[0:100]:
    for player2 in list(playerDict.keys())[0:100]:
        if player1 != player2:
            matchPlayed = tuple(sorted([player1, player2]))
            if matchPlayed not in playerMatches:
                playerMatches.append(matchPlayed)

def get_match_data(match):
    global output_file_name
    
    player1, player2 = match
    api_url = "https://api.api-tennis.com/tennis/?method=get_H2H&APIkey={}&first_player_key={}&second_player_key={}".format(api_key, str(player1), str(player2))
    print(api_url)
    f = open(url_file, "a")
    f.write(api_url)
    f.close()
    response = requests.get(api_url)
    status = response.status_code
    data = response.json()
    print(player1, "VS", player2)
    print("Status Code:", str(status))

    if status == 200:
        with open(output_file_name, "a") as output_file:
            for playerResults in ["firstPlayerResults", "secondPlayerResults"]:
                tournament_key = ""
                for match in data["result"][playerResults]:
                    if match["tournament_key"] != tournament_key:
                        event_date = match["event_date"]
                        winnerType = match["event_winner"]
                        if winnerType == "First Player":
                            winner_key = match["first_player_key"]
                            losser_key = match["second_player_key"]
                            winner_name = match["event_first_player"]
                            losser_name = match["event_second_player"]
                            if int(winner_key) in playerDict.keys():
                                winner_DOB = playerDict[int(winner_key)][1]
                            else:
                                winner_DOB = "NULL"
                            if int(losser_key) in playerDict.keys():
                                losser_DOB = playerDict[int(losser_key)][1]
                            else:
                                losser_DOB = "NULL"
                            # losser_DOB = playerDict[int(losser_key)][1]

                            row = [player1, player2, event_date, winner_name, losser_name, winner_key, losser_key, winner_DOB, losser_DOB]
                            writer = csv.writer(output_file)
                            writer.writerow(row)

                        tournament_key = match["tournament_key"]
    
    else:
        print("Error: Status Code", str(status))
        return

if __name__ == '__main__':
    with Pool(processes=4) as pool:
        pool.map(get_match_data, playerMatches)