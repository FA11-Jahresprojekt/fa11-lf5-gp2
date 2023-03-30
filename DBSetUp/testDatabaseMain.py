
from database import Database

testDataBase = Database.getInstance()

print(testDataBase.testSelectRankingData())
print(testDataBase.getTopPlayersForGameAndDifficulty("Bauernschach", 5, 2))
print(testDataBase.getTopPlayersForGameAndDifficulty("Bauernschach", 3, 2))
print(testDataBase.getTopPlayersForGameAndDifficulty("Dame", 5, 2))
print(testDataBase.getTopPlayersForGameAndDifficulty("Dame", 3, 2))

print(testDataBase.getGamesSummaryForGameAndDifficultyAndPlayerID("Dame", 3, 2))

print(testDataBase.getGameHistoryForChosenPlayer(1))