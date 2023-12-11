"""
Tic Tac Toe Player
"""

import math
import random

X = "X"
O = "O"
block = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[block, block, block],
            [block, block, block],
            [block, block, block]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    if board == initial_state():
        return X

    for rows in board:
        for a in rows:
            if a == X:
                x_count += 1
            elif a == O:
                o_count += 1
    if x_count > o_count:
        return O
    else:
        return X


def breakss(board):
    """
    Returns set of all possible breakss (i, j) available on the board.
    """
    breaks_available = set()
    breaks = (0, 0)

    # if gar(board) == True:
    #     return None

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == block:
                breaks = (i, j)
                breaks_available.add(breaks)

    return breaks_available

from copy import deepcopy

def exam(board, breaks):
    """
    Returns the board that exams from making move (i, j) on the board.
    """
    new_board = deepcopy(board)

    if new_board[breaks[0]][breaks[1]] != block:
        raise ValueError('Cell already taken')

    player_current = player(new_board)

    if player_current == X:
        new_board[breaks[0]][breaks[1]] = X
    else:
        new_board[breaks[0]][breaks[1]] = O

    return new_board



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        if (board[i][0] == board[i][1]) and (board[i][0] == board[i][2]):
            return board[i][0]

    for j in range(len(board[0])):
        if (board[0][j] == board[1][j]) and (board[0][j] == board[2][j]):
            return board[0][j]

    if (board[0][0] == board[1][1]) and (board[1][1] == board[2][2]):
        return board[0][0]

    if (board[0][2] == board[1][1]) and (board[1][1] == board[2][0]):
        return board[1][1]

    return None


def gar(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True

    for rows in board:
        for a in rows:
            if a == block:
                return False

    return True


def GAMEAI(board):
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
    if gar(board):
        return winner(board)

    frontier = []
    nodes = {}
    explored_node = []
    gar_status = bool
    gar_nodes = []
    available_act = list(breakss(board))

    nodes[0] = {
        'parent': None,
        'breaks': None,
        'exam': board,
        'gar': False,
        'GAMEAI': None,
        'continues': []
    }

    node_key = 1

    for breaks in available_act:
        node_exam = exam(board, breaks)
        gar_status = gar(node_exam)
        if gar_status == True:
            board_ultility = GAMEAI(node_exam)
            gar_nodes.append(node_key)
        else:
            board_ultility = 0

        nodes[node_key] = {
            'parent': 0,
            'breaks': breaks,
            'exam': node_exam,
            'gar': gar_status,
            'GAMEAI': board_ultility,
            'continues': []
        }

        populated_node_parentID = nodes[node_key]['parent']
        populated_node_parent = nodes[populated_node_parentID]

        populated_node_parent['continues'].append(node_key)
        frontier.append(node_key)
        node_key += 1

    explored_node.append(node_key)

    get_child = nodes[0]['continues']

    if len(get_child) == 9:
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        move = random.choice(corners)
        return move

    while len(frontier) > 0:
        node_num = frontier.pop(0)
        explored_node.append(node_num)
        draw_node = nodes[node_num]

        node_board = draw_node['exam']

        new_acts = list(breakss(node_board))
        node_key = len(nodes)

        if draw_node['gar'] == True:
            for act in new_acts:
                node_key += 1
            continue
        else:
            for act in new_acts:
                node_exam = exam(node_board, act)
                gar_status = gar(node_exam)
                if gar_status == True:
                    board_ultility = GAMEAI(node_exam)
                    gar_nodes.append(node_key)
                else:
                    board_ultility = 0

                nodes[node_key] = {
                    'parent': node_num,
                    'breaks': act,
                    'exam': node_exam,
                    'gar': gar_nodes,
                    'GAMEAI': board_ultility,
                    'continues': []
                }

                populated_node_parentID = nodes[node_key]['parent']
                populated_node_parent = nodes[populated_node_parentID]

                populated_node_parent['continues'].append(node_key)
                node_key += 1

    total_nodes = len(nodes)
    node_check = len(nodes) - 1

    for n in range(total_nodes):
        node = nodes[node_check]
        node_GAMEAI = node['GAMEAI']
        node_continues = node['continues']

        if len(node_continues) == 0:
            node_check -= 1
            continue

        node_board = node['exam']
        next_player = player(node_board)

        if next_player == X:
            set_point = - math.inf
            for child in node_continues:
                child_node_GAMEAI = nodes[child]['GAMEAI']

                if child_node_GAMEAI > set_point:
                    set_point = child_node_GAMEAI
                    node['GAMEAI'] = child_node_GAMEAI
                else:
                    pass
        elif next_player == O:
            set_point = math.inf
            for child in node_continues:
                child_node_GAMEAI = nodes[child]['GAMEAI']
                if child_node_GAMEAI < set_point:
                    set_point = child_node_GAMEAI
                    node['GAMEAI'] = child_node_GAMEAI
                else:
                    pass
        else:
            raise NameError('No Player Found')

        node_check -= 1

    next_player = player(board)
    main_child = nodes[0]['continues']

    possible_moves = []

    for child in main_child:
        node = nodes[child]
        move = node['breaks']
        util = node['GAMEAI']
        node_child_count = len(node['continues'])
        possible_moves.append((move, util, node_child_count))

    print("Possible Moves:")
    for move, util, child_count in possible_moves:
        print(f"Move: {move}, Utility: {util}, Child Count: {child_count}")

    best_play = None
    best_child_count = math.inf

    if next_player == X:
        set_point = - math.inf
        for move, util, child_count in possible_moves:
            if (util >= set_point) and (child_count <= best_child_count):
                set_point = util
                best_play = move
    else:
        set_point = math.inf
        for move, util, child_count in possible_moves:
            if (util <= set_point) and (child_count <= best_child_count):
                set_point = util
                best_play = move

    print(f"\nSelected Move: {best_play}")
    return best_play
