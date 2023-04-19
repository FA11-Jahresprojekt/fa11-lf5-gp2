# from minimax import Algo, Action
import copy
import abc
import re
from abc import ABC
from typing import Optional
from random import randint

from minimax import minimax


def containsKey(dict, searchKey) -> bool:
    for key in dict.keys():
        if key == searchKey:
            return True
    return False


class Pawn:
    def __init__(self, posX, posY, player):
        self.posX = posX
        self.posY = posY
        self.player = player

    def __str__(self):
        return self.player


class MoveAction:
    def __init__(self, pawn: Pawn, targetPosX: int, targetPosY: int):
        self.pawn = pawn
        self.targetPosX = targetPosX
        self.targetPosY = targetPosY


class GameField:
    def __init__(self, size=6, players=["A", "B"]):
        self.playerPawns = {player: [] for player in players}
        self.gameField = [[None for _ in range(size)] for _ in range(size)]

    def addPawnToGameField(self, pawn) -> None:
        if not containsKey(self.playerPawns, pawn.player):
            return
        self.playerPawns.get(pawn.player).append(pawn)
        self.gameField[pawn.posY][pawn.posX] = pawn

    def getAllPawns(self) -> [Pawn]:
        return self.gameField

    def getPawnsForPlayerKey(self, player) -> [Pawn]:
        return self.playerPawns.get(player)

    def getPawnForPos(self, posX: int, posY: int) -> Optional[Pawn]:
        return self.gameField[posY][posX]

    def movePawnPos(self, oldPosX, oldPosY, posX, posY) -> None:
        pawn = self.gameField[oldPosY][oldPosX]
        if pawn is None:
            return
        self.movePawn(pawn, posX, posY)

    def movePawn(self, pawn: Pawn, posX: int, posY: int) -> None:
        targetPawn = self.gameField[posY][posX]
        if targetPawn is not None:
            targetPawns = self.getPawnsForPlayerKey(targetPawn.player)
            for i in range(len(targetPawns)):
                if targetPawn is targetPawns[i]:
                    targetPawns[i] = None
                    break
        self.gameField[pawn.posY][pawn.posX] = None
        self.gameField[posY][posX] = pawn
        pawn.posX = posX
        pawn.posY = posY

    def getSize(self) -> int:
        return len(self.gameField)

    def printGameField(self):
        for row in self.gameField:
            for col in row:
                print("-" if col is None else col, end=" ")
            print()

    def checkIfNotOutOfBounds(self, posX: int, posY: int) -> bool:
        return (0 <= posX < self.getSize()) and (0 <= posY < self.getSize())

    def checkIfSpotContainsEnemy(self, posX: int, posY: int, enemy: str):
        return self.gameField[posY][posX] is not None and self.gameField[posY][posX].player == enemy

    def checkIfFreeSpot(self, posX: int, posY: int) -> bool:
        return self.gameField[posY][posX] is None


# def countChilds(action: Action):
#     amountChilds = 0
#     for child in action.childs:
#         amountChilds += countChilds(child)
#     return len(action.childs) + amountChilds

class Game:
    def __init__(self, difficultly: int):
        self.difficultly = difficultly
        self.gameField = GameField()
        self.generatePawns()
        self.currentPlayer = "A"

    @abc.abstractmethod
    def generatePawns(self) -> None:
        pass

    @abc.abstractmethod
    def checkIfWon(self, player: str) -> bool:
        pass

    @abc.abstractmethod
    def checkIfLose(self, player: str) -> bool:
        pass

    def getPossiblePawnsForPlayer(self, player: str) -> []:
        pawnsList = []
        for pawn in self.gameField.getPawnsForPlayerKey(player):
            if pawn is not None and len(self.getPossiblePawnDestinationsForChosenPawn(pawn)) > 0:
                pawnsList.append([pawn.posX, pawn.posY])
        return pawnsList

    @abc.abstractmethod
    def checkIfMoveValid(self, move: MoveAction) -> bool:
        return True

    @abc.abstractmethod
    def getPossiblePawnDestinationsForChosenPawn(self, pawn: Pawn):
        return []

    @abc.abstractmethod
    def movePawn(self, move: MoveAction) -> bool:
        return False

    def switchPlayer(self):
        self.currentPlayer = "B" if self.currentPlayer == "A" else "A"
        return self.currentPlayer

