import pandas
import time
class Team:
    def __init__(self,teamName,divisionName):
        self.teamName=teamName
        self.divisionName=divisionName
        self.conferenceName=0
        self.numberOfWins = 0
        self.numberOfLosses= 0
        self.winLossD = {}
        self.pointDifferentialPerTeam={}
        self.conferenceRank = 0

        self.scheduleQueue=[]
        self.simQueue=[]

        self.predictiveWins=0
        self.predictiveLosses=0
        self.predictiveRank=0

    def setConference(self, conference):
        self.conferenceName = conference

    def updateTeamStats(self,game):
        opposingTeamName=game.getOpposingTeam(self.teamName)
        if opposingTeamName not in self.winLossD:
            self.winLossD[game.getOpposingTeam(self.teamName)]=[0,0]


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

    def playGame(self):
        self.homeTeam.updateTeamStats(self)
        self.awayTeam.updateTeamStats(self)
        self.homeTeam.scheduleQueue.remove(self)
        self.awayTeam.scheduleQueue.remove(self)

    def simulateGame(self, targetTeam, bottomEight):

    #Target Team is the team that we want to have the best possible season

        #Target Team always wins
        if self.homeTeam == targetTeam or self.awayTeam == targetTeam:
            None

        #If it's interconference we assume our boy loses
        elif self.homeTeam.conferenceName != self.awayTeam.conferenceName:
            None

        #At this point we must be within our own conference and not playing the target team
        #If both teams are bottom 8 then we assume the lesser wins
        elif self.homeTeam in bottomEight and self.awayTeam in bottomEight:
            if self.homeTeam.predictiveWins > self.awayTeam.predictiveWins:
                self.awayTeam.predictiveWins += 1
            else:
                self.homeTeam.predictiveWins += 1

        else:
            if self.homeTeam.predictiveWins > self.awayTeam.predictiveWins:
                self.homeTeam.predictiveWins += 1
            else:
                self.awayTeam.predictiveWins += 1

        #Pop game from simQueue of participants




class Conference:
    def __init__(self,competingConference):
        self.competingConference=competingConference
        self.conferenceTeams={}
        self.gamesPlayedByEachTeam={}
        self.ineligiblePlayoffTeams=[]

    def addGame(self,game):
        self.gamesPlayedByEachTeam[game.homeTeam].append(game)
        self.gamesPlayedByEachTeam[game.awayTeam].append(game)

    def addTeam(self,team):
        self.conferenceTeams[team.teamName]=team
        team.setConference(self)

    def findCurrentConferenceStandings(self):

        sortedTeams = sorted(self.conferenceTeams.values(), key = Team.numberOfWins)

        rank = 15;

        for t in sortedTeams:
            t.conferenceRank = rank
            rank -= 1

    def findPredictiveConferenceStandings(self):

        sortedTeams = sorted(self.conferenceTeams.values(), key = Team.predictiveWins)

        rank = 15;

        for t in sortedTeams:
            t.predictiveRank = rank
            rank -= 1


def determinePlayoffEligibility(games, team):
    if(team.numberOfWins + team.numberOfLosses <= 41):
        return True


    bottomEight = []

    for t in team.conferenceTeams.values():
        t.predictiveWins = t.numberOfWins
        t.predictiveLosses = t.numberOfLosses

    team.predictiveWins = team.numberOfWins + team.scheduleQueue.qsize()

    sortedTeams = sorted(team.conferenceTeams.values(), key=Team.predictiveWins)
    for i in range(8):

        actualTeam = sortedTeams[i]

        if actualTeam == team:
            i -= 1
            continue

        actualTeam.simQueue = actualTeam.scheduleQueue

        bottomEight.append(actualTeam)

    for simTeam in bottomEight:
        while simTeam.simQueue.empty() is False:

            simGame = simTeam.simQueue[0]
            simTeam.simQueue.remove(simGame)
            simGame.simulateGame(team, bottomEight)

            if simGame.homeTeam != simTeam:
                simGame.awayTeam.simQueue.remove(simGame)

            else:
                simGame.homeTeam.simQueue.remove(simGame)

    if(team.predictiveWins < max(bottomEight, key = Team.predictiveWins)):
        #Put date in for playoff elimination
        return False

    return True


division_Info=pandas.read_csv("Division_Info.csv")
nba_Season=pandas.read_csv("NBA_2016_2017_Scores.csv")
westernConference=0
easternConference=Conference(westernConference)
westernConference=Conference(easternConference)
teams = {}
games = []
results = []

for index,row in division_Info.iterrows():
    team= Team(row[0],row[1])

    #Conference.addTeam adds the conference itself to the team object
    if row[2]=='East':
        easternConference.addTeam(team)
    else:
        westernConference.addTeam(team)

    teams[str(row[0])] = team


for t in teams:
    teams[t].winLossD = teams

for index, row in nba_Season.iterrows():

    #row[5] is away or home winner
    #row[1] == home team
    #row[2] == away team
    #row[0] == date
    #row[3] == home score
    #row[4] == away score

    g = Game(row[0], teams[str(row[1])], teams[str(row[2])], row[3], row[4], row[5])

    #We first establish a Game object for each tuple of the CSV
    games.append(g)
    teams[row[2]].scheduleQueue.append(g)
    teams[row[1]].scheduleQueue.append(g)

for game in games:
    game.playGame()

    for te in teams:
        print(str(te) + ' ')
        print(str(teams[te]))

        if determinePlayoffEligibility(games, teams[te]) is False:
            #TODO Write date and team to excel
            results.append(tuple(te.teamName, game.date))

results.to_csv('result')