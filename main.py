import numpy as np
import pygame

ROW_COUNT = 6
COLUMN_COUNT = 7

SQUARE_SIZE = 100
SCREEN_WIDTH = COLUMN_COUNT * SQUARE_SIZE
SCREEN_HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font('freesansbold.ttf', 64)


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def print_board(board):
    print(board)


def draw_board(board):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            pygame.draw.rect(screen, (0, 0, 255), (c * SQUARE_SIZE, 100 + r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == 0:
                pygame.draw.circle(screen, (0, 0, 0), (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(100 + r * SQUARE_SIZE + SQUARE_SIZE / 2)), 45)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, (255, 0, 0), (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(100 + r * SQUARE_SIZE + SQUARE_SIZE / 2)), 45)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, (255, 255, 0), (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(100 + r * SQUARE_SIZE + SQUARE_SIZE / 2)), 45)


def valid_column(board, column):
    if board[0][column] == 0:
        return True
    else:
        return False


def get_row(board, column):
    for row in range(ROW_COUNT - 1, -1, -1):
        if board[row][column] == 0:
            return row


def drop_piece(board, column, row, player_index):
    board[row][column] = player_index


def if_won(board, column, row):
    # checking row wise
    for i in range(COLUMN_COUNT - 3):
        if board[row][i] == board[row][i + 1] == board[row][i + 2] == board[row][i + 3] != 0:
            return True

    # checking column wise
    for i in range(ROW_COUNT - 3):
        if board[i][column] == board[i + 1][column] == board[i + 2][column] == board[i + 3][column] != 0:
            return True

    # checking diagonally
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3] != 0:
                return True

    for r in range(ROW_COUNT - 1, ROW_COUNT - 4, -1):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3] != 0:
                return True


def if_game_over(board):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == 0:
                return False

    return True


def main():
    game_over = False
    board = create_board()
    screen.fill((0, 0, 0))
    turn = 0
    row = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
                xpos = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, (255, 0, 0), (xpos, int(SQUARE_SIZE / 2)), 45)
                else:
                    pygame.draw.circle(screen, (255, 255, 0), (xpos, int(SQUARE_SIZE / 2)), 45)

            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = event.pos[0]
                column = int(x_pos / 100)

                if valid_column(board, column):
                    row = get_row(board, column)
                    drop_piece(board, column, row, turn + 1)
                    turn += 1
                else:
                    pass

                if if_won(board, column, row):
                    print_board(board)
                    print('Player #' + str(turn) + ' won!!')
                    game_over = True
                    text = font.render("Player #" + str(turn + 1) + " Won!!", True, (255, 255, 255))
                    screen.blit(text, (250, 250))

                if if_game_over(board):
                    print('Game Over')
                    game_over = True

                turn = turn % 2
        draw_board(board)
        pygame.display.update()


main()
