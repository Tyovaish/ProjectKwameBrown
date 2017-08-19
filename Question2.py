import pandas
class Team:
    def __init__(self,teamName,divisionName,conferenceName):
        self.teamName=teamName
        self.divisionName=divisionName
        self.conferenceName=conferenceName
        self.gamesPlayedByTeam=[]
        self.winLossGeneral = 0
        self.winLossD = {}
        self.homeScore = 0
        self.awayScore = 0
        self.homeRecord = 0
        self.awayRecord = 0
    def addGame(self,game):
        self.gamesPlayedByTeam.append(game)

class Game:
    def __init__(self,date,homeTeam, awayTeam, homeScore,awayScore):
        self.date=date
        self.homeTeam=homeTeam
        self.awayTeam=awayTeam
        self.homeScore=homeScore
        self.awayScore=awayScore
        homeTeam.addGame(self)
        awayTeam.addGame(self)
    def isWinner(self,team):
        if self.homeTeam == team and self.homeScore>self.awayScore:
            return True
        else:
            return False
division_Info=pandas.read_csv("Division_Info.csv")
nba_Season=pandas.read_csv("NBA_2016_2017_Scores.csv")
teams = {}
for index, row in division_Info.iterrows():
    teams[row[0]] = Team(row[0],row[1],row[2])