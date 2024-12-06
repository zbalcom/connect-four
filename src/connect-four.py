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
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Board data structure
class Board:
    def __init__(self, col_count = COLUMN_COUNT, row_count = ROW_COUNT):
        self.col_count = col_count
        self.row_count = row_count
        self.data = [[0 for _ in range(self.row_count)] for _ in range(self.col_count)]
        self.last_play = (0, 0)
        # winner is -1 for a draw, 0 for none, 1 for player 1, 2 for player 2
        self.winner = 0
    
    # Return number of columns
    def columns(self) -> int:
        return self.col_count
    
    # Return number of rows
    def rows(self) -> int:
        return self.row_count
    
    # Return which piece exists at the specified row and column
    def get(self, col: int, row: int) -> int:
        return self.data[col][row]
    
    # Place given piece at given coordinates (col, row)
    def place_piece(self, col: int, row: int, piece: int):
        self.data[col][row] = piece
    
    # Return last open row in given column (-1 if column is full)
    def get_open_row(self, col: int) -> int:
        for r in reversed(range(self.row_count)):
            if self.get(col, r) == 0:
                return r
        return -1

    # Return true if column is not full
    def is_valid_column(self, col: int) -> bool:
        return self.get(col, 0) == 0
    
    def get_valid_moves(self) -> list[int]:
        return list(filter(self.is_valid_column, range(self.col_count)))
    
    # Play the turn player's piece (val) in the chosen column, in the furthest row possible
    # Return the success of the play (True/False) and the current winner, if any
    def play(self, piece: int, col: int) -> tuple[bool, int]:

        # Do not allow more plays if somebody has won
        if self.winner == 0:

            # Drop the piece into the first open space from the bottom
            row = self.get_open_row(col)
            if row in range(self.row_count):
                self.place_piece(col, row, piece)
                self.last_play = (col, row)
                self.winner = self.check_win()
                return (True, self.winner)
            
        return (False, self.winner)
    
    # Return the winning player
    # -1: draw
    # 0: none
    # 1: player 1
    # 2: player 2
    def check_win(self) -> int:
        draw = True
        for c in range(self.col_count):
            draw = draw and self.get(c, 0) != 0
        
        c, r = self.last_play
        last_player = self.get(c, r)

        # Check a line for 4 of the given piece in a row
        def check_four(line: list[int], piece: int) -> bool:
            count = 0
            for p in line:
                if p == piece:
                    count += 1
                    if count >= 4:
                        return True
                else:
                    count = 0
            return False

        up_left = min(c, r)
        up_right = min(self.col_count - c - 1, r)
        down_left = min(c, self.row_count - r - 1)
        down_right = min(self.col_count - c - 1, self.row_count - r - 1)

        win = (check_four(self.data[c], last_player) # vertical win
            or check_four([self.get(i, r) for i in range(self.col_count)], last_player) # horizontal win
            or check_four([self.get(c + i, r + i) for i in range(-up_left, down_right + 1)], last_player) # diagonal down win
            or check_four([self.get(c + i, r - i - 1) for i in range(-down_left, up_right + 1)], last_player)) # diagonal up win
        
        if win:
            return last_player
        if draw:
            return -1
        return 0

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
            match board.get(c, r):
                case 1:
                    circle_color = RED
                case 2:
                    circle_color = YELLOW
            
            pygame.draw.rect(screen, BLUE, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, circle_color, (x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2), RADIUS)
    pygame.display.update()

# Main game loop
board = Board()
turn_player = 1
mouse = (-1, -1)
draw_board(board, mouse)
game_over = False
winner = 0

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            mouse = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            column = mouse[0] // SQUARE_SIZE
            played, winner = board.play(turn_player, column)
            game_over = winner != 0
            if game_over:
                match winner:
                    case -1:
                        print("It's a draw!")
                    case 1:
                        print("Red wins!")
                    case 2:
                        print("Yellow wins!")
                break
            if played:
                turn_player = 2 if turn_player == 1 else 1
        
    draw_board(board, mouse, turn_player)