class MiniMaxNode:
    def __init__(self, game: Game, childs: [], moveAction: Optional[MoveAction] = None, maximizingPlayer=False):
        self.game = game
        self.childs = childs
        self.moveAction = moveAction
        self.maximizingPlayer = maximizingPlayer

    def staticEvaluation(self):
        player = "B" if self.maximizingPlayer else "A"
        score = 0

        if player == "B":
            if self.moveAction.targetPosY == 5:
                return 50
        else:
            if self.moveAction.targetPosY == 0:
                return -50

        if player == "B":
            score = score + self.moveAction.targetPosY * 2
        else:
            score = score - (5 - self.moveAction.targetPosY) * 2

        playerAPawn = self.game.getPossiblePawnsForPlayer("A")
        playerBPawn = self.game.getPossiblePawnsForPlayer("B")

        score = score - len(playerAPawn)
        score = score + len(playerBPawn)

        for pawn in playerAPawn:
            score = score - ((5 - pawn[1]) * 0.5)
        for pawn in playerBPawn:
            score = score + (pawn[1] * 0.5)

        return score


class BauernSchach(Game, ABC):

    def __init__(self, difficultly: int, gameField: GameField = GameField()):
        self.gameField = gameField
        super().__init__(difficultly)

    def generatePawns(self) -> None:
        size = self.gameField.getSize()
        for y in [0, size - 1]:
            for x in range(size):
                pawn = Pawn(x, y, ("B" if y == 0 else "A"))
                self.gameField.addPawnToGameField(pawn)

    def checkIfWon(self, player) -> bool:
        for pawn in self.gameField.getPawnsForPlayerKey(player):
            if pawn is not None and pawn.posY == (self.gameField.getSize() - 1 if player == "B" else 0):
                return True

        return False

    def checkIfLose(self, player: str) -> bool:
        return len(self.getPossiblePawnsForPlayer(player)) == 0

    def checkIfMoveValid(self, move: MoveAction) -> bool:
        return True

    def getPossiblePawnDestinationsForChosenPawn(self, pawn: Pawn) -> []:
        lineCoord = pawn.posY
        columnCoord = pawn.posX
        possiblePawnDestinations = []
        enemy = "B" if pawn.player == "A" else "A"
        # alternating columnSummand, depending on which player is currently playing
        lineSummand = 0
        if pawn.player == "A":
            lineSummand = -1
        elif pawn.player == "B":
            lineSummand = 1
        # Checks if Spot in Front is not out of bounds and free
        if self.gameField.checkIfNotOutOfBounds(columnCoord, lineCoord + lineSummand):
            if self.gameField.checkIfFreeSpot(columnCoord, lineCoord + lineSummand):
                possiblePawnDestinations.append([columnCoord, lineCoord + lineSummand])
        # Checks if Spot in the Front-Left is not out of bounds and is occupied by an Enemy
        if self.gameField.checkIfNotOutOfBounds(columnCoord - 1, lineCoord + lineSummand):
            if self.gameField.checkIfSpotContainsEnemy(columnCoord - 1, lineCoord + lineSummand, enemy):
                possiblePawnDestinations.append([columnCoord - 1, lineCoord + lineSummand])
        # Checks if Spot in the Front-Right is not out of bounds and is occupied by an Enemy
        if self.gameField.checkIfNotOutOfBounds(columnCoord + 1, lineCoord + lineSummand):
            if self.gameField.checkIfSpotContainsEnemy(columnCoord + 1, lineCoord + lineSummand, enemy):
                possiblePawnDestinations.append([columnCoord + 1, lineCoord + lineSummand])
        return possiblePawnDestinations

    def movePawn(self, move: MoveAction) -> bool:
        if self.checkIfMoveValid(move):
            targetPawn = self.gameField.gameField[move.targetPosY][move.targetPosX]
            if targetPawn is not None:
                targetPawns = self.gameField.getPawnsForPlayerKey(targetPawn.player)
                for i in range(len(targetPawns)):
                    if targetPawn is targetPawns[i]:
                        targetPawns[i] = None
                        break
            self.gameField.gameField[move.pawn.posY][move.pawn.posX] = None
            self.gameField.gameField[move.targetPosY][move.targetPosX] = move.pawn
            move.pawn.posX = move.targetPosX
            move.pawn.posY = move.targetPosY
            return True


