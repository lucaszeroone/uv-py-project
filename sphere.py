import pygame
import math
import numpy as np
from pygame.locals import *

# 初始化
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("0-1球体")
clock = pygame.time.Clock()

# 球体参数
radius = 150
center = [width//2, height//2]
rotation_speed = 0.01

# 生成球体点阵
def generate_sphere_points():
    points = []
    for theta in np.linspace(0, 2*math.pi, 20):  # 经度
        for phi in np.linspace(0, math.pi, 10):  # 纬度
            x = radius * math.sin(phi) * math.cos(theta)
            y = radius * math.sin(phi) * math.sin(theta)
            z = radius * math.cos(phi)
            points.append((x, y, z))
    return points

# 旋转函数
def rotate_point(x, y, z, angle_x, angle_y, angle_z):
    # X轴旋转
    new_y = y * math.cos(angle_x) - z * math.sin(angle_x)
    new_z = y * math.sin(angle_x) + z * math.cos(angle_x)
    y, z = new_y, new_z
    
    # Y轴旋转
    new_x = x * math.cos(angle_y) + z * math.sin(angle_y)
    new_z = -x * math.sin(angle_y) + z * math.cos(angle_y)
    x, z = new_x, new_z
    
    # Z轴旋转
    new_x = x * math.cos(angle_z) - y * math.sin(angle_z)
    new_y = x * math.sin(angle_z) + y * math.cos(angle_z)
    x, y = new_x, new_y
    
    return x, y, z

# 主循环
def main():
    points = generate_sphere_points()
    angle_x, angle_y, angle_z = 0, 0, 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        # 清屏
        screen.fill((0, 0, 0))
        
        # 旋转角度
        angle_x += rotation_speed
        angle_y += rotation_speed * 0.7
        angle_z += rotation_speed * 0.3
        
        # 绘制球体
        for point in points:
            x, y, z = rotate_point(*point, angle_x, angle_y, angle_z)
            
            # 透视投影
            scale = 500 / (500 + z)
            x_proj = int(x * scale) + center[0]
            y_proj = int(y * scale) + center[1]
            
            # 根据索引交替显示0和1
            idx = points.index(point)
            if idx % 2 == 0:
                text = "0"
                color = (255, 0, 0)  # 红色
            else:
                text = "1"
                color = (0, 255, 0)  # 绿色
            
            # 绘制文本
            font = pygame.font.SysFont('Arial', 20)
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(x_proj, y_proj))
            screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
