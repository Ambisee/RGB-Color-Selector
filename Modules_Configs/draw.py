# -- Modules -- #
import pygame

try:
    from config import *
except:
    from Modules_Configs.config import *

# -- Functions -- #
def redraw_window(window, coldis, colpick, colscroll, title, result, value, _value):
    window.fill((255,255,255))
    window.blit(title, (colpick.CPW // 2 - title.get_width() // 2, 5))
    window.blit(value, (WIDTH // 4 - value.get_width() // 2, colpick.y + colpick.CPH))
    window.blit(_value, (WIDTH // 4 - _value.get_width() // 2, colpick.y + colpick.CPH + _value.get_height() + 2))
    coldis.draw(window ,result)
    colpick.draw(window)
    for scroll in colscroll:
        scroll.draw()

def drawInputs(window):
    pass