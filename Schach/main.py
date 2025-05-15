import pygame
import os
import copy

#  Initialisierung 
pygame.init()
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

#  Farben 
GREEN = (0, 255, 0)
CYAN_BLUE = (20, 90, 110)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
DARK_GRAY = (30, 30, 30)
BLUE = (50, 150, 255)

#  Fenster Setup 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Schach in Python")

#  Globale Variablen 
PIECE_IMAGES = {}
board = []
selected_square = None
valid_moves = []
current_player = "g"
game_over = False
winner = None
highlight_king = None

#  Hilfsfunktionen und Bilder
def load_images():
    for piece in ['bP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'gP', 'gR', 'gN', 'gB', 'gQ', 'gK']:
        path = os.path.join("images", piece + ".png")
        image = pygame.image.load(path)
        PIECE_IMAGES[piece] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

def reset_board():
    return [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP"] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        ["gP"] * 8,
        ["gR", "gN", "gB", "gQ", "gK", "gB", "gN", "gR"]
    ]

def draw_text(text, size, x, y):
    font = pygame.font.SysFont("Arial", size, bold=True)
    label = font.render(text, True, (255, 255, 255))
    rect = label.get_rect(center=(x, y))
    WIN.blit(label, rect)

def draw_button(text, x, y, action):
    rect = pygame.Rect(x - 100, y - 25, 200, 50)
    mouse, click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
    pygame.draw.rect(WIN, BLUE, rect, border_radius=10)
    if rect.collidepoint(mouse) and click[0]:
        pygame.time.delay(150)
        action()
    draw_text(text, 30, x, y)

#  Farben im Spiel
def draw_board():
    WIN.fill(GREEN)
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 != 0:
                pygame.draw.rect(WIN, CYAN_BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    if selected_square:
        for r, c in valid_moves:
            center = (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2)
            color = RED if board[r][c] and board[r][c][0] != current_player else YELLOW
            pygame.draw.circle(WIN, color, center, 25 if color == RED else 10)
    if highlight_king:
        r, c = highlight_king
        pygame.draw.rect(WIN, RED, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)

def draw_pieces():
    for r in range(ROWS):
        for c in range(COLS):
            piece = board[r][c]
            if piece:
                WIN.blit(PIECE_IMAGES[piece], (c * SQUARE_SIZE, r * SQUARE_SIZE))

#  Spiellogik 
def handle_click(row, col):
    global selected_square, valid_moves, current_player, game_over, winner
    if game_over:
        return

    piece = board[row][col]
    if selected_square:
        if (row, col) in valid_moves:
            from_r, from_c = selected_square
            moving = board[from_r][from_c]
            board[row][col], board[from_r][from_c] = moving, ""
            if moving[1] == "P" and row in (0, 7):
                board[row][col] = moving[0] + "Q"
            selected_square, valid_moves = None, []
            if is_checkmate("b" if current_player == "g" else "g"):
                game_over, winner = True, current_player
            else:
                current_player = "g" if current_player == "b" else "b"
        elif piece and piece[0] == current_player:
            selected_square = (row, col)
            valid_moves = get_legal_moves(row, col)
        else:
            selected_square, valid_moves = None, []
    elif piece and piece[0] == current_player:
        selected_square = (row, col)
        valid_moves = get_legal_moves(row, col)

def is_checkmate(color):
    return is_in_check(board, color) and not any(get_legal_moves(r, c)
        for r in range(8) for c in range(8)
        if board[r][c] and board[r][c][0] == color)

def is_in_check(b, color):
    global highlight_king
    king = next(((r, c) for r in range(8) for c in range(8) if b[r][c] == color + "K"), None)
    if not king:
        return False
    for r in range(8):
        for c in range(8):
            if b[r][c] and b[r][c][0] != color:
                if king in get_valid_moves(b, r, c):
                    highlight_king = king
                    return True
    highlight_king = None
    return False

def get_legal_moves(row, col):
    piece = board[row][col]
    color = piece[0]
    moves = get_valid_moves(board, row, col)
    legal = []
    for r, c in moves:
        temp = copy.deepcopy(board)
        temp[r][c], temp[row][col] = temp[row][col], ""
        if not is_in_check(temp, color):
            legal.append((r, c))
    return legal

def get_valid_moves(b, row, col):
    piece = b[row][col]
    if not piece:
        return []

    color, kind = piece[0], piece[1]
    moves = []
    direction = -1 if color == "g" else 1

    def on_board(r, c): return 0 <= r < 8 and 0 <= c < 8
    def enemy(r, c): return on_board(r, c) and b[r][c] and b[r][c][0] != color


    #Spielfiguren

    if kind == "P":
        start_row = 6 if color == "g" else 1
        for step in [1, 2] if row == start_row else [1]:
            r = row + direction * step
            if on_board(r, col) and not b[r][col]:
                moves.append((r, col))
            else:
                break
        for dc in [-1, 1]:
            r, c = row + direction, col + dc
            if enemy(r, c):
                moves.append((r, c))

    elif kind in "RBQ":
        dirs = {
            "R": [(-1,0), (1,0), (0,-1), (0,1)],
            "B": [(-1,-1), (-1,1), (1,-1), (1,1)],
            "Q": [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
        }[kind]
        for dr, dc in dirs:
            r, c = row + dr, col + dc
            while on_board(r, c):
                if not b[r][c]:
                    moves.append((r, c))
                elif b[r][c][0] != color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

    elif kind == "N":
        for dr, dc in [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]:
            r, c = row + dr, col + dc
            if on_board(r, c) and (not b[r][c] or b[r][c][0] != color):
                moves.append((r, c))

    elif kind == "K":
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr or dc:
                    r, c = row + dr, col + dc
                    if on_board(r, c) and (not b[r][c] or b[r][c][0] != color):
                        moves.append((r, c))

    return moves

#  Hauptmenü und Spielstart/ende
def main_menu():
    while True:
        WIN.fill(DARK_GRAY)
        draw_text("Schach", 80, WIDTH // 2, HEIGHT // 4)
        draw_button("Spiel starten", WIDTH // 2, HEIGHT // 2, start_game)
        draw_button("Beenden", WIDTH // 2, HEIGHT // 2 + 80, quit_game)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()

def start_game():
    global board, game_over, winner, selected_square, valid_moves, current_player
    board = reset_board()
    game_over, winner = False, None
    selected_square, valid_moves = None, []
    current_player = "g"
    main_game_loop()

def quit_game():
    pygame.quit(); exit()

def main_game_loop():
    clock = pygame.time.Clock()
    load_images()
    while True:
        clock.tick(60)
        draw_board()
        draw_pieces()
        if game_over:
            draw_text(f"{'Grün' if winner == 'g' else 'Blau'} gewinnt!", 40, WIDTH // 2, HEIGHT // 2 - 40)
            draw_button("Neustarten", WIDTH // 2, HEIGHT // 2 + 10, start_game)
            draw_button("Zum Menü", WIDTH // 2, HEIGHT // 2 + 70, main_menu)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
            if e.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mx, my = pygame.mouse.get_pos()
                handle_click(my // SQUARE_SIZE, mx // SQUARE_SIZE)

if __name__ == "__main__":
    main_menu()