class Dame(Game, ABC):

    def __init__(self, difficultly: int, gameField: GameField = GameField()):
        self.gameField = gameField
        super().__init__(difficultly)

    def generatePawns(self) -> None:
        size = self.gameField.getSize()
        for y in [0, 1, size - 2, size - 1]:
            for x in range(size):
                if (x % 2 != 0 and y % 2 == 0) or (x % 2 == 0 and y % 2 != 0):
                    pawn = Pawn(x, y, ("B" if y == 0 or y == 1 else "A"))
                    self.gameField.addPawnToGameField(pawn)
        # pawns = [Pawn(0, 5, "A"), Pawn(1, 4, "B"), Pawn(3, 2, "B"), Pawn(5, 0, "B"), Pawn(4, 5, "A")]
        #
        # for pawn in pawns:
        #     self.gameField.addPawnToGameField(pawn)

    def checkIfWon(self, player) -> bool:
        for pawn in self.gameField.getPawnsForPlayerKey(player):
            if pawn is not None and pawn.posY == (self.gameField.getSize() - 1 if player == "B" else 0):
                return True

    def checkIfLose(self, player: str) -> bool:
        return len(self.getPossiblePawnsForPlayer(player)) == 0

    def getPossiblePawnDestinationsForChosenPawn(self, pawn: Pawn, recursiveMove=False) -> []:
        lineCoord = pawn.posY
        columnCoord = pawn.posX
        possiblePawnDestinations = []
        enemy = "B" if pawn.player == "A" else "A"
        # alternating columnSummand, depending on which player is currently playing
        lineSummand = 0
        if pawn.player == "A":
            lineSummand = -1
        elif pawn.player == "B":
            lineSummand = 1
        if not recursiveMove:
            # Checks if Spot in the Front-Left is not out of bounds and is free
            if self.gameField.checkIfNotOutOfBounds(columnCoord - 1, lineCoord + lineSummand):
                if self.gameField.checkIfFreeSpot(columnCoord - 1, lineCoord + lineSummand):
                    possiblePawnDestinations.append([columnCoord - 1, lineCoord + lineSummand])
            # Checks if Spot in the Front-Right is not out of bounds and is not occupied by an Enemy
            if self.gameField.checkIfNotOutOfBounds(columnCoord + 1, lineCoord + lineSummand):
                if self.gameField.checkIfFreeSpot(columnCoord + 1, lineCoord + lineSummand):
                    possiblePawnDestinations.append([columnCoord + 1, lineCoord + lineSummand])
        # Checks if Spot in the Front-Left is not out of bounds, is occupied by an Enemy and if Spot behind is free and not out of bounds
        if self.gameField.checkIfNotOutOfBounds(columnCoord - 1, lineCoord + lineSummand):
            if self.gameField.checkIfSpotContainsEnemy(columnCoord - 1, lineCoord + lineSummand, enemy):
                if self.gameField.checkIfNotOutOfBounds(columnCoord - 2, lineCoord + (lineSummand * 2)):
                    if self.gameField.checkIfFreeSpot(columnCoord - 2, lineCoord + (lineSummand * 2)):
                        possiblePawnDestinations.append([columnCoord - 2, lineCoord + (lineSummand * 2)])
        # Checks if Spot in the Front-Right is not out of bounds, is occupied by an Enemy and if Spot behind is free and not out of bounds
        if self.gameField.checkIfNotOutOfBounds(columnCoord + 1, lineCoord + lineSummand):
            if self.gameField.checkIfSpotContainsEnemy(columnCoord + 1, lineCoord + lineSummand, enemy):
                if self.gameField.checkIfNotOutOfBounds(columnCoord + 2, lineCoord + (lineSummand * 2)):
                    if self.gameField.checkIfFreeSpot(columnCoord + 2, lineCoord + (lineSummand * 2)):
                        possiblePawnDestinations.append([columnCoord + 2, lineCoord + (lineSummand * 2)])
        return possiblePawnDestinations

    def movePawn(self, move: MoveAction) -> bool:
        if self.checkIfMoveValid(move):
            directionX = move.targetPosX - move.pawn.posX
            directionY = move.targetPosY - move.pawn.posY
            if directionX == 2 or directionX == -2:
                targetPawn = self.gameField.gameField[move.targetPosY - int(directionY / 2)][
                    move.targetPosX - int(directionX / 2)]
                if targetPawn is not None:
                    targetPawns = self.gameField.getPawnsForPlayerKey(targetPawn.player)
                    for i in range(len(targetPawns)):
                        if targetPawn is targetPawns[i]:
                            targetPawns[i] = None
                            self.gameField.gameField[move.targetPosY - int(directionY / 2)][
                                move.targetPosX - int(directionX / 2)] = None
                            self.gameField.gameField[move.pawn.posY][move.pawn.posX] = None
                            self.gameField.gameField[move.targetPosY][move.targetPosX] = move.pawn
                            move.pawn.posX = move.targetPosX
                            move.pawn.posY = move.targetPosY
                            if len(self.getPossiblePawnDestinationsForChosenPawn(move.pawn, True)) > 0:
                                return False
                            return True
            self.gameField.gameField[move.pawn.posY][move.pawn.posX] = None
            self.gameField.gameField[move.targetPosY][move.targetPosX] = move.pawn
            move.pawn.posX = move.targetPosX
            move.pawn.posY = move.targetPosY
            return True


