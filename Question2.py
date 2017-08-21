import pandas
import time
class Team:
    def __init__(self,teamName,divisionName,conferenceName):
        self.teamName=teamName
        self.divisionName=divisionName
        self.conferenceName=conferenceName
        self.numberOfWins = 0
        self.numberOfLosses= 0
        self.winLossD = {}
        self.pointDifferentialPerTeam={}

    def updateTeamStats(self,game):
        opposingTeamName=game.getOpposingTeam(self.teamName)
        if opposingTeamName not in self.winLoss:
            self.winLossD[game.getOpposingTeam(self.teamName)]=[0,0]
        if opposingTeamName not in self.winLossPercentagePerTeam:
            self.pointDifferentialPerTeam[opposingTeamName] =0

        if game.isWinner(self.teamName):
            self.numberOfWins += 1
            self.winLossD[opposingTeamName][0]+=1
        else:
            self.numberOfLosses += 1
            self.winLossD[opposingTeamName][1] += 1
        opposingTeamScore=game.getTeamScore(opposingTeamName)
        teamScore=game.getTeamScore(self.teamName)
        self.pointDifferentialPerTeam=teamScore-opposingTeamScore

    def getWinPercentage(self,teams):
        totalGamesPlayed=0
        totalInDivisionWins=0
        for opposingTeamName in teams:
                totalGamesPlayed+=self.winLossD[opposingTeamName][0]+self.winLoss[opposingTeamName][1]
                totalInDivisionWins+=self.winLoss[opposingTeamName][0]
        return totalInDivisionWins/totalGamesPlayed

    def getPointDifferential(self,teams):
        totalPointDifferential=0
        for opposingTeamName in teams:
               totalPointDifferential+=self.pointDifferentialPerTeam[opposingTeamName]
        return totalPointDifferential

    def printData(self):
        print(self.teamName,' ',str(self.numberOfWins),'-',str(self.numberOfLosses))

class Game:
    def __init__(self,date,homeTeam, awayTeam, homeScore,awayScore,winningTeam):
        self.date=time.strptime(date,"%m/%d/%Y")
        self.homeTeam=homeTeam
        self.awayTeam=awayTeam
        self.homeScore=homeScore
        self.awayScore=awayScore
        self.winner=0
        if winningTeam=='Home':
            self.winner=homeTeam
        else:
            self.winner=awayTeam

    def isWinner(self,team):
        if team==self.winner:
            return True
        else:
            return False
    def getOpposingTeam(self,team):
        if self.homeTeam==team:
            return self.awayTeam
        else:
            return self.homeTeam
    def getTeamScore(self,team):
        if self.homeTeam == team:
            return self.homeScore
        else:
            return self.awayScore
    def printData(self):
        print(self.homeTeam.teamName, ' ', self.awayTeam.teamName)

class Conference:
    def __init__(self,competingConference):
        self.competingConference=competingConference
        self.conferenceTeams={}
        self.gamesPlayedByEachTeam={}
        self.ineligiblePlayoffTeams=[]
    def addGame(self,game):
        self.gamesPlayedByEachTeam[game.homeTeam]=game
        self.gamesPlayedByEachTeam[game.awayTeam]=game

    def addTeam(self,team):
        self.conferenceTeams[team.teamName]=team

    def playGame(self,game):
        self.conferenceTeams[game.homeTeam].updateTeamStats(game)
        self.conferenceTeams[game.awayTeam].updateTeamStats(game)
        if game.homeTeam not in self.ineligiblePlayoffTeams and (not self.determinePlayoffEligibility(game.homeTeam)):
            self.ineligiblePlayoffTeams.append(game.homeTeam)
        if game.awayTeam not in self.ineligiblePlayoffTeams and (not self.determinePlayoffEligibility(game.awayTeam)):
            self.ineligiblePlayoffTeams.append(game.awayTeam)

    #def determinePlayoffEligibility(self,team):

    #def findCurrentConferenceStandings(self):


division_Info=pandas.read_csv("Division_Info.csv")
nba_Season=pandas.read_csv("NBA_2016_2017_Scores.csv")
westernConference=0
easternConference=Conference(westernConference)
westernConference=Conference(easternConference)
for index,row in division_Info.iteritems():
    team=Team(row[0],row[1],row[2])
    if row[2]=='East':
        easternConference.addTeam(team)
    else:
        westernConference.addTeam(team)



