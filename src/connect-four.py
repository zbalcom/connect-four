import sys
import pygame

# Initialize PyGame
pygame.init()

# Set constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_SIZE = 100
RADIUS = SQUARE_SIZE // 2 - 5
width = COLUMN_COUNT * SQUARE_SIZE
height = ROW_COUNT * SQUARE_SIZE
size = (width, height)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Board data structure
class Board:
    def __init__(self, row_count = ROW_COUNT, col_count = COLUMN_COUNT):
        self.row_count = row_count
        self.col_count = col_count
        self.data = [[0 for _ in range(self.col_count)] for _ in range(self.row_count)]
    
    # Return number of rows
    def rows(self) -> int:
        return self.row_count
    
    # Return number of columns
    def columns(self) -> int:
        return self.col_count
    
    # Play the turn player's piece (val) in the chosen column
    # Return True if successful, False otherwise (e.g. if the column was full)
    def play(self, val: int, col: int) -> bool:
        for i in range(self.row_count):
            if self.data[i][col] == 0:
                self.data[i][col] = val
                return True
        return False
    
    # Return which piece exists at the specified row and column
    def get(self, row: int, col: int) -> int:
        return self.data[row][col]

# Create the screen
screen = pygame.display.set_mode(size)

# Draw the board
def draw_board(board: Board, mouse_pos: tuple[int, int], player: int = 1):
    pygame.draw.rect(screen, BLACK, (0, 0, board.columns() * SQUARE_SIZE, SQUARE_SIZE))

    for c in range(board.columns()):
        # x coordinate to draw the present square
        x = c * SQUARE_SIZE

        # draw floating piece to indicate which column the player is hovering over
        hovering = mouse_pos[0] in range(x, x + SQUARE_SIZE)
        if hovering:
            pygame.draw.circle(screen, (RED if player == 1 else YELLOW), (x + SQUARE_SIZE // 2, SQUARE_SIZE // 2), RADIUS)

        for r in range(board.rows()):
            # y coordinate to draw the present square
            y = r * SQUARE_SIZE + SQUARE_SIZE
            
            # color of the piece at the present square
            circle_color = BLACK
            match board.get(r, c):
                case 1:
                    circle_color = RED
                case 2:
                    circle_color = YELLOW
            
            pygame.draw.rect(screen, BLUE, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, circle_color, (x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2), RADIUS)
    pygame.display.update()

# Main game loop
board = Board()
mouse = (-1, -1)
draw_board(board, mouse)
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            mouse = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        
    draw_board(board, mouse)