class KI(ABC):

    def __init__(self, game: Game):
        self.game = game

    def generateAllMoveActions(self, player: str):
        actions = []
        pawns = self.game.getPossiblePawnsForPlayer(player)
        for pawnPos in pawns:
            pawn = self.game.gameField.getPawnForPos(pawnPos[0], pawnPos[1])
            pawnPossiblePositions = self.game.getPossiblePawnDestinationsForChosenPawn(pawn)
            for pawnTargetPos in pawnPossiblePositions:
                actions.append(MoveAction(pawn, pawnTargetPos[0], pawnTargetPos[1]))
        return actions

    def getAction(self, player: str) -> MoveAction:
        possibleActions = self.generateAllMoveActions(player)
        moveAction = self.chooseMoveAction(possibleActions)
        pawn = self.game.gameField.getPawnForPos(moveAction.pawn.posX, moveAction.pawn.posY)
        return MoveAction(pawn, moveAction.targetPosX, moveAction.targetPosY)

    @abc.abstractmethod
    def chooseMoveAction(self, possible_actions: []) -> MoveAction:
        pass


class RandomKi(KI, ABC):

    def chooseMoveAction(self, possible_actions: []) -> MoveAction:
        random = randint(0, len(possible_actions) - 1)
        return possible_actions[random]


