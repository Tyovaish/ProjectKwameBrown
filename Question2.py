class Team:
    def __init__(self,teamName,divisionName,conferenceName):
        self.teamName=teamName
        self.divisionName=divisionName
        self.conferenceName=conferenceName
        self.gamesPlayedByTeam=[]
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