import numpy as np
import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 1
AI = 2
EMPTY = 0
WINDOW_LENGTH = 4

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c] == piece for i in range(WINDOW_LENGTH)):
                return True

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r + i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True

    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r - i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True

    return False

def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]
    is_terminal = winning_move(board, PLAYER) or winning_move(board, AI) or len(valid_locations) == 0

    if depth == 0 or is_terminal:
        if winning_move(board, AI):
            return None, 1000000
        elif winning_move(board, PLAYER):
            return None, -1000000
        else:
            return None, 0

    if maximizing_player:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value

    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER)
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

board = create_board()
game_over = False
turn = random.randint(PLAYER, AI)

while not game_over:
    print_board(board)

    if turn == PLAYER:
        col = int(input("Enter column (0-6): "))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER)
            if winning_move(board, PLAYER):
                print("PLAYER WINS!")
                game_over = True
            turn = AI

    else:
        col, _ = minimax(board, 5, -math.inf, math.inf, True)
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI)
            if winning_move(board, AI):
                print("AI WINS!")
                game_over = True
            turn = PLAYER