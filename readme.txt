Requirements to run the scripts:

1. You need to have python installed on your PC/Laptop
2. You need to install some packages on your PC for that. all required packages are in requirements.txt file
3. Open the CMD inside your folder where all files are present and run the following command
   pip install -r requirements.txt
4. You must have Chrome installed on your PC
5. You need to download the chrome drivers and place it inside the same files folder
6. download the drivers based on your chrome version from the following link
   https://chromedriver.chromium.org/downloads

Now you are ready to run the scripts

There are three different scripts.

1. playerapi.py -> this script get the players information from the api (right now we have enough players information to get more than 20k records so you can ignore it)
2. matchPlayed.pu -> this script get the matches played between two players. (right now we have enough players information to get more than 20k records so you can ignore it)
3. matchAstro.py -> this script get the our database from the astro site. (you just need to run this on your pc to make the database)

playerapi.py

in line 8 and 9 you can change to get extra players, right now we have 2000 players data. so if you want to get 1000 more just change it to
startingID = 2001
endingID = 3000
it will extra 1000 more players

matchesDetails.py

before running this make sure, you have right players in the file whose data you want to get. It will start from line first of playerAPI.csv

matchAstro.py

it will get database by getting information from matchPlayed.csv file. you can edit it if you want to change anything but remove complete row
