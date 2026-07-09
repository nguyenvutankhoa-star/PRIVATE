# dot_field.py
import pygame
import math
from settings import *

class DotField:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.dots = []
        self.build_dots()
        self.mouse_x, self.mouse_y = -9999, -9999
        self.prev_mouse_x, self.prev_mouse_y = -9999, -9999
        self.mouse_speed = 0
        self.engagement = 0
        self.frame_count = 0

    def build_dots(self):
        step = DOT_RADIUS + DOT_SPACING
        cols = int(self.width / step) + 1
        rows = int(self.height / step) + 1
        pad_x = (self.width % step) / 2
        pad_y = (self.height % step) / 2
        
        self.dots = []
        for row in range(rows):
            for col in range(cols):
                ax = pad_x + col * step
                ay = pad_y + row * step
                self.dots.append([ax, ay, ax, ay, 0.0, 0.0, ax, ay])

    def update_mouse_speed(self, mx, my):
        if self.prev_mouse_x != -9999:
            dx = self.prev_mouse_x - mx
            dy = self.prev_mouse_y - my
            self.mouse_speed += (math.sqrt(dx * dx + dy * dy) - self.mouse_speed) * 0.5
        if self.mouse_speed < 0.001: self.mouse_speed = 0
        self.prev_mouse_x, self.prev_mouse_y = mx, my
        self.mouse_x, self.mouse_y = mx, my

    def draw(self, screen):
        self.frame_count += 1
        target_engagement = min(self.mouse_speed / 5, 1)
        self.engagement += (target_engagement - self.engagement) * 0.06
        if self.engagement < 0.001: self.engagement = 0
            
        cr_sq = CURSOR_RADIUS * CURSOR_RADIUS
        rad = DOT_RADIUS / 2

        for i, dot in enumerate(self.dots):
            ax, ay, sx, sy, vx, vy, x, y = dot
            dx_mouse, dy_mouse = self.mouse_x - ax, self.mouse_y - ay
            dist_sq = dx_mouse * dx_mouse + dy_mouse * dy_mouse

            if dist_sq < cr_sq and self.engagement > 0.01:
                dist = math.sqrt(dist_sq) or 0.001
                t_val = 1 - dist / CURSOR_RADIUS
                push = t_val * t_val * BULGE_STRENGTH * self.engagement
                angle = math.atan2(dy_mouse, dx_mouse)
                sx += (ax - math.cos(angle) * push - sx) * 0.15
                sy += (ay - math.sin(angle) * push - sy) * 0.15
            else:
                sx += (ax - sx) * 0.1
                sy += (ay - sy) * 0.1

            dot[2], dot[3] = sx, sy
            current_rad = rad
            
            if SPARKLE and ((i * 2654435761) ^ (self.frame_count >> 3)) % 100 < 3:
                current_rad = rad * 2.5

            alpha = 255
            if dist_sq > cr_sq:
                alpha = max(40, 255 - (dist_sq - cr_sq) * 0.001)
            
            pygame.draw.circle(screen, (*DOT_COLOR[:3], int(alpha)), (int(sx), int(sy)), max(1, int(current_rad)))