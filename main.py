# main.py
import pygame
import sys
from settings import *
from dot_field import DotField
from ui import draw_text, Button

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("UI with DotField Background")
        self.clock = pygame.time.Clock()
        
        # Tải fonts
        self.font_title = pygame.font.SysFont("segoeui", 64, bold=False)
        self.font_subtitle = pygame.font.SysFont("segoeui", 20)
        self.font_mono = pygame.font.SysFont("consolas", 16, bold=True)
        
        # Khởi tạo các thành phần
        self.dot_field = DotField(WIDTH, HEIGHT)
        self.start_button = Button(200, 600, 200, 45, "Start Now", self.font_subtitle)

        # Tải ảnh nền 1 lần
        try:
            self.background_image = pygame.image.load("Background.png").convert()
            self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        except pygame.error:
            self.background_image = None
            print("Không thể tải ảnh Background.png. Vui lòng kiểm tra lại tên file hoặc đường dẫn.")

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            self.handle_events(mouse_pos)
            self.update(mouse_pos)
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(FPS)

    def handle_events(self, mouse_pos):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Kiểm tra sự kiện cho nút bấm
            if self.start_button.handle_event(event, mouse_pos):
                print("Nút Start Now đã được nhấn!")

    def update(self, mouse_pos):
        # Cập nhật logic vật lý và giao diện
        self.dot_field.update_mouse_speed(*mouse_pos)
        self.start_button.update(mouse_pos)

    def draw(self):
        try:
            background_image = pygame.image.load("Background.png")
            background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        except:
            background_image = None
            print("Không thể tải ảnh Background.png. Vui lòng Kiểm tra lại tên file hoặc đường dẫn.") 
            
        # Vẽ nền ảnh nếu có, nếu không thì nền màu
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(BG_COLOR)
        
        # Vẽ lớp hạt
        self.dot_field.draw(self.screen)
        

        # Vẽ nút bấm
        self.start_button.draw(self.screen)

if __name__ == "__main__":
    app = App()
    app.run()