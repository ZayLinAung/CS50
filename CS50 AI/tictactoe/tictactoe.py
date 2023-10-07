"""
Tic Tac Toe Player
"""

import math, copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    if(terminal(board)):
        return None
    numX = 0
    numO = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                numX += 1
            elif board[i][j] == O:
                numO += 1
    if numX > numO:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    if terminal(board):
        return None
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action not in actions(board):
        raise Exception("Not valid")

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if(board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != EMPTY):
            return board[i][0]
        elif(board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != EMPTY):
            return board[0][i]
        elif((board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[1][1] != EMPTY) or (board[2][0] == board[1][1] and board[1][1] == board[0][2] and board[1][1] != EMPTY)):
            return board[1][1]
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if(winner(board) == X or winner(board) == O):
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if board == initial_state():
        return (1,1)

    best_moves = {}
    if player(board) == X:
        for action in actions(board):
            best_moves[min_value(result(board, action))] = action
        return best_moves[max(best_moves)]

    elif player(board) == O:
        for action in actions(board):
            best_moves[max_value(result(board, action))] = action
        return best_moves[min(best_moves)]

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
