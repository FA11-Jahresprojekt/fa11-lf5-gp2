import sqlite3


class Database:
    __instance = None

    def __init__(self):
        self.__connection = sqlite3.connect("DB/database.db")
        self.__cursor = self.__connection.cursor()
        self.setupTables()
        # self.testPersonData()
        # self.testGameData()

    def setupTables(self):
        sqlCreatePersonTableStatement = """
        CREATE TABLE IF NOT EXISTS person (
        pid Integer PRIMARY KEY,
        userName VARCHAR(30),
        password VARCHAR(30),
        UNIQUE(userName)
        );"""

        sqlCreateGameTableStatement = """
        CREATE TABLE IF NOT EXISTS game (
        gid Integer PRIMARY KEY,
        pid Integer,
        gameName VARCHAR(30),
        difficulty Integer,
        outcome VARCHAR(30),
        destroyedPawns Integer,
        FOREIGN KEY(pid) REFERENCES person(pid)
        );"""
        self.__cursor.execute(sqlCreatePersonTableStatement)
        self.__cursor.execute(sqlCreateGameTableStatement)
        self.__connection.commit()

    def testGameData(self):
        gid = 4
        pid = 2
        gameName = "Bauernschach"
        difficulty = 3
        outcome = "won"
        destroyedPawns = 6
        self.__cursor.execute("INSERT INTO game VALUES(?,?,?,?,?,?)",
                              (gid, pid, gameName, difficulty, outcome, destroyedPawns))
        self.__connection.commit()

    def testPersonData(self):
        pid = 2
        testUserName = "Tester"
        self.__cursor.execute("INSERT INTO person VALUES(?,?,?)", (pid, testUserName, None))
        self.__connection.commit()

    def testSelectRankingData(self):
        sqlSelectStatement = """
        SELECT 
        person.userName, game.gameName, game.difficulty, 
        COUNT() AS 'totalGames', 
        COUNT(CASE WHEN outcome = 'won'       then 1 END) AS 'gamesWon', 
        COUNT(CASE WHEN outcome = 'lost'      then 1 END) AS 'gamesLost', 
        COUNT(CASE WHEN outcome = 'cancelled' then 1 END) AS 'gamesCancelled', 
        SUM(game.destroyedPawns) AS 'destroyedPawns' 
        FROM person
        LEFT OUTER JOIN game ON person.pid = game.pid
        GROUP By  person.pid, game.difficulty, game.gameName
        ORDER BY gamesWon DESC
        """
        self.__cursor.execute(sqlSelectStatement)
        self.__connection.commit()
        return self.__cursor.fetchall()

    def getTopPlayersForGameAndDifficulty(self, gameName, difficulty, playerCount):
        """get the {playerCount} amount of top Players for the game: {gameName} and the difficulty: {difficulty}

        Args:
            gameName (str): string representing the game
            difficulty (int): int representing the depth of search for the algorithm
            playerCount (int): int representing the amount of players to be returned

        Returns:
            list: Lists filled with:
                    pid (int)
                    userName (str),
                    difficulty (int),
                    total amount of games (int),
                    amount of games won (int),
                    amount of games lost (int),
                    amount of games cancelled (int),
                    summ of destroyedPawns (int)
        """
        sqlSelectStatement = """
        SELECT 
        person.pid, person.userName, game.difficulty, 
        COUNT() AS 'totalGames', 
        COUNT(CASE WHEN game.outcome = 'won'       then 1 END) AS 'gamesWon', 
        COUNT(CASE WHEN game.outcome = 'lost'      then 1 END) AS 'gamesLost', 
        COUNT(CASE WHEN game.outcome = 'cancelled' then 1 END) AS 'gamesCancelled', 
        SUM(game.destroyedPawns) AS 'destroyedPawns' 
        FROM person
        LEFT OUTER JOIN game ON person.pid = game.pid
        WHERE game.gameName = ? AND game.difficulty = ?
        GROUP By person.pid, game.difficulty, game.gameName
        ORDER BY gamesWon DESC
        LIMIT(?)
        """
        self.__cursor.execute(sqlSelectStatement, (gameName, difficulty, playerCount))
        self.__connection.commit()
        return self.__cursor.fetchall()

    def getGamesSummaryForGameAndDifficultyAndPlayerID(self, gameName, difficulty, playerID):
        """get the summary of the games for a chosen game, difficulty and playerID

            Args:
                gameName (str): string representing the game
                difficulty (int): int representing the depth of search for the algorithm
                playerID (int): int representing the primary key of the chosen player

            Returns:
                list: Lists filled with:
                        pid (int)
                        userName (str),
                        difficulty (int),
                        total amount of games (int),
                        amount of games won (int),
                        amount of games lost (int),
                        amount of games cancelled (int),
                        summ of destroyedPawns (int)
        """
        sqlSelectStatement = """
            SELECT 
            person.pid, person.userName, game.difficulty, 
            COUNT() AS 'totalGames', 
            COUNT(CASE WHEN game.outcome = 'won'       then 1 END) AS 'gamesWon', 
            COUNT(CASE WHEN game.outcome = 'lost'      then 1 END) AS 'gamesLost', 
            COUNT(CASE WHEN game.outcome = 'cancelled' then 1 END) AS 'gamesCancelled', 
            SUM(game.destroyedPawns) AS 'destroyedPawns' 
            FROM person
            LEFT OUTER JOIN game ON person.pid = game.pid
            WHERE game.gameName = ? AND game.difficulty = ? AND person.pid = ?
            GROUP By person.pid, game.difficulty, game.gameName
            """
        self.__cursor.execute(sqlSelectStatement, (gameName, difficulty, playerID))
        self.__connection.commit()
        return self.__cursor.fetchall()

    def getGameHistoryForChosenPlayer(self, playerID):
        """get the game-history for a chosen Player

        Args:
            playerID (int): int representing the primary key of the chosen player

        Returns:
            list: Lists filled with:
                    gameName (str),
                    difficulty (int),
                    outcome (str),
                    destroyedPawns (int)
        """
        sqlSelectStatement = """
        SELECT 
        gameName, difficulty, outcome, destroyedPawns 
        FROM game
        WHERE pid =?
        ORDER BY gid DESC
        """
        self.__cursor.execute(sqlSelectStatement, (playerID,))
        self.__connection.commit()
        return self.__cursor.fetchall()

    def registerNewPerson(self, userName, password):
        """Adds a new set of data representing

                Args:
                    userName (str): string representing the name of the User
                    password (string): string representing the hash version of the password

                Returns:
                    none
        """
        sqlInsertStatement = """
        INSERT INTO person values(?,?,?)
        """
        self.__cursor.execute(sqlInsertStatement, (None, userName, password))
        self.__connection.commit()

    def getPersonByUserName(self, userName):
        """Adds a new set of data representing

                Args:
                    userName (str): string representing the name of the User

                Returns:
                    list: List filled with:
                            pid (int),
                            userName (str),
                            password (str) in hash format
        """
        sqlSelectStatement = """
        SELECT * FROM person 
        WHERE userName = ?
        """
        self.__cursor.execute(sqlSelectStatement, (userName,))
        self.__connection.commit()
        return self.__cursor.fetchall()

    def registerNewGame(self, pid, gameName, difficulty, outcome, destroyedPawns):
        """Adds a new set of data representing

                Args:
                    pid (int): int representing the id of the player that played this game
                    gameName (str): string representing the game
                    difficulty (int): int representing the depth of search for the algorithm
                    outcome (str): string representing the outcome of the game ('won'/'lost'/'cancelled')
                    destroyedPawns (int): int representing the number of opponents destroyed in this game

                Returns:
                    none
        """
        sqlInsertStatement = """
        INSERT INTO game VALUES(?,?,?,?,?,?)
        """
        self.__cursor.execute(sqlInsertStatement, (None, pid, gameName, difficulty, outcome, destroyedPawns))
        self.__connection.commit()

    @staticmethod
    def getInstance():
        """returns the sole existing instance of the database. If it doesn't exist yet, it will be created"""
        if Database.__instance is None:
            Database.__instance = Database()
        return Database.__instance
