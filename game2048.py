import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_SIZE = 500
GRID_SIZE = 4
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
PADDING = 10
BACKGROUND_COLOR = (187, 173, 160)
EMPTY_COLOR = (205, 193, 180)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

class Game2048:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption('2048')
        self.clock = pygame.time.Clock()
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) 
                      for j in range(GRID_SIZE) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.board[i][j]
                color = TILE_COLORS[value]
                rect = pygame.Rect(
                    j * CELL_SIZE + PADDING,
                    i * CELL_SIZE + PADDING,
                    CELL_SIZE - 2 * PADDING,
                    CELL_SIZE - 2 * PADDING
                )
                pygame.draw.rect(self.screen, color, rect, border_radius=5)
                if value != 0:
                    font = pygame.font.SysFont('Arial', 40, bold=True)
                    text = font.render(str(value), True, (119, 110, 101))
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

    def move(self, direction):
        moved = False
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if direction == 'up' and i > 0:
                    if self.board[i-1][j] == 0:
                        self.board[i-1][j] = self.board[i][j]
                        self.board[i][j] = 0
                        moved = True
                    elif self.board[i-1][j] == self.board[i][j]:
                        self.board[i-1][j] *= 2
                        self.board[i][j] = 0
                        self.score += self.board[i-1][j]
                        moved = True
                elif direction == 'down' and i < GRID_SIZE-1:
                    if self.board[i+1][j] == 0:
                        self.board[i+1][j] = self.board[i][j]
                        self.board[i][j] = 0
                        moved = True
                    elif self.board[i+1][j] == self.board[i][j]:
                        self.board[i+1][j] *= 2
                        self.board[i][j] = 0
                        self.score += self.board[i+1][j]
                        moved = True
                elif direction == 'left' and j > 0:
                    if self.board[i][j-1] == 0:
                        self.board[i][j-1] = self.board[i][j]
                        self.board[i][j] = 0
                        moved = True
                    elif self.board[i][j-1] == self.board[i][j]:
                        self.board[i][j-1] *= 2
                        self.board[i][j] = 0
                        self.score += self.board[i][j-1]
                        moved = True
                elif direction == 'right' and j < GRID_SIZE-1:
                    if self.board[i][j+1] == 0:
                        self.board[i][j+1] = self.board[i][j]
                        self.board[i][j] = 0
                        moved = True
                    elif self.board[i][j+1] == self.board[i][j]:
                        self.board[i][j+1] *= 2
                        self.board[i][j] = 0
                        self.score += self.board[i][j+1]
                        moved = True
        return moved

    def move_up(self):
        moved = self.move('up')
        if moved:
            self.add_new_tile()

    def move_down(self):
        moved = self.move('down')
        if moved:
            self.add_new_tile()

    def move_left(self):
        moved = self.move('left')
        if moved:
            self.add_new_tile()

    def move_right(self):
        moved = self.move('right')
        if moved:
            self.add_new_tile()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.move_down()
                    elif event.key == pygame.K_LEFT:
                        self.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.move_right()

            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game2048()
    game.run()
