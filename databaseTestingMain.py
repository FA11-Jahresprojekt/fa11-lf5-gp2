import sqlite3
from database import Database

testDataBase = Database.getInstance()

testDataBase.registerNewPerson()
testDataBase.registerNewGame()
testDataBase.getPersonByUserName()
testDataBase.getTopPlayersForGameAndDifficulty()
testDataBase.getGameHistoryForChosenPlayer()
testDataBase.getGamesSummaryForGameAndDifficultyAndPlayerID()



# print(testDataBase.registerNewPerson("Tester4", 123))
testDataBase.registerNewGame(1, "Bauernschach", 3, "cancelled", 3)
testDataBase.registerNewGame(1, "Bauernschach", 3, "cancelled", 3)
testDataBase.registerNewGame(1, "Bauernschach", 3, "cancelled", 3)
testDataBase.registerNewGame(1, "Bauernschach", 3, "cancelled", 3)
testDataBase.registerNewGame(1, "Bauernschach", 3, "cancelled", 3)
print(testDataBase.testSelectRankingData())
print(testDataBase.getTopPlayersForGameAndDifficulty("Bauernschach", 5, 2))
print(testDataBase.getTopPlayersForGameAndDifficulty("Bauernschach", 3, 5))
# print(testDataBase.getTopPlayersForGameAndDifficulty("Dame", 5, 2))
# print(testDataBase.getTopPlayersForGameAndDifficulty("Dame", 3, 2))
#
print(testDataBase.getGamesSummaryForGameAndDifficultyAndPlayerID("Bauernschach", 3, 1))
#
print(testDataBase.getGameHistoryForChosenPlayer(1))
#
# print(hash(1))
# print(hash(str(1)))
# print(hash(int(str(1))))
# print(hash("Hallo"))
# print(hash(20))
# print(hash(str(20)))
# print(hash(int(str(20))))