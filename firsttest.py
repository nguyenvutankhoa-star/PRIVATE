import pygame
import math
import sys

# --- CẤU HÌNH ---
WIDTH, HEIGHT = 500,700

FPS = 60

# Cấu hình DotField
DOT_RADIUS = 1.5
DOT_SPACING = 14
CURSOR_RADIUS = 400
CURSOR_FORCE = 0.1
BULGE_ONLY = True
BULGE_STRENGTH = 60
WAVE_AMPLITUDE = 0
SPARKLE = True

# Màu sắc
BG_COLOR = (13, 17, 23)          # Nền tối
DOT_COLOR = (0, 229, 153)        # Xanh lục cho các chấm
TEXT_WHITE = (240, 246, 252)     # Trắng hơi xám cho Title
TEXT_GRAY = (139, 148, 158)      # Xám cho Subtitle
BRAND_GREEN = (0, 229, 153)      # Xanh lục cho Button & Badge
BADGE_BG = (22, 27, 34)          # Nền xám đen của Badge
BADGE_BORDER = (48, 54, 61)

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

            # Giảm độ sáng của dot nếu ở xa chuột để tạo hiệu ứng "Glow" tập trung ở chuột
            alpha = 255
            if dist_sq > cr_sq:
                alpha = max(40, 255 - (dist_sq - cr_sq) * 0.001)
            
            # Vẽ dot
            pygame.draw.circle(screen, (*DOT_COLOR[:3], int(alpha)), (int(sx), int(sy)), max(1, int(current_rad)))

def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))
    return text_surface.get_rect(topleft=(x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("UI with DotField Background")
    clock = pygame.time.Clock()

    # Khởi tạo fonts
    # Khuyến nghị: Tải file .ttf về thư mục dự án và thay đổi 'None' thành 'tên_font.ttf' để đẹp hơn
    try:
        font_title = pygame.font.SysFont("segoeui", 64, bold=False)
        font_subtitle = pygame.font.SysFont("segoeui", 20)
        font_mono = pygame.font.SysFont("consolas", 16, bold=True)
    except:
        font_title = pygame.font.Font(None, 74)
        font_subtitle = pygame.font.Font(None, 28)
        font_mono = pygame.font.Font(None, 24)

    # Tải ảnh nền
    try:
        background_image = pygame.image.load("Background.png")
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    except:
        background_image = None
        print("Không thể tải ảnh Background.png")

    dot_field = DotField(WIDTH, HEIGHT)

    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Xử lý click button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Kiểm tra xem chuột có nằm trong vùng của Button không (tọa độ giả định ở phần render)
                if button_rect.collidepoint(mx, my):
                    print("Nút Start Now đã được nhấn!")

        dot_field.mouse_x, dot_field.mouse_y = mx, my
        dot_field.update_mouse_speed(mx, my)

        # 1. VẼ NỀN (Lớp dưới cùng)
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BG_COLOR)

        # 2. VẼ DOTFIELD (Lớp ở giữa)
        dot_field.draw(screen)

        # 3. VẼ GIAO DIỆN CHỮ VÀ NÚT (Lớp trên cùng)
        # Margin trái
        margin_x = 80
        start_y = 120

        # --- Vẽ Badge ---
        # badge_rect = pygame.Rect(margin_x, start_y, 220, 36)
        # pygame.draw.rect(screen, BADGE_BORDER, badge_rect, border_radius=6)
        # pygame.draw.rect(screen, BADGE_BG, badge_rect.inflate(-2, -2), border_radius=6)
        
        


        # Cập nhật màn hình
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()