# -- Modules -- #
from pyperclip import copy
import pygame

try:
    from config import *
except:
    from Modules_Configs.config import *

# -- Variables -- #
height = 30

# -- Classes -- #
class WhichColor:
    def __init__(self, x, y, font):
        self.colors = [font.render("R", True, (255,255,255)), font.render("G", True, (255,255,255)), font.render("B", True, (255,255,255))]
        self.rgb = [(255,0,0), (0,255,0), (0,0,255)]
        self.drop = False
        self.edge = height
        self.selected_col = 0
        self.rect = pygame.Rect(x, y, self.edge, self.edge) 

    def checkClicked(self, x, y):
        if self.rect.collidepoint((x, y)):
            return True
        else:
            return False
    
    def isSelected(self, x, y):
        if self.drop == True:
            rectcop = self.rect.copy()
            rectcop.height = 3 * (self.edge + 5)
            rectcop.y = self.rect.y + self.edge
            if rectcop.collidepoint((x, y)):
                return True
        return False

    def switch(self, y):
        self.selected_col = (y - self.rect.y - self.edge) // (self.edge + 5)
        self.drop = False

    def draw(self, window):
        main = self.colors[self.selected_col]
        text_width = main.get_width()
        text_height = main.get_height()
        pygame.draw.rect(window, self.rgb[self.selected_col], self.rect)
        window.blit(self.colors[self.selected_col], (self.rect.x + self.rect.width//2 - text_width // 2, self.rect.y + self.rect.height//2 - text_height // 2))
        
        if self.drop:
            copies = self.rect.copy()
            for i in range(3):
                copies.y = copies.y + copies.height + 5
                pygame.draw.rect(window, self.rgb[i], copies)
                window.blit(self.colors[i], (copies.x + copies.width//2 - self.colors[i].get_width()//2, copies.y + copies.height//2 - self.colors[i].get_height()//2))

class InputBar:
    def __init__(self, x, y, font):
        self.font = font
        self.active_col = pygame.Color(0, 179, 255)
        self.deactive_col = pygame.Color(125,125,125)
        self.text = ""
        self.active = False
        self.color = self.active_col if self.active else self.deactive_col
        self.x = x
        self.y = y
        self.length = 100
        self.height = height
        self.rect = pygame.Rect(x, y, self.length, self.height)
    
    def isSelected(self, x, y):
        if self.rect.collidepoint((x, y)):
            self.active = True
        else:
            self.active = False
        self.color = self.active_col if self.active else self.deactive_col

    def keyFunc(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif len(self.text) >= 3 or not self.active:
            return
        elif event.unicode.isdigit():
            self.text += event.unicode

    def draw(self, window):
        self.label = self.font.render(self.text, True, self.color)

        pygame.draw.rect(window, self.color, self.rect, 2)
        window.blit(self.label, (self.rect.x + 5, self.rect.y + self.rect.height//2 - self.label.get_height()//2))

class InputGroup:
    def __init__(self, surf_w, midline, font):
        self.font = font
        self.gap = 10
        
        self.selector = WhichColor(0, 0, self.font)
        self.ibar = InputBar(0, 0, self.font)
        self.button = pygame.Rect(0, 0, 150, self.ibar.rect.height)
        self.apply_text = font.render("Apply (ENTER)", True, pygame.Color('white'))
        
        self.total_length = self.selector.edge + self.ibar.length + self.button.width + (2 * self.gap)
        self.selector.rect.midleft = ((surf_w - self.total_length) // 2, midline)
        self.ibar.rect.midleft = (self.selector.rect.right + self.gap, midline)
        self.button.midleft = (self.selector.rect.x + self.total_length - self.button.width, midline)
        self.text_x = self.button.x + self.button.width // 2 - self.apply_text.get_width() // 2        
        self.text_y = self.button.y + self.button.height // 2 - self.apply_text.get_height() // 2

    def change(self, cs):
        if self.ibar.text == "":
            pass
        elif int(self.ibar.text) in range(0, 256):
            col = self.selector.selected_col
            cs[col].color[col] = int(self.ibar.text)
            cs[col].x_circ = cs[col].x_bar + int(self.ibar.text)
        self.ibar.text = ""

    def draw(self, window):
        self.selector.draw(window)
        self.ibar.draw(window)

        pygame.draw.rect(window, self.ibar.color, self.button)
        window.blit(self.apply_text, (self.text_x, self.text_y))
    
class CopyButton:
    def __init__(self, font, midline):
        self.font = font
        self.length = 200
        self.height = 50
        self.rect = pygame.Rect(0, 0, self.length, self.height)
        self.text = font.render("Copy Value (C)", True, (255, 255, 255))
        self.color = (0, 179, 255)
        self.clicked = (77, 202, 255)
        
        self.rect.midleft = (WIDTH // 4 - self.length // 2, midline)
        self.text_x = self.rect.x + self.rect.width // 2 - self.text.get_width() // 2
        self.text_y = self.rect.y + self.rect.height // 2 - self.text.get_height() // 2
    
    def pycopy(self, text):
        copy(text)

    def isSelected(self, x, y, text):
        if self.rect.collidepoint((x, y)):
            self.pycopy(text)
            return True
        return False

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.text, (self.text_x, self.text_y))