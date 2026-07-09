# ui.py
import pygame
from settings import *

def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))
    return text_surface.get_rect(topleft=(x, y))

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.is_hovered = False

    def handle_event(self, event, mouse_pos):
        # Kiểm tra xem nút có được click không
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(mouse_pos):
                return True
        return False

    def update(self, mouse_pos):
        # Cập nhật trạng thái hover
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        # Đổi màu nếu đang hover
        color = HOVER_GREEN if self.is_hovered else BRAND_GREEN
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        # Căn giữa chữ trong nút
        text_surf = self.font.render(self.text, True, BG_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)