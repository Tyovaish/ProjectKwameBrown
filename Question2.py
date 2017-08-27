import datetime
import sys
import pandas

class Division:
    def __init__(self, name):
        self.name = name
        self.teams = []

    def addTeam(self, team):
        self.teams.append(team)
        team.divisionName = self

class Team:
    def __init__(self,teamName,divisionName):
        self.teamName=teamName
        self.divisionName=0
        self.conferenceName=0
        self.numberOfWins = 0
        self.numberOfLosses= 0
        self.winLossD = {}
        self.pointDifferentialPerTeam={}
        self.conferenceRank = 0
        self.divisionRank = 0

        self.scheduleQueue=[]
        self.simQueue=[]

        self.stillAlive = True

        self.predictiveWins=0
        self.predictiveLosses=0
        self.predictiveRank=0
        self.predictiveWinLossD = {}


    def predictiveWinCount(self):
        return self.predictiveWins

    def setConference(self, conference):
        self.conferenceName = conference

    def updateTeamStats(self,game):
        opposingTeamName=game.getOpposingTeam(self.teamName)
        if opposingTeamName not in self.winLossD:
            self.winLossD[game.getOpposingTeam(self.teamName)]=[0,0]


        if game.isWinner(self):
            self.numberOfWins += 1
            self.winLossD[opposingTeamName][0]+=1
        else:
            self.numberOfLosses += 1
            self.winLossD[opposingTeamName][1] += 1
        opposingTeamScore=game.getTeamScore(opposingTeamName)
        teamScore=game.getTeamScore(self)
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
    def __init__(self,datePlayed,homeTeam, awayTeam, homeScore,awayScore,winningTeam):
        d = datePlayed.split('/')
        self.datePlayed=datetime.date(int(d[2]), int(d[0]), int(d[1]))
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
        if self.homeTeam.teamName==team:
            return self.awayTeam.teamName
        else:
            return self.homeTeam.teamName
    def getTeamScore(self,team):
        if self.homeTeam.teamName == team:
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

                #TODO add winLossD simulation
        if self.awayTeam.teamName not in self.homeTeam.predictiveWinLossD:
            self.homeTeam.predictiveWinLossD[self.awayTeam.teamName] = [0, 0]

        if self.homeTeam.teamName not in self.awayTeam.predictiveWinLossD:
            self.awayTeam.predictiveWinLossD[self.homeTeam.teamName] = [0, 0]
    #Target Team is the team that we want to have the best possible season

        #Target Team always wins
        if self.homeTeam == targetTeam or self.awayTeam == targetTeam:
            if self.homeTeam != targetTeam:
                targetTeam.predictiveWinLossD[self.homeTeam.teamName][0] += 1

            if self.awayTeam != targetTeam:
                targetTeam.predictiveWinLossD[self.awayTeam.teamName][0] += 1

        #If it's interconference we assume our boy loses
        elif self.homeTeam.conferenceName != self.awayTeam.conferenceName:
            None

        #At this point we must be within our own conference and not playing the target team
        #If both teams are bottom 8 then we assume the lesser wins
        elif self.homeTeam in bottomEight and self.awayTeam in bottomEight:
            if self.homeTeam.predictiveWins > self.awayTeam.predictiveWins:
                self.awayTeam.predictiveWins += 1
                #TODO Just like this
                self.awayTeam.predictiveWinLossD[self.homeTeam.teamName][0] += 1
            else:
                self.homeTeam.predictiveWins += 1
                self.homeTeam.predictiveWinLossD[self.awayTeam.teamName][0] += 1

        else:
            if self.homeTeam.predictiveWins > self.awayTeam.predictiveWins:
                self.homeTeam.predictiveWins += 1
                self.homeTeam.predictiveWinLossD[self.awayTeam.teamName][0] += 1

            else:
                self.awayTeam.predictiveWins += 1
                self.awayTeam.predictiveWinLossD[self.homeTeam.teamName][0] += 1

        #Pop game from simQueue of participants




class Conference:
    def __init__(self,competingConference):
        self.competingConference=competingConference
        self.conferenceTeams=[]
        self.gamesPlayedByEachTeam={}
        self.ineligiblePlayoffTeams=[]

    def addGame(self,game):
        self.gamesPlayedByEachTeam[game.homeTeam].append(game)
        self.gamesPlayedByEachTeam[game.awayTeam].append(game)

    def addTeam(self,team):
        self.conferenceTeams.append(team)
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

def predictiveWinCount(team):
    return team.predictiveWins


def WinCount(team):
    return team.numberOfWins


