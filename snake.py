import pygame
import random
import time

# 初始化
pygame.init()

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 游戏设置
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
SPEED = 7

# 方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('snake')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 25)
        self.reset_game()

    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False

    def generate_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

    def move_snake(self):
        if self.game_over:
            return

        # 更新方向
        self.direction = self.next_direction

        # 计算新头部位置
        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        # 检查碰撞
        if (new_head in self.snake or 
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.game_over = True
            return

        # 移动蛇
        self.snake.insert(0, new_head)

        # 检查是否吃到食物
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def change_direction(self, direction):
        # 防止直接反向移动
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction

    def draw(self):
        self.screen.fill(BLACK)

        # 绘制蛇
        for segment in self.snake:
            pygame.draw.rect(
                self.screen, 
                GREEN, 
                (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            )

        # 绘制食物
        pygame.draw.rect(
            self.screen, 
            RED, 
            (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )

        # 绘制分数
        score_text = self.font.render(f'分数: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # 游戏结束弹窗
        if self.game_over:
            # 半透明背景
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            self.screen.blit(s, (0, 0))
            
            # 弹窗内容
            popup_width, popup_height = 300, 200
            popup_x, popup_y = WIDTH//2 - popup_width//2, HEIGHT//2 - popup_height//2
            
            # 弹窗背景
            pygame.draw.rect(self.screen, (50, 50, 50), (popup_x, popup_y, popup_width, popup_height))
            pygame.draw.rect(self.screen, WHITE, (popup_x, popup_y, popup_width, popup_height), 2)
            
            # 游戏结束文字
            game_over_text = self.font.render('游戏结束!', True, WHITE)
            self.screen.blit(game_over_text, 
                           (WIDTH//2 - game_over_text.get_width()//2, popup_y + 40))
            
            # 分数显示
            score_text = self.font.render(f'最终分数: {self.score}', True, WHITE)
            self.screen.blit(score_text, 
                           (WIDTH//2 - score_text.get_width()//2, popup_y + 80))
            
            # 重新开始按钮
            button_rect = pygame.Rect(WIDTH//2 - 100, popup_y + 120, 200, 50)
            pygame.draw.rect(self.screen, GREEN, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)
            
            restart_text = self.font.render('重新开始', True, BLACK)
            self.screen.blit(restart_text, 
                           (button_rect.centerx - restart_text.get_width()//2, 
                            button_rect.centery - restart_text.get_height()//2))

        pygame.display.update()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.change_direction(RIGHT)
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                    mouse_pos = pygame.mouse.get_pos()
                    popup_height = 200  # 与draw方法中的弹窗高度一致
                    button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - popup_height//2 + 120, 200, 50)
                    if button_rect.collidepoint(mouse_pos):
                        self.reset_game()

            self.move_snake()
            self.draw()
            self.clock.tick(SPEED)

        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