class MiniMaxKI(KI, ABC):

    def convertGameFieldToMiniMaxNode(self, player: str, depth=3) -> MiniMaxNode:
        return MiniMaxNode(self.game, self.gameToMiniMaxNodes(self.game, player, depth), player != "A")

    def gameToMiniMaxNodes(self, game: Game, player: str, depth: int) -> []:
        if depth == 0:
            return []
        nodes = []
        possiblePawns = game.getPossiblePawnsForPlayer(player)
        for pawnPos in possiblePawns:
            pawn = game.gameField.getPawnForPos(pawnPos[0], pawnPos[1])
            pawnPossiblePositions = game.getPossiblePawnDestinationsForChosenPawn(pawn)
            for pawnTargetPos in pawnPossiblePositions:
                newGame = copy.deepcopy(game)
                newPawn = newGame.gameField.getPawnForPos(pawnPos[0], pawnPos[1])

                newPawnVirtual = copy.deepcopy(newPawn)
                moveActionVirtual = MoveAction(newPawnVirtual, pawnTargetPos[0], pawnTargetPos[1])

                moveAction = MoveAction(newPawn, pawnTargetPos[0], pawnTargetPos[1])

                newGame.movePawn(moveAction)
                enemy = "B" if player == "A" else "A"
                nodes.append(MiniMaxNode(newGame, self.gameToMiniMaxNodes(newGame, enemy, depth - 1), moveActionVirtual,
                                         player == "A"))
        return nodes

    def chooseMoveAction(self, possible_actions: []) -> MoveAction:
        node = self.convertGameFieldToMiniMaxNode("B", self.game.difficultly)
        outcome = minimax(node, self.game.difficultly)
        outcome[2].append(outcome[1])
        print(outcome[0])
        return outcome[2][1].moveAction


class GameController:

    def __init__(self, gameObj: Game, ki: str):
        self.game = gameObj
        class_ = globals()[ki]
        self.ki = class_(gameObj)

    def startGame(self, startPlayer="A"):
        self.doAction(startPlayer)

    def controlKI(self):
        print("KI is Playing")
        moveAction = self.ki.getAction("B")
        self.game.movePawn(moveAction)

    def doAction(self, player: str, pawn: Optional[Pawn] = None):
        if self.game.checkIfLose(player):
            print("Game Over!")
            return
        # "KI" is Playing
        if player == "B":
            self.controlKI()
        else:
            moveAction = self.userInputPossibleMoves(player, pawn)
            if not self.game.movePawn(moveAction):
                self.game.gameField.printGameField()
                return self.doAction(player, moveAction.pawn)
        self.game.gameField.printGameField()
        if self.game.checkIfWon(player):
            print("Game Over!")
            return

        enemy = "B" if player == "A" else "A"
        self.doAction(enemy)

    def userInputPossibleMoves(self, player: str, pawn: Optional[Pawn]):
        playerPawns = self.game.getPossiblePawnsForPlayer(player) if pawn is None else [[pawn.posX, pawn.posY]]

        pawnLoc = None
        while pawnLoc not in playerPawns:
            print("Possible Pawn(s) to Choose:")
            print(playerPawns)
            print("Please insert a column coordinate to choose your pawn which is to be moved")
            col = int(self.rawUserInput("Column-Coordinate: ", r'^[0-5]$'))
            print("Please insert a line coordinate to choose your pawn which is to be moved")
            line = int(self.rawUserInput("Line-Coordinate: ", r'^[0-5]$'))
            pawnLoc = [col, line]
        pawn = self.game.gameField.getPawnForPos(pawnLoc[0], pawnLoc[1])
        locations = self.game.getPossiblePawnDestinationsForChosenPawn(pawn)

        loc = [-1, -1]
        while loc not in locations:
            print("Possible Destinationtile(s) to Choose:")
            print(locations)
            print("Please insert a column coordinate, to choose the destination, to which your pawn will be moved")
            col = int(self.rawUserInput("Column-Coordinate: ", r'^[0-5]$'))
            print("Please insert a line coordinate, to choose the destination, to which your pawn will be moved")
            line = int(self.rawUserInput("Line-Coordinate: ", r'^[0-5]$'))
            loc = [col, line]

        return MoveAction(pawn, loc[0], loc[1])

    def rawUserInput(self, prompt: str, regex: str):
        uInput = input(prompt)

        if uInput.casefold() == "BACK".casefold():
            return None
        while not re.match(regex, uInput):
            print("Deine Eingabe entspricht nicht dem Erforderlichen Format.")
            return self.rawUserInput(prompt, regex)

        return uInput

