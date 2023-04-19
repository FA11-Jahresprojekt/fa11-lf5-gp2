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

    @abc.abstractmethod
    def getPossiblePawnsForPlayer(self, player: str) -> []:
        pass

    @abc.abstractmethod
    def checkIfMoveValid(self, move: MoveAction) -> bool:
        return True

    @abc.abstractmethod
    def getPossiblePawnDestinationsForChosenPawn(self, pawn: Pawn):
        pass

    def movePawn(self, move: MoveAction) -> bool:
        if self.checkIfMoveValid(move):
            self.gameField.movePawn(move.pawn, move.targetPosX, move.targetPosY)
            return True
        else:
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
        player = "A" if self.maximizingPlayer else "B"
        score = 0

        if player == "A":
            if self.moveAction.targetPosY == 5:
                return 50
        else:
            if self.moveAction.targetPosY == 0:
                return -50

        if player == "A":
            score = score + self.moveAction.targetPosY * 2
        else:
            score = score - (5 - self.moveAction.targetPosY) * 2

        playerAPawn = self.game.getPossiblePawnsForPlayer("A")
        playerBPawn = self.game.getPossiblePawnsForPlayer("B")

        score = score + len(playerAPawn)
        score = score - len(playerBPawn)

        for pawn in playerAPawn:
            score = score + (pawn[1] * 0.5)
        for pawn in playerBPawn:
            score = score - ((5 - pawn[1]) * 0.5)

        return score


class BauernSchach(Game, ABC):

    def __init__(self, difficultly: int, gameField: GameField = GameField()):
        self.gameField = gameField
        super().__init__(difficultly)

    def generatePawns(self) -> None:
        size = self.gameField.getSize()
        for y in [0, size - 1]:
            for x in range(size):
                pawn = Pawn(x, y, ("A" if y == 0 else "B"))
                self.gameField.addPawnToGameField(pawn)

    def checkIfWon(self, player) -> bool:
        for pawn in self.gameField.getPawnsForPlayerKey(player):
            if pawn is not None and pawn.posY == (self.gameField.getSize() - 1 if player == "A" else 0):
                return True

        return False

    def checkIfLose(self, player: str) -> bool:
        return len(self.getPossiblePawnsForPlayer(player)) == 0

    def checkIfMoveValid(self, move: MoveAction) -> bool:
        return True

    def getPossiblePawnsForPlayer(self, player: str) -> []:
        pawnsList = []
        for pawn in self.gameField.getPawnsForPlayerKey(player):
            if pawn is not None and len(self.getPossiblePawnDestinationsForChosenPawn(pawn)) > 0:
                pawnsList.append([pawn.posX, pawn.posY])
        return pawnsList

    def getPossiblePawnDestinationsForChosenPawn(self, pawn: Pawn) -> []:
        lineCoord = pawn.posY
        columnCoord = pawn.posX
        possiblePawnDestinations = []
        enemy = "B" if pawn.player == "A" else "A"
        # alternating columnSummand, depending on which player is currently playing
        lineSummand = 0
        if pawn.player == "A":
            lineSummand = 1
        elif pawn.player == "B":
            lineSummand = -1
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


class Dame(Game, ABC):

    def __init__(self, difficultly: int, gameField: GameField = GameField()):
        self.gameField = gameField
        super().__init__(difficultly)

    def generatePawns(self) -> None:
        size = self.gameField.getSize()
        for y in [0, 1, size - 2, size - 1]:
            for x in range(size):
                if (x % 2 != 0 and y % 2 == 0) or (x % 2 == 0 and y % 2 != 0):
                    pawn = Pawn(x, y, ("A" if y == 0 or y == 1 else "B"))
                    self.gameField.addPawnToGameField(pawn)

    def checkIfWon(self, player) -> bool:
        # TODO: Create Win Condition for Game Dame
        return False


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
        return MiniMaxNode(self.game, self.gameToMiniMaxNodes(self.game, player, depth), player == "A")

    def gameToMiniMaxNodes(self, game: Game, player: str, depth: int) -> []:
        if depth == 0:
            return []
        nodes = []
        possiblePawns = game.getPossiblePawnsForPlayer(player)
        for pawnPos in possiblePawns:
            pawn = game.gameField.getPawnForPos(pawnPos[0], pawnPos[1])
            pawnPossiblePositions = game.getPossiblePawnDestinationsForChosenPawn(pawn)
            for pawnTargetPos in pawnPossiblePositions:
                newPawn = copy.deepcopy(pawn)
                newPawnVirtual = copy.deepcopy(pawn)
                moveActionVirtual = MoveAction(newPawnVirtual, pawnTargetPos[0], pawnTargetPos[1])
                moveAction = MoveAction(newPawn, pawnTargetPos[0], pawnTargetPos[1])
                newGame = copy.deepcopy(game)
                newGame.movePawn(moveAction)
                enemy = "B" if player == "A" else "A"
                nodes.append(MiniMaxNode(newGame, self.gameToMiniMaxNodes(newGame, enemy, depth - 1), moveActionVirtual,
                                         player != "A"))
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

    def doAction(self, player: str):
        if self.game.checkIfLose(player):
            print("Game Over!")
            return
        # "KI" is Playing
        if player == "B":
            self.controlKI()
        else:
            moveAction = self.userInputPossibleMoves(player)
            if not self.game.movePawn(moveAction):
                self.game.gameField.printGameField()
                return self.doAction(player)
        self.game.gameField.printGameField()
        if self.game.checkIfWon(player):
            print("Game Over!")
            return

        enemy = "B" if player == "A" else "A"
        self.doAction(enemy)

    def userInputPossibleMoves(self, player: str):
        playerPawns = self.game.getPossiblePawnsForPlayer(player)

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
