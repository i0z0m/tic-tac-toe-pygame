
from typing import List, Tuple, Optional
import pygame
import random


# Constants
WIDTH = 300
HEIGHT = 300
ROWS = 3
COLS = 3
CELL_SIZE = WIDTH // COLS
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


def check_winner(board: List[List[str]]) -> Optional[str]:
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]
    for col in range(COLS):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    if all(board[row][col] != ' ' for row in range(ROWS) for col in range(COLS)):
        return 'Draw'
    return None


def cpu_turn(board: List[List[str]], cpu_symbol: str) -> None:
    player_symbol = 'O' if cpu_symbol == 'X' else 'X'
    # Try to win
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                board[row][col] = cpu_symbol
                if check_winner(board) == cpu_symbol:
                    return
                board[row][col] = ' '
    # Try to block the player from winning
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                board[row][col] = player_symbol
                if check_winner(board) == player_symbol:
                    board[row][col] = cpu_symbol
                    return
                board[row][col] = ' '
    # Random move
    empty_cells = [(row, col) for row in range(ROWS)
                   for col in range(COLS) if board[row][col] == ' ']
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = cpu_symbol


def initialize_game() -> Tuple[pygame.Surface, List[List[str]], str, str]:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic-Tac-Toe")
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    player_symbol, cpu_symbol = ('X', 'O') if random.choice([
        True, False]) else ('O', 'X')
    return screen, board, player_symbol, cpu_symbol


def draw_board(screen: pygame.Surface, board: List[List[str]]) -> None:
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE,
                             row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            symbol = board[row][col]
            if symbol != ' ':
                color = BLUE if symbol == 'X' else RED
                font = pygame.font.Font(None, 72)
                text = font.render(symbol, True, color)
                screen.blit(text, (col * CELL_SIZE + CELL_SIZE //
                            3, row * CELL_SIZE + CELL_SIZE // 4))


def display_winner(screen: pygame.Surface, winner: str) -> None:
    text_color = BLUE if winner == 'X' else RED if winner == 'O' else BLACK
    font = pygame.font.Font(None, 36)
    text = font.render(f"{winner} wins!" if winner !=
                       'Draw' else "It's a Draw!", True, text_color)
    screen.blit(text, (WIDTH // 4, HEIGHT // 2))


def player_turn(board: List[List[str]], player_symbol: str, mouse_pos: Tuple[int, int]) -> Optional[str]:
    col = mouse_pos[0] // CELL_SIZE
    row = mouse_pos[1] // CELL_SIZE
    if board[row][col] == ' ':
        board[row][col] = player_symbol
        return check_winner(board)
    return None


def game_loop():
    screen, board, player_symbol, cpu_symbol = initialize_game()

    # If CPU is 'X', it goes first
    if cpu_symbol == 'X':
        cpu_turn(board, cpu_symbol)

    running = True
    winner = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and winner is None:
                winner = player_turn(board, player_symbol,
                                     pygame.mouse.get_pos())
                if winner is None:
                    cpu_turn(board, cpu_symbol)
                    winner = check_winner(board)

        draw_board(screen, board)

        # Display winner
        if winner:
            display_winner(screen, winner)

        pygame.display.flip()


if __name__ == "__main__":
    game_loop()
