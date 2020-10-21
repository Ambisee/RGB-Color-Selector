# -- Modules -- #
from pygame import gfxdraw
import pygame

try:
    from config import *
except:
    from Modules_Configs.config import *

# --- Classes --- #
class ColorDisplay:
    def __init__(self):
        self.width = WIDTH // 2
        self.height = HEIGHT
        self.red = 0
        self.green = 0
        self.blue = 0
    
    def update_color(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b
    
    def draw(self, window, text):
        pygame.draw.rect(window, (self.red, self.green, self.blue), (WIDTH // 2, 0, self.width, self.height))
        window.blit(text, (WIDTH // 4 * 3 - text.get_width() // 2, 5))

class ColorPicker:
    CPW = WIDTH // 2
    CPH = HEIGHT // 3

    def __init__(self):
        self.color = (255, 255, 255)
        self.y = 50
        self.surface =  pygame.Surface((self.CPW, self.CPH))
        self.rect = pygame.Rect(0, self.y, self.CPW, self.CPH)
    
    def draw(self, window):
        window.blit(self.surface, (0, self.y))
        self.surface.fill((255,255,255))


class ColorScroll:
    def __init__(self, row, color_in, surface, rgb, font):
        self.rgb = rgb
        self.color_in = color_in
        self.color = [0, 0, 0]
        self.color_permanent = self.color.copy()
        self.color_permanent[self.color_in] = 255
        self.length = 255
        self.height = 20
        self.radius = 20
        self.surface = surface
        self.surface_rect = surface.get_rect()
        self.letter = font.render(rgb, True, self.color_permanent)
        
        self.total_length = self.letter.get_width() + self.length + 35
        self.initial_x = (self.surface_rect.width - self.total_length) // 2
        self.lerrect = self.letter.get_rect()
        self.lerrect.midleft = (self.initial_x, int((self.surface_rect.height // 3) * (row + 0.5)))
        self.x_bar = self.lerrect.x + self.lerrect.width + 35
        self.y_bar = self.lerrect.y + self.lerrect.height // 2 - self.height // 2
        self.x_circ = self.x_bar
        self.y_circ = self.y_bar + self.height // 2
        self.minX = self.x_circ
        self.maxX = self.x_circ + 255

    def update_x(self, x):
        self.x_circ = x

    def draw(self):
        # (10, self.y_bar + self.height // 2 - self.letter.get_height()//2)
        self.surface.blit(self.letter, self.lerrect)
        pygame.draw.rect(self.surface, self.color_permanent, (self.x_bar, self.y_bar, self.length, self.height))
        
        gfxdraw.aacircle(self.surface, self.x_circ, self.y_circ, self.radius + 3, (255,255,255))
        gfxdraw.filled_circle(self.surface, self.x_circ, self.y_circ, self.radius + 3, (255,255,255))

        gfxdraw.aacircle(self.surface, self.x_circ, self.y_circ, self.radius, self.color)
        gfxdraw.filled_circle(self.surface, self.x_circ, self.y_circ, self.radius, self.color)