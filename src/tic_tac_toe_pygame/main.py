
from typing import List, Tuple, Optional
import pygame
import random
import asyncio

# Constants
WIDTH = 210
HEIGHT = 210
ROWS = 5
COLS = 5
K = min(ROWS, COLS)
CELL_SIZE = WIDTH // COLS
FONT_SIZE = WIDTH // 5
BLACK = (50, 50, 50)
RED = (231, 76, 60)
BLUE = (52, 152, 219)
WHITE = (236, 240, 241)


def check_sequence(sequence: List[str], k: int) -> Optional[str]:
    for i in range(len(sequence) - k + 1):
        if all(sequence[i + j] == sequence[i] != ' ' for j in range(k)):
            return sequence[i]
    return None

def check_winner(board: List[List[str]], k: int) -> Optional[str]:
    # Check rows
    for row in board:
        winner = check_sequence(row, k)
        if winner is not None:
            return winner
    # Check columns
    for col in range(COLS):
        winner = check_sequence([board[row][col] for row in range(ROWS)], k)
        if winner is not None:
            return winner
    # Check main diagonal
    winner = check_sequence([board[i][i] for i in range(ROWS)], k)
    if winner is not None:
        return winner
    # Check secondary diagonal
    winner = check_sequence([board[i][ROWS - i - 1] for i in range(ROWS)], k)
    if winner is not None:
        return winner
    # Check for draw
    if all(board[row][col] != ' ' for row in range(ROWS) for col in range(COLS)):
        return 'Draw'
    return None


def cpu_turn(board: List[List[str]], cpu_symbol: str, k: int) -> None:
    player_symbol = 'O' if cpu_symbol == 'X' else 'X'
    # Try to win
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                board[row][col] = cpu_symbol
                if check_winner(board, k) == cpu_symbol:
                    return
                board[row][col] = ' '
    # Try to block the player from winning
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                board[row][col] = player_symbol
                if check_winner(board, k) == player_symbol:
                    board[row][col] = cpu_symbol
                    return
                board[row][col] = ' '
    # Random move
    empty_cells = [(row, col) for row in range(ROWS) for col in range(COLS) if board[row][col] == ' ']
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
    for row in range(1, ROWS):
        pygame.draw.line(screen, BLACK, (0, row * CELL_SIZE), (COLS * CELL_SIZE, row * CELL_SIZE), 1)
    for col in range(1, COLS):
        pygame.draw.line(screen, BLACK, (col * CELL_SIZE, 0), (col * CELL_SIZE, ROWS * CELL_SIZE), 1)
    for row in range(ROWS):
        for col in range(COLS):
            symbol = board[row][col]
            if symbol != ' ':
                color = BLUE if symbol == 'X' else RED
                font = pygame.font.Font(None, FONT_SIZE)
                text = font.render(symbol, True, color)
                screen.blit(text, (col * CELL_SIZE + CELL_SIZE // 3, row * CELL_SIZE + CELL_SIZE // 4))


def display_winner(screen: pygame.Surface, winner: str) -> None:
    text_color = BLUE if winner == 'X' else RED if winner == 'O' else BLACK
    font = pygame.font.Font(None, FONT_SIZE)
    text = font.render(f" {winner} won!" if winner != 'Draw' else "  Draw!", True, text_color)
    screen.blit(text, (WIDTH // 4, HEIGHT // 2))


def player_turn(board: List[List[str]], player_symbol: str, mouse_pos: Tuple[int, int], k: int) -> Optional[str]:
    col = mouse_pos[0] // CELL_SIZE
    row = mouse_pos[1] // CELL_SIZE

    # Check if the click is within the board
    if 0 <= row < len(board) and 0 <= col < len(board[0]):
        # If the cell is not empty, return 'invalid'
        if board[row][col] != ' ':
            return 'invalid'
        else:
            board[row][col] = player_symbol
            return check_winner(board, k)

    return None


async def game_loop(k: int):
    screen, board, player_symbol, cpu_symbol = initialize_game()

    # If CPU is 'X', it goes first
    if cpu_symbol == 'X':
        cpu_turn(board, cpu_symbol, k)

    running = True
    winner = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and winner is None:
                result = player_turn(board, player_symbol, pygame.mouse.get_pos(), k)
                if result != 'invalid':
                    winner = result
                    if winner is None:
                        cpu_turn(board, cpu_symbol, k)
                        winner = check_winner(board, k)

        draw_board(screen, board)

        # Display winner
        if winner:
            display_winner(screen, winner)

        pygame.display.flip()
        await asyncio.sleep(0)


async def main():
    await game_loop(K)

asyncio.run(main())
