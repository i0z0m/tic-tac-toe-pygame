import pygame
import sys

# ゲームの初期化
pygame.init()

# ゲームボードの幅と高さ
WIDTH = 300
HEIGHT = 300

# マス目の数とサイズ
ROWS = 3
COLS = 3
CELL_SIZE = WIDTH // COLS

# カラーパレット
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# ゲーム画面の作成
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# ゲームボードの初期化
board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# 現在のプレイヤー
current_player = 'X'

# ゲームループ
running = True
while running:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # マウスの左ボタンがクリックされたとき
            mouse_pos = pygame.mouse.get_pos()
            col = mouse_pos[0] // CELL_SIZE
            row = mouse_pos[1] // CELL_SIZE
            if board[row][col] == ' ':
                board[row][col] = current_player
                # プレイヤーの交代
                current_player = 'O' if current_player == 'X' else 'X'

    # 画面の背景を描画
    screen.fill(WHITE)

    # ゲームボードの描画
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
            font = pygame.font.SysFont(None, 100)
            if board[row][col] == 'X':
                text = font.render('X', True, BLUE)
            elif board[row][col] == 'O':
                text = font.render('O', True, RED)
            else:
                continue
            text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
            screen.blit(text, text_rect)

    # 画面の更新
    pygame.display.flip()

# ゲームの終了
pygame.quit()
sys.exit()

