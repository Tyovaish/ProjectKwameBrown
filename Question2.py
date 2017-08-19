import pandas
import time
class Team:
    def __init__(self,teamName,divisionName,conferenceName):
        self.teamName=teamName
        self.divisionName=divisionName
        self.conferenceName=conferenceName
        self.gamesPlayedByTeam=[]
        self.winGeneral = 0
        self.lossGeneral= 0
        self.winLossD = {}
        self.inPlayoffContention=True
    def addGame(self,game):
        self.gamesPlayedByTeam.append(game)
        if game.getOpposingTeam(self).teamName not in self.winLossD:
            self.winLossD[game.getOpposingTeam(self).teamName]=[0,0]
        if game.isWinner(self):
            self.winGeneral += 1
            self.winLossD[game.getOpposingTeam(self).teamName][0]+=1
        else:
            self.lossGeneral += 1
            self.winLossD[game.getOpposingTeam(self).teamName][1] += 1
    def numberOfGamesLeft(self):
        return 82-len(self.gamesPlayedByTeam)
    def gamesAfterAndOnDate(self,date):
        games=[]
        for i in self.gamesPlayedByTeam:
            if i.date>=time.strptime(date,"%m/%d/%Y"):
                games.append(i)
        return games

    def printData(self):
        print(self.teamName,' ',str(self.winGeneral),'-',str(self.lossGeneral))

class Game:
    def __init__(self,date,homeTeam, awayTeam, homeScore,awayScore):
        self.date=time.strptime(date,"%m/%d/%Y")
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
    def getOpposingTeam(self,team):
        if self.homeTeam==team:
            return self.awayTeam
        else:
            return self.homeTeam

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

for teamName,winsLoss in teams['Boston Celtics'].winLossD.items():
    print(teamName,' Wins:',winsLoss[0] ,'Losses',winsLoss[1])