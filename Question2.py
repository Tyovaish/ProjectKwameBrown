import pandas
class Team:
    def __init__(self,teamName,divisionName,conferenceName):
        self.teamName=teamName
        self.divisionName=divisionName
        self.conferenceName=conferenceName
        self.gamesPlayedByTeam=[]
        self.winGeneral = 0
        self.lossGeneral= 0
        self.winLossD = {}
    def addGame(self,game):
        self.gamesPlayedByTeam.append(game)
        if game.isWinner(self):
            self.winGeneral += 1
        else:
            self.lossGeneral += 1
    def printData(self):
        print(self.teamName,' ',str(self.winGeneral),'-',str(self.lossGeneral))

class Game:
    def __init__(self,date,homeTeam, awayTeam, homeScore,awayScore):
        self.date=date
        self.homeTeam=homeTeam
        self.awayTeam=awayTeam
        self.homeScore=homeScore
        self.awayScore=awayScore
    def isWinner(self,team):
        if self.homeTeam == team and self.homeScore>self.awayScore:
            return True
        if self.awayTeam==team and self.awayScore>self.homeScore:
            return True
        return False
    def printData(self):
        print(self.homeTeam.teamName, ' ', self.awayTeam.teamName)


division_Info=pandas.read_csv("Division_Info.csv")
nba_Season=pandas.read_csv("NBA_2016_2017_Scores.csv")
teams = {}
for index, row in division_Info.iterrows():
    teams[row[0]] = Team(row[0],row[1],row[2])

for index, row in nba_Season.iterrows():
    gamePlayed=Game(row[0],teams[row[1]],teams[row[2]],row[3],row[4])
    teams[row[1]].addGame(gamePlayed)
    teams[row[2]].addGame(gamePlayed)

for teamName,teamData in teams.items():
    teamData.printData()