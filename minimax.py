import random
import math


def minimax(position, depth, alpha, beta):
    if depth == 0:  # or game over in position
        return position.staticEvaluation()

    if position.maximizingPlayer:
        maxEval = -math.inf
        for child in position.childs:
            eval = minimax(child, depth - 1, alpha, beta)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval

    else:
        minEval = +math.inf
        for child in position.childs:
            eval = minimax(child, depth - 1, alpha, beta)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval


class MiniMaxNode:
    def __init__(self, childs=[], maximizingPlayer=False, x=None):
        self.x = x
        self.childs = childs
        self.maximizingPlayer = maximizingPlayer

    def staticEvaluation(self):
        # x = random.randint(-10, 10)
        return self.x


node = MiniMaxNode([
    MiniMaxNode([
        MiniMaxNode(
            [], True, 5
        ),
        MiniMaxNode(
            [], True, 8
        )
    ]),
    MiniMaxNode([

        MiniMaxNode(
            [], True, -2
        ),
        MiniMaxNode(
            [], True, 7
        )
    ])
], True)

val = minimax(node, 2, -math.inf, math.inf)

# print(node)

print(val)
