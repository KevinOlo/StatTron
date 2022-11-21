
from doctest import master
from tkinter import *
from tkinter.font import BOLD
from requests import get
from pprint import PrettyPrinter


BASE_URL = "https://data.nba.net"
ALL_JSON = "/prod/v1/today.json"

printer = PrettyPrinter()
win = Tk()



def get_links():
    data = get(BASE_URL + ALL_JSON).json()
    links = data['links']
    return links


def get_scoreboard():
    scoreboard = get_links()['currentScoreboard']
    games = get(BASE_URL + scoreboard).json()['games']

    for game in games:
        home_team = game['hTeam']
        away_team = game['vTeam']
        clock = game['clock']
        period = game['period']

        print("------------------------------------------")
        print(f"{home_team['triCode']} vs {away_team['triCode']}")
        print(f"{home_team['score']} - {away_team['score']}")
        print(f"{clock} <> {period['current']}")
    


def get_stats():
    stats = get_links()['leagueTeamStatsLeaders']
    teams = get(BASE_URL + stats).json()['league']['standard']['regularSeason']['teams']

    teams = list(filter(lambda x : x['name'] != "Team", teams))
    #teams.sort(key=lambda x : int(x['ppg']['rank']))
    




    for i, team in enumerate(teams):        #ads num ranking to left of teams
        name = team['name']
        nickname = team['nickname']
        ppg = team['ppg']['avg']
        print(f"{i + 1}. {name} - {nickname} - {ppg}")

def close():
    win.quit()

def statlbl():
    return get_stats()





def scorelbl():
       return get_scoreboard()



win.title('NBA Know All')

win.iconbitmap('/kobelogo.ico')

win.geometry('800x800')

Button(win, text= "Close the Window", font=("Calibri",14,"bold"), activebackground = 'red' , bd = 3 , command=close).pack( side = BOTTOM)

Button(win, text= "Click To Show Stats", bd= 3,  command= statlbl, justify= CENTER).pack()


Button(win, text= "Show Scores", bd= 3,  command= scorelbl, justify= CENTER).pack()

#Label(win, text= None, font=('calibri', 14)).pack()


win.mainloop()