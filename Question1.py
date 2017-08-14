
def findProbabilityOfConsecutiveLoses(numberOfGamesInSeason,consecutiveLossThreshold,probOfLosing): # finds the probability of more than k consecutive losses in n games
    P=[0]*(numberOfGamesInSeason+1) #creates an array the size of the amount of games+1
    P[consecutiveLossThreshold]=probOfLosing**consecutiveLossThreshold #finds the probability of getting all loses with k games (Base Case)
    for i in range(consecutiveLossThreshold,numberOfGamesInSeason):
        P[i+1]=P[i]+(1-P[i-consecutiveLossThreshold])*(1-probOfLosing)*probOfLosing**(i) #dyan
    return P[numberOfGamesInSeason];
numberOfGamesInSeason =82
consecutiveLossThreshold=2
probOfLosing = .2
print(findProbabilityOfConsecutiveLoses(numberOfGamesInSeason,consecutiveLossThreshold,probOfLosing))

for i in range(0,1000,1):
    probabilityOfConsecutiveLossesWithChangedLossProbability=findProbabilityOfConsecutiveLoses(numberOfGamesInSeason,consecutiveLossThreshold,i/1000)
    if probabilityOfConsecutiveLossesWithChangedLossProbability>.5 and probabilityOfConsecutiveLossesWithChangedLossProbability<.501:
        print(i/1000)
