import pygame
import random

# 初始化
pygame.init()

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# 游戏设置
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT
GAME_AREA_LEFT = BLOCK_SIZE

# 方块形状
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

SHAPE_COLORS = [CYAN, YELLOW, PURPLE, ORANGE, BLUE, GREEN, RED]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('俄罗斯方块')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 25)
        self.reset_game()

    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.fall_speed = 0.5  # 秒
        self.fall_time = 0

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = SHAPE_COLORS[SHAPES.index(shape)]
        return {
            'shape': shape,
            'color': color,
            'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
            'y': 0
        }

    def valid_position(self, piece=None, x=None, y=None):
        if piece is None:
            piece = self.current_piece
        if x is None:
            x = piece['x']
        if y is None:
            y = piece['y']

        for i, row in enumerate(piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    if (x + j < 0 or x + j >= GRID_WIDTH or 
                        y + i >= GRID_HEIGHT or 
                        (y + i >= 0 and self.grid[y + i][x + j])):
                        return False
        return True

    def rotate_piece(self):
        # 转置矩阵并反转每行实现旋转
        rotated = [list(row) for row in zip(*self.current_piece['shape'][::-1])]
        old_shape = self.current_piece['shape']
        self.current_piece['shape'] = rotated
        if not self.valid_position():
            self.current_piece['shape'] = old_shape

    def lock_piece(self):
        for i, row in enumerate(self.current_piece['shape']):
            for j, cell in enumerate(row):
                if cell and self.current_piece['y'] + i >= 0:
                    self.grid[self.current_piece['y'] + i][self.current_piece['x'] + j] = self.current_piece['color']
        
        # 检查消除行
        self.clear_lines()
        
        # 生成新方块
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        
        # 检查游戏结束
        if not self.valid_position():
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        for i in range(GRID_HEIGHT):
            if all(self.grid[i]):
                lines_cleared += 1
                for j in range(i, 0, -1):
                    self.grid[j] = self.grid[j-1][:]
                self.grid[0] = [0 for _ in range(GRID_WIDTH)]
        
        # 计分
        if lines_cleared == 1:
            self.score += 100 * self.level
        elif lines_cleared == 2:
            self.score += 300 * self.level
        elif lines_cleared == 3:
            self.score += 500 * self.level
        elif lines_cleared == 4:
            self.score += 800 * self.level
        
        # 升级
        if self.score // 2000 > self.level - 1:
            self.level += 1
            self.fall_speed = max(0.05, self.fall_speed * 0.8)

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(
                    self.screen, 
                    WHITE, 
                    (GAME_AREA_LEFT + x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 
                    1
                )
                if self.grid[y][x]:
                    pygame.draw.rect(
                        self.screen, 
                        self.grid[y][x], 
                        (GAME_AREA_LEFT + x * BLOCK_SIZE + 1, y * BLOCK_SIZE + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2)
                    )

    def draw_current_piece(self):
        for i, row in enumerate(self.current_piece['shape']):
            for j, cell in enumerate(row):
                if cell and self.current_piece['y'] + i >= 0:
                    pygame.draw.rect(
                        self.screen, 
                        self.current_piece['color'], 
                        (
                            GAME_AREA_LEFT + (self.current_piece['x'] + j) * BLOCK_SIZE + 1, 
                            (self.current_piece['y'] + i) * BLOCK_SIZE + 1, 
                            BLOCK_SIZE - 2, 
                            BLOCK_SIZE - 2
                        )
                    )

    def draw_next_piece(self):
        next_x = GRID_WIDTH + 2
        next_y = 2
        for i, row in enumerate(self.next_piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen, 
                        self.next_piece['color'], 
                        (
                            GAME_AREA_LEFT + (next_x + j) * BLOCK_SIZE + 1, 
                            (next_y + i) * BLOCK_SIZE + 1, 
                            BLOCK_SIZE - 2, 
                            BLOCK_SIZE - 2
                        )
                    )

    def draw_info(self):
        score_text = self.font.render(f'分数: {self.score}', True, WHITE)
        level_text = self.font.render(f'等级: {self.level}', True, WHITE)
        next_text = self.font.render('下一个:', True, WHITE)
        
        self.screen.blit(score_text, (GAME_AREA_LEFT + (GRID_WIDTH + 1) * BLOCK_SIZE, 100))
        self.screen.blit(level_text, (GAME_AREA_LEFT + (GRID_WIDTH + 1) * BLOCK_SIZE, 150))
        self.screen.blit(next_text, (GAME_AREA_LEFT + (GRID_WIDTH + 1) * BLOCK_SIZE, 200))

    def draw_game_over(self):
        game_over_text = self.font.render('游戏结束!', True, RED)
        restart_text = self.font.render('按R键重新开始', True, WHITE)
        
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                         SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                                       SCREEN_HEIGHT // 2 + 10))

    def run(self):
        running = True
        while running:
            self.screen.fill(BLACK)
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if not self.game_over:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.current_piece['x'] -= 1
                            if not self.valid_position():
                                self.current_piece['x'] += 1
                        elif event.key == pygame.K_RIGHT:
                            self.current_piece['x'] += 1
                            if not self.valid_position():
                                self.current_piece['x'] -= 1
                        elif event.key == pygame.K_DOWN:
                            self.current_piece['y'] += 1
                            if not self.valid_position():
                                self.current_piece['y'] -= 1
                                self.lock_piece()
                        elif event.key == pygame.K_UP:
                            self.rotate_piece()
                        elif event.key == pygame.K_SPACE:
                            while self.valid_position(y=self.current_piece['y'] + 1):
                                self.current_piece['y'] += 1
                            self.lock_piece()
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        self.reset_game()

            # 自动下落
            if not self.game_over:
                current_time = pygame.time.get_ticks() / 1000
                if current_time - self.fall_time > self.fall_speed:
                    self.fall_time = current_time
                    self.current_piece['y'] += 1
                    if not self.valid_position():
                        self.current_piece['y'] -= 1
                        self.lock_piece()

            # 绘制
            self.draw_grid()
            self.draw_current_piece()
            self.draw_next_piece()
            self.draw_info()
            if self.game_over:
                self.draw_game_over()
            
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()
