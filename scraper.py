from bs4 import BeautifulSoup
import requests
import pandas as pd

info = []
position = []
username = []
accuracy = []
play_count = []
performance_points = []
SS_ranks = []
S_ranks = []
A_ranks = []
highest_accuracy = 0
highest_accuracy_info = []
highest_play_count = 0
highest_play_count_info = []
highest_SS_ranks = 0
highest_SS_ranks_info = []
highest_S_ranks = 0
highest_S_ranks_info = []
highest_A_ranks = 0
highest_A_ranks_info = []
space = ""

# 1 page is equal to 50 players, hence 10 pages are top 500 players
# More pages may take a while
# and going to high doesn't work...
page_number = 1 # Starting page
amount_of_pages = 10

headers = {'Accept-Language': 'en-US,en;q=0.8'}

# Loop to go through all the pages
for i in range(1, amount_of_pages + 1):
  url = 'https://osu.ppy.sh/rankings/osu/performance?page=' + str(page_number) + '#scores'
  response = requests.get(url,headers=headers)
  soup = BeautifulSoup(response.text, "html.parser")
  
  # Gets all the information of all the players
  for player in soup.select('td.ranking-page-table__column'):
    info.append(player.get_text().strip())
  page_number += 1 # To go to next page of the website

  # Each page has 50 players hence iterating 50 times 
  for j in range(0, 50):
    position.append(int(info[0].strip("#")))
    username.append(" " + info[3])

    # To retrieve player accuracy 
    accuracy.append(float(info[4].strip("%")))

    # and get the most accurate player
    if accuracy[-1] > highest_accuracy:
      highest_accuracy = float(info[4].strip("%"))
      highest_accuracy_name = info[3]
      highest_accuracy_position = info[0]

    # To retrieve player number of plays 
    play_count.append(int(info[5].replace(",", "")))

    # and get the player with the highest play count
    if play_count[-1] > highest_play_count:
      highest_play_count = int(info[5].replace(",", ""))
      highest_play_count_name = info[3]
      highest_play_count_position = info[0]

    # To retrieve pp count, already sorted from highest to lowest
    performance_points.append(int(info[6].replace(",", "")))

    # To retrieve SS-ranks achieved by a player
    SS_ranks.append(int(info[7].replace(",", "")))

    # and get the player with the highest SS count
    if SS_ranks[-1] > highest_SS_ranks:
      highest_SS_ranks = int(info[7].replace(",", ""))
      highest_SS_ranks_name = info[3]
      highest_SS_ranks_position = info[0]

    # To retrieve S-ranks achieved by a player
    S_ranks.append(int(info[8].replace(",", "")))

    # and get the player with the highest S count
    if S_ranks[-1] > highest_SS_ranks:
      highest_S_ranks = int(info[8].replace(",", ""))
      highest_S_ranks_name = info[3]
      highest_S_ranks_position = info[0]

    # To retrieve A-ranks achieved by a player
    A_ranks.append(int(info[9].replace(",", "")))

    # and get the player with the highest A count
    if S_ranks[-1] > highest_SS_ranks:
      highest_A_ranks = int(info[9].replace(",", ""))
      highest_A_ranks_name = info[3]
      highest_A_ranks_position = info[0]

    # To retrieve the player information per line from the leaderboard
    for i in range(0, 10):
      info.pop(0)

highest_accuracy_info.append("Highest Accuracy")
highest_accuracy_info.append(highest_accuracy_name)
highest_accuracy_info.append("position: " + highest_accuracy_position)
highest_accuracy_info.append("Accuracy: " + str(highest_accuracy) + "%")

highest_play_count_info.append("Highest Play Count")
highest_play_count_info.append(highest_play_count_name)
highest_play_count_info.append("position" + highest_play_count_position)
highest_play_count_info.append("Play count: " + str(highest_play_count))

highest_SS_ranks_info.append("Highest SS ranks")
highest_SS_ranks_info.append(highest_SS_ranks_name)
highest_SS_ranks_info.append("Position: " + highest_SS_ranks_position)
highest_SS_ranks_info.append("SS ranks: " + str(highest_SS_ranks))

highest_S_ranks_info.append("Highest S ranks")
highest_S_ranks_info.append(highest_S_ranks_name)
highest_S_ranks_info.append("Position: " + highest_S_ranks_position)
highest_S_ranks_info.append("S ranks: " + str(highest_S_ranks))

highest_A_ranks_info.append("Highest A ranks")
highest_A_ranks_info.append(highest_A_ranks_name)
highest_A_ranks_info.append("Position: " + highest_A_ranks_position)
highest_A_ranks_info.append("A ranks: " + str(highest_A_ranks))

# Adds necessary whitespace to ensure that all arrays are the same (also to prevent the same text from being printed on the same column)
for k in range(0, ((amount_of_pages) * 50) - 4):
  highest_accuracy_info.append("")
  highest_play_count_info.append("")
  highest_SS_ranks_info.append("")
  highest_S_ranks_info.append("")
  highest_A_ranks_info.append("")

# The dataframe
df = pd.DataFrame(
    {'Position': position,
     'Username': username,
     'Accuracy / %': accuracy,
     'Play Count': play_count,
     'Performance Points': performance_points,
     'SS Ranks': SS_ranks,
     'S Ranks': S_ranks,
     'A Ranks': A_ranks,
     '': space,
     '                ': highest_accuracy_info,
     ' ': space,
     '  ': space,
     '                  ': highest_play_count_info,
     '   ': space,
     '    ': space,
     '          ': highest_SS_ranks_info,
     '     ': space,
     '      ': space,
     '            ': highest_S_ranks_info,
     '       ': space,
     '        ': space,
     '              ': highest_A_ranks_info
     }
    )

# To check dataframe is working 
print(df.head())

# Converting to csv
df.to_csv("Osu! Leaderboard.csv", index = False)
