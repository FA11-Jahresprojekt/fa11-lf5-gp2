import random
import math
import copy


def minimax(position, depth, alpha=-math.inf, beta=math.inf, parent=None):
    if parent is None:
        parent = []
    if depth == 0 or len(position.childs) == 0:  # or game over in position
        return [position.staticEvaluation(), position, parent]

    if position.maximizingPlayer:
        maxEval = -math.inf
        maxEvalNode = None
        maxParent = None
        for child in position.childs:
            newParent = copy.deepcopy(parent)
            newParent.append(position)
            eval, evalNode, p = minimax(child, depth - 1, alpha, beta, newParent)
            maxEval = max(maxEval, eval)
            if maxEval == eval:
                maxEvalNode = evalNode
                maxParent = p
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return [maxEval, maxEvalNode, maxParent]

    else:
        minEval = +math.inf
        minEvalNode = None
        minParent = None
        for child in position.childs:
            newParent = copy.deepcopy(parent)
            newParent.append(position)
            eval, evalNode, p = minimax(child, depth - 1, alpha, beta, newParent)
            minEval = min(minEval, eval)
            if minEval == eval:
                minEvalNode = evalNode
                minParent = p
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return [minEval, minEvalNode, minParent]
