# test 
import pygame
import random
import sys

pygame.init()

GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
GRID_X_OFFSET = 50
GRID_Y_OFFSET = 50

WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + 2 * GRID_X_OFFSET + 200
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + 2 * GRID_Y_OFFSET

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)

COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED]

TETROMINO_SHAPES = [
    [['.....',
      '..#..',
      '.###.',
      '.....',
      '.....'],
     ['.....',
      '.#...',
      '.##..',
      '.#...',
      '.....'],
     ['.....',
      '.....',
      '.###.',
      '..#..',
      '.....'],
     ['.....',
      '..#..',
      '.##..',
      '..#..',
      '.....']],
    
    [['.....',
      '.....',
      '.##..',
      '.##..',
      '.....']],
    
    [['.....',
      '.....',
      '.###.',
      '.#...',
      '.....'],
     ['.....',
      '.##..',
      '..#..',
      '..#..',
      '.....'],
     ['.....',
      '...#.',
      '.###.',
      '.....',
      '.....'],
     ['.....',
      '.#...',
      '.#...',
      '.##..',
      '.....']],
    
    [['.....',
      '.....',
      '.###.',
      '...#.',
      '.....'],
     ['.....',
      '..#..',
      '..#..',
      '.##..',
      '.....'],
     ['.....',
      '.#...',
      '.###.',
      '.....',
      '.....'],
     ['.....',
      '.##..',
      '.#...',
      '.#...',
      '.....']],
    
    [['.....',
      '.....',
      '..##.',
      '.##..',
      '.....'],
     ['.....',
      '.#...',
      '.##..',
      '..#..',
      '.....']],
    
    [['.....',
      '.....',
      '.##..',
      '..##.',
      '.....'],
     ['.....',
      '..#..',
      '.##..',
      '.#...',
      '.....']],
    
    [['.....',
      '.....',
      '.####',
      '.....',
      '.....'],
     ['.....',
      '..#..',
      '..#..',
      '..#..',
      '..#..']]
]

class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = GRID_WIDTH // 2 - 2
        self.y = 0
        self.rotation = 0
    
    def get_rotated_shape(self):
        return self.shape[self.rotation % len(self.shape)]
    
    def get_cells(self):
        cells = []
        shape = self.get_rotated_shape()
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '#':
                    cells.append((self.x + j, self.y + i))
        return cells

class TetrisGame:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500
        self.game_over = False
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
    
    def get_new_piece(self):
        shape_index = random.randint(0, len(TETROMINO_SHAPES) - 1)
        return Tetromino(TETROMINO_SHAPES[shape_index], COLORS[shape_index])
    
    def is_valid_position(self, piece, dx=0, dy=0, rotation=0):
        temp_rotation = piece.rotation
        piece.rotation = (piece.rotation + rotation) % len(piece.shape)
        
        for x, y in piece.get_cells():
            new_x, new_y = x + dx, y + dy
            if (new_x < 0 or new_x >= GRID_WIDTH or 
                new_y >= GRID_HEIGHT or 
                (new_y >= 0 and self.grid[new_y][new_x] != 0)):
                piece.rotation = temp_rotation
                return False
        
        piece.rotation = temp_rotation
        return True
    
    def place_piece(self, piece):
        for x, y in piece.get_cells():
            if y >= 0:
                self.grid[y][x] = piece.color
    
    def clear_lines(self):
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y][x] != 0 for x in range(GRID_WIDTH)):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        lines_cleared = len(lines_to_clear)
        self.lines_cleared += lines_cleared
        self.score += lines_cleared * 100 * self.level
        self.level = self.lines_cleared // 10 + 1
        self.fall_speed = max(50, 500 - (self.level - 1) * 50)
    
    def update(self, dt):
        if self.game_over:
            return
        
        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            if self.is_valid_position(self.current_piece, dy=1):
                self.current_piece.y += 1
            else:
                self.place_piece(self.current_piece)
                self.clear_lines()
                self.current_piece = self.next_piece
                self.next_piece = self.get_new_piece()
                
                if not self.is_valid_position(self.current_piece):
                    self.game_over = True
            
            self.fall_time = 0
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if self.is_valid_position(self.current_piece, dx=-1):
                    self.current_piece.x -= 1
            elif event.key == pygame.K_RIGHT:
                if self.is_valid_position(self.current_piece, dx=1):
                    self.current_piece.x += 1
            elif event.key == pygame.K_DOWN:
                if self.is_valid_position(self.current_piece, dy=1):
                    self.current_piece.y += 1
            elif event.key == pygame.K_UP:
                if self.is_valid_position(self.current_piece, rotation=1):
                    self.current_piece.rotation = (self.current_piece.rotation + 1) % len(self.current_piece.shape)
            elif event.key == pygame.K_SPACE:
                while self.is_valid_position(self.current_piece, dy=1):
                    self.current_piece.y += 1
    
    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(
                    GRID_X_OFFSET + x * CELL_SIZE,
                    GRID_Y_OFFSET + y * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                )
                
                if self.grid[y][x] != 0:
                    pygame.draw.rect(self.screen, self.grid[y][x], rect)
                
                pygame.draw.rect(self.screen, WHITE, rect, 1)
    
    def draw_piece(self, piece):
        for x, y in piece.get_cells():
            if y >= 0:
                rect = pygame.Rect(
                    GRID_X_OFFSET + x * CELL_SIZE,
                    GRID_Y_OFFSET + y * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                )
                pygame.draw.rect(self.screen, piece.color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 1)
    
    def draw_ui(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        lines_text = self.font.render(f"Lines: {self.lines_cleared}", True, WHITE)
        
        self.screen.blit(score_text, (GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20, 50))
        self.screen.blit(level_text, (GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20, 100))
        self.screen.blit(lines_text, (GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20, 150))
        
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, RED)
            restart_text = self.font.render("Press R to restart", True, WHITE)
            self.screen.blit(game_over_text, (GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20, 200))
            self.screen.blit(restart_text, (GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20, 250))
    
    def restart(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500
        self.game_over = False
    
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.restart()
                    else:
                        self.handle_input(event)
            
            self.update(dt)
            
            self.screen.fill(BLACK)
            self.draw_grid()
            if not self.game_over:
                self.draw_piece(self.current_piece)
            self.draw_ui()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()