def determinePlayoffEligibility(games, team):
    if(team.numberOfWins + team.numberOfLosses <= 41) or (team.stillAlive is False):
        return True


    bottomEight = []

    for t in team.conferenceName.conferenceTeams:
        t.predictiveWins = t.numberOfWins
        t.predictiveLosses = t.numberOfLosses

    team.predictiveWins = team.numberOfWins + len(team.scheduleQueue)

    team.predictiveWinLoss = {}

    for t in team.winLossD:
        team.predictiveWinLossD[t] = team.winLossD[t].copy()

    #TODO initialize predictiveWinLossD with a COPY of the information in winLossD, don't just pass the reference

    index = 0
    sortedTeams = sorted(team.conferenceName.conferenceTeams, key=WinCount)
    while len(bottomEight) < 7:

        actualTeam = sortedTeams[index]



        if actualTeam.teamName == team.teamName:
            index += 1
            continue

        actualTeam.predictiveWinLossD = {}
        actualTeam.simQueue = actualTeam.scheduleQueue.copy()

        for t in actualTeam.winLossD:
            actualTeam.predictiveWinLossD[t] = actualTeam.winLossD[t].copy()

        bottomEight.append(actualTeam)
        index += 1

    for simTeam in bottomEight:
        while len(simTeam.simQueue) != 0:

            simGame = simTeam.simQueue[0]

            simGame.simulateGame(team, bottomEight)

            if simGame in simGame.homeTeam.simQueue:
                simGame.homeTeam.simQueue.remove(simGame)

            if simGame in simGame.awayTeam.simQueue:
                simGame.awayTeam.simQueue.remove(simGame)

    tiedTeams = []

    tiedTeams.append(team)

    for t in bottomEight:
        if t.predictiveWins == team.predictiveWins:
            tiedTeams.append(t)

    tieWinner = 0

    if team.predictiveWins == max(bottomEight, key = predictiveWinCount).predictiveWins:
        tieWinner = determineTieBreaker(tiedTeams)

        if tieWinner != team:
            # Put date in for playoff elimination
            team.stillAlive = False
            return False

    if(team.predictiveWins < max(bottomEight, key = predictiveWinCount).predictiveWins):
        #Put date in for playoff elimination
        team.stillAlive = False
        return False

    return True

def determineTieBreaker(teams):

    while len(teams) > 1:
        tWin = determineTieBreaker2Teams(teams[0], teams[1])

        if(tWin == teams[0]):
            teams.remove(teams[1])
        else:
            teams.remove(teams[0])

        return teams[0]


def determineTieBreaker2Teams(team1, team2):


    if team1.predictiveWinLossD[team2.teamName][0] > team2.predictiveWinLossD[team1.teamName][0]:
        return team1

    else:
        return team2

    if team1.divisionName != team2.divisionName:
        d1 = sorted(team1.divisionName.teams, key = predictiveWinCount)
        d2 = sorted(team2.divisionName.teams, key = predictiveWinCount)

        if d1[0] == team1 and d2[0] != team2:
            return team1

        if d1[0] != team1 and d2[0] == team2:
            return team2

    t1 = 0
    t2 = 0

    for t in team1.divisionName.teams:
        t1 += team1.predictiveWinLossD[t.teamName][0]

    for t in team2.divisionName.teams:
        t2 += team2.predictiveWinLossD[t.teamName][0]

    if t1 > t2:
        return team1

    if t2 > t1:
        return team2

    t1 = 0
    t2 = 0

    for t in team1.conferenceName.conferenceTeams:
        t1 += team1.predictiveWinLossD[t.teamName][0]

    for t in team2.conferenceName.conferenceTeams:
        t2 += team2.predictiveWinLossD[t.teamName][0]

    if t1 > t2:
        return team1

    if t2 > t1:
        return team2

division_Info=pandas.read_csv(sys.argv[0])
nba_Season=pandas.read_csv(sys.argv[1])
westernConference=0
easternConference=Conference(westernConference)
westernConference=Conference(easternConference)

divisions = {}
atlanticDivision=Division('Atlantic')
divisions['Atlantic'] = atlanticDivision
divisions['Central']=Division('Central')
divisions['Southeast']=Division('Southeast')
divisions['Northwest']=Division('Northwest')
divisions['Pacific']=Division('Pacific')
divisions['Southwest']=Division('Southwest')


teams = {}
games = []
resultsTeam = []
resultsDate = []

for index,row in division_Info.iterrows():
    team= Team(row[0],row[1])

    #Conference.addTeam adds the conference itself to the team object
    if row[2]=='East':
        easternConference.addTeam(team)
    else:
        westernConference.addTeam(team)

    divisions[str(row[1])].addTeam(team)

    teams[str(row[0])] = team



for index, row in nba_Season.iterrows():

    #row[5] is away or home winner
    #row[1] == home team
    #row[2] == away team
    #row[0] == date
    #row[3] == home score
    #row[4] == away score

    g = Game(row[0], teams[str(row[1])], teams[str(row[2])], row[3], row[4], row[5])

    #We first  a Game object for each tuple of the CSV
    games.append(g)
    teams[row[2]].scheduleQueue.append(g)
    teams[row[1]].scheduleQueue.append(g)

for game in games:

    game.playGame()

    for te in teams:

        if determinePlayoffEligibility(games, teams[te]) is False:
            #TODO Write date and team to excel
            resultsTeam.append(te)
            resultsDate.append(game.datePlayed)

df = pandas.DataFrame({"Date" : resultsDate, "Team Name" : resultsTeam})
df.to_csv("submission.csv", index = False)