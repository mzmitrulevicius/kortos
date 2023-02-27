import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import copy


name_xpath = (
    "/html/body/div[4]/div/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/input"
)
birthday_xpath = (
    "/html/body/div[4]/div/div[2]/div/div/div/div[1]/div[2]/div/div/div[2]/div/input"
)
find_out_button = (
    "/html/body/div[4]/div/div[2]/div/div/div/div[1]/div[2]/div/div/div[6]/button"
)
month_xpath = (
    "/html/body/div[4]/div/div[2]/div/div/div/div[1]/div[2]/div/div/div[4]/select"
)
year_xpath = (
    "/html/body/div[4]/div/div[2]/div/div/div/div[1]/div[2]/div/div/div[5]/select"
)
table_xpath = "/html/body/div[4]/div/div[2]/div/div/div/div[1]/div[5]/table"
# table_xpath = "/html/body/div[4]/div/div[2]/div/div/div/div[1]/div[5]"

monthDict = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}
input_file = "matchPlayed.csv"
database = "database.csv"
statistics = "statistics.csv"
timeout = 30

planets_details = {
    "pl1.png": "Mercury",
    "pl2.png": "Venus",
    "pl3.png": "Mars",
    "pl4.png": "Jupiter",
    "pl5.png": "Saturn",
    "pl6.png": "Uranus",
    "pl7.png": "Neptune",
}

name = "Seven Stars"
options = Options()
driver = webdriver.Chrome("chromedriver", options=options)
url = "https://www.sevenreflections.com/monthlyreading/"
driver.get(url)

name_field = driver.find_element("xpath", name_xpath)
name_field.send_keys(name)

database_csv = open(database, "a+")
writer_database = csv.writer(database_csv)

statistics_csv = open(statistics, "a+")
writer_statistics = csv.writer(statistics_csv)

header = {
    "Sunday": [],
    "Monday": [],
    "Tuesday": [],
    "Wednesday": [],
    "Thursday": [],
    "Friday": [],
    "Saturday": [],
}

with open(input_file, "r") as input_file:
    reader = csv.reader(input_file)
    for index, match in enumerate(reader):
        if index != 0:
            (
                date,
                winner_id,
                winner_name,
                winner_dob,
                loser_id,
                loser_name,
                loser_dob,
            ) = match
            if winner_dob != "NULL" and loser_dob != "NULL":
                splitted_dob = winner_dob.split(".")
                winner_dob = [splitted_dob[1], splitted_dob[0], splitted_dob[2]]
                splitted_dob = loser_dob.split(".")
                loser_dob = [splitted_dob[1], splitted_dob[0], splitted_dob[2]]

                year, month, date = date.split("-")
                month = int(month)
                date_match = int(date)

                print("selecting date {} month {} and Year {}".format(date_match,monthDict[month], year))
                select = Select(driver.find_element("xpath", month_xpath))
                select.select_by_visible_text(monthDict[month])

                select = Select(driver.find_element("xpath", year_xpath))
                select.select_by_visible_text(year)
                data_to_store = []
                for dob in [winner_dob, loser_dob]:
                    calendar_dictionary = {}
                    planets = []
                    dob_field = driver.find_element("xpath", birthday_xpath)
                    dob_field.send_keys(Keys.COMMAND, "A")
                    dob_field.send_keys(Keys.BACKSPACE)
                    for data in dob:
                        dob_field.send_keys(data)

                    clicked = False
                    while not clicked:
                        element_present = EC.presence_of_element_located(
                            (By.XPATH, find_out_button)
                        )
                        WebDriverWait(driver, timeout).until(element_present)
                        find_out = driver.find_element("xpath", find_out_button)
                        try:
                            find_out.click()
                            clicked = True
                        except:
                            print("trying clicking")
                            pass
                        time.sleep(10)
                    element_present = EC.presence_of_element_located(
                        (By.XPATH, table_xpath)
                    )
                    WebDriverWait(driver, timeout).until(element_present)
                    htmlData = driver.page_source

                    soup = BeautifulSoup(htmlData, features="lxml")
                    table1 = soup.find("table", "calendar")

                    trs = table1.find_all("tr")
                    for i in trs[-1].find_all("td"):
                        image = i.find("img")
                        planet = image.get("src").split("/")[-1]
                        planets.append(planets_details[planet])
                    print(planets)
                    for i in trs:
                        try:
                            row = 0
                            for index, j in enumerate(i.find_all("td")):
                                try:
                                    row = int(j["colspan"])
                                except:
                                    pass
                                table_inside = j.find_all("table")
                                for kindex, k in enumerate(table_inside):
                                    for index1, l in enumerate(k.find_all("tr")):
                                        if index1 == 0:
                                            date = int(l.text.strip())
                                            calendar_dictionary[date] = {}
                                        elif index1 == 1:
                                            calendar_dictionary[date][
                                                "value"
                                            ] = l.text.strip()
                                        else:
                                            image = l.find("img")
                                            card = image.get("alt")
                                            calendar_dictionary[date][
                                                "card"
                                            ] = card.strip()
                                            calendar_dictionary[date][
                                                "planet"
                                            ] = planets[row]
                                            row+=1
                                
                        except Exception as e:
                            print(e)
                    time.sleep(2)
                    data_to_store.append(copy.deepcopy(calendar_dictionary[date_match]))
                    print(calendar_dictionary[date_match])
                writer_statistics.writerow(
                    [
                        data_to_store[0]["card"]
                        + " in "
                        + data_to_store[0]["planet"]
                        + " won against "
                        + data_to_store[1]["card"]
                        + " in "
                        + data_to_store[1]["planet"]
                    ]
                )
                writer_database.writerow(
                    [
                        data_to_store[0]["card"]
                        + " "
                        + data_to_store[0]["value"]
                        + " in "
                        + data_to_store[0]["planet"]
                        + " VS "
                        + data_to_store[1]["card"]
                        + " "
                        + data_to_store[1]["value"]
                        + " in "
                        + data_to_store[1]["planet"]
                        + " = "
                        + data_to_store[0]["card"]
                        + " "
                        + data_to_store[0]["value"]
                        + " in "
                        + data_to_store[0]["planet"]
                    ]
